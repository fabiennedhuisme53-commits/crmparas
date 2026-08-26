#!/usr/bin/env python3
"""
Paraveda CRM v2.6 — professional Calculator (🧮) in the top-right header pill.

Adds a self-contained PVCalc component (trigger button + modal calculator):
  - Immediate-execution calculator: digits, + - × ÷, %, ±, ⌫, C, =
  - Big monospace display + expression line
  - Calculation history tape (last 8)
  - Full keyboard support (digits, ops, Enter, Backspace, Escape)
  - Professional styling using ONLY existing Tailwind classes
The trigger is injected into the profile pill (E) which renders in BOTH the
admin and girl layouts — one patch covers everyone.
Anchors must match exactly once or the script aborts.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

CALC = r'''var __pvC={open:!1,d:"0",v:null,b:null,h:!1,hist:[]};
function PVCalc(){
const[o,i]=ee.useState(__pvC.open),[d,m]=ee.useState(__pvC.d),[v,A]=ee.useState(__pvC.v),[b,y]=ee.useState(__pvC.b),[h,g]=ee.useState(__pvC.h),[N,w]=ee.useState(__pvC.hist.slice());
const k=(C,F,Be)=>Be==="+"?C+F:Be==="-"?C-F:Be==="×"?C*F:F===0?NaN:C/F;
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
isNaN(Be)?m("Error"):(w(Pe=>[`${b} ${v} ${F} = ${Be}`,...Pe].slice(0,8)),m(String(Be)));
y(null),A(null),g(!0);return}};
ee.useEffect(()=>{if(!o)return;const C=F=>{const Be=F.key;
if(Be&&Be.length===1&&"0123456789.".includes(Be))D(Be);
else if("+"===Be)D("+");else if("-"===Be)D("-");else if("*"===Be)D("×");else if("/"===Be)D("÷");
else if("Enter"===Be||"="===Be)F.preventDefault(),D("=");
else if("Backspace"===Be)D("⌫");else if("Escape"===Be)F.preventDefault(),D("C"),i(!1);
else if("%"===Be)D("%");else if("c"===Be||"C"===Be)D("C")};
return window.addEventListener("keydown",C),()=>window.removeEventListener("keydown",C)},[o,d,b,v,h]);
ee.useEffect(()=>{__pvC.open=o,__pvC.d=d,__pvC.v=v,__pvC.b=b,__pvC.h=h,__pvC.hist=N},[o,d,v,b,h,N]);
const U=C=>{try{const F=Number(C);return isNaN(F)?"Error":F.toLocaleString("fr-FR",{maximumFractionDigits:10})}catch{return C}};
const q=v!==null&&b!==null&&!isNaN(b)?`${U(b)} ${v} ${h?"":d}`:"";
const Y=[["C","bg-red-50 text-red-600"],["⌫","bg-slate-100 text-slate-600"],["%","bg-slate-100 text-slate-600"],["÷","bg-indigo-50 font-extrabold text-indigo-700"],["7",""],["8",""],["9",""],["×","bg-indigo-50 font-extrabold text-indigo-700"],["4",""],["5",""],["6",""],["-","bg-indigo-50 font-extrabold text-indigo-700"],["1",""],["2",""],["3",""],["+","bg-indigo-50 font-extrabold text-indigo-700"],["±","bg-slate-100 text-slate-600"],["0",""],[".",""],["=","bg-indigo-600 text-white shadow-md font-extrabold"]];
return s.jsxs(s.Fragment,{children:[
s.jsx("button",{onClick:()=>i(!o),title:"آلة حاسبة (Calculator)",className:"grid h-8 w-8 place-items-center rounded-xl border border-slate-200 bg-white text-base shadow-sm transition hover:bg-slate-100 active:scale-[0.97]",children:"🧮"}),
o&&s.jsx("div",{className:"fixed inset-0 z-[80] grid place-items-center bg-slate-900/60 p-4 backdrop-blur-sm",onClick:()=>i(!1),children:s.jsxs("div",{dir:"ltr",onClick:C=>C.stopPropagation(),className:"w-full max-w-sm overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl",children:[
s.jsxs("div",{className:"flex items-center justify-between bg-gradient-to-l from-indigo-500 to-violet-600 px-4 py-3 text-white",children:[
s.jsxs("div",{className:"flex items-center gap-2",children:[s.jsx("span",{className:"text-base",children:"🧮"}),s.jsx("b",{className:"text-sm tracking-tight",children:"Calculator"})]}),
s.jsx("button",{onClick:()=>i(!1),title:"إغلاق",className:"grid h-7 w-7 place-items-center rounded-lg bg-white/20 transition hover:bg-white/30",children:"✕"})]}),
s.jsxs("div",{className:"px-4 pt-4",children:[
s.jsx("p",{className:"h-4 text-right font-mono text-[11px] text-slate-400",children:q}),
s.jsx("p",{className:"mt-1 truncate text-right font-mono text-3xl font-extrabold text-slate-900",children:U(d)})]}),
s.jsxs("div",{className:"p-4",children:[
s.jsx("div",{className:"grid grid-cols-4 gap-2",children:Y.map(([C,F])=>s.jsx("button",{onClick:()=>D(C),className:`h-12 rounded-xl border text-lg font-bold text-slate-800 transition hover:bg-slate-50 active:scale-[0.96] ${"="===C?"border-indigo-600":"border-slate-200"} ${F||"bg-white"}`,children:C},C))}),
N.length>0&&s.jsx("div",{className:"mt-3 max-h-32 overflow-auto border-t border-slate-100 pt-2",children:N.map((C,F)=>s.jsx("p",{className:"text-right font-mono text-[11px] text-slate-400",children:C},F))})]})]})})]})}


'''

def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    inj_at = 'function Vj(){'
    pill_anchor = 'shadow-sm",children:[s.jsx("span",{className:"grid h-6 w-6 place-items-center rounded-full bg-gradient-to-br from-indigo-500'
    pill_inject = 'shadow-sm",children:[s.jsx(PVCalc,{}),s.jsx("span",{className:"grid h-6 w-6 place-items-center rounded-full bg-gradient-to-br from-indigo-500'

    if s.count(inj_at) != 1:
        print(f"ABORT: Vj anchor matched {s.count(inj_at)}"); sys.exit(1)
    if s.count(pill_anchor) != 1:
        print(f"ABORT: pill anchor matched {s.count(pill_anchor)}"); sys.exit(1)

    s = s.replace(inj_at, CALC + "\n" + inj_at, 1)
    s = s.replace(pill_anchor, pill_inject, 1)

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — Calculator injected (component + header button in profile pill)")


if __name__ == "__main__":
    main()
