// Paraveda CRM — live preview server
// Serves the patched app/ statically and routes /api.php through REAL PHP
// (php-wasm 8.3) executing the real api.php v2 — so persistence is real.
const http = require('http');
const fs = require('fs');
const path = require('path');

const APP_DIR = path.join(__dirname, '../app');
const PORT = process.env.PORT || 3000;

let phpInstance = null;
let chain = Promise.resolve(); // serialize wasm PHP requests

async function getPhp() {
  if (phpInstance) return phpInstance;
  const { PHP } = require('@php-wasm/universal');
  const { loadNodeRuntime } = require('@php-wasm/node');
  const runtime = await loadNodeRuntime('8.3', { emscriptenOptions: { processId: 2100 } });
  const php = new PHP(runtime);
  php.mkdirTree('/srv');
  php.writeFile('/srv/api.php', fs.readFileSync(path.join(APP_DIR, 'api.php'), 'utf8'));
  phpInstance = php;
  return php;
}

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
};

function buildCode(req, bodyB64) {
  const url = new URL(req.url, 'http://x');
  const qs = url.search.slice(1);
  const hdr = n => (req.headers[n] || '').replace(/'/g, "\\'");
  let code = `<?php
$_SERVER['REQUEST_METHOD']='${req.method}';
$_SERVER['REMOTE_ADDR']='${req.socket.remoteAddress || '127.0.0.1'}';
$_SERVER['QUERY_STRING']='${qs.replace(/'/g, "\\'")}';
$_SERVER['HTTP_USER_AGENT']='${hdr('user-agent')}';
${req.headers['x-sync-token'] ? `$_SERVER['HTTP_X_SYNC_TOKEN']='${hdr('x-sync-token')}';` : ''}
$_GET=[];`;
  for (const [k, v] of url.searchParams) code += `$_GET['${k.replace(/'/g, "\\'")}']='${String(v).replace(/'/g, "\\'")}';`;
  if (bodyB64) code += `$GLOBALS['CRM_RAW_INPUT']=base64_decode('${bodyB64}');`;
  code += `\nchdir('/srv');\nrequire '/srv/api.php';\n`;
  return code;
}

const server = http.createServer(async (req, res) => {
  try {
    if (req.url.split('?')[0] === '/api.php') {
      const chunks = [];
      req.on('data', c => chunks.push(c));
      req.on('end', async () => {
        const bodyB64 = chunks.length ? Buffer.concat(chunks).toString('base64') : null;
        // re-load latest api.php so edits are reflected
        const php = await getPhp();
        php.writeFile('/srv/api.php', fs.readFileSync(path.join(APP_DIR, 'api.php'), 'utf8'));
        const code = buildCode(req, bodyB64);
        const run = chain.then(() => php.run({ code }));
        chain = run.catch(() => {});
        const r = await run;
        const out = Buffer.from(r.bytes);
        res.writeHead(r.httpStatusCode || 200, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
        res.end(out);
      });
      return;
    }
    // static
    let p = req.url.split('?')[0];
    if (p === '/') p = '/index.html';
    const file = path.normalize(path.join(APP_DIR, p));
    if (!file.startsWith(APP_DIR)) { res.writeHead(403).end('forbidden'); return; }
    fs.readFile(file, (err, data) => {
      if (err) { res.writeHead(404, { 'Content-Type': 'text/plain' }).end('not found'); return; }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
      res.end(data);
    });
  } catch (e) {
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end('server error: ' + e.message);
  }
});

server.listen(PORT, '0.0.0.0', () => console.log(`Paraveda CRM preview on http://0.0.0.0:${PORT}`));
