// Unit test of the BULK-DELETE button code AS SHIPPED in app/index.html.
// Extracts the exact injected onClick from the bundle and executes it with
// mocked store functions — plus verifies the button sits inside the
// selection toolbar (the D.size>0 block, right after the bulk-copy buttons).
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '../app/index.html'), 'utf8');

let pass = 0, fail = 0;
const check = (n, c, x = '') => { c ? (pass++, console.log('  ✔ ' + n)) : (fail++, console.log('  ✘ FAIL: ' + n + (x ? ' — ' + x : ''))); };

// ---- 1) placement: inside the selection toolbar, after the copy buttons ----
const posToolbar = html.indexOf('D.size>0&&s.jsxs("div"');
const posCopyAll = html.indexOf('children:"نسخ الكل"})');
const posBulk = html.indexOf('حذف المحدد');
const posTable = html.indexOf('No,{children:[s.jsxs("table"');
check('bulk button found in bundle', posBulk > 0);
check('bulk button is INSIDE the selection toolbar (D.size>0 block)', posToolbar > 0 && posBulk > posToolbar && (posTable < 0 || posBulk < posTable));
check('bulk button sits right after the bulk-copy buttons', posCopyAll > 0 && posBulk > posCopyAll && posBulk - posCopyAll < 800, 'dist=' + (posBulk - posCopyAll));

// ---- 2) behaviour: run the REAL onClick with mocked store ----
const m = html.match(/onClick:\(\)=>\{const se=La;if\(!se\|\|!se\.length\)return;confirm[\s\S]*?تم مسح \$\{se\.length\} طلبية`\)\)\}/);
check('injected onClick source extracted from shipped file', !!m, m ? '' : 'not found');
if (m) {
  const src = m[0].replace(/^onClick:/, '');
  // factory closes over (La, c, T, Sa, confirm, Set) — the returned arrow reads them from scope
  const factory = new Function('La', 'c', 'T', 'Sa', 'confirm', 'Set', '"use strict";return (' + src + ')');
  const makeFn = (la, del, set, toast, conf) => factory(la, del, set, toast, conf, Set);

  // empty selection → nothing happens
  let confirmCalls = 0, delIds = [], setSel = null, toasts = [];
  makeFn([], id => delIds.push(id), v => (setSel = v), t => toasts.push(t), () => (confirmCalls++, true))();
  check('empty selection → no confirm, no deletes', confirmCalls === 0 && delIds.length === 0);

  // 5 selected + confirm YES → delete each, reset selection, toast with count
  confirmCalls = 0; delIds = []; setSel = null; toasts = [];
  const sel = [{ id: 3 }, { id: 7 }, { id: 9 }, { id: 21 }, { id: 44 }];
  makeFn(sel, id => delIds.push(id), v => (setSel = v), t => toasts.push(t), () => (confirmCalls++, true))();
  check('confirm asks with the real count', confirmCalls === 1);
  check('each selected order deleted via store del() (order preserved)', delIds.length === 5 && delIds.join() === '3,7,9,21,44', delIds.join());
  check('selection reset to empty Set', setSel instanceof Set && setSel.size === 0);
  check('toast reports the count', toasts.length === 1 && toasts[0].includes('5'), toasts[0]);

  // confirm NO → nothing deleted
  confirmCalls = 0; delIds = []; setSel = null; toasts = [];
  makeFn(sel, id => delIds.push(id), v => (setSel = v), t => toasts.push(t), () => (confirmCalls++, false))();
  check('confirm CANCEL → nothing deleted, selection kept', confirmCalls === 1 && delIds.length === 0 && setSel === null);
}

// ---- 3) v2.4: demo seed disabled at the source (dp() must return []) ----
function extractBalanced(str, startIdx, open, close) {
  let i = startIdx, depth = 0, inStr = null;
  for (; i < str.length; i++) {
    const c = str[i];
    if (inStr) { if (c === '\\') { i++; continue; } if (c === inStr) inStr = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
    if (c === open) depth++;
    else if (c === close) { depth--; if (depth === 0) return str.slice(startIdx, i + 1); }
  }
  throw new Error('unbalanced');
}
try {
  const a4Idx = html.search(/[,;]A4=/);
  const a4Src = 'var A4=' + extractBalanced(html, a4Idx + 1 + 'A4='.length, '[', ']') + ';';
  const dpIdx = html.indexOf('function dp(){');
  const dpSrc = extractBalanced(html, dpIdx + 'function dp()'.length, '{', '}');
  const result = new Function(a4Src + ' function dp()' + dpSrc + ' return dp();')();
  check('v2.4: factory seed dp() returns EMPTY list (demo dead at source)', Array.isArray(result) && result.length === 0, 'n=' + (result && result.length));
} catch (e) {
  check('v2.4: factory seed dp() returns EMPTY list (demo dead at source)', false, e.message);
}
check('v2.4: reset() neutered in the store', html.includes('reset:()=>{}'));
check('v2.4: no Save/Reset buttons left', !html.includes('children:"Save CMD"') && !html.includes('children:"Reset"') && !html.includes('children:"Save"})') && !html.includes('children:"↺ Reset"'));
check('v2.4: auto-checkpoint effect present', html.includes('clearTimeout(__t)},[a,c])'));

console.log(`\n===== BULK-DELETE UNIT RESULT: ${pass} passed, ${fail} failed =====`);
process.exit(fail ? 1 : 0);
