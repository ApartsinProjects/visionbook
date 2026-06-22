"""Propagate book.json metadata into the book's HTML pages.

book.json is the SINGLE SOURCE OF TRUTH. Edit it, then run:
    python scripts/apply_meta.py
to update the edition label everywhere (cover edition-pill, TOC subtitle, and
every chapter/section footer). Idempotent: safe to run repeatedly.

Currently propagates the edition string. Extend `apply()` to cover more fields
(counts, copyright) as needed. The book-skills build pipeline reads the same
book.json so freshly generated pages are correct by construction.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = json.load(open(os.path.join(ROOT,"book.json"), encoding="utf-8"))
EDITION = META["edition"]
EXCL = {"android","mobile","build","KDP","visionbook-app","_coverwork","backup","node_modules","_book-writers",".git"}
ED_RE = re.compile(r'\b(First|Second|Third|Fourth|Web) Edition\b')

def apply():
    changed = 0
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in EXCL]
        for f in fn:
            if not f.endswith(".html"): continue
            p = os.path.join(dp, f)
            s = open(p, encoding="utf-8").read()
            ns = ED_RE.sub(EDITION, s)
            if ns != s:
                open(p, "w", encoding="utf-8").write(ns); changed += 1
    print(f"apply_meta: edition='{EDITION}' -> {changed} files updated")

if __name__ == "__main__":
    apply()
