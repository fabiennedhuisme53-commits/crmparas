// FULL-APP E2E test — the user's exact scenario, on the real patched bundle.
//
// Scenario: the team deleted ALL orders on the server (orders = []),
// and 7 users exist. A brand-new browser (empty localStorage) opens the CRM.
//
// BEFORE the fix: the app fell back to the 168 demo orders (empty list treated as
// "no data") and re-pushed them; users list stuck on [admin]; no live updates.
//
// EXPECTED NOW: server state wins, login works with a SERVER user (not in seed),
// no demo orders are ever pushed, and a later server change arrives live via poll.
//
// Run from tests/:  node test-app.cjs
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '../app/index.html'), 'utf8');
const code = html.match(/<script type="module" crossorigin>([\s\S]*?)<\/script>/)[1];

const sleep = ms => new Promise(r => setTimeout(r, ms));
let pass = 0, fail = 0;
const check = (n, c, x = '') => { c ? (pass++, console.log('  ✔ ' + n)) : (fail++, console.log('  ✘ FAIL: ' + n + (x ? ' — ' + x : ''))); };

const USERS = [
  { id: 1, username: 'admin@paraveda.ma', password: 'admintest123', role: 'admin', agent: '' },
  ...['meryam', 'imane', 'aya', 'sanae', 'rachida', 'hiba'].map((n, i) => ({ id: i + 2, username: n + '@paraveda.ma', password: 'pass' + i, role: 'user', agent: n })),
];
const REAL_ORDER = { id: 1, dateCreation: '2026-08-24', dateConfirmation: '', statut: 'Nouvelle commande', remarques: '', idCmd: '1001', nom: 'عميل حقيقي', telephone: '0612345678', ville: 'Casablanca', adresse: '', qte: 1, prix: 350, produit: 'منتج حقيقي', livraison: '', upsell: 0, carousell: '', agent: 'meryam', link: '', carosellFlag: '', originLead: 'Facebook', commission: 35, fees: '' };

function makeDom() {
  const dom = new JSDOM('<!doctype html><html><head></head><body><div id="root"></div></body></html>', {
    url: 'http://crm.local/',
    pretendToBeVisual: true,
    runScripts: 'outside-only',
  });
  const w = dom.window;
  w.matchMedia = q => ({ matches: false, media: q, onchange: null, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false; } });
  w.IntersectionObserver = class { constructor() {} observe() {} unobserve() {} disconnect() {} takeRecords() { return []; } };
  w.ResizeObserver = class { observe() {} unobserve() {} disconnect() {} };
  w.scrollTo = () => {};
  w.alert = () => {};
  w.confirm = () => true;
  w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: () => () => ({ width: 0, height: 0 }) });
  if (!w.URL.createObjectURL) w.URL.createObjectURL = () => 'blob:fake';
  if (!w.URL.revokeObjectURL) w.URL.revokeObjectURL = () => {};
  return { dom, w };
}

(async () => {
  console.log('\n== E2E: fresh browser opens CRM with EMPTY orders on server ==');
  const server = {
    data: {
      afrizon_users_v1: { t: 1001, d: USERS },
      afrizon_orders_v5: { t: 1002, d: [] },
      afrizon_agent_names_v1: { t: 1003, d: ['Meryam', 'Sanae'] },
    },
    posts: [],
    gets: 0,
  };

  const { dom, w } = makeDom();
  w.fetch = async (url, opts = {}) => {
    if (opts.method === 'POST') {
      server.posts.push(JSON.parse(opts.body));
      return { ok: true, json: async () => ({ ok: true }) };
    }
    server.gets++;
    return { ok: true, json: async () => JSON.parse(JSON.stringify(server.data)) };
  };

  // fresh browser: empty localStorage — boot the REAL app
  w.eval(code);
  await sleep(7000); // initial sync + 3s queue flush + a poll

  const ls = w.localStorage;
  const lsOrders = ls.getItem('afrizon_orders_v5');
  const lsUsers = ls.getItem('afrizon_users_v1');

  check('client synced (poll running)', server.gets >= 2, 'gets=' + server.gets);
  check('orders localStorage = server empty state', lsOrders === '[]', String(lsOrders).slice(0, 60));
  check('users localStorage = 7 server users', lsUsers && JSON.parse(lsUsers).length === 7, String(lsUsers).slice(0, 60));

  const demoOrdersPushed = server.posts.filter(p => p.key === 'afrizon_orders_v5' && Array.isArray(p.d) && p.d.length > 100);
  check('NO demo orders (168) ever pushed to server', demoOrdersPushed.length === 0, JSON.stringify(demoOrdersPushed.map(p => p.d.length)));
  const ordersPushed = server.posts.filter(p => p.key === 'afrizon_orders_v5');
  check('orders pushes (if any) carry empty/server content only', ordersPushed.every(p => Array.isArray(p.d) && p.d.length === 0), 'pushes=' + ordersPushed.length);

  console.log('\n== E2E: login with a SERVER user (impossible before — seed only had admin) ==');
  const inputs = [...w.document.querySelectorAll('input')];
  let userFound = false;
  try {
    const setter = Object.getOwnPropertyDescriptor(w.HTMLInputElement.prototype, 'value').set;
    const userInput = inputs.find(i => (i.placeholder || '').toLowerCase().includes('admin') || (i.placeholder || '').toLowerCase().includes('user') || i.type === 'text' || i.type === 'email');
    const passInput = inputs.find(i => i.type === 'password');
    if (userInput && passInput) {
      setter.call(userInput, 'meryam@paraveda.ma');
      userInput.dispatchEvent(new w.Event('input', { bubbles: true }));
      setter.call(passInput, 'pass0');
      passInput.dispatchEvent(new w.Event('input', { bubbles: true }));
      await sleep(150);
      const btn = [...w.document.querySelectorAll('button')].find(b => /دخول|connecter|login|se connecter|تسجيل/i.test(b.textContent || ''));
      if (btn) { btn.click(); await sleep(800); }
    }
    userFound = ls.getItem('afrizon_session_v1') !== null;
  } catch (e) { /* soft */ }
  check('login with server user meryam@paraveda.ma succeeded', userFound, 'session=' + ls.getItem('afrizon_session_v1'));

  console.log('\n== E2E: LIVE update — another agent adds a real order on the server ==');
  server.data.afrizon_orders_v5 = { t: Date.now(), d: [REAL_ORDER] };
  await sleep(7000); // next 5s poll
  const after = ls.getItem('afrizon_orders_v5');
  check('real order arrived LIVE via poll (no reload)', after && after.includes('منتج حقيقي'), String(after).slice(0, 60));
  check('demo product never appeared in local orders', !after || !after.includes('نظارة القراءة'));

  const demoPushedAfter = server.posts.filter(p => p.key === 'afrizon_orders_v5' && Array.isArray(p.d) && p.d.length > 100);
  check('still no demo orders pushed after live update', demoPushedAfter.length === 0);

  console.log(`\n===== E2E RESULT: ${pass} passed, ${fail} failed =====`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('SUITE ERROR:', e); process.exit(1); });
