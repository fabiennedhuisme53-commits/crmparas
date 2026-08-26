#!/usr/bin/env python3
"""
Paraveda CRM v2.7 — PROFESSIONAL calculator (full redesign with dedicated CSS).

Root cause of the previous ugly look: the built Tailwind stylesheet is a fixed
compiled set — `grid-cols-4` was NOT in it, so keys stacked in one column.
Fix: append a dedicated `pv-*` stylesheet (full visual control, no dependency
on the compiled classes) and rewrite PVCalc to use it:

  - dark "real calculator" display with live thousand separators + expression line
  - keys with press animation, operator keys that LIGHT UP when selected
  - gradient = key, red C, functional ⌫/%/±
  - history tape with its own clear button
  - keyboard support (digits, ops, Enter, Backspace, Escape)
  - state survives header remounts (module mirror)
Also removes the previous v2.6 injection if present.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

CSS = """
/* ===== PV Calculator (custom, not part of compiled Tailwind) ===== */
.pv-modal{position:fixed;inset:0;z-index:80;display:grid;place-items:center;background:rgba(15,23,42,.62);-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px);padding:16px;animation:pvIn .16s ease-out}
@keyframes pvIn{from{opacity:0;transform:scale(.95)}to{opacity:1;transform:scale(1)}}
@keyframes pvPop{from{opacity:0;transform:scale(.9) translateY(10px)}to{opacity:1;transform:scale(1) translateY(0)}}
.pv-card{width:100%;max-width:380px;border-radius:20px;overflow:hidden;background:#fff;border:1px solid #e2e8f0;box-shadow:0 24px 80px rgba(15,23,42,.4);animation:pvPop .22s cubic-bezier(.34,1.4,.64,1)}
.pv-head{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:linear-gradient(270deg,#6366f1,#8b5cf6);color:#fff}
.pv-title{display:flex;align-items:center;gap:8px;font:800 14px/1 system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:.3px}
.pv-x{display:grid;place-items:center;height:28px;width:28px;border:0;border-radius:8px;background:rgba(255,255,255,.22);color:#fff;font-weight:700;cursor:pointer;transition:.15s}
.pv-x:hover{background:rgba(255,255,255,.4)}
.pv-disp{background:#0f172a;padding:14px 18px 12px}
.pv-expr{height:16px;text-align:right;font:600 11px/16px ui-monospace,SFMono-Regular,Menlo,monospace;color:#94a3b8;white-space:nowrap;overflow:hidden;direction:ltr}
.pv-num{margin-top:4px;text-align:right;font:800 34px/1.25 ui-monospace,SFMono-Regular,Menlo,monospace;color:#fff;white-space:nowrap;overflow-x:auto;overflow-y:hidden;direction:ltr;scrollbar-width:none}
.pv-num::-webkit-scrollbar{display:none}
.pv-body{padding:14px}
.pv-keys{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.pv-k{height:48px;border-radius:14px;border:1px solid #e2e8f0;background:#fff;font:700 18px system-ui,-apple-system,'Segoe UI',sans-serif;color:#1e293b;cursor:pointer;transition:transform .08s,background .15s,box-shadow .15s;user-select:none}
.pv-k:hover{background:#f8fafc;box-shadow:0 1px 5px rgba(15,23,42,.09)}
.pv-k:active{transform:scale(.93)}
.pv-k-op{background:#eef2ff;border-color:#c7d2fe;color:#4338ca}
.pv-k-op.pv-on{background:#6366f1;border-color:#6366f1;color:#fff;box-shadow:0 4px 14px rgba(99,102,241,.5)}
.pv-k-eq{background:linear-gradient(180deg,#6366f1,#4f46e5);border-color:#4f46e5;color:#fff;box-shadow:0 4px 14px rgba(79,70,229,.38)}
.pv-k-eq:hover{background:linear-gradient(180deg,#5457e5,#4338ca)}
.pv-k-cl{background:#fef2f2;border-color:#fecaca;color:#dc2626}
.pv-k-fn{background:#f1f5f9;border-color:#e2e8f0;color:#475569;font-size:16px}
.pv-hist{margin-top:12px;border-top:1px solid #f1f5f9;padding-top:8px}
.pv-hist-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:4px}
.pv-hist-label{font:800 10px system-ui,sans-serif;color:#94a3b8;letter-spacing:.8px;text-transform:uppercase}
.pv-hist-clear{border:0;background:#f1f5f9;color:#64748b;font:700 10px system-ui,sans-serif;border-radius:6px;padding:3px 8px;cursor:pointer;transition:.15s}
.pv-hist-clear:hover{background:#e2e8f0}
.pv-hist-list{max-height:96px;overflow:auto}
.pv-h{margin:2px 0;text-align:right;font:600 11px ui-monospace,monospace;color:#94a3b8;direction:ltr}
.pv-trig{display:grid;place-items:center;height:32px;width:32px;border-radius:10px;border:1px solid #e2e8f0;background:#fff;font-size:16px;cursor:pointer;transition:.15s;box-shadow:0 1px 3px rgba(15,23,42,.07)}
.pv-trig:hover{background:#f1f5f9;transform:translateY(-1px)}
.pv-trig:active{transform:scale(.93)}
"""

CALC = """var __pvC={open:!1,d:"0",v:null,b:null,h:!1,hist:[]};
function PVCalc(){
const[o,i]=ee.useState(__pvC.open),[d,m]=ee.useState(__pvC.d),[v,A]=ee.useState(__pvC.v),[b,y]=ee.useState(__pvC.b),[h,g]=ee.useState(__pvC.h),[N,w]=ee.useState(__pvC.hist.slice());
const k=(C,F,Be)=>Be==="+"?C+F:Be==="-"?C-F:Be==="×"?C*F:F===0?NaN:C/F;
const fm=F=>{if(F==="Error")return"Error";const Be=F.endsWith(".")?F.slice(0,-1):F,Pe=Be.split("."),xe=/^-?\\d+$/.test(Pe[0])?Number(Pe[0]).toLocaleString("fr-FR"):Pe[0];return F.endsWith(".")?xe+".":Pe.length>1?xe+"."+Pe[1]:xe};
const D=C=>{
if("C"===C){m("0"),A(null),y(null),g(!1);return}
if("⌫"===C){m(F=>F.length>1?F.slice(0,-1):"0");return}
if("±"===C){m(F=>F.startsWith("-")?F.slice(1):"0"===F?F:"-"+F);return}
if("%"===C){m(F=>{const Be=parseFloat(F);return isNaN(Be)?"0":String(Be/100)});return}
if("0123456789.".includes(C)){
if("."===C){if(h){m("0."),g(!1);return}m(F=>F.includes(".")?F:F+".");return}
if(h){m("0"===C?"0":C),g("0"===C);return}
m(F=>"0"===F?C:F+C);return}
if("+-×÷".includes(C)){
const F=parseFloat(d)||0;
if(v!==null&&!h){const Be=k(b,F,v);y(isNaN(Be)?null:Be),A(C),m(isNaN(Be)?"Error":String(Be)),g(!0)}
else{y(h&&v!==null?b:F),A(C),g(!0)}
return}
if("="===C){
if(v===null||b===null)return;
const F=parseFloat(d)||0,Be=k(b,F,v);
isNaN(Be)?m("Error"):(w(Pe=>[`${fm(String(b))} ${v} ${fm(String(F))} = ${fm(String(Be))}`,...Pe].slice(0,8)),m(String(Be)));
y(null),A(null),g(!0);return}};
ee.useEffect(()=>{if(!o)return;const C=F=>{const Be=F.key;
if(Be&&Be.length===1&&"0123456789.".includes(Be))D(Be);
else if("+"===Be)D("+");else if("-"===Be)D("-");else if("*"===Be)D("×");else if("/"===Be)D("÷");
else if("Enter"===Be||"="===Be)F.preventDefault(),D("=");
else if("Backspace"===Be)D("⌫");else if("Escape"===Be)F.preventDefault(),D("C"),i(!1);
else if("%"===Be)D("%");else if("c"===Be||"C"===Be)D("C")};
return window.addEventListener("keydown",C),()=>window.removeEventListener("keydown",C)},[o,d,b,v,h]);
ee.useEffect(()=>{__pvC.open=o,__pvC.d=d,__pvC.v=v,__pvC.b=b,__pvC.h=h,__pvC.hist=N},[o,d,v,b,h,N]);
const q=v!==null&&b!==null&&!isNaN(b)?`${fm(String(b))} ${v} ${h?"":d}`:"";
const Y=[["C","pv-k pv-k-cl"],["⌫","pv-k pv-k-fn"],["%","pv-k pv-k-fn"],["÷","pv-k pv-k-op"],["7","pv-k"],["8","pv-k"],["9","pv-k"],["×","pv-k pv-k-op"],["4","pv-k"],["5","pv-k"],["6","pv-k"],["-","pv-k pv-k-op"],["1","pv-k"],["2","pv-k"],["3","pv-k"],["+","pv-k pv-k-op"],["±","pv-k pv-k-fn"],["0","pv-k"],[".","pv-k"],["=","pv-k pv-k-eq"]];
return s.jsxs(s.Fragment,{children:[
s.jsx("button",{onClick:()=>i(!o),title:"آلة حاسبة (Calculator)",className:"pv-trig",children:"🧮"}),
o&&s.jsx("div",{className:"pv-modal",onClick:()=>i(!1),children:s.jsxs("div",{dir:"ltr",onClick:C=>C.stopPropagation(),className:"pv-card",children:[
s.jsxs("div",{className:"pv-head",children:[
s.jsxs("div",{className:"pv-title",children:[s.jsx("span",{children:"🧮"}),s.jsx("span",{children:"Calculator"})]}),
s.jsx("button",{onClick:()=>i(!1),title:"إغلاق (Esc)",className:"pv-x",children:"✕"})]}),
s.jsxs("div",{className:"pv-disp",children:[
s.jsx("div",{className:"pv-expr",children:q}),
s.jsx("div",{className:"pv-num",children:fm(d)})]}),
s.jsxs("div",{className:"pv-body",children:[
s.jsx("div",{className:"pv-keys",children:Y.map(([C,F])=>s.jsx("button",{onClick:()=>D(C),className:F+("+-×÷".includes(C)&&v===C?" pv-on":""),children:C},C))}),
N.length>0&&s.jsxs("div",{className:"pv-hist",children:[
s.jsxs("div",{className:"pv-hist-head",children:[
s.jsx("span",{className:"pv-hist-label",children:"Historique"}),
s.jsx("button",{onClick:()=>w([]),className:"pv-hist-clear",children:"مسح ✕"})]}),
s.jsx("div",{className:"pv-hist-list",children:N.map((C,F)=>s.jsx("div",{className:"pv-h",children:C},F))})]})]})]})})]})}
"""

TRIG_ANCHOR = 'shadow-sm",children:[s.jsx("span",{className:"grid h-6 w-6 place-items-center rounded-full bg-gradient-to-br from-indigo-500'
TRIG_NEW = 'shadow-sm",children:[s.jsx(PVCalc,{}),s.jsx("span",{className:"grid h-6 w-6 place-items-center rounded-full bg-gradient-to-br from-indigo-500'


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    # 1) remove previous v2.6 injection if present
    i = s.find('var __pvC=')
    j = s.find('function Vj(){', i) if i > -1 else -1
    if i > -1 and j > i:
        s = s[:i] + s[j:]
        print("removed old PVCalc injection")
    s = s.replace('s.jsx(PVCalc,{}),', '', 1)

    # 2) append CSS inside the style block
    k = s.find('</style>')
    if k < 0:
        print("ABORT: </style> not found"); sys.exit(1)
    s = s[:k] + CSS + s[k:]
    print("appended pv-* stylesheet")

    # 3) inject new PVCalc before Vj
    vj = 'function Vj(){'
    if s.count(vj) != 1:
        print(f"ABORT: Vj anchor = {s.count(vj)}"); sys.exit(1)
    s = s.replace(vj, CALC + "\n" + vj, 1)
    print("injected PVCalc v2.7")

    # 4) trigger in the pill
    if s.count(TRIG_ANCHOR) != 1:
        print(f"ABORT: pill anchor = {s.count(TRIG_ANCHOR)}"); sys.exit(1)
    s = s.replace(TRIG_ANCHOR, TRIG_NEW, 1)
    print("trigger injected in profile pill")

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — v2.7 professional calculator")


if __name__ == "__main__":
    main()
