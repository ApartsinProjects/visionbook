"""Per-section depth metrics for the graduate-depth audit."""
import re, glob, csv

secs = sorted(glob.glob("part-*/module-*/section-*.html"))
with open("_diagnostics/depth-audit/metrics.csv", "w", newline="", encoding="utf-8") as out:
    w = csv.writer(out)
    w.writerow(["section", "words", "math_display", "code_blocks", "exercises", "deriv_terms"])
    for f in secs:
        t = open(f, encoding="utf-8", errors="replace").read()
        words = len(re.sub(r"<[^>]+>", " ", t).split())
        mathd = t.count("$$") // 2
        code = t.count("<pre")
        ex = t.count("callout exercise")
        deriv = len(re.findall(r"deriv|theorem|proof|lemma|objective|gradient|bound", t, re.I))
        w.writerow([f.replace("\\", "/"), words, mathd, code, ex, deriv])
print("wrote _diagnostics/depth-audit/metrics.csv with", len(secs), "sections")
