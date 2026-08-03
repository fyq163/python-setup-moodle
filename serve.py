#!/usr/bin/env python3
"""Zero-dependency live-reload static server for the markdown-driven guide.

How the "edit .md -> refresh" workflow works:
  1. This server serves the static files (same as `python3 -m http.server`).
  2. It injects a tiny reload client into every .html response.
  3. A background thread watches all .md/.html/.css/.js/.svg/... files.
  4. When you save a file, the client is notified and the browser reloads.
No build step, no external packages, works on GitHub Pages unchanged.

Usage:
    python3 serve.py [port]        # default 8000
Then open http://localhost:<port>/ and edit any .md — the page reloads on save.
"""
import http.server
import os
import sys
import time
import threading

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

_lock = threading.Lock()
_state = {}          # path -> mtime
_counter = 0
_event = threading.Event()

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.codebuddy'}
WATCH_EXT = ('.md', '.html', '.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.gif')


def scan(initial=False):
    global _counter
    changed = False
    seen = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for fn in filenames:
            if not fn.lower().endswith(WATCH_EXT):
                continue
            p = os.path.join(dirpath, fn)
            seen.add(p)
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            if initial:
                _state[p] = m
            else:
                old = _state.get(p)
                if old is None or old != m:
                    _state[p] = m
                    changed = True
    if not initial:
        for p in list(_state):
            if p not in seen:
                del _state[p]
                changed = True
    if changed and not initial:
        with _lock:
            _counter += 1
        _event.set()
        _event.clear()


def watcher():
    scan(initial=True)
    while True:
        time.sleep(0.5)
        scan(initial=False)


CONTENT_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.md': 'text/markdown; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.json': 'application/json',
}

RELOAD_CLIENT = b"""<script>
(function(){
  var last = 0;
  function poll(){
    fetch('/__reload?last='+last).then(function(r){ return r.text(); }).then(function(t){
      var n = parseInt(t, 10);
      if (n > last) { last = n; location.reload(); } else { poll(); }
    }).catch(function(){ setTimeout(poll, 2000); });
  }
  poll();
})();
</script>
"""


class Handler(http.server.BaseHTTPRequestHandler):
    def _safe(self, path):
        real = os.path.realpath(path)
        return real == ROOT or real.startswith(ROOT + os.sep)

    def do_GET(self):
        url = self.path.split('?', 1)[0]
        if url == '/__reload':
            self.handle_reload()
            return
        if url == '/':
            url = '/index.html'
        fpath = os.path.normpath(os.path.join(ROOT, url.lstrip('/')))
        if not self._safe(fpath) or not os.path.isfile(fpath):
            self.send_error(404, 'Not found')
            return
        ext = os.path.splitext(fpath)[1].lower()
        ctype = CONTENT_TYPES.get(ext, 'application/octet-stream')
        with open(fpath, 'rb') as f:
            data = f.read()
        if ext == '.html':
            idx = data.rfind(b'</body>')
            if idx != -1:
                data = data[:idx] + RELOAD_CLIENT + data[idx:]
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def handle_reload(self):
        try:
            last = int(self.path.split('last=', 1)[1])
        except Exception:
            last = 0
        deadline = time.time() + 60
        while True:
            with _lock:
                cur = _counter
            if cur > last or time.time() > deadline:
                break
            _event.wait(0.5)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(str(_counter).encode())

    def log_message(self, fmt, *args):
        pass


if __name__ == '__main__':
    threading.Thread(target=watcher, daemon=True).start()
    srv = http.server.ThreadingHTTPServer(('0.0.0.0', PORT), Handler)
    print(f"Live-reload server on http://localhost:{PORT}/  (Ctrl+C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()
