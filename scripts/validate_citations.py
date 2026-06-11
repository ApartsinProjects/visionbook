"""Citation gate for VisionBook: extract every arXiv ID and DOI from chapter/appendix
bibliographies and validate each against arXiv/Crossref via the bibtest skill.

For each arXiv/DOI hit we also fuzzy-compare the RESOLVED title against the cited
title, so a real-but-wrong identifier (misattribution) is caught, not just a
malformed/nonexistent one.

Usage: python scripts/validate_citations.py [--limit N] [--json out.json]
Exit 0 if all resolve and match; 1 if any not_found / mismatch.
"""
import json
import re
import sys
import difflib
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, r"C:\Users\apart\.claude\skills\bibtest")
from bibtest import BibliographyChecker  # noqa: E402

checker = BibliographyChecker(email="apartsin@gmail.com")

ARXIV = re.compile(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', re.I)
DOI = re.compile(r'(?:doi\.org/|doi:\s*)(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)', re.I)

def bib_blocks(html):
    """Yield (identifier_kind, id, cited_text) per bibliography entry.

    Split on entry boundaries (bib-entry-card, else <li>) so each identifier is
    paired with ITS OWN entry's text; regex-matching nested <div>s collapses
    entries and mis-pairs titles.
    """
    m = re.search(r'<section class="bibliography".*?</section>', html, re.S)
    region = m.group(0) if m else html
    if '<div class="bib-entry-card">' in region:
        chunks = region.split('<div class="bib-entry-card">')[1:]
    elif '<li' in region:
        chunks = re.split(r'<li[ >]', region)[1:]
    else:
        chunks = [region]
    for chunk in chunks:
        text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', chunk)).strip()
        for ax in ARXIV.findall(chunk):
            yield ("arxiv", ax, text)
        for d in DOI.findall(chunk):
            yield ("doi", d.rstrip('.'), text)

def cited_title(text):
    # titles in our cards sit in quotes or after the year; grab the longest quoted span, else a mid chunk
    q = re.findall(r'["“]([^"”]{12,200})["”]', text)
    if q:
        return max(q, key=len)
    return text[:160]

def sim(a, b):
    norm = lambda s: re.sub(r'[^a-z0-9 ]', '', s.lower())
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()

def main():
    limit = int(sys.argv[sys.argv.index('--limit')+1]) if '--limit' in sys.argv else None
    seen, items = set(), []
    for idx in sorted(ROOT.glob("part-*/module-*/index.html")) + sorted(ROOT.glob("appendices/*/index.html")):
        html = idx.read_text(encoding="utf-8", errors="replace")
        for kind, ident, text in bib_blocks(html):
            key = (kind, ident)
            if key in seen:
                continue
            seen.add(key)
            items.append((kind, ident, cited_title(text), idx.relative_to(ROOT).as_posix()))
    if limit:
        items = items[:limit]
    print(f"Validating {len(items)} unique citations ({sum(1 for i in items if i[0]=='arxiv')} arXiv, {sum(1 for i in items if i[0]=='doi')} DOI)...")
    problems = []
    for n, (kind, ident, title, where) in enumerate(items, 1):
        try:
            if kind == "arxiv":
                # arXiv API rate-limits hard (429); every arXiv paper also has a
                # DataCite DOI 10.48550/arXiv.<id> resolvable via Crossref/OpenAlex/
                # DataCite, which are not blocked. Try the DOI path first.
                r = checker.check_doi(f"10.48550/arXiv.{ident}")
                status = getattr(getattr(r, "status", "?"), "value", str(getattr(r, "status", "?")))
                if status != "valid":
                    r = checker.check_arxiv(ident)  # fallback to arXiv API
                    status = getattr(getattr(r, "status", "?"), "value", str(getattr(r, "status", "?")))
            else:
                r = checker.check_doi(ident)
                status = getattr(getattr(r, "status", "?"), "value", str(getattr(r, "status", "?")))
            rtitle = getattr(r, "title", "") or ""
            ok = status == "valid"
            time.sleep(1.0)  # polite pacing
            ratio = sim(title, rtitle) if rtitle else 0.0
            mismatch = ok and rtitle and ratio < 0.55
            tag = "MISATTRIB" if mismatch else ("BAD" if not ok else "ok")
            if tag != "ok":
                problems.append({"kind": kind, "id": ident, "status": status, "ratio": round(ratio, 2),
                                 "cited": title[:80], "resolved": rtitle[:80], "where": where})
            if n % 25 == 0 or tag != "ok":
                print(f"[{n}/{len(items)}] {tag:9} {kind}:{ident}  ({where})")
        except Exception as e:
            problems.append({"kind": kind, "id": ident, "status": f"ERR {e}", "where": where})
    print(f"\nDONE. {len(items)} checked, {len(problems)} problems.")
    for p in problems:
        print("  " + json.dumps(p, ensure_ascii=False))
    if '--json' in sys.argv:
        Path(sys.argv[sys.argv.index('--json')+1]).write_text(json.dumps(problems, indent=1), encoding="utf-8")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
