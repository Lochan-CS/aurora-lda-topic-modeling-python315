"""Python standard-library web server; compatible with Python 3.15."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from lda_engine import fit_lda

BASE = Path(__file__).resolve().parent
ASSETS = {'/': ('index.html', 'text/html; charset=utf-8'), '/static/style.css': ('static/style.css', 'text/css; charset=utf-8'), '/static/app.js': ('static/app.js', 'text/javascript; charset=utf-8')}

class Handler(BaseHTTPRequestHandler):
    def respond(self, status, payload, mime='application/json; charset=utf-8'):
        data = payload if isinstance(payload, bytes) else json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        route = urlsplit(self.path).path
        if route not in ASSETS:
            return self.respond(404, {'error': 'Not found'})
        path, mime = ASSETS[route]
        self.respond(200, (BASE / path).read_bytes(), mime)

    def do_POST(self):
        if urlsplit(self.path).path != '/api/analyze':
            return self.respond(404, {'error': 'Not found'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 500000:
                return self.respond(413, {'error': 'Request size must be between 1 and 500000 bytes.'})
            request = json.loads(self.rfile.read(size))
            if not isinstance(request, dict):
                raise ValueError('Expected a JSON object.')
            result = fit_lda(request.get('documents'), request.get('topics'), iterations=160)
            self.respond(200, result)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self.respond(400, {'error': str(exc)})
        except Exception:
            self.respond(500, {'error': 'Unexpected server error.'})

if __name__ == '__main__':
    print('Aurora LDA Studio running at http://127.0.0.1:8000')
    print('Press Ctrl+C to stop.')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
