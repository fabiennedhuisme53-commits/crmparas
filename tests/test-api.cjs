// Paraveda CRM api.php v2.1 FINAL — full behavioural test suite (real PHP via WASM)
// Run from tests/:  npm i && node test-api.cjs
const { PHP } = require('@php-wasm/universal');
const { loadNodeRuntime } = require('@php-wasm/node');
const fs = require('fs');
const path = require('path');

const API = fs.readFileSync(path.join(__dirname, '../app/api.php'), 'utf8');
const SEEDS = JSON.parse(fs.readFileSync(path.join(__dirname, 'seeds.json'), 'utf8'));
const TOKEN = API.match(/\$SECRET = '([a-f0-9]+)';/)[1];
const OLD_USERS_SEED = [{ id: 1, username: 'admin@paraveda.ma', password: 'admin123', role: 'admin', agent: '' }];

let pass = 0, fail = 0;
function check(name, cond, extra = '') {
  if (cond) { pass++; console.log('  ✔ ' + name); }
  else { fail++; console.log('  ✘ FAIL: ' + name + (extra ? ' — ' + extra : '')); }
}

function buildReq(method, { token, query = {}, body = null, ua = 'test-agent', ip = '10.0.0.5', pre = '' } = {}) {
  const q = Object.entries(query).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&');
  let php = `<?php
$_SERVER['REQUEST_METHOD']='${method}';
$_SERVER['REMOTE_ADDR']='${ip}';
$_SERVER['HTTP_USER_AGENT']='${ua}';
$_SERVER['QUERY_STRING']='${q}';
$_GET=[]; `;
  if (token) php += `$_SERVER['HTTP_X_SYNC_TOKEN']='${token}';`;
  for (const [k, v] of Object.entries(query)) php += `$_GET['${k}']='${String(v).replace(/'/g, "\\'")}';`;
  if (body !== null) {
    const b64 = Buffer.from(JSON.stringify(body), 'utf8').toString('base64');
    php += `$GLOBALS['CRM_RAW_INPUT']=base64_decode('${b64}');`;
  }
  php += `\n${pre}\nchdir('/srv');\nrequire '/srv/api.php';\n`;
  return php;
}

(async () => {
  const php = new PHP(await loadNodeRuntime('8.3', { emscriptenOptions: { processId: 1300 } }));
  php.mkdirTree('/srv');
  php.writeFile('/srv/api.php', API);

  async function req(method, opts) {
    const r = await php.run({ code: buildReq(method, opts) });
    const text = Buffer.from(r.bytes).toString('utf8').trim();
    let json = null;
    try { json = JSON.parse(text); } catch {}
    return { status: r.httpStatusCode, text, json };
  }
  const post = (key, t, d, extra = {}) => req('POST', { token: TOKEN, body: { key, t, d }, ...extra });
  const get = () => req('GET', { token: TOKEN });

  const now = Date.now();
  const usersSeedNew = JSON.parse(SEEDS.users_seed);
  const ordersSeed = JSON.parse(SEEDS.orders_seed);
  const agentsSeed = JSON.parse(SEEDS.agents_seed);
  const usersV2 = [
    { id: 1, username: 'admin@paraveda.ma', password: 'whatever', role: 'admin', agent: '' },
    ...['Meryam','imane','AYA','Sanae','RACHIDA','HIBA'].map((n, i) => ({ id: i + 2, username: n + '@paraveda.ma', password: 'pass' + i, role: 'user', agent: n })),
  ];

  console.log('\n== 1. fresh install ==');
  let r = await get();
  check('GET fresh → {}', r.text === '{}', r.text.slice(0, 80));

  console.log('\n== 2. initial seed push allowed (first install) ==');
  r = await post('afrizon_users_v1', now - 50000, usersSeedNew);
  check('new seed accepted on empty key', r.json && r.json.ok === true, r.text.slice(0, 120));
  r = await post('afrizon_orders_v5', now - 50000, ordersSeed);
  check('orders seed accepted on empty key', r.json && r.json.ok === true, r.text.slice(0, 120));
  r = await post('afrizon_agent_names_v1', now - 50000, agentsSeed);
  check('agents seed accepted on empty key', r.json && r.json.ok === true, r.text.slice(0, 120));

  console.log('\n== 3. real work: add 6 users, delete all orders ==');
  r = await post('afrizon_users_v1', now - 40000, usersV2);
  check('users v2 stored', r.json && r.json.ok === true, r.text.slice(0, 120));
  r = await post('afrizon_orders_v5', now - 30000, []);
  check('orders emptied', r.json && r.json.ok === true, r.text.slice(0, 120));
  r = await get();
  check('GET shows 7 users', r.json && Array.isArray(r.json.afrizon_users_v1.d) && r.json.afrizon_users_v1.d.length === 7);
  check('GET shows 0 orders', r.json && Array.isArray(r.json.afrizon_orders_v5.d) && r.json.afrizon_orders_v5.d.length === 0);
  check('GET output is object shape', r.text.startsWith('{'));

  console.log('\n== 4. THE INCIDENT (both generations of cached browsers) ==');
  const ghostT = now + 3600_000;
  r = await post('afrizon_users_v1', ghostT, OLD_USERS_SEED, { ua: 'old-cached-browser', ip: '10.9.9.8' });
  check('ghost OLD seed (admin123) REJECTED', r.json && r.json.ok === false && r.json.rejected === 'ghost_seed', r.text.slice(0, 120));
  r = await post('afrizon_users_v1', ghostT, usersSeedNew, { ua: 'new-ghost-browser', ip: '10.9.9.9' });
  check('ghost NEW seed REJECTED', r.json && r.json.ok === false && r.json.rejected === 'ghost_seed', r.text.slice(0, 120));
  r = await post('afrizon_orders_v5', ghostT, ordersSeed, { ua: 'ghost-browser', ip: '10.9.9.9' });
  check('ghost orders seed (168 demo) REJECTED', r.json && r.json.ok === false && r.json.rejected === 'ghost_seed', r.text.slice(0, 120));
  check('ghost rejections use HTTP 200 (no client retry storm)', r.status === 200);
  r = await get();
  check('users still 7 after ghosts', r.json.afrizon_users_v1.d.length === 7);
  check('orders still 0 after ghosts', r.json.afrizon_orders_v5.d.length === 0);

  console.log('\n== 5. generic ghost guard (old identical version of any key) ==');
  const chatV1 = [{ id: 1, msg: 'salam' }];
  const chatV2 = [{ id: 1, msg: 'salam' }, { id: 2, msg: 'labas?' }];
  r = await post('afrizon_chat_v1', now - 20000, chatV1);
  check('chat v1 stored', r.json.ok === true);
  r = await post('afrizon_chat_v1', now - 10000, chatV2);
  check('chat v2 stored', r.json.ok === true);
  r = await post('afrizon_chat_v1', now, chatV1);
  check('within grace: old identical version allowed', r.json.ok === true, r.text.slice(0, 120));
  await post('afrizon_chat_v1', now + 1000, chatV2);
  const aged = `<?php
$m = json_decode(file_get_contents('/crm-paraveda-data/meta.json'), true);
$m['keys']['afrizon_chat_v1']['hist'][0]['seen'] = time() - 7200;
file_put_contents('/crm-paraveda-data/meta.json', json_encode($m));
echo 'aged';`;
  await php.run({ code: aged });
  r = await post('afrizon_chat_v1', now + 2000, chatV1);
  check('after grace: old identical version REJECTED (ghost)', r.json && r.json.ok === false && r.json.rejected === 'ghost', r.text.slice(0, 120));
  r = await get();
  check('chat still v2', r.json.afrizon_chat_v1.d.length === 2);

  console.log('\n== 6. noop + stale + clock skew ==');
  r = await post('afrizon_users_v1', now + 5000, usersV2);
  check('identical content → noop ok', r.json.ok === true && r.json.noop === true, r.text.slice(0, 120));
  const usersV3 = [...usersV2, { id: 99, username: 'x@paraveda.ma', password: 'x', role: 'user', agent: 'X' }];
  r = await post('afrizon_users_v1', 1000, usersV3);
  check('older-t write ignored as stale', r.json.ok === true && r.json.stale === true, r.text.slice(0, 120));
  r = await get();
  check('stale write did not change data (still 7 users)', r.json.afrizon_users_v1.d.length === 7);
  r = await post('afrizon_villes_v2', now + 365 * 24 * 3600 * 1000, ['Casablanca', 'Rabat']);
  check('far-future t accepted but clamped', r.json.ok === true);
  r = await get();
  check('clamped t <= now+61s', r.json.afrizon_villes_v2.t <= Date.now() + 61000, String(r.json.afrizon_villes_v2.t));

  console.log('\n== 7. corruption & deletion auto-recovery ==');
  await php.run({ code: `<?php file_put_contents('/crm-paraveda-data/crm_data.json', 'GARBAGE{{{{'); echo 'corrupted';` });
  r = await get();
  check('GET after corruption auto-recovered', r.json && r.json.afrizon_users_v1 && r.json.afrizon_users_v1.d.length === 7, r.text.slice(0, 100));
  await php.run({ code: `<?php unlink('/crm-paraveda-data/crm_data.json'); echo 'deleted';` });
  r = await get();
  check('GET after deletion auto-recovered', r.json && r.json.afrizon_users_v1 && r.json.afrizon_users_v1.d.length === 7, r.text.slice(0, 100));

  console.log('\n== 8. auth & validation (old token must fail) ==');
  r = await req('POST', { token: 'paraveda-2026-sync', body: { key: 'afrizon_users_v1', t: now, d: usersSeedNew } });
  check('OLD token rejected', r.json && r.json.ok === false);
  r = await req('POST', { token: 'wrong', body: { key: 'afrizon_users_v1', t: now, d: usersSeedNew } });
  check('bad token rejected', r.json && r.json.ok === false);
  r = await post('not_a_key', now, {});
  check('unknown key rejected', r.json && r.json.ok === false);
  r = await req('POST', { token: TOKEN, body: null });
  check('empty body rejected', r.json && r.json.ok === false);
  r = await req('GET', { query: { action: 'status' } });
  check('status without token → 403', r.json && r.json.ok === false);
  r = await req('GET', { token: 'paraveda-2026-sync', query: { action: 'status', token: 'paraveda-2026-sync' } });
  check('status with OLD token → 403', r.json && r.json.ok === false);

  console.log('\n== 9. status / backups / restore ==');
  r = await req('GET', { token: TOKEN, query: { action: 'status' } });
  check('status ok with new token', r.json && r.json.ok === true);
  check('status shows storage mode', r.json.storage && typeof r.json.storage.mode === 'string');
  check('status shows install id', r.json.install && r.json.install.id.length === 12);
  check('status counters present', r.json.counters && typeof r.json.counters.ghost_seed === 'number');
  check('status audit tail shows ghost events', (r.json.audit_tail || []).some(l => l.includes('ghost_seed')));
  console.log('    counters:', JSON.stringify(r.json.counters));

  r = await req('GET', { token: TOKEN, query: { action: 'backups' } });
  check('backups listed', r.json && r.json.ok === true && r.json.backups.length > 0, 'count=' + (r.json.backups || []).length);
  const oldest = r.json.backups[r.json.backups.length - 1].file;
  r = await req('POST', { token: TOKEN, body: { action: 'restore', file: oldest } });
  check('restore executed', r.json && r.json.ok === true, r.text.slice(0, 120));
  r = await get();
  check('after restore: orders back to demo state', r.json.afrizon_orders_v5.d.length === 168, 'n=' + r.json.afrizon_orders_v5.d.length);
  r = await req('POST', { token: TOKEN, body: { action: 'restore', file: '../../etc/passwd' } });
  check('restore path traversal blocked', r.json && r.json.ok === false);

  console.log('\n== 10. fresh instance: legacy crm_data.json migration ==');
  const php2 = new PHP(await loadNodeRuntime('8.3', { emscriptenOptions: { processId: 1301 } }));
  php2.mkdirTree('/srv');
  php2.writeFile('/srv/api.php', API);
  php2.writeFile('/srv/crm_data.json', JSON.stringify({ afrizon_users_v1: { t: 123456, d: usersV2 } }));
  const r2 = await php2.run({ code: buildReq('GET', { token: TOKEN }) });
  const j2 = JSON.parse(Buffer.from(r2.bytes).toString());
  check('legacy data migrated & served', j2.afrizon_users_v1 && j2.afrizon_users_v1.d.length === 7);
  check('legacy file untouched (kept as fallback)', php2.fileExists('/srv/crm_data.json'));

  console.log('\n== 11. restore bumps t so all clients adopt it ==');
  // نزرع نسخة احتياطية قديمة بـ t صغير جداً ثم نسترجعها
  await php.run({ code: `<?php
$old = json_encode(array('afrizon_users_v1' => array('t' => 1000, 'd' => json_decode(file_get_contents('/crm-paraveda-data/crm_data.json'), true)['afrizon_users_v1']['d'])));
file_put_contents('/crm-paraveda-data/backups/b-20210202-020202-222.json', $old);
echo 'planted';` });
  r = await req('POST', { token: TOKEN, body: { action: 'restore', file: 'b-20210202-020202-222.json' } });
  check('restore ok', r.json && r.json.ok === true, r.text.slice(0, 80));
  r = await get();
  check('after restore: t bumped to ~now (clients will adopt)', r.json.afrizon_users_v1.t >= Date.now() - 3000, String(r.json.afrizon_users_v1.t));

  console.log('\n== 12. backups size cap (disk protection) ==');
  await php.run({ code: `<?php
$dir = '/crm-paraveda-data/backups';
for ($i = 1; $i <= 6; $i++) {
  file_put_contents(sprintf('%s/b-20200101-0000%02d-001.json', $dir, $i), str_repeat('x', 2000));
}
echo 'dummies created';` });
  r = await req('GET', { token: TOKEN, query: { action: 'backups' } });
  const beforeCount = r.json.backups.filter(b => b.file.startsWith('b-2020')).length;
  check('6 dummy backups planted', beforeCount === 6);
  // كتابة حقيقية على مفتاح موجود (users) بمحتوى جديد → تُنشأ نسخة → التصفية تعمل
  r = await req('POST', { token: TOKEN, body: { key: 'afrizon_users_v1', t: Date.now() + 9000, d: usersV3 }, pre: `$GLOBALS['CRM_BACKUPS_MAX_BYTES'] = 4000;` });
  check('write with tiny cap succeeds', r.json && r.json.ok === true, r.text.slice(0, 80));
  r = await req('GET', { token: TOKEN, query: { action: 'backups' } });
  const after2020 = r.json.backups.filter(b => b.file.startsWith('b-2020')).length;
  check('old heavy backups trimmed below cap', after2020 < beforeCount, `before=${beforeCount} after=${after2020}`);
  check('at least 2 backups survive the trim', r.json.backups.length >= 2);

  console.log('\n== 13. demo auto-wipe (exact factory seed) ==');
  const php3 = new PHP(await loadNodeRuntime('8.3', { emscriptenOptions: { processId: 1302 } }));
  php3.mkdirTree('/srv');
  php3.writeFile('/srv/api.php', API);
  const demoOrders = JSON.parse(SEEDS.orders_seed);
  php3.mkdirTree('/crm-paraveda-data');
  php3.writeFile('/crm-paraveda-data/crm_data.json', JSON.stringify({
    afrizon_users_v1: { t: 900, d: usersV2 },
    afrizon_orders_v5: { t: 1000, d: demoOrders },
  }));
  r = await (async () => {
    const rr = await php3.run({ code: buildReq('GET', { token: TOKEN }) });
    return { text: Buffer.from(rr.bytes).toString().trim(), json: JSON.parse(Buffer.from(rr.bytes).toString()) };
  })();
  check('GET wiped exact-demo orders to empty', r.json.afrizon_orders_v5 && Array.isArray(r.json.afrizon_orders_v5.d) && r.json.afrizon_orders_v5.d.length === 0 && r.json.afrizon_users_v1 && r.json.afrizon_users_v1.d.length === 7, 'orders=' + (r.json.afrizon_orders_v5 ? r.json.afrizon_orders_v5.d.length : '?') + ' users=' + (r.json.afrizon_users_v1 ? r.json.afrizon_users_v1.d.length : '?'));
  check('wipe bumped t so clients adopt the empty list', r.json.afrizon_orders_v5.t >= Date.now() - 5000, String(r.json.afrizon_orders_v5.t));
  r = await (async () => {
    const rr = await php3.run({ code: buildReq('GET', { token: TOKEN, query: { action: 'status' } }) });
    return { json: JSON.parse(Buffer.from(rr.bytes).toString()) };
  })();
  const wipes = (r.json.audit_tail || []).filter(l => l.includes('demo_autowipe')).length;
  check('wipe happened exactly once (flag works)', wipes === 1, 'wipes=' + wipes);

  // mixed data must NOT be touched
  const php4 = new PHP(await loadNodeRuntime('8.3', { emscriptenOptions: { processId: 1303 } }));
  php4.mkdirTree('/srv');
  php4.writeFile('/srv/api.php', API);
  php4.mkdirTree('/crm-paraveda-data');
  php4.writeFile('/crm-paraveda-data/crm_data.json', JSON.stringify({
    afrizon_orders_v5: { t: 1000, d: [...demoOrders, { ...demoOrders[0], id: 999, nom: 'REAL CLIENT' }] },
  }));
  const r4 = await php4.run({ code: buildReq('GET', { token: TOKEN }) });
  const j4 = JSON.parse(Buffer.from(r4.bytes).toString());
  check('mixed demo+real data left untouched (169 orders kept)', j4.afrizon_orders_v5.d.length === 169, 'n=' + j4.afrizon_orders_v5.d.length);

  console.log(`\n===== RESULT: ${pass} passed, ${fail} failed =====`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('SUITE ERROR:', e); process.exit(1); });
