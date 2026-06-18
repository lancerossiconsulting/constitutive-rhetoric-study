#!/usr/bin/env python
"""Generate /downloads/*.docx, *.pdf (+ conference *.pptx) from page source.
Reuses the built page HTML so downloads stay in sync with the site.
Deps: pandoc on PATH, fpdf2. Run from repo root: python tools/build_downloads.py
"""
import os, re, subprocess, tempfile, html
from fpdf import FPDF

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "downloads")
BASE = "https://lancerossiconsulting.github.io/constitutive-rhetoric-study"

# slug -> (source dir, wants pptx)
PAGES = {
    "journal-article": ("journal-article", False),
    "conference-paper": ("conference-paper", True),
    "substack": ("substack", False),
    "practice-brief": ("practice-brief", False),
    "podcast-outline": ("podcast-outline", False),
    "literature-review": ("literature-review", False),
}

ARIAL = "C:/Windows/Fonts/arial.ttf"
ARIALB = "C:/Windows/Fonts/arialbd.ttf"
ARIALI = "C:/Windows/Fonts/ariali.ttf"


def split_front_matter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        return {}, text
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        mm = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
        if mm:
            fm[mm.group(1)] = mm.group(2)
    return fm, body


def resolve_liquid(s):
    # {{ '/x/' | relative_url }} -> BASE + /x/
    s = re.sub(r"\{\{\s*'([^']*)'\s*\|\s*relative_url\s*\}\}", lambda m: BASE + m.group(1), s)
    s = re.sub(r"\{\{\s*site\.github_repo\s*\}\}", "https://github.com/lancerossiconsulting/constitutive-rhetoric-study", s)
    s = re.sub(r"\{\{\s*site\.tagline\s*\}\}", "", s)
    s = re.sub(r"\{\{.*?\}\}", "", s)            # any remaining output tags
    s = re.sub(r"\{%-?.*?-?%\}", "", s, flags=re.S)  # tags
    return s


def clean_body(body):
    body = resolve_liquid(body)
    # drop the working-draft banner block
    body = re.sub(r'<div class="draft-banner">.*?</div>', "", body, flags=re.S)
    return body


def to_clean_html(fm, body):
    title = fm.get("title", "")
    subtitle = fm.get("subtitle", "")
    head = f"<h1>{html.escape(title)}</h1>\n"
    if subtitle:
        head += f"<p><em>{html.escape(subtitle)}</em></p>\n"
    head += '<p><strong>Working draft, subject to revision.</strong></p>\n<hr>\n'
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title></head><body>\n{head}{body}\n</body></html>"


def run(cmd):
    subprocess.run(cmd, check=True)


def html_to_blocks(clean_html):
    """pandoc -> gfm, return list of (kind, text)."""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(clean_html); src = f.name
    md = subprocess.run(["pandoc", src, "-f", "html", "-t", "gfm", "--wrap=none"],
                        capture_output=True, text=True, encoding="utf-8", check=True).stdout
    os.unlink(src)
    blocks = []
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            blocks.append(("gap", "")); continue
        h = re.match(r"^(#{1,6})\s+(.*)$", line)
        if h:
            blocks.append((f"h{len(h.group(1))}", h.group(2))); continue
        if re.match(r"^[-*]\s+", line):
            blocks.append(("li", re.sub(r"^[-*]\s+", "", line))); continue
        if re.match(r"^\d+\.\s+", line):
            blocks.append(("li", re.sub(r"^\d+\.\s+", "", line))); continue
        blocks.append(("p", line))
    return blocks


def strip_md(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)   # links -> text
    s = re.sub(r"[*_`]+", "", s)                       # emphasis marks
    s = re.sub(r"<[^>]+>", "", s)                      # stray tags
    s = html.unescape(s).replace("↩", "").strip()
    # insert soft breaks into very long unbroken tokens (e.g. DOIs) so wrapping works
    return re.sub(r"(\S{42})(?=\S)", r"\1 ", s)


def build_pdf(blocks, title, path):
    pdf = FPDF(format="Letter"); pdf.set_auto_page_break(True, margin=18)
    pdf.add_font("A", "", ARIAL); pdf.add_font("A", "B", ARIALB); pdf.add_font("A", "I", ARIALI)
    pdf.add_page(); pdf.set_margins(20, 18, 20)
    sizes = {"h1": 20, "h2": 14, "h3": 12}

    def cell(txt, style, size, h):
        pdf.set_font("A", style, size)
        pdf.multi_cell(0, h, txt, new_x="LMARGIN", new_y="NEXT")

    for kind, text in blocks:
        text = strip_md(text)
        if kind == "gap":
            pdf.ln(2); continue
        if kind in sizes:
            pdf.ln(3); cell(text, "B", sizes[kind], 7); pdf.ln(1)
        elif kind == "li":
            cell("- " + text, "", 11, 6)
        else:
            cell(text, "", 11, 6)
    pdf.output(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, (d, wants_pptx) in PAGES.items():
        src = os.path.join(ROOT, d, "index.html")
        fm, body = split_front_matter(open(src, encoding="utf-8").read())
        clean = to_clean_html(fm, clean_body(body))
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(clean); chtml = f.name
        title = fm.get("title", slug)
        run(["pandoc", chtml, "-f", "html", "-o", os.path.join(OUT, f"{slug}.docx"),
             "--metadata", f"title={title}"])
        if wants_pptx:
            run(["pandoc", chtml, "-f", "html", "-o", os.path.join(OUT, f"{slug}.pptx"),
                 "--slide-level=2", "--metadata", f"title={title}"])
        os.unlink(chtml)
        build_pdf(html_to_blocks(clean), title, os.path.join(OUT, f"{slug}.pdf"))
        print("built", slug)


if __name__ == "__main__":
    main()
