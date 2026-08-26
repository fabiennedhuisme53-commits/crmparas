// Extract factory seed data from the built CRM bundle and emit exact JSON
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '../app/index.html'), 'utf8');

// bracket/brace-balanced scanner that respects strings
function extractAfter(src, startIdx, openChar, closeChar) {
  let i = startIdx, depth = 0, inStr = null;
  for (; i < src.length; i++) {
    const c = src[i];
    if (inStr) {
      if (c === '\\') { i++; continue; }
      if (c === inStr) inStr = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
    if (c === openChar) depth++;
    else if (c === closeChar) {
      depth--;
      if (depth === 0) return src.slice(startIdx, i + 1);
    }
  }
  throw new Error('unbalanced');
}
function grabEq(name) {
  const m = html.match(new RegExp('(?:^|[,;])' + name.replace(/\$/g, '\\$') + '\\s*='));
  if (!m) throw new Error('not found: ' + name);
  const i = m.index + m[0].length;
  return extractAfter(html, i, '[', ']');
}
function grabFn(name) {
  const m = html.match(new RegExp('function ' + name + '\\(\\)\\{'));
  if (!m) throw new Error('fn not found: ' + name);
  const i = m.index + m[0].length - 1; // at '{'
  return extractAfter(html, i, '{', '}');
}

const A4 = eval(grabEq('A4'));
const vp = eval(grabEq('vp'));
const k4 = eval(grabEq('k4'));
const dpSrc = grabFn('dp'); // "{return A4.map(...)}"
const dp = new Function('A4', dpSrc);
const orders = dp(A4);

function parseInt2(x) { const n = parseInt(x); return isNaN(n) ? 1 : n; } // mimic ||1 fallback for qte

// Re-run dp mapping manually to reproduce exactly what the bundle does
// (the eval'd dp already applies the same expressions from the bundle source)
const seeds = {
  users_seed: k4,
  orders_seed: orders,
  agents_seed: vp,
};
const out = {};
for (const [k, v] of Object.entries(seeds)) {
  out[k] = JSON.stringify(v);
}
fs.writeFileSync('/tmp/seeds.json', JSON.stringify(out, null, 2));
console.log('users :', out.users_seed.slice(0, 120));
console.log('orders: count =', orders.length, ' first =', out.orders_seed.slice(0, 90));
console.log('agents:', out.agents_seed);
