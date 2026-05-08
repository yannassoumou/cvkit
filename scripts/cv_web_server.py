#!/usr/bin/env python3
"""
CV Web Server — Simple HTTP server for browsing and editing CVs.

Serves the CV repo as a lightweight web dashboard:
- Browse all Offers/ folders
- Preview PDFs inline
- Download DOCX/PDF files
- Edit master CV (CV_Master_texte.txt) via a simple text editor
- Edit offer_data.md files

Usage:
    python3 scripts/cv_web_server.py [--port PORT]

The server binds to 0.0.0.0 and prints the URL on startup.
Run as: python3 scripts/cv_web_server.py &
Stop with: kill <PID> or Ctrl+C

Designed to run after commit/push in the CV job application workflow.
"""

import http.server
import json
import os
import socket
import socketserver
import sys
import threading
import urllib.parse
from pathlib import Path

# Configuration
CV_ROOT = Path(__file__).resolve().parent.parent  # Project root from scripts/
OFFERS_DIR = CV_ROOT / "Offers"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None

def get_free_port():
    """Find a random available port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def get_all_offers():
    """Scan Offers/ directory and return structured data."""
    offers = []
    if not OFFERS_DIR.exists():
        return offers
    for folder in sorted(OFFERS_DIR.iterdir()):
        if folder.is_dir() and not folder.name.startswith('.'):
            files = {}
            for f in folder.iterdir():
                if f.is_file():
                    files[f.name] = {
                        "size": f.stat().st_size,
                        "type": f.suffix.lower(),
                        "path": str(f.relative_to(CV_ROOT))
                    }
            offers.append({
                "name": folder.name,
                "path": str(folder.relative_to(CV_ROOT)),
                "files": files
            })
    return offers

class CVHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler with API endpoints and file serving."""

    def __init__(self, *args, **kwargs):
        kwargs.pop('directory', None)  # Remove directory kwarg to avoid conflict
        super().__init__(*args, directory=str(CV_ROOT), **kwargs)

    def log_message(self, format, *args):
        """Suppress normal request logging."""
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API: list all offers
        if path == "/api/offers":
            self._json_response(get_all_offers())
            return

        # API: get master CV content
        if path == "/api/cv-text":
            cv_file = CV_ROOT / "CV_Master_texte.txt"
            if cv_file.exists():
                self._json_response({"content": cv_file.read_text(encoding="utf-8")})
            else:
                self._json_response({"error": "CV_Master_texte.txt not found"}, 404)
            return

        # API: get offer data
        if path.startswith("/api/offer/"):
            offer_name = urllib.parse.unquote(path.split("/api/offer/", 1)[1])
            offer_file = OFFERS_DIR / offer_name / "offre_data.md"
            if offer_file.exists():
                self._json_response({"content": offer_file.read_text(encoding="utf-8")})
            else:
                self._json_response({"error": "offre_data.md not found"}, 404)
            return

        # API: list files in an offer
        if path.startswith("/api/offer-files/"):
            offer_name = urllib.parse.unquote(path.split("/api/offer-files/", 1)[1])
            offer_folder = OFFERS_DIR / offer_name
            if offer_folder.exists():
                files = {}
                for f in offer_folder.iterdir():
                    if f.is_file():
                        files[f.name] = {
                            "size": f.stat().st_size,
                            "type": f.suffix.lower(),
                            "path": str(f.relative_to(CV_ROOT))
                        }
                self._json_response(files)
            else:
                self._json_response({"error": "Offer not found"}, 404)
            return

        # Serve the dashboard HTML
        if path == "/" or path == "/index.html":
            dashboard_path = CV_ROOT / "dashboard.html"
            if dashboard_path.exists():
                self._serve_file(dashboard_path)
            else:
                self._json_response({"error": "dashboard.html not found"}, 500)
            return

        # Serve other static files
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API: save master CV
        if path == "/api/save-cv-text":
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length).decode('utf-8')
                cv_file = CV_ROOT / "CV_Master_texte.txt"
                cv_file.write_text(body, encoding="utf-8")
                self._json_response({"status": "ok", "message": "CV saved"})
            except Exception as e:
                self._json_response({"error": str(e)}, 500)
            return

        # API: save offer data
        if path.startswith("/api/save-offer/"):
            try:
                offer_name = urllib.parse.unquote(path.split("/api/save-offer/", 1)[1])
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length).decode('utf-8')
                offer_file = OFFERS_DIR / offer_name / "offre_data.md"
                offer_file.write_text(body, encoding="utf-8")
                self._json_response({"status": "ok", "message": "Offer data saved"})
            except Exception as e:
                self._json_response({"error": str(e)}, 500)
            return

        self._json_response({"error": "Method not allowed"}, 405)

    def _json_response(self, data, status=200):
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(response.encode('utf-8')))
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def _serve_file(self, filepath):
        try:
            content = filepath.read_bytes()
            self.send_response(200)
            if filepath.suffix == '.html':
                self.send_header('Content-Type', 'text/html; charset=utf-8')
            elif filepath.suffix == '.css':
                self.send_header('Content-Type', 'text/css')
            elif filepath.suffix == '.js':
                self.send_header('Content-Type', 'application/javascript')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self._json_response({"error": str(e)}, 500)


def main():
    port = PORT or get_free_port()
    os.chdir(str(CV_ROOT))

    # Generate dashboard if it doesn't exist
    dashboard_path = CV_ROOT / "dashboard.html"
    if not dashboard_path.exists():
        generate_dashboard(dashboard_path)

    handler = lambda *args, **kwargs: CVHandler(*args, **kwargs)

    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        url = f"http://0.0.0.0:{port}"
        print(f"\n{'='*60}")
        print(f"  CV WEB SERVER")
        print(f"{'='*60}")
        print(f"  URL: {url}")
        print(f"  Root: {CV_ROOT}")
        print(f"  Offers: {len(get_all_offers())} offers found")
        print(f"{'='*60}")
        print(f"  Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            sys.exit(0)


def generate_dashboard(path):
    """Generate the HTML dashboard for browsing and editing CVs."""
    html = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CV Manager</title>
<style>
  :root {
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #242836;
    --border: #2e3348;
    --text: #e4e6f0;
    --text-dim: #8b8fa8;
    --accent: #6c8cff;
    --accent-hover: #8aa4ff;
    --green: #4ade80;
    --orange: #fb923c;
    --red: #f87171;
    --radius: 8px;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }

  /* Header */
  .header { background: var(--surface); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
  .header h1 { font-size: 20px; font-weight: 600; }
  .header h1 span { color: var(--accent); }
  .header-actions { display: flex; gap: 8px; }
  .btn { padding: 8px 16px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); border-radius: var(--radius); cursor: pointer; font-size: 13px; transition: all 0.15s; }
  .btn:hover { border-color: var(--accent); background: rgba(108,140,255,0.1); }
  .btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  .btn-sm { padding: 4px 12px; font-size: 12px; }

  /* Layout */
  .layout { display: flex; height: calc(100vh - 57px); }
  .sidebar { width: 320px; background: var(--surface); border-right: 1px solid var(--border); overflow-y: auto; flex-shrink: 0; }
  .main { flex: 1; overflow-y: auto; padding: 24px; }

  /* Sidebar */
  .sidebar-section { padding: 16px; border-bottom: 1px solid var(--border); }
  .sidebar-section h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--text-dim); margin-bottom: 12px; }
  .offer-item { padding: 10px 12px; border-radius: var(--radius); cursor: pointer; transition: all 0.15s; margin-bottom: 2px; display: flex; align-items: center; gap: 10px; }
  .offer-item:hover { background: var(--surface2); }
  .offer-item.active { background: rgba(108,140,255,0.15); border: 1px solid var(--accent); }
  .offer-icon { font-size: 16px; }
  .offer-name { font-size: 13px; font-weight: 500; flex: 1; word-break: break-word; }
  .offer-badge { font-size: 10px; padding: 2px 6px; border-radius: 4px; background: var(--surface2); color: var(--text-dim); }

  /* Cards */
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; margin-bottom: 16px; }
  .card h2 { font-size: 18px; margin-bottom: 12px; }
  .card h3 { font-size: 14px; color: var(--text-dim); margin-bottom: 8px; }

  /* File list */
  .file-list { list-style: none; }
  .file-item { display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: var(--radius); transition: background 0.15s; cursor: pointer; }
  .file-item:hover { background: var(--surface2); }
  .file-icon { font-size: 16px; width: 24px; text-align: center; }
  .file-name { font-size: 13px; flex: 1; }
  .file-size { font-size: 11px; color: var(--text-dim); }
  .file-actions { display: flex; gap: 4px; }

  /* Editor */
  .editor-container { display: flex; flex-direction: column; height: calc(100vh - 120px); }
  .editor-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
  .editor-header h2 { font-size: 16px; }
  textarea { width: 100%; flex: 1; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); color: var(--text); padding: 16px; font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace; font-size: 13px; resize: none; line-height: 1.6; tab-size: 4; }
  textarea:focus { outline: none; border-color: var(--accent); }

  /* PDF preview */
  .pdf-preview { width: 100%; height: calc(100vh - 180px); border: 1px solid var(--border); border-radius: var(--radius); background: #fff; }

  /* Toast */
  .toast { position: fixed; bottom: 24px; right: 24px; padding: 12px 20px; background: var(--green); color: #000; border-radius: var(--radius); font-size: 13px; font-weight: 500; transform: translateY(100px); opacity: 0; transition: all 0.3s; z-index: 999; }
  .toast.show { transform: translateY(0); opacity: 1; }

  /* Empty state */
  .empty-state { text-align: center; padding: 60px 20px; color: var(--text-dim); }
  .empty-state .icon { font-size: 48px; margin-bottom: 16px; }
  .empty-state p { font-size: 14px; }

  /* Stats bar */
  .stats { display: flex; gap: 16px; margin-bottom: 20px; }
  .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; flex: 1; }
  .stat-value { font-size: 24px; font-weight: 700; color: var(--accent); }
  .stat-label { font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }

  /* Responsive */
  @media (max-width: 768px) {
    .sidebar { width: 260px; }
    .stats { flex-direction: column; }
  }
</style>
</head>
<body>

<div class="header">
  <h1>📄 <span>CV</span> Manager</h1>
  <div class="header-actions">
    <button class="btn" onclick="loadMasterCV()">✏️ Master CV</button>
    <button class="btn" onclick="location.reload()">🔄 Refresh</button>
  </div>
</div>

<div class="layout">
  <div class="sidebar">
    <div class="sidebar-section">
      <h3>📁 Offers</h3>
      <div id="offer-list"></div>
    </div>
    <div class="sidebar-section">
      <h3>📄 Master CV</h3>
      <div class="offer-item" onclick="loadMasterCV()">
        <span class="offer-icon">📝</span>
        <span class="offer-name">CV_Master_texte.txt</span>
      </div>
    </div>
  </div>

  <div class="main" id="main-content">
    <div class="empty-state">
      <div class="icon">👈</div>
      <p>Select an offer from the sidebar or click <strong>Master CV</strong> to edit</p>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
let currentView = 'home'; // home, offer, editor
let currentOffer = null;
let editorContent = '';

// Initialize
async function init() {
  const offers = await api('/api/offers');
  renderOfferList(offers);
  showStats(offers);
}

async function api(path) {
  const res = await fetch(path);
  return res.json();
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

function showStats(offers) {
  let totalFiles = 0;
  offers.forEach(o => totalFiles += Object.keys(o.files).length);
  document.getElementById('main-content').innerHTML = `
    <div class="stats">
      <div class="stat-card">
        <div class="stat-value">${offers.length}</div>
        <div class="stat-label">Offers</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${totalFiles}</div>
        <div class="stat-label">Files</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">📝</div>
        <div class="stat-label">Master CV Ready</div>
      </div>
    </div>
    <div class="empty-state">
      <div class="icon">👈</div>
      <p>Select an offer from the sidebar or click <strong>Master CV</strong> to edit</p>
    </div>
  `;
}

function renderOfferList(offers) {
  const el = document.getElementById('offer-list');
  if (!offers.length) {
    el.innerHTML = '<p style="color:var(--text-dim);font-size:13px;padding:8px;">No offers found</p>';
    return;
  }
  el.innerHTML = offers.map(o => `
    <div class="offer-item" onclick="loadOffer('${o.name}')" id="offer-${o.name}">
      <span class="offer-icon">📁</span>
      <span class="offer-name">${o.name}</span>
      <span class="offer-badge">${Object.keys(o.files).length}</span>
    </div>
  `).join('');
}

function getFileIcon(name) {
  const ext = name.split('.').pop().toLowerCase();
  const icons = { pdf: '📕', docx: '📘', md: '📝', txt: '📄', png: '🖼️', jpg: '🖼️', jpeg: '🖼️', html: '🌐', js: '⚙️' };
  return icons[ext] || '📄';
}

async function loadOffer(name) {
  currentOffer = name;
  document.querySelectorAll('.offer-item').forEach(e => e.classList.remove('active'));
  const el = document.getElementById(`offer-${name}`);
  if (el) el.classList.add('active');

  const files = await api(`/api/offer-files/${encodeURIComponent(name)}`);
  let filesHtml = Object.entries(files).map(([fname, fdata]) => `
    <li class="file-item" onclick="openFile('${name}', '${fname}')">
      <span class="file-icon">${getFileIcon(fname)}</span>
      <span class="file-name">${fname}</span>
      <span class="file-size">${formatSize(fdata.size)}</span>
      <div class="file-actions">
        <button class="btn btn-sm" onclick="event.stopPropagation(); downloadFile('${fdata.path}')">⬇️</button>
      </div>
    </li>
  `).join('');

  document.getElementById('main-content').innerHTML = `
    <div class="card">
      <h2>📁 ${name}</h2>
      <h3>${Object.keys(files).length} files</h3>
      <ul class="file-list">${filesHtml}</ul>
    </div>
  `;
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024*1024) return (bytes/1024).toFixed(1) + ' KB';
  return (bytes/(1024*1024)).toFixed(1) + ' MB';
}

async function openFile(offerName, fileName) {
  const ext = fileName.split('.').pop().toLowerCase();
  const filePath = `${offerName}/${fileName}`;

  if (ext === 'pdf') {
    document.getElementById('main-content').innerHTML = `
      <div class="card">
        <div class="editor-header">
          <h2>📕 ${fileName}</h2>
          <button class="btn" onclick="downloadFile('${offerName}/${fileName}')">⬇️ Download</button>
        </div>
        <iframe class="pdf-preview" src="/${filePath}"></iframe>
      </div>
    `;
  } else if (ext === 'md') {
    const data = await api(`/api/offer/${encodeURIComponent(offerName)}`);
    document.getElementById('main-content').innerHTML = `
      <div class="editor-container">
        <div class="editor-header">
          <h2>📝 ${fileName}</h2>
          <div>
            <button class="btn" onclick="downloadFile('${offerName}/${fileName}')">⬇️ Download</button>
            <button class="btn active" onclick="saveOfferData('${offerName}')">💾 Save</button>
          </div>
        </div>
        <textarea id="editor" spellcheck="false">${escapeHtml(data.content || '')}</textarea>
      </div>
    `;
  } else {
    downloadFile(`${offerName}/${fileName}`);
  }
}

async function loadMasterCV() {
  document.querySelectorAll('.offer-item').forEach(e => e.classList.remove('active'));
  const data = await api('/api/cv-text');
  document.getElementById('main-content').innerHTML = `
    <div class="editor-container">
      <div class="editor-header">
        <h2>📝 Master CV — CV_Master_texte.txt (Source of Truth)</h2>
        <div>
          <button class="btn" onclick="downloadFile('CV_Master_texte.txt')">⬇️ Download</button>
          <button class="btn active" onclick="saveMasterCV()">💾 Save</button>
        </div>
      </div>
      <textarea id="editor" spellcheck="false">${escapeHtml(data.content || '')}</textarea>
    </div>
  `;
}

async function saveMasterCV() {
  const content = document.getElementById('editor').value;
  const res = await fetch('/api/save-cv-text', {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: content
  });
  const data = await res.json();
  if (data.status === 'ok') {
    showToast('✅ Master CV saved!');
    editorContent = content;
  } else {
    showToast('❌ Error: ' + data.error);
  }
}

async function saveOfferData(offerName) {
  const content = document.getElementById('editor').value;
  const res = await fetch(`/api/save-offer/${encodeURIComponent(offerName)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: content
  });
  const data = await res.json();
  if (data.status === 'ok') {
    showToast('✅ Offer data saved!');
  } else {
    showToast('❌ Error: ' + data.error);
  }
}

function downloadFile(path) {
  window.open(`/${path}`, '_blank');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Tab support in textarea
document.addEventListener('keydown', function(e) {
  const ta = document.getElementById('editor');
  if (ta && document.activeElement === ta && e.key === 'Tab') {
    e.preventDefault();
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    ta.value = ta.value.substring(0, start) + '    ' + ta.value.substring(end);
    ta.selectionStart = ta.selectionEnd = start + 4;
  }
});

init();
</script>
</body>
</html>"""
    path.write_text(html, encoding='utf-8')


if __name__ == '__main__':
    main()
