"""Content-canary audit for VisionBook.

Checks every produced chapter against the plan in toc.html:
  1. File completeness: index.html + every section-N.M.html per chapter.
  2. Dash discipline: em dashes (U+2014), en dashes (U+2013), spaced ' -- ' in prose.
  3. Structural canaries per section file: chapter-header, epigraph, big-picture,
     key-insight, research-frontier, code-caption count vs code-block count,
     chapter-nav, closing </html>.
  4. Link integrity: every internal href in non-vendor html resolves on disk.

Usage: python scripts/audit_book.py [--json]
Exit code 0 = clean, 1 = findings.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"vendor", "templates", "node_modules", ".git", ".claude", "styles", "scripts"}

# chapter -> (part_dir, module_dir, [section numbers])
def parse_toc():
    toc = (ROOT / "toc.html").read_text(encoding="utf-8")
    chapters = {}
    # Split on chapter-card openings; nested section <li> elements make a
    # card-content regex unreliable, the split keeps each card's full chunk.
    for card in toc.split('<li class="toc-chapter">')[1:]:
        dir_m = re.search(r'toc-chapter-dir">([a-z0-9\-]+)/([a-z0-9\-]+)/</code>', card)
        if not dir_m:
            continue
        part_dir, module_dir = dir_m.groups()
        if not module_dir.startswith("module-"):
            continue
        secs = re.findall(r'toc-section-num">(\d+\.\d+)</span>', card)
        num_m = re.search(r"module-(\d+)", module_dir)
        chapters[int(num_m.group(1))] = (part_dir, module_dir, secs)
    return chapters


def html_files():
    for p in ROOT.rglob("*.html"):
        if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            yield p


def strip_code(html):
    """Remove pre/code blocks so CLI flags don't trip the dash scan."""
    return re.sub(r"<pre.*?</pre>", "", html, flags=re.S)


def main():
    findings = {"missing_files": [], "dashes": [], "structure": [], "broken_links": []}
    chapters = parse_toc()

    for num, (part_dir, module_dir, secs) in sorted(chapters.items()):
        cdir = ROOT / part_dir / module_dir
        if not (cdir / "index.html").exists():
            findings["missing_files"].append(f"ch{num}: {part_dir}/{module_dir}/index.html")
        for s in secs:
            if not (cdir / f"section-{s}.html").exists():
                findings["missing_files"].append(f"ch{num}: section-{s}.html")

    for f in html_files():
        rel = str(f.relative_to(ROOT)).replace("\\", "/")
        html = f.read_text(encoding="utf-8", errors="replace")
        prose = strip_code(html)
        for ch, name in ((u"—", "em-dash"), (u"–", "en-dash")):
            n = prose.count(ch)
            if n:
                findings["dashes"].append(f"{rel}: {n} {name}")
        if re.search(r"\w -- \w", prose):
            findings["dashes"].append(f"{rel}: spaced double hyphen")

        if re.match(r"section-\d+\.\d+", f.name):
            checks = {
                "chapter-header": "chapter-header" in html,
                "epigraph": 'class="epigraph"' in html,
                "big-picture": "big-picture" in html,
                "key-insight": "key-insight" in html,
                "research-frontier": "research-frontier" in html,
                "chapter-nav": "chapter-nav" in html,
                "closing-html": html.rstrip().endswith("</html>"),
            }
            missing = [k for k, ok in checks.items() if not ok]
            n_code = len(re.findall(r"<pre>", html))
            n_capt = len(re.findall(r'class="code-caption"', html))
            if n_capt < n_code:
                missing.append(f"captions {n_capt}/{n_code}")
            caps = re.findall(r'class="code-caption"[^>]*>(.*?)</div>', html, re.S)
            if len(caps) != len(set(c.strip() for c in caps)):
                missing.append("duplicate captions")
            if missing:
                findings["structure"].append(f"{rel}: {', '.join(missing)}")

        for href in re.findall(r'href="([^"#]+?\.html)(?:#[^"]*)?"', html):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target = (f.parent / href).resolve()
            if not target.exists():
                findings["broken_links"].append(f"{rel} -> {href}")

    total = sum(len(v) for v in findings.values())
    if "--json" in sys.argv:
        print(json.dumps(findings, indent=1))
    else:
        for k, v in findings.items():
            print(f"== {k}: {len(v)}")
            for item in v[:40]:
                print("   " + item)
            if len(v) > 40:
                print(f"   ... and {len(v) - 40} more")
        print(f"TOTAL FINDINGS: {total}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
