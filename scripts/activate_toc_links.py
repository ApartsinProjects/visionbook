"""Activate navigation links in toc.html for every target that exists on disk.

Idempotent and rerunnable: cards already linked are left alone; unproduced
targets stay unlinked. Run after each production wave and at finalize.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOC = ROOT / "toc.html"

PART_DIRS = {
    "part-1": "part-1-image-processing",
    "part-2": "part-2-classical-computer-vision",
    "part-3": "part-3-deep-learning-for-vision",
    "part-4": "part-4-generative-vision-models",
}

def main():
    html = TOC.read_text(encoding="utf-8")
    stats = {"chapters": 0, "sections": 0, "parts": 0, "already": 0, "skipped": 0}

    # 1. Header nav: book title -> cover (span form only; idempotent).
    html = html.replace(
        '<span class="book-title-link">Building Vision AI: From Pixels to Generative Models</span>',
        '<a class="book-title-link" href="index.html">Building Vision AI: From Pixels to Generative Models</a>',
    )

    # 2. Chapter cards: link the title span to the card's directory target.
    def link_card(m):
        card = m.group(0)
        dir_m = re.search(r'toc-chapter-dir">([^<]+)</code>', card)
        if not dir_m:
            return card
        target = dir_m.group(1)
        if target.endswith("/"):
            target += "index.html"
        if not (ROOT / target).exists():
            stats["skipped"] += 1
            return card
        if 'toc-card-link' in card:
            stats["already"] += 1
        else:
            card = card.replace(
                '<span class="toc-chapter-title">',
                f'<a class="toc-card-link" href="{target}"><span class="toc-chapter-title">',
                1,
            ).replace("</span>", "</span></a>", 1) if False else re.sub(
                r'(<span class="toc-chapter-title">.*?</span>)',
                lambda t: f'<a class="toc-card-link" href="{target}">{t.group(1)}</a>',
                card, count=1, flags=re.S,
            )
            stats["chapters"] += 1
        # 3. Section rows inside this card.
        sec_dir = target.rsplit("/", 1)[0]
        def link_sec(sm):
            num, text = sm.group(1), sm.group(2)
            if "<a " in text:
                return sm.group(0)
            sec_file = f"{sec_dir}/section-{num}.html"
            if not (ROOT / sec_file).exists():
                return sm.group(0)
            stats["sections"] += 1
            return (f'<li><span class="toc-section-num">{num}</span> '
                    f'<a class="toc-sec-link" href="{sec_file}">{text}</a></li>')
        card = re.sub(
            r'<li><span class="toc-section-num">([\d.]+)</span> (.*?)</li>',
            link_sec, card, flags=re.S,
        )
        return card

    # Cards end with the dir-code line then the card's closing </li>. Anchoring on
    # </code></li> avoids stopping at a nested section-list <li>.
    html = re.sub(r'<li class="toc-chapter">.*?</code>\s*</li>',
                  link_card, html, flags=re.S)

    # 4. Part headers: link the bare title text after the separator span.
    def link_part(m):
        sec_id, title = m.group(1), m.group(2)
        targets = {**{k: v + "/index.html" for k, v in PART_DIRS.items()},
                   "front-matter": "front-matter/foreword.html",
                   "appendices": "appendices/index.html",
                   "capstone": "capstone/index.html"}
        target = targets.get(sec_id)
        if not target or not (ROOT / target).exists() or title.startswith("<a"):
            return m.group(0)
        stats["parts"] += 1
        return m.group(0).replace("</span> " + title + "</h2>",
                                  f'</span> <a href="{target}">{title}</a></h2>')

    html = re.sub(
        r'<section class="toc-part[^"]*"[^>]*id="([\w-]+)">\s*<header class="toc-part-header">\s*'
        r'<h2 class="toc-part-title">.*?</span> ([^<]+)</h2>',
        link_part, html, flags=re.S)

    # 5. Link CSS (once).
    if ".toc-card-link" not in html:
        html = html.replace("</style>", """.toc-card-link { color: inherit; text-decoration: none; }
.toc-card-link:hover .toc-chapter-title { color: #e94560; }
.toc-sec-link { color: inherit; text-decoration: none; border-bottom: 1px dotted #c3cad6; }
.toc-sec-link:hover { color: #e94560; border-bottom-color: #e94560; }
.toc-part-title a { color: #ffffff; text-decoration: none; border-bottom: 1px dotted rgba(255,255,255,0.5); }
.toc-part-title a:hover { color: rgba(255,255,255,0.85); }
</style>""", 1)

    # 6. Draft note reflects live state.
    html = html.replace(
        "Chapter links activate as content is produced; the planned directory path is shown under each chapter.",
        "Linked chapters and sections are live; unlinked ones are still in production. The planned directory path is shown under each chapter.",
    )

    TOC.write_text(html, encoding="utf-8")
    print(stats)


if __name__ == "__main__":
    main()
