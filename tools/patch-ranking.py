#!/usr/bin/env python3
"""
Paraveda CRM — Ranking page professional redesign (v2.5).

Replaces ONLY the JSX return of component M_ ("Classement des Filles").
All the existing computed data (R = ranked list w/ conf, liv, ret, ca, taux,
delta, progress, photo — _ = aggregate stats — S/E/C podium — L top progress —
F delta chip — controls state) stays 100% untouched; only the layout changes.

New layout:
  1. Hero header (title + period + sort/month/all controls) — unchanged logic,
     cleaner grouping
  2. KPI strip — 4 big visible cards: Total Confirmés (+Δ), CA Total (+Δ),
     Taux moyen (+Δ), Objectif mensuel (progress vs editable target)
  3. Podium top-3 — medals/crown/photos + confirmés + taux + CA + NEW:
     livraisons/retours line + evolution chip vs last month
  4. "Classement Complet" table — now ALL agents (not just 4+), with rank
     medals, avatar, Confirmés + Δ, Livrées, Retours, Taux pill, CA MAD,
     progression bar, and a bold TOTAL footer row
  5. Sidebar — Statistiques (with editable objective), Top Progression,
     motivational card

Only Tailwind classes that already exist in the built stylesheet are used.
Anchors must match exactly once or the script aborts.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

START = 'return s.jsxs("div",{dir:"ltr",className:"h-full overflow-auto bg-slate-50"'
END = 'const L_='

NEW_JSX = r'''return s.jsxs("div",{dir:"ltr",className:"h-full overflow-auto bg-slate-50",children:[
s.jsx("div",{className:"sticky top-0 z-10 border-b border-slate-200 bg-white px-6 py-4",children:s.jsxs("div",{className:"flex flex-wrap items-center gap-4",children:[
s.jsx("div",{className:"grid h-12 w-12 place-items-center rounded-2xl bg-violet-50 text-2xl",children:"🏆"}),
s.jsxs("div",{children:[
s.jsx("h1",{className:"text-2xl font-extrabold tracking-tight text-slate-900",children:"Classement des Filles"}),
s.jsxs("p",{className:"text-sm text-slate-500",children:["Performance des confirmatrices · ",s.jsx("span",{className:"font-bold text-orange-600",children:["⏱ ",i]})]})]}),
s.jsxs("div",{className:"ml-auto flex flex-wrap items-center gap-2",children:[
s.jsxs("select",{value:w,onChange:Y=>N(Y.target.value),className:"rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-medium outline-none",children:[
s.jsx("option",{value:"conf",children:"Trier: Confirmés"}),
s.jsx("option",{value:"ca",children:"Trier: Montant"}),
s.jsx("option",{value:"taux",children:"Trier: Réussite"})]}),
s.jsxs("div",{className:`flex items-center gap-2 rounded-xl border px-3 py-2 ${b?"border-slate-200 bg-slate-100 opacity-60":"border-slate-200 bg-white"}`,children:[
s.jsx("select",{disabled:b,value:d,onChange:Y=>m(Number(Y.target.value)),className:"bg-transparent text-sm font-semibold outline-none",children:D_.map((Y,oe)=>s.jsx("option",{value:oe,children:Y},Y))}),
s.jsx("select",{disabled:b,value:h,onChange:Y=>g(Number(Y.target.value)),className:"bg-transparent text-sm font-semibold outline-none",children:[h-1,h,h+1].map(Y=>s.jsx("option",{value:Y,children:Y},Y))}),
s.jsx("span",{className:"text-slate-400",children:"📅"})]}),
s.jsx("button",{onClick:()=>y(!b),className:`rounded-xl px-4 py-2 text-sm font-bold transition ${b?"bg-violet-600 text-white":"border border-slate-200 bg-white text-slate-600 hover:bg-slate-50"}`,children:b?"✓ Tout":"Tout"})]})]})}),
s.jsxs("div",{className:"grid gap-4 p-6 pb-0 sm:grid-cols-2 lg:grid-cols-4",children:[
s.jsxs("div",{className:"rounded-2xl border border-slate-200 bg-white p-5",children:[
s.jsxs("div",{className:"flex items-center gap-2",children:[s.jsx("span",{className:"grid h-8 w-8 place-items-center rounded-lg bg-emerald-50 text-base",children:"✅"}),s.jsx("p",{className:"text-xs font-bold uppercase tracking-wide text-slate-500",children:"Total Confirmés"})]}),
s.jsxs("div",{className:"mt-3 flex items-end gap-3",children:[
s.jsx("b",{className:"text-3xl font-extrabold text-slate-900",children:Ts(_.conf)}),
s.jsxs("div",{children:[s.jsx(F,{v:_.dConf}),s.jsx("p",{className:"text-[10px] text-slate-400",children:"vs mois dernier"})]})]})]}),
s.jsxs("div",{className:"rounded-2xl border border-slate-200 bg-white p-5",children:[
s.jsxs("div",{className:"flex items-center gap-2",children:[s.jsx("span",{className:"grid h-8 w-8 place-items-center rounded-lg bg-amber-50 text-base",children:"💰"}),s.jsx("p",{className:"text-xs font-bold uppercase tracking-wide text-slate-500",children:"CA Total"})]}),
s.jsxs("div",{className:"mt-3 flex items-end gap-3",children:[
s.jsxs("b",{className:"text-3xl font-extrabold text-slate-900",children:[Ts(_.ca)," MAD"]),
s.jsxs("div",{children:[s.jsx(F,{v:_.dCa}),s.jsx("p",{className:"text-[10px] text-slate-400",children:"vs mois dernier"})]})]})]}),
s.jsxs("div",{className:"rounded-2xl border border-slate-200 bg-white p-5",children:[
s.jsxs("div",{className:"flex items-center gap-2",children:[s.jsx("span",{className:"grid h-8 w-8 place-items-center rounded-lg bg-violet-50 text-base",children:"⭐"}),s.jsx("p",{className:"text-xs font-bold uppercase tracking-wide text-slate-500",children:"Taux Réussite"})]}),
s.jsxs("div",{className:"mt-3 flex items-end gap-3",children:[
s.jsxs("b",{className:"text-3xl font-extrabold text-slate-900",children:[_.taux,"%"]),
s.jsxs("div",{children:[s.jsx(F,{v:_.dTaux,suffix:"pt"}),s.jsx("p",{className:"text-[10px] text-slate-400",children:"vs mois dernier"})]})]})]}),
s.jsxs("div",{className:"rounded-2xl border border-slate-200 bg-white p-5",children:[
s.jsxs("div",{className:"flex items-center gap-2",children:[s.jsx("span",{className:"grid h-8 w-8 place-items-center rounded-lg bg-indigo-50 text-base",children:"🎯"}),s.jsx("p",{className:"text-xs font-bold uppercase tracking-wide text-slate-500",children:"Objectif Mensuel"})]}),
s.jsxs("div",{className:"mt-3 flex items-center gap-2",children:[
s.jsx("b",{className:"text-2xl font-extrabold text-violet-600",children:Ts(_.conf)}),s.jsx("span",{className:"text-slate-400",children:"/"}),
s.jsx("input",{type:"number",value:v,onChange:Y=>{const oe=Number(Y.target.value)||0;A(oe),localStorage.setItem(z2,String(oe))},className:"w-20 rounded border border-slate-200 px-2 py-0.5 text-lg font-extrabold text-slate-900 outline-none focus:border-violet-400"})]}),
s.jsxs("div",{className:"mt-2 flex items-center gap-2",children:[
s.jsx("div",{className:"h-2 flex-1 rounded-full bg-slate-100",children:s.jsx("div",{className:"h-2 rounded-full bg-violet-600",style:{width:`${Math.min(100,v?_.conf/v*100:0)}%`}})}),
s.jsxs("span",{className:"text-xs font-bold text-slate-500",children:[v?Math.round(_.conf/v*100):0,"%"]})]})]})]}),
s.jsxs("div",{className:"grid gap-5 p-6 lg:grid-cols-[1fr_320px]",children:[
s.jsxs("div",{className:"space-y-5",children:[
s.jsxs("div",{className:"grid gap-4 sm:grid-cols-3",children:C.map(Y=>{const oe=S[Y],K=O_[Y];return oe?s.jsxs("div",{className:`relative rounded-2xl border-2 bg-white p-5 text-center shadow-sm transition hover:-translate-y-1 hover:shadow-lg ${Y===0?"sm:-mt-4 sm:pb-7":""}`,style:{borderColor:Y===0?K.ring:"#e2e8f0",background:`linear-gradient(180deg, ${K.soft}, #fff)`},children:[
K.crown&&s.jsx("div",{className:"absolute -top-6 left-1/2 -translate-x-1/2 text-3xl",children:"👑"}),
s.jsx("div",{className:"absolute left-4 top-4 grid h-9 w-9 place-items-center rounded-full text-lg shadow-sm",style:{background:K.chip},children:K.medal}),
s.jsx("div",{className:"mx-auto w-fit",children:s.jsx(od,{name:oe.name,photo:oe.photo,size:Y===0?96:80,ring:K.chip})}),
s.jsx("h3",{className:"mt-3 text-lg font-extrabold",style:{color:K.text},children:oe.name}),
s.jsxs("p",{className:"mt-1 text-sm text-slate-600",children:[s.jsx("b",{className:"text-base",children:Ts(oe.conf)})," confirmés"]}),
s.jsxs("p",{className:"mt-1 text-xs font-semibold text-slate-500",children:["🚚 ",oe.liv," · ↩️ ",oe.ret]}),
s.jsxs("p",{className:"mt-1 text-sm font-semibold",style:{color:K.text},children:["⭐ ",oe.taux,"%"]}),
s.jsxs("div",{className:"mt-2 flex items-center justify-center gap-2",children:[s.jsx(F,{v:oe.delta}),s.jsx("span",{className:"text-[10px] text-slate-400",children:"vs mois dernier"})]}),
s.jsxs("div",{className:"mt-3 rounded-xl py-2.5 text-sm font-extrabold",style:{background:K.chip,color:K.text},children:[Ts(oe.ca)," MAD"]})]},oe.name):s.jsx("div",{className:"hidden sm:block"},Y)})}),
s.jsxs("div",{className:"overflow-hidden rounded-2xl border border-slate-200 bg-white",children:[
s.jsxs("div",{className:"flex items-center gap-3 border-b border-slate-100 px-5 py-4",children:[
s.jsx("span",{className:"grid h-9 w-9 place-items-center rounded-xl bg-violet-50 text-lg",children:"📊"}),
s.jsx("h3",{className:"text-base font-bold text-slate-800",children:"Classement Complet"}),
s.jsxs("span",{className:"ml-auto rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600",children:[R.length," filles"]})]}),
s.jsxs("div",{className:"overflow-x-auto",children:s.jsxs("table",{className:"w-full",children:[
s.jsx("thead",{children:s.jsxs("tr",{className:"border-b border-slate-100 text-left text-xs font-semibold text-slate-500",children:[
s.jsx("th",{className:"px-5 py-3 text-center",children:"#"}),
s.jsx("th",{className:"px-3 py-3",children:"Fille"}),
s.jsx("th",{className:"px-3 py-3 text-center",children:"Confirmés"}),
s.jsx("th",{className:"px-3 py-3 text-center",children:"Livrées"}),
s.jsx("th",{className:"px-3 py-3 text-center",children:"Retours"}),
s.jsx("th",{className:"px-3 py-3 text-center",children:"Taux"}),
s.jsx("th",{className:"px-3 py-3 text-right",children:"Montant"}),
s.jsx("th",{className:"px-3 py-3 w-56",children:"Progression"})]})}),
s.jsxs("tbody",{children:[
R.map((Y,oe)=>{const K=oe===0?"🥇":oe===1?"🥈":oe===2?"🥉":String(oe+1);return s.jsxs("tr",{className:"border-b border-slate-50 transition hover:bg-slate-50",children:[
s.jsx("td",{className:"px-5 py-3 text-center",children:s.jsx("span",{className:oe<3?"text-xl":"text-sm font-semibold text-slate-400",children:K})}),
s.jsxs("td",{className:"px-3 py-3",children:s.jsxs("div",{className:"flex items-center gap-3",children:[
s.jsx(od,{name:Y.name,photo:Y.photo,size:36,ring:oe<3?"#ddd6fe":"#f1f5f9"}),
s.jsxs("div",{children:[
s.jsx("p",{className:"text-sm font-bold text-slate-800",children:Y.name}),
s.jsx(F,{v:Y.delta})]})]})}),
s.jsx("td",{className:"px-3 py-3 text-center text-base font-extrabold text-slate-900",children:Ts(Y.conf)}),
s.jsx("td",{className:"px-3 py-3 text-center text-sm font-bold text-emerald-600",children:Ts(Y.liv)}),
s.jsx("td",{className:"px-3 py-3 text-center text-sm font-bold text-red-500",children:Ts(Y.ret)}),
s.jsx("td",{className:"px-3 py-3 text-center",children:s.jsx("span",{className:"inline-block rounded-full px-2.5 py-1 text-xs font-bold",style:{background:Y.taux>=80?"#d1fae5":Y.taux>=70?"#fef3c7":"#fee2e2",color:Y.taux>=80?"#047857":Y.taux>=70?"#b45309":"#b91c1c"},children:[Y.taux,"%"]})}),
s.jsxs("td",{className:"px-3 py-3 text-right text-sm font-extrabold text-slate-900",children:[Ts(Y.ca)," ",s.jsx("span",{className:"text-[10px] font-bold text-slate-400",children:"MAD"})]}),
s.jsx("td",{className:"px-3 py-3",children:s.jsxs("div",{className:"flex items-center gap-3",children:[
s.jsx("div",{className:"h-2 flex-1 rounded-full bg-slate-100",children:s.jsx("div",{className:"h-2 rounded-full bg-violet-500 transition-all",style:{width:`${Y.progress}%`}})}),
s.jsxs("span",{className:"w-9 text-right text-xs font-bold text-slate-500",children:[Y.progress,"%"]})]})})]},Y.name)}),
s.jsxs("tr",{className:"border-t-2 border-slate-200 bg-slate-50",children:[
s.jsx("td",{className:"px-5 py-3"}),
s.jsx("td",{className:"px-3 py-3 text-xs font-bold uppercase tracking-wide text-slate-500",children:"TOTAL ÉQUIPE"}),
s.jsx("td",{className:"px-3 py-3 text-center text-base font-extrabold text-slate-900",children:Ts(_.conf)}),
s.jsx("td",{className:"px-3 py-3 text-center text-sm font-bold text-emerald-600",children:"—"}),
s.jsx("td",{className:"px-3 py-3 text-center text-sm font-bold text-red-500",children:"—"}),
s.jsx("td",{className:"px-3 py-3 text-center",children:s.jsx("span",{className:"inline-block rounded-full bg-violet-100 px-2.5 py-1 text-xs font-bold text-violet-700",children:[_.taux,"%"]})}),
s.jsxs("td",{className:"px-3 py-3 text-right text-sm font-extrabold text-slate-900",children:[Ts(_.ca)," MAD"]}),
s.jsx("td",{className:"px-3 py-3"})]}),
!R.length&&s.jsx("tr",{children:s.jsx("td",{colSpan:8,className:"py-10 text-center text-sm text-slate-400",children:"Aucune fille dans le classement — zid agentات من Work Team"})]})]})]}))]}),
s.jsxs("div",{className:"space-y-4",children:[
s.jsxs("div",{className:"rounded-2xl border border-slate-200 bg-white p-5",children:[
s.jsxs("div",{className:"mb-4 flex items-center gap-2",children:[s.jsx("span",{className:"grid h-8 w-8 place-items-center rounded-lg bg-violet-50",children:"📈"}),s.jsx("h3",{className:"font-bold text-slate-800",children:"Statistiques"})]}),
s.jsxs("div",{className:"space-y-4",children:[
s.jsxs("div",{children:[s.jsx("p",{className:"text-xs text-slate-500",children:"Total confirmés"}),s.jsxs("div",{className:"flex items-end gap-3",children:[s.jsx("b",{className:"text-2xl font-extrabold text-slate-900",children:Ts(_.conf)}),s.jsxs("div",{children:[s.jsx(F,{v:_.dConf}),s.jsx("p",{className:"text-[10px] text-slate-400",children:"vs mois dernier"})]})]})]}),
s.jsxs("div",{children:[s.jsx("p",{className:"text-xs text-slate-500",children:"Taux de réussite moyen"}),s.jsxs("div",{className:"flex items-end gap-3",children:[s.jsxs("b",{className:"text-2xl font-extrabold text-slate-900",children:[_.taux,"%"]}),s.jsxs("div",{children:[s.jsx(F,{v:_.dTaux,suffix:"pt"}),s.jsx("p",{className:"text-[10px] text-slate-400",children:"vs mois dernier"})]})]})]}),
s.jsxs("div",{children:[s.jsx("p",{className:"text-xs text-slate-500",children:"Montant total généré"}),s.jsxs("div",{className:"flex items-end gap-3",children:[s.jsxs("b",{className:"text-2xl font-extrabold text-slate-900",children:[Ts(_.ca)," MAD"]}),s.jsxs("div",{children:[s.jsx(F,{v:_.dCa}),s.jsx("p",{className:"text-[10px] text-slate-400",children:"vs mois dernier"})]})]})]})]})]}),
L&&s.jsxs("div",{className:"rounded-2xl border border-slate-200 bg-white p-5",children:[
s.jsxs("div",{className:"mb-3 flex items-center gap-2",children:[s.jsx("span",{className:"grid h-8 w-8 place-items-center rounded-lg bg-emerald-50",children:"🚀"}),s.jsx("h3",{className:"font-bold text-slate-800",children:"Top Progression"})]}),
s.jsxs("div",{className:"flex items-center gap-3",children:[
s.jsx(od,{name:L.name,photo:L.photo,size:44,ring:"#f1f5f9"}),
s.jsxs("div",{children:[s.jsx("p",{className:"font-bold text-slate-800",children:L.name}),s.jsxs("p",{className:"text-lg font-extrabold text-emerald-600",children:[L.delta>=0?"+":"",L.delta,"%"]}),s.jsx("p",{className:"text-[10px] text-slate-400",children:"vs mois dernier"})]}),
s.jsx("span",{className:"ml-auto text-3xl",children:"📈"})]})]}),
s.jsxs("div",{className:"rounded-2xl bg-gradient-to-br from-violet-100 to-indigo-100 p-5 text-center",children:[
s.jsx("div",{className:"text-3xl",children:"👑"}),
s.jsx("p",{className:"mt-2 font-bold text-violet-800",children:"Continuez votre excellent travail !"}),
s.jsx("p",{className:"mt-1 text-sm text-violet-600",children:"Chaque confirmation compte ✨"})]})]})]})]}'''


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    if s.count(START) != 1:
        print(f"ABORT: START matched {s.count(START)} times"); sys.exit(1)
    i = s.find(START)
    j = s.find(END, i)
    if j < 0:
        print("ABORT: END not found after START"); sys.exit(1)

    old = s[i:j]
    if len(old) > 13000 or 'Classement des Filles' not in old:
        print(f"ABORT: suspicious span (len={len(old)})"); sys.exit(1)

    s = s[:i] + NEW_JSX + "}\n" + s[j:]
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"OK — Ranking redesigned (replaced {len(old)} chars with {len(NEW_JSX)})")


if __name__ == "__main__":
    main()
