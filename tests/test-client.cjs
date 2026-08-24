// Behavioural test of the PATCHED client sync code (extracted from the bundle)
// Run from tests/:  node test-client.cjs
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '../app/index.html'), 'utf8');
const SEEDS = JSON.parse(fs.readFileSync(path.join(__dirname, 'seeds.json'), 'utf8'));

const start = html.indexOf('Rd="');
const end = html.indexOf('const Zc="afrizon_worktimes_v1"');
if (start < 0 || end < 0 || end <= start) { console.error('sync block not found'); process.exit(1); }
const block = html.slice(start, end);
const TOKEN = block.match(/Rd="([^"]+)"/)[1];

let pass = 0, fail = 0;
const check = (n, c, x = '') => { c ? (pass++, console.log('  ✔ ' + n)) : (fail++, console.log('  ✘ FAIL: ' + n + (x ? ' — ' + x : ''))); };
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function makeClient({ serverGetResponses, serverLog }) {
  const ls = new Map();
  global.localStorage = {
    getItem: k => (ls.has(k) ? ls.get(k) : null),
    setItem: (k, v) => ls.set(k, String(v)),
    removeItem: k => ls.delete(k),
  };
  let getIdx = 0;
  global.fetch = async (url, opts = {}) => {
    if (opts.method === 'POST') {
      serverLog.push({ body: JSON.parse(opts.body), token: opts.headers['X-Sync-Token'] });
      return { ok: true, json: async () => ({ ok: true }) };
    }
    const resp = serverGetResponses[Math.min(getIdx++, serverGetResponses.length - 1)];
    if (resp === 'FAIL') throw new Error('network down');
    return { ok: true, json: async () => resp };
  };
  const run = new Function('localStorage', 'fetch', block + `
    return { sync: S4, push: aa, isSynced: () => $c, setCb: Ms };`);
  return run(global.localStorage, global.fetch);
}

(async () => {
  const goodData = {
    afrizon_users_v1: { t: 111000, d: JSON.parse(SEEDS.users_seed).concat([{ id: 2, username: 'meryam@p.ma', password: 'x', role: 'user', agent: 'Meryam' }]) },
    afrizon_orders_v5: { t: 112000, d: [] },
  };

  console.log('\n== A. THE INCIDENT: fresh browser (empty localStorage) opens the CRM ==');
  const serverLogA = [];
  const cA = await makeClient({ serverGetResponses: [goodData], serverLog: serverLogA });
  global.localStorage.setItem('afrizon_users_v1', SEEDS.users_seed);
  cA.push('afrizon_users_v1');
  cA.sync();
  await sleep(3600);
  check('client synced', cA.isSynced() === true);
  const usersPush = serverLogA.find(p => p.body.key === 'afrizon_users_v1');
  check('users were pushed only AFTER sync', !!usersPush);
  check('pushed SERVER data (2 users), NOT the factory seed', usersPush && usersPush.body.d.length === 2 && usersPush.body.d[1].username === 'meryam@p.ma',
    usersPush ? JSON.stringify(usersPush.body.d).slice(0, 90) : 'no push');
  check('push carries the current token', usersPush && usersPush.token === TOKEN);
  check('token is not the old exposed one', TOKEN !== 'paraveda-2026-sync');
  check('local ct updated from server', Number(global.localStorage.getItem('ct_afrizon_users_v1')) >= 111000);

  console.log('\n== B. server down at boot → retry (P2) → queue flush ==');
  const serverLogB = [];
  const cB = await makeClient({ serverGetResponses: ['FAIL', goodData], serverLog: serverLogB });
  global.localStorage.setItem('afrizon_users_v1', SEEDS.users_seed);
  cB.push('afrizon_users_v1');
  cB.sync();
  await sleep(300);
  check('not synced while server down', cB.isSynced() === false);
  check('no premature POST while unsynced', serverLogB.length === 0);
  await sleep(5300);
  check('synced after retry', cB.isSynced() === true);
  await sleep(3400);
  const pushB = serverLogB.find(p => p.body.key === 'afrizon_users_v1');
  check('queued push flushed with SERVER data after recovery', pushB && pushB.body.d.length === 2, pushB ? 'len=' + pushB.body.d.length : 'no push');

  console.log('\n== C. normal edit flow after sync ==');
  const serverLogC = [];
  const cC = await makeClient({ serverGetResponses: [goodData], serverLog: serverLogC });
  await cC.sync();
  await sleep(100);
  global.localStorage.setItem('afrizon_chat_v1', JSON.stringify([{ id: 1, msg: 'hi' }]));
  cC.push('afrizon_chat_v1');
  await sleep(400);
  const pushC = serverLogC.find(p => p.body.key === 'afrizon_chat_v1');
  check('edit pushed normally', pushC && pushC.body.d[0].msg === 'hi');
  check('unknown key ignored client-side', (cC.push('bogus_key'), true) && !serverLogC.some(p => p.body.key === 'bogus_key'));

  console.log(`\n===== CLIENT RESULT: ${pass} passed, ${fail} failed =====`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('SUITE ERROR:', e); process.exit(1); });
