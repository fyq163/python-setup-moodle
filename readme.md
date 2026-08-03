# Python Setup Guide for HKU Beginners

A beginner-friendly, static website that teaches new HKU postgraduate students how to
install a Python environment and run their first lessons. Content is written in
**Markdown** and rendered to HTML in the browser — no build step required.

## How it works (markdown-driven)

- Each HTML page is a thin **shell**. Its `<body>` carries `data-md="<file>.md"`.
- `assets/js/render.js` fetches that Markdown file, parses it with
  [`marked`](https://marked.js.org/) and sanitizes it with
  [`DOMPurify`](https://github.com/cure53/DOMPurify), then injects the HTML into the page.
- The top navigation, the index chapter cards, the sidebar table of contents, the
  Required/Optional/Skippable tag, and the Prev/Next pager are all generated automatically
  from `assets/js/site.js` and from each `.md` file's frontmatter.
- [TDesign web components](https://tdesign.tencent.com/web-components) are loaded via CDN
  and used for the chapter tag chips (`<t-tag>`). If the CDN is blocked, the page falls
  back to plain CSS — it still works. (shadcn requires React + a bundler, so it is not
  used in this no-build static site.)

### Editing content

1. Open the relevant `.md` file (`index.md` or `pages/<chapter>.md`).
2. Edit the text. Frontmatter at the top controls the page title and tag:
   ```markdown
   ---
   title: 3 · Installing Python
   tag: Required
   ---
   ```
3. Save and **refresh the browser** — the HTML updates instantly. No compilation.

### Markdown features supported

- Standard Markdown: headings, lists, tables, fenced code blocks, links, images.
- **GitHub-style alerts** become callouts: `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`,
  `> [!IMPORTANT]`.
- A standalone image `![alt](path)` is wrapped in a `<figure>` with the `alt` text as the
  caption. Use `assets/img/placeholder.svg` as a placeholder and replace `src` later.
- Shell code blocks (`bash`/`sh`/`zsh`/`powershell`/`cmd`) get colored `$` prompts and
  `#` comments automatically.
- Use `<!-- TODO: ... -->` comments in the Markdown for authoring notes (they are hidden
  when rendered).

### Adding a new chapter

1. Create `pages/<name>.md` with `title`/`tag` frontmatter.
2. Create `pages/<name>.html` copying any existing shell and setting
   `data-md="<name>.md"`.
3. Add an entry to `window.SITE.chapters` in `assets/js/site.js`
   (`{ name, n, title, tag, desc }`). The nav, index cards, and pager update automatically.

## Workflow: edit Markdown → refresh

The site is **markdown-driven**: each page `fetch()`es its `.md` and renders it in the
browser, so content is never compiled — it is read live. To see your edits, the browser
just needs to reload the `.md`.

### Option A — Auto-refresh while editing (recommended)

`serve.py` is a zero-dependency live-reload server. It watches every `.md`/`.html`/`.css`/
`.js` file and tells the browser to reload the moment you save:

```sh
python3 serve.py 8000
# edit any .md, save, and the page reloads automatically
```

No `pip install`, no bundler. The HTML served is still plain static files, so GitHub
Pages deployment is unchanged. (If you prefer Node tooling, `npx browser-sync start
--server --files "**/*"` does the same thing.)

### Option B — Manual refresh

You can use any static server; just refresh the browser after saving:

```sh
python3 -m http.server 8000
# then visit http://localhost:8000/ and refresh after edits
```

> Why not open the `.html` directly? The browser blocks `fetch()` of local files over
> `file://`. Always serve over HTTP (either option above).

## Deploy to GitHub Pages

The site is plain static files — push to the repo and enable GitHub Pages on the branch
(root). No Jekyll or build step is needed. `marked`, `DOMPurify`, and TDesign are loaded
from jsDelivr, so the live site needs internet access for those scripts.

## Project status

See `AGENTS.md` for the full plan. Chapters are skeletons with placeholder text and TODO
markers; the structure, navigation, and Markdown rendering pipeline are complete.
