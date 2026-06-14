"""Generate all VisionBook illustrations in ONE Gemini Batch API job (50% cost).

Reads every part-*/module-*/images/_specs.json (written by the planning wave),
submits all prompts as a single batch, and maps each returned image back to
{chapter_dir}/images/{filename} by request order. Budget-aware: Batch API (half
price), image-size 1K, single job.

Usage:
  python scripts/gen_illustrations.py --dry-run     # count + cost estimate, no spend
  python scripts/gen_illustrations.py               # submit the batch and save images
  python scripts/gen_illustrations.py --only 33,34  # restrict to chapters (retry)
"""
import base64
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((Path.home() / ".gemini-imagegen.json").read_text())
MODEL = CFG.get("default_model", "gemini-3.1-flash-image")
PRICE_PER_IMG = 0.039  # flash-image approx; batch halves it

def collect():
    items = []  # (chapter, chapter_dir, filename, prompt, Path)
    only = None
    if "--only" in sys.argv:
        only = set(int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(","))
    for spec_file in sorted(ROOT.glob("part-*/module-*/images/_specs.json")):
        data = json.loads(spec_file.read_text(encoding="utf-8"))
        ch = data["chapter"]
        if only and ch not in only:
            continue
        img_dir = spec_file.parent
        for s in data["specs"]:
            items.append((ch, data["dir"], s["filename"], s["prompt"], img_dir / s["filename"]))
    return items

def main():
    items = collect()
    n = len(items)
    full = n * PRICE_PER_IMG
    print(f"{n} illustrations across {len(set(i[0] for i in items))} chapters.")
    print(f"Model: {MODEL}, image-size 1K, aspect 4:3.")
    print(f"Est cost: ${full:.2f} full price -> ${full/2:.2f} via Batch API (50%).")
    if "--dry-run" in sys.argv:
        # show per-chapter counts
        from collections import Counter
        c = Counter(i[0] for i in items)
        print("per-chapter:", dict(sorted(c.items())))
        return

    from google import genai
    from google.genai import types
    client = genai.Client(api_key=CFG["api_key"])

    if "--sync" in sys.argv:
        import concurrent.futures
        def gen_one(it):
            ch, cdir, fname, prompt, outpath = it
            if outpath.exists():
                return ("skip", fname)
            for attempt in range(4):
                try:
                    resp = client.models.generate_content(
                        model=MODEL, contents=prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=["IMAGE"],
                            image_config=types.ImageConfig(aspect_ratio="4:3", image_size="1K")))
                    for part in resp.parts:
                        if part.inline_data:
                            outpath.parent.mkdir(parents=True, exist_ok=True)
                            part.as_image().save(str(outpath))
                            return ("ok", fname)
                    return ("noimg", fname)
                except Exception as e:
                    if attempt == 3:
                        return (f"ERR:{e.__class__.__name__}", fname)
                    time.sleep(5 * (attempt + 1))
        print(f"Synchronous generation of {n} images (4 workers, full price ~${full:.2f})...", flush=True)
        ok_n = 0; bad = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
            for i, (status, fname) in enumerate(ex.map(gen_one, items), 1):
                if status in ("ok", "skip"):
                    ok_n += 1
                else:
                    bad.append(f"{status}:{fname}")
                if i % 20 == 0:
                    print(f"  {i}/{n} done, {ok_n} ok", flush=True)
        print(f"\nSaved {ok_n}/{n}. Failures: {len(bad)}", flush=True)
        for b in bad:
            print("  ", b)
        sys.exit(0)

    reqs = [types.InlinedRequest(
        contents=[types.Content(parts=[types.Part(text=it[3])], role="user")],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="4:3", image_size="1K"),
        ),
    ) for it in items]

    if "--resume" in sys.argv:
        # Reconnect to the most recent visionbook-illus batch instead of resubmitting.
        cand = [b for b in client.batches.list(config={"page_size": 50})
                if (getattr(b, "display_name", "") or "").startswith("visionbook-illus")]
        if not cand:
            print("No existing visionbook-illus batch to resume."); sys.exit(1)
        job = cand[0]
        name = job.name
        print(f"Resuming existing job: {name} ({getattr(job,'display_name','')})")
    else:
        print(f"Submitting ONE batch of {n} requests (Batch API, 50% cost)...")
        job = client.batches.create(model=MODEL, src=reqs,
                                    config={"display_name": f"visionbook-illus-{int(time.time())}"})
        name = job.name
        print(f"Job: {name}", flush=True)

    def poll_get():
        # transient 429/500/503 during polling must not kill a running batch
        for attempt in range(6):
            try:
                return client.batches.get(name=name)
            except Exception as e:
                if attempt == 5:
                    raise
                print(f"  poll retry ({e.__class__.__name__}); backing off", flush=True)
                time.sleep(30 * (attempt + 1))
    while True:
        job = poll_get()
        state = job.state.name if hasattr(job.state, "name") else str(job.state)
        if state in ("JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED"):
            break
        print(f"  state={state}", flush=True)
        time.sleep(20)
    if state != "JOB_STATE_SUCCEEDED":
        print(f"Batch ended: {state}")
        sys.exit(1)

    saved, missing = 0, []
    for i, rw in enumerate(job.dest.inlined_responses):
        ch, cdir, fname, _, outpath = items[i]
        resp = rw.response
        ok = False
        if resp and resp.candidates:
            for cand in resp.candidates:
                for part in (cand.content.parts if cand.content else []):
                    if part.inline_data and part.inline_data.data:
                        d = part.inline_data.data
                        if isinstance(d, str):
                            d = base64.b64decode(d)
                        outpath.parent.mkdir(parents=True, exist_ok=True)
                        outpath.write_bytes(d)
                        saved += 1
                        ok = True
                        break
                if ok:
                    break
        if not ok:
            missing.append(f"ch{ch}:{fname}")
    print(f"\nSaved {saved}/{n}. Missing: {len(missing)}")
    for m in missing:
        print("  MISSING", m)

if __name__ == "__main__":
    main()
