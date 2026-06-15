"""Normalize KFX-hostile SVG syntax inside a built EPUB (does NOT touch web source).

ROOT CAUSE this fixes (KFX error E00115 "SVG specified ... not renderable"):
  The book's inline SVGs were authored with lowercase element/attribute names
  (`<radialgradient>`, `<lineargradient>`, `markerwidth`, `viewbox`, ...). In an
  HTML document the browser's HTML5 parser silently case-corrects SVG foreign
  content (`radialgradient` -> `radialGradient`), so the web book renders fine.
  An EPUB content document is strict XHTML/XML: NO case correction happens, so
  those become *unknown* elements/attributes. KFX cannot render such an SVG and
  fails the whole conversion with a single, hint-free E00115.

What this does, scoped to <svg>...</svg> only (prose/code untouched):
  1. Case-correct every SVG camelCase element name (linearGradient, feGaussianBlur, ...).
  2. Case-correct every SVG camelCase attribute name (viewBox, gradientUnits, markerWidth, ...).
  3. Convert px in the `font:` shorthand to em (/16); the standalone
     `font-size:Npx` form is handled by sanitize_epub_kindle.py.
  4. Remove empty `<filter .../>` defs and their `filter="url(#...)"` references
     (drop-shadow effects KFX cannot render; an empty filter renders transparent).

Rebuilds a valid EPUB in place (writes via temp, mimetype stored first).
Usage: python scripts/fix_svg_kfx_normalize.py KDP/output/building-vision-ai-kindle.epub
"""
import re
import sys
import zipfile
from pathlib import Path

SVG_BLOCK = re.compile(r"<svg\b.*?</svg>", re.S | re.I)

# Canonical SVG camelCase element names (anything not here stays lowercase).
SVG_ELEMENTS = [
    "linearGradient", "radialGradient", "clipPath", "foreignObject", "textPath",
    "feBlend", "feColorMatrix", "feComponentTransfer", "feComposite",
    "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight",
    "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR",
    "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology",
    "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile",
    "feTurbulence", "glyphRef", "altGlyph", "altGlyphDef", "altGlyphItem",
]

# Canonical SVG camelCase attribute names.
SVG_ATTRS = [
    "viewBox", "preserveAspectRatio", "gradientUnits", "gradientTransform",
    "spreadMethod", "patternUnits", "patternContentUnits", "patternTransform",
    "markerWidth", "markerHeight", "markerUnits", "refX", "refY", "clipPathUnits",
    "maskUnits", "maskContentUnits", "primitiveUnits", "filterUnits", "filterRes",
    "stdDeviation", "baseFrequency", "numOctaves", "stitchTiles", "startOffset",
    "textLength", "lengthAdjust", "pathLength", "tableValues", "kernelMatrix",
    "kernelUnitLength", "surfaceScale", "specularConstant", "specularExponent",
    "diffuseConstant", "limitingConeAngle", "pointsAtX", "pointsAtY", "pointsAtZ",
    "xChannelSelector", "yChannelSelector", "attributeName", "attributeType",
    "calcMode", "keyTimes", "keySplines", "keyPoints", "repeatCount", "repeatDur",
    "requiredFeatures", "requiredExtensions", "systemLanguage", "targetX",
    "targetY", "edgeMode", "zoomAndPan", "externalResourcesRequired", "baseProfile",
    "contentStyleType", "contentScriptType",
]

# element-name regexes: match <name  or </name as a whole token, case-insensitively
ELEM_RES = [(re.compile(r"(</?)" + name + r"\b", re.I), name) for name in SVG_ELEMENTS]
# attr-name regexes: match the attribute name immediately before '=' (token start at
# a non-name char), case-insensitively
ATTR_RES = [(re.compile(r"(?<![\w-])" + name + r"(?=\s*=)", re.I), name) for name in SVG_ATTRS]

FONT_PX = re.compile(r"(font\s*:\s*[^;\"']*?)(\d*\.?\d+)px", re.I)
SVG_OPEN = re.compile(r"<svg\b[^>]*>", re.I)
VIEWBOX_VAL = re.compile(r'viewBox\s*=\s*"[\d.\-]+\s+[\d.\-]+\s+([\d.]+)\s+([\d.]+)"', re.I)


def add_dimensions(open_tag):
    """If an <svg> open tag has a viewBox but no width/height attrs, add them
    (KFX computes 0-height for svgs sized only by CSS height:auto -> E00115)."""
    if re.search(r"\bwidth\s*=", open_tag) and re.search(r"\bheight\s*=", open_tag):
        return open_tag
    m = VIEWBOX_VAL.search(open_tag)
    if not m:
        return open_tag
    w, h = m.group(1), m.group(2)
    add = ""
    if not re.search(r"\bwidth\s*=", open_tag):
        add += f' width="{w}"'
    if not re.search(r"\bheight\s*=", open_tag):
        add += f' height="{h}"'
    return open_tag[:4] + add + open_tag[4:]  # insert right after "<svg"
EMPTY_FILTER_DEF = re.compile(r"<filter\b[^>]*>\s*</filter>|<filter\b[^>]*/>", re.I)
FILTER_USE = re.compile(r'\s*filter\s*=\s*"url\(#[^)]*\)"', re.I)


def _font_px_to_em(m):
    return f"{m.group(1)}{float(m.group(2)) / 16:.4g}em"


def fix_svg(block):
    for rx, name in ELEM_RES:
        block = rx.sub(lambda m, nm=name: m.group(1) + nm, block)
    for rx, name in ATTR_RES:
        block = rx.sub(name, block)
    block = FONT_PX.sub(_font_px_to_em, block)
    # remove drop-shadow filters KFX cannot render
    block = EMPTY_FILTER_DEF.sub("", block)
    block = FILTER_USE.sub("", block)
    # give the root <svg> explicit width/height so KFX never computes 0 height
    block = SVG_OPEN.sub(lambda m: add_dimensions(m.group(0)), block, count=1)
    return block


def process_text(text):
    n = [0]

    def repl(m):
        n[0] += 1
        return fix_svg(m.group(0))

    return SVG_BLOCK.sub(repl, text), n[0]


CSS_RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")


def process_css(text):
    """In CSS rules whose selector targets svg, drop height:auto and width:100%
    (these override the svg's width/height attrs and make KFX compute 0 height
    -> E00115). Keep max-width:100% for responsive down-scaling."""
    n = [0]

    def repl(m):
        sel, body = m.group(1), m.group(2)
        if "svg" not in sel.lower():
            return m.group(0)
        new = re.sub(r"(?:^|;)\s*height\s*:\s*auto\s*(?=;|$)", "", body, flags=re.I)
        new = re.sub(r"(?:^|;)\s*width\s*:\s*100%\s*(?=;|$)", "", new, flags=re.I)
        if new != body:
            n[0] += 1
        return f"{sel}{{{new}}}"

    return CSS_RULE.sub(repl, text), n[0]


def main():
    src = Path(sys.argv[1])
    tmp = src.with_suffix(src.suffix + ".tmp")
    zin = zipfile.ZipFile(src, "r")
    total = 0
    entries = []
    for name in zin.namelist():
        data = zin.read(name)
        if name.lower().endswith((".xhtml", ".html", ".htm", ".svg")):
            txt = data.decode("utf-8", "replace")
            txt, c = process_text(txt)
            total += c
            data = txt.encode("utf-8")
        elif name.lower().endswith(".css"):
            txt = data.decode("utf-8", "replace")
            txt, _ = process_css(txt)
            data = txt.encode("utf-8")
        entries.append((name, data))
    zin.close()
    with zipfile.ZipFile(tmp, "w") as zout:
        if "mimetype" in dict(entries):
            zi = zipfile.ZipInfo("mimetype")
            zi.compress_type = zipfile.ZIP_STORED
            zout.writestr(zi, b"application/epub+zip")
        for name, data in entries:
            if name == "mimetype":
                continue
            zout.writestr(name, data, zipfile.ZIP_DEFLATED)
    tmp.replace(src)
    print(f"{src.name}: normalized {total} <svg> blocks")


if __name__ == "__main__":
    main()
