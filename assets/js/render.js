// Renders the Markdown file named in <body data-md="..."> into #content, then:
//  - builds the top navigation, index TOC cards and Prev/Next pager from window.SITE
//  - sets the page <title> and a TDesign <t-tag> chip + <h1> from the Markdown frontmatter
//  - auto-generates heading ids and the sidebar table of contents
//  - turns GitHub-style alerts (> [!NOTE]) into styled callouts and standalone images into figures
// Markdown is parsed with `marked` and sanitized with `DOMPurify` (loaded via CDN).
(function () {
  'use strict';

  function slugify(s) {
    return s.toLowerCase().trim()
      .replace(/[^\w\s-]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-');
  }
  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function tagTheme(tag) {
    if (tag === 'Required') return 'success';
    if (tag === 'Optional') return 'warning';
    if (tag === 'Skippable') return 'primary';
    return 'default';
  }
  function tagClass(tag) {
    if (tag === 'Required') return 'required';
    if (tag === 'Optional') return 'optional';
    if (tag === 'Skippable') return 'skip';
    return 'optional';
  }

  function parseFrontmatter(text) {
    var m = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
    if (!m) return { meta: {}, body: text };
    var meta = {};
    m[1].split('\n').forEach(function (line) {
      var i = line.indexOf(':');
      if (i > 0) { meta[line.slice(0, i).trim()] = line.slice(i + 1).trim(); }
    });
    return { meta: meta, body: text.slice(m[0].length) };
  }

  function highlightShell(code) {
    var lines = code.textContent.split('\n');
    code.innerHTML = lines.map(function (line) {
      if (/^\s*\$/.test(line)) {
        var i = line.indexOf('$');
        return escapeHtml(line.slice(0, i)) + '<span class="prompt">$</span>' + escapeHtml(line.slice(i + 1));
      }
      if (/^\s*#/.test(line)) return '<span class="comment">' + escapeHtml(line) + '</span>';
      return escapeHtml(line);
    }).join('\n');
  }

  function postProcess(content) {
    var toc = [];
    content.querySelectorAll('h1, h2, h3').forEach(function (h) {
      if (!h.id) h.id = slugify(h.textContent);
      if (h.tagName !== 'H1') toc.push({ level: h.tagName, text: h.textContent, id: h.id });
    });
    content.querySelectorAll('blockquote').forEach(function (bq) {
      var first = bq.firstElementChild;
      if (first && /^\[!(\w+)\]/.test(first.textContent || '')) {
        var kind = (first.textContent.match(/\[!(\w+)\]/) || [])[1].toLowerCase();
        bq.classList.add('note', 'note-' + kind);
        // Strip the leading [!TYPE] marker from the text instead of deleting the
        // whole paragraph — this works whether the marker is on its own line or
        // shares a line with the body text, so no content is lost.
        [].forEach.call(bq.childNodes, function (node) {
          if (node.nodeType === 1 && /^\[!(\w+)\]/.test(node.textContent || '')) {
            node.textContent = node.textContent.replace(/^\[!(\w+)\]\s*/, '');
            if (node.textContent.trim() === '') node.remove();
          }
        });
      }
    });
    content.querySelectorAll('p > img:only-child').forEach(function (img) {
      var fig = document.createElement('figure');
      fig.className = 'screenshot';
      img.parentNode.insertBefore(fig, img);
      fig.appendChild(img);
      var cap = document.createElement('figcaption');
      cap.textContent = img.getAttribute('alt') || '';
      fig.appendChild(cap);
      img.addEventListener('error', function () { img.classList.add('img-failed'); });
    });
    content.querySelectorAll('pre code').forEach(function (code) {
      if (/language-(bash|sh|shell|console|zsh|powershell|cmd)/.test(code.className || '')) highlightShell(code);
    });
    content.querySelectorAll('pre').forEach(function (pre) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-btn';
      btn.textContent = 'Copy';
      btn.addEventListener('click', function () {
        var code = pre.querySelector('code');
        var text = code ? code.innerText : pre.innerText;
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = 'Copied!';
          setTimeout(function () { btn.textContent = 'Copy'; }, 1500);
        }).catch(function () {
          btn.textContent = 'Press Ctrl+C';
          setTimeout(function () { btn.textContent = 'Copy'; }, 1500);
        });
      });
      pre.appendChild(btn);
    });
    return toc;
  }

  function buildToc(toc, el) {
    if (!el) return;
    var ol = document.createElement('ol');
    toc.forEach(function (item) {
      var li = document.createElement('li');
      if (item.level === 'H3') li.style.marginLeft = '.6rem';
      var a = document.createElement('a');
      a.href = '#' + item.id;
      a.textContent = item.text;
      li.appendChild(a);
      ol.appendChild(li);
    });
    el.innerHTML = '';
    el.appendChild(ol);
  }

  function pagerLink(c, dir, arrow, base) {
    var a = document.createElement('a');
    a.href = base + 'pages/' + c.name + '.html';
    a.innerHTML = '<span class="dir">' + arrow + ' ' + dir + '</span><span class="ttl">' +
      c.n + ' · ' + escapeHtml(c.title) + '</span>';
    return a;
  }

  function buildChrome() {
    var SITE = window.SITE || { brand: 'Guide', chapters: [] };
    function pageBase() { return /pages\/.*\.html$/.test(location.pathname) ? '../' : ''; }
    function chapterHref(name) { return pageBase() + 'pages/' + name + '.html'; }

    var topnav = document.getElementById('topnav');
    if (topnav) {
      topnav.innerHTML = '<a class="brand" href="' + pageBase() + 'index.html"><span class="dot"></span> ' + SITE.brand + '</a>';
      var nav = document.createElement('nav');
      nav.className = 'navlinks';
      SITE.chapters.forEach(function (c) {
        var a = document.createElement('a');
        a.href = chapterHref(c.name);
        a.textContent = c.title.split('·').pop().trim() || c.title;
        nav.appendChild(a);
      });
      topnav.appendChild(nav);
    }

    var tocHome = document.getElementById('tochome');
    if (tocHome) {
      SITE.chapters.forEach(function (c) {
        var a = document.createElement('a');
        a.className = 'toc-item';
        a.href = chapterHref(c.name);
        a.innerHTML = '<span class="num">' + c.n + '</span>' +
          '<h3>' + escapeHtml(c.title) + '</h3>' +
          '<p>' + escapeHtml(c.desc || '') + '</p>' +
          '<div class="meta"><span class="tag tag-' + tagClass(c.tag) + '">' + escapeHtml(c.tag) + '</span></div>';
        tocHome.appendChild(a);
      });
    }

    var pager = document.getElementById('pager');
    if (pager) {
      var cur = location.pathname.split('/').pop();
      var idx = SITE.chapters.findIndex(function (c) { return c.name + '.html' === cur; });
      if (idx >= 0) {
        if (idx > 0) pager.appendChild(pagerLink(SITE.chapters[idx - 1], 'Previous', '←', pageBase()));
        if (idx < SITE.chapters.length - 1) pager.appendChild(pagerLink(SITE.chapters[idx + 1], 'Next', '→', pageBase()));
      }
    }

    var footer = document.getElementById('footer');
    if (footer) {
      footer.innerHTML = '<p>' + SITE.brand + ' · <a href="' + pageBase() + 'index.html">Back to home</a></p>' +
        '<p>Content is a work in progress — see <a href="' + pageBase() + 'readme.md">readme.md</a> for the project status.</p>';
    }
  }

  function applyTheme() {
    // Respect the OS "night mode" / dark color scheme preference.
    var mq = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
    document.documentElement.setAttribute('data-theme', mq && mq.matches ? 'dark' : 'light');
    // Keep in sync if the user toggles their OS theme while the page is open.
    if (mq && mq.addEventListener) {
      mq.addEventListener('change', function (e) {
        document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
      });
    }
  }

  function render() {
    applyTheme();
    buildChrome();
    var mdPath = document.body.getAttribute('data-md');
    var content = document.getElementById('content');
    var pagehead = document.getElementById('pagehead');
    var tocEl = document.getElementById('toc');
    if (!mdPath || !content) return;

    fetch(mdPath)
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
      .then(function (text) {
        var fm = parseFrontmatter(text);
        var html = (window.marked ? window.marked.parse(fm.body) : fm.body);
        if (window.DOMPurify) html = window.DOMPurify.sanitize(html);
        content.innerHTML = html;
        var toc = postProcess(content);

        if (fm.meta.title) document.title = fm.meta.title;
        if (pagehead && fm.meta.title) {
          if (fm.meta.tag && fm.meta.tag !== 'Home') {
            var t = document.createElement('t-tag');
            t.setAttribute('theme', tagTheme(fm.meta.tag));
            t.textContent = fm.meta.tag;
            pagehead.appendChild(t);
          }
          var h1 = document.createElement('h1');
          h1.id = 'top';
          h1.textContent = fm.meta.title;
          pagehead.appendChild(h1);
        }
        buildToc(toc, tocEl);
      })
      .catch(function (err) {
        content.innerHTML = '<div class="note note-warning"><strong>Could not load ' + escapeHtml(mdPath) +
          '</strong><br>This page reads its content from a Markdown file. Serve the site over HTTP ' +
          '(e.g. <code>python3 -m http.server</code>) instead of opening the file directly, and make sure ' +
          '<code>' + escapeHtml(mdPath) + '</code> exists.<br><small>' + escapeHtml(String(err)) + '</small></div>';
      });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render);
  else render();
})();
