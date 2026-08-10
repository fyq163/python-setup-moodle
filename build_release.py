#!/usr/bin/env python3
"""
Build a self-contained, dependency-free HTML release.

This produces the `release/` directory: one fully inlined `.html` file per
chapter (plus `index.html`). Each output file:

  * embeds the stylesheet inline (`<style>`), no external css
  * has NO <script> tags and NO CDN references
  * renders the Markdown to static HTML at build time (no client-side fetch)
  * ships its own sidebar TOC, Prev/Next pager and footer as plain HTML

It is meant for places that only accept raw, standalone HTML (paste the file
content straight into an HTML editor / CMS). Some JS-driven effects (copy
buttons, dark-mode toggle, TDesign chips) are intentionally dropped — the
content and structure stay intact.

Run it in your own CI (e.g. a local `conda activate nlp-mark` env):
    conda activate nlp-mark
    pip install -r requirements-release.txt
    python3 build_release.py

Requires: Python 3.8+, the `markdown` package.

TODO: image references in the release still point to the local relative path
(`../assets/img/...`) as produced by the Markdown. Before publishing, rewrite
these to GitHub permalinks (e.g.
`https://github.com/fyq163/python-setup-moodle/raw/main/assets/img/...`) so the
release needs no bundled `assets/` folder. This step is done manually.
"""
import os
import re
import html as _html
import markdown as _md

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ROOT, "pages")
CSS = os.path.join(ROOT, "css", "style.css")
OUT = os.path.join(ROOT, "release")

# Chapter order / metadata. Mirrors assets/js/site.js but kept here so the
# release build is independent of the live site's JS.
CHAPTERS = [
    ("unix-basics",          "1 · Basic Unix-like Systems", "Skippable", "Command line, terminal, sudo, -h/--help, options vs arguments, exe vs no-extension."),
    ("virtual-environment",  "2 · Virtual Environments",    "Optional",   "Why not just use the system Python. uv vs conda, local vs global environments."),
    ("installation",         "3 · Installing Python",       "Required",   "Standalone installer, conda, and uv — across macOS (arm64), Windows (amd64) and Linux (x86_64)."),
    ("ide-setup",            "4 · Code Editors & IDEs",      "Required",   "VS Code / Cursor / CodeBuddy, PyCharm Community, and GitHub Copilot student access."),
    ("recommended-reading",  "5 · Recommended Reading",      "Optional",   "PEP 8 style, language servers (ty, pyright) and linters (ruff) to level up."),
]

MD_EXTENSIONS = ["fenced_code", "tables", "sane_lists"]


# ---------------------------------------------------------------------------
# Markdown loading
# ---------------------------------------------------------------------------
def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s.strip("-") or "section"


def render_body(md_text):
    """Render markdown to HTML and add heading ids / collect a TOC."""
    html = _md.markdown(md_text, extensions=MD_EXTENSIONS)
    # Rewrite local image paths (../assets/img/...) to GitHub permalink
    # via jsDelivr CDN, so the release HTML is fully self-contained and
    # needs no bundled assets/ folder.
    GITHUB_CDN = "https://cdn.jsdelivr.net/gh/fyq163/python-setup-moodle@main"
    html = re.sub(
        r'src="\.\./assets/img/([^"]+)"',
        lambda mo: 'src="%s/assets/img/%s"' % (GITHUB_CDN, mo.group(1)),
        html,
    )
    # Turn any leftover GitHub-style alert markers into emoji callouts.
    html = re.sub(
        r'<blockquote>\s*<p>\s*\[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]\s*',
        lambda mo: '<blockquote class="note note-' + mo.group(1).lower() + '"><p>',
        html,
    )
    toc = []
    heading_re = re.compile(r"<(h[123])([^>]*)>(.*?)</\1>", re.DOTALL)

    def repl(mo):
        tag, attrs, inner = mo.group(1), mo.group(2), mo.group(3)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        hid = slugify(text)
        if 'id="' not in attrs:
            attrs = attrs + ' id="%s"' % hid
        if tag != "h1":
            toc.append((tag, text, hid))
        return "<%s%s>%s</%s>" % (tag, attrs, inner, tag)

    html = heading_re.sub(repl, html)
    return html, toc


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------
def read_css():
    with open(CSS, encoding="utf-8") as f:
        return f.read()


def tag_chip_html(tag):
    if tag in ("Required", "Optional", "Skippable"):
        cls = {"Required": "required", "Optional": "optional", "Skippable": "skip"}[tag]
        return '<span class="tag tag-%s">%s</span>' % (cls, _html.escape(tag))
    return ""


def toc_html(toc):
    if not toc:
        return ""
    items = "".join(
        '<li class="toc-%s"><a href="#%s">%s</a></li>'
        % (lvl.lower(), hid, _html.escape(txt))
        for lvl, txt, hid in toc
    )
    return '<aside class="sidebar"><h4>In this chapter</h4><nav id="toc"><ol>%s</ol></nav></aside>' % items


def pager_html(current_name):
    idx = [c[0] for c in CHAPTERS].index(current_name)
    parts = []
    if idx > 0:
        prev_n, prev_title = CHAPTERS[idx - 1][1], CHAPTERS[idx - 1][0]
        parts.append('<a class="prev" href="%s.html"><span class="dir">← Previous</span><span class="ttl">%s</span></a>'
                     % (prev_title.split("·")[-1].strip().lower().replace(" ", "-"), CHAPTERS[idx - 1][1]))
    if idx < len(CHAPTERS) - 1:
        nxt_n, nxt_title = CHAPTERS[idx + 1][1], CHAPTERS[idx + 1][0]
        parts.append('<a class="next" href="%s.html"><span class="dir">→ Next</span><span class="ttl">%s</span></a>'
                     % (nxt_title.split("·")[-1].strip().lower().replace(" ", "-"), CHAPTERS[idx + 1][1]))
    return '<nav class="pager">%s</nav>' % "".join(parts)


def nav_html():
    links = "".join(
        '<a href="%s.html">%s</a>' % (c[0], c[1].split("·")[-1].strip())
        for c in CHAPTERS
    )
    return '<header id="topnav" class="topnav"><a class="brand" href="index.html"><span class="dot"></span> Python Setup Guide</a><nav class="navlinks">%s</nav></header>' % links


def build_chapter(name, title, tag, desc, css):
    md_path = os.path.join(PAGES, name + ".md")
    with open(md_path, encoding="utf-8") as f:
        meta, body = parse_frontmatter(f.read())
    title = meta.get("title", title)
    tag = meta.get("tag", tag)
    body_html, toc = render_body(body)

    chip = tag_chip_html(tag)
    h1 = '<h1 id="top">%s</h1>' % _html.escape(title)
    pagehead = '<div id="pagehead" class="pagehead">%s%s</div>' % (chip, h1)

    doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
</head>
<body data-md="{name}.md">
{nav}
<div class="layout">
{toc}
<div class="article">
{pagehead}
<main id="content" class="markdown">
{body}
</main>
</div>
</div>
{pager}
<footer id="footer" class="site">
<p>Python Setup Guide &middot; <a href="index.html">Back to home</a></p>
<p>Content is a work in progress &mdash; see the project readme for status.</p>
</footer>
</body>
</html>
""".format(title=_html.escape(title), css=css, name=name, nav=nav_html(),
           toc=toc_html(toc), pagehead=pagehead, body=body_html,
           pager=pager_html(name))
    return doc


def build_index(css):
    md_path = os.path.join(ROOT, "index.md")
    with open(md_path, encoding="utf-8") as f:
        meta, body = parse_frontmatter(f.read())
    title = meta.get("title", "Python Setup Guide for HKU Beginners")
    body_html, toc = render_body(body)

    # Chapter cards grid
    cards = "".join(
        '<a class="toc-item" href="%s.html"><span class="num">%s</span><h3>%s</h3><p>%s</p><div class="meta">%s</div></a>'
        % (c[0], c[1].split("·")[0].strip(), c[1].split("·")[-1].strip(),
           _html.escape(c[3]), tag_chip_html(c[2]))
        for c in CHAPTERS
    )
    cards = '<div id="tochome" class="toc-grid">%s</div>' % cards

    doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
</head>
<body data-md="index.md">
{nav}
<section class="hero"><div class="container">
<span class="eyebrow">The University of Hong Kong &middot; Programming Bootcamp</span>
<h1>Welcome, new HKU students &#128075;</h1>
<p class="lead">This guide helps you set up a Python environment on your own computer and use it to
learn your first Python lessons &mdash; even if you have never opened a terminal before.
Pick the chapters you need; skip the ones you already know.</p>
<div>
<span class="pill">&#128013; CPython (reference implementation)</span>
<span class="pill">&#128187; macOS &middot; Windows &middot; Linux</span>
<span class="pill">&#128640; Beginner friendly</span>
</div>
</div></section>
<section class="container" style="padding-top:2.4rem;">
<div id="content" class="markdown">
{body}
</div>
<h2 id="toc">Chapters</h2>
{cards}
</section>
<footer id="footer" class="site">
<p>Python Setup Guide &middot; <a href="index.html">Back to home</a></p>
<p>Content is a work in progress &mdash; see the project readme for status.</p>
</footer>
</body>
</html>
""".format(title=_html.escape(title), css=css, nav=nav_html(), body=body_html, cards=cards)
    return doc


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    css = read_css()
    # index
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index(css))
    # chapters
    for name, title, tag, desc in CHAPTERS:
        out = build_chapter(name, title, tag, desc, css)
        with open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8") as f:
            f.write(out)
        print("built release/%s.html" % name)
    # No local assets/ folder: release references images via GitHub permalink.
    print("release build complete -> %s" % OUT)


if __name__ == "__main__":
    main()
