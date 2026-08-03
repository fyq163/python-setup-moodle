// Site-wide configuration: chapter list (order, titles, tags, descriptions).
// Edits here update the top navigation, the index TOC cards, and the Prev/Next pager.
// Each chapter has a matching Markdown file (pages/<name>.md) that holds the body text.
window.SITE = {
  brand: 'Python Setup Guide',
  chapters: [
    { name: 'unix-basics',          n: 1, title: 'Basic Unix-like Systems', tag: 'Skippable', desc: 'Command line, terminal, sudo, -h/--help, options vs arguments, exe vs no-extension.' },
    { name: 'virtual-environment',  n: 2, title: 'Virtual Environments',    tag: 'Optional',   desc: 'Why not just use the system Python. uv vs conda, local vs global environments.' },
    { name: 'installation',         n: 3, title: 'Installing Python',       tag: 'Required',   desc: 'Standalone installer, conda, and uv — across macOS (arm64), Windows (amd64) and Linux (x86_64).' },
    { name: 'ide-setup',            n: 4, title: 'Code Editors & IDEs',     tag: 'Required',   desc: 'VS Code / Cursor / CodeBuddy, PyCharm Community, and GitHub Copilot student access.' },
    { name: 'recommended-reading',  n: 5, title: 'Recommended Reading',     tag: 'Optional',   desc: 'PEP 8 style, language servers (ty, pyright) and linters (ruff) to level up.' }
  ]
};
