#!/usr/bin/env python3
"""
Paraveda CRM v4.0 — SAPPHIRE LUXE: sidebar navigation + light executive content.
A completely different design chosen by the engineer: a deep sapphire vertical
sidebar (the classic professional-dashboard look) + a bright ivory content area
with gold accents.

Structural CSS only (zero JS changes), desktop ≥1024px:
  - admin shell flex-col → flex-row; header becomes a 272px vertical sidebar
  - the horizontal tabs row becomes a vertical nav (icon + label items,
    active = white pill with gold notch)
  - footer shortcut bar becomes a floating glass bar over the content
Visual language:
  - sidebar: midnight sapphire gradient, glowing active pill
  - content: light #eef1f7 with soft aurora hints, white cards, layered shadows
  - accents: sapphire #2b3f9e + gold #d9a83a
  - typography: Cairo (Arabic) + Inter (latin/numbers)
Mobile keeps the previous horizontal layout. Idempotent.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

OLD_START = "/* ═══════════ PARAVEDA DARK PRO v3.1"
OLD_END = "END PARAVEDA DARK PRO ═══════════ */"

LUXE = r"""
/* ═══════════ PARAVEDA SAPPHIRE LUXE v4.0 — sidebar + executive light ═══════════ */
:root{color-scheme:light}
*{-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
html,body{font-family:'Cairo','Inter',system-ui,-apple-system,'Segoe UI',Tahoma,sans-serif}
[dir="ltr"]{font-family:'Inter','Cairo',system-ui,sans-serif}
body{font-variant-numeric:tabular-nums;letter-spacing:.1px;background:#eef1f7;color:#1e293b}
b,strong{font-weight:800}.font-extrabold,.font-black{letter-spacing:-.2px}
::selection{background:#c7d2fe;color:#1e1b4b}

/* ── content backdrop: soft aurora ivory ── */
.h-dvh.bg-slate-100,.min-h-screen{background:
  radial-gradient(900px 420px at 92% -10%,rgba(59,76,178,.10),transparent 60%),
  radial-gradient(760px 380px at -8% 108%,rgba(217,168,58,.07),transparent 55%),
  linear-gradient(178deg,#f2f4fa 0%,#edf0f8 55%,#eef1f7 100%)}

/* ═══════ THE SIDEBAR (desktop) ═════════ */
@media (min-width:1024px){
  .flex.h-dvh.flex-col.bg-slate-100{flex-direction:row}
  .flex.h-dvh.flex-col.bg-slate-100>header{
    display:flex;flex-direction:column;width:274px;min-width:274px;height:100dvh;
    background:linear-gradient(197deg,#111e44 0%,#0b1230 52%,#0e1738 100%)!important;
    border-bottom:0!important;border-inline-end:1px solid rgba(148,163,184,.16);
    box-shadow:10px 0 44px -22px rgba(10,16,44,.55);padding-bottom:10px;
  }
  /* sidebar top: logo + controls (allow wrap, hide breadcrumb) */
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child{flex-wrap:wrap;gap:10px;padding:14px 14px 10px;border-bottom:1px solid rgba(148,163,184,.12)}
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child>div[class*="md:flex"]{display:none!important}
  /* nav column */
  .flex.h-dvh.flex-col.bg-slate-100>header>nav{flex:1;min-height:0;margin-top:6px;display:flex;flex-direction:column;overflow:hidden}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div{
    flex-direction:column!important;align-items:stretch!important;gap:3px!important;
    overflow-y:auto!important;overflow-x:hidden!important;padding:8px 12px!important;
    scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.18) transparent;
  }
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div::-webkit-scrollbar{width:6px}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div::-webkit-scrollbar-thumb{background:rgba(255,255,255,.16);border-radius:99px}
  /* hide horizontal separators */
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>div[class*="w-px"]{display:none!important}
  /* nav items: uniform luxe pills */
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button{
    width:100%;justify-content:flex-start!important;gap:10px!important;
    padding:9px 13px!important;border-radius:12px;font-size:12.5px;
    background:transparent!important;border-color:transparent!important;
    box-shadow:none!important;color:#c3cde8!important;letter-spacing:.1px;
  }
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button:hover{
    background:rgba(255,255,255,.07)!important;color:#fff!important;transform:none!important;
  }
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button[class*="ring-2"]{
    background:#fff!important;color:#172554!important;font-weight:800;
    box-shadow:0 8px 22px -8px rgba(255,255,255,.28),0 0 0 1px rgba(217,168,58,.35)!important;
    position:relative;
  }
  /* gold notch on the active item */
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button[class*="ring-2"]::before{
    content:"";position:absolute;inset-inline-start:4px;top:22%;bottom:22%;width:3px;
    border-radius:99px;background:linear-gradient(180deg,#f2c14e,#d9a83a);
  }
  /* footer shortcuts → floating glass bar over the content */
  .flex.h-dvh.flex-col.bg-slate-100>footer{
    position:fixed;bottom:10px;inset-inline-start:286px;inset-inline-end:12px;z-index:40;
    border-radius:16px;border:1px solid rgba(148,163,184,.22);
    background:rgba(255,255,255,.86);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);
    box-shadow:0 14px 34px -18px rgba(15,23,42,.35);padding:6px 10px;
  }
  .flex.h-dvh.flex-col.bg-slate-100>.flex-1.overflow-hidden{padding-bottom:52px}
}

/* ═══════ CONTENT (all sizes) ═════════ */
/* cards */
.rounded-2xl.border,.rounded-xl.border{border-color:#e4e8f2!important;box-shadow:0 1px 2px rgba(15,23,42,.04),0 12px 32px -16px rgba(30,41,110,.14)}
.rounded-2xl.border:hover{box-shadow:0 2px 6px rgba(15,23,42,.05),0 18px 42px -16px rgba(30,41,110,.2)}
[class*="shadow-2xl"]{box-shadow:0 30px 80px -20px rgba(15,23,42,.3)!important}
/* header (girls layout + inner sticky bars) */
header.bg-white,.shrink-0.border-b.bg-white{background:rgba(255,255,255,.85)!important;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
div.sticky.top-0{background:rgba(255,255,255,.92);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
/* tables */
table{font-variant-numeric:tabular-nums}
table td,table th{border-color:#e6eaf2}
thead th{font-weight:800;letter-spacing:.35px}
tbody tr{transition:background-color .13s}
tbody tr:hover{background-color:rgba(59,76,178,.055)}
/* buttons & focus */
button{cursor:pointer;transition:transform .09s ease,box-shadow .2s ease,background-color .18s ease}
button:not(.pv-k):not(.pv-trig):not(.pv-x):active{transform:scale(.965)}
button:focus-visible,a:focus-visible{outline:2px solid #2b3f9e;outline-offset:2px;border-radius:8px}
input,select,textarea{font-family:inherit}
input:focus,select:focus,textarea:focus{outline:none;border-color:#a5b4fc;box-shadow:0 0 0 3px rgba(59,76,178,.13)}
input[type="checkbox"],input[type="radio"]{accent-color:#2b3f9e}
/* KPI numbers get a sapphire tint */
.text-3xl.font-extrabold,.text-2xl.font-extrabold{color:#172554}
/* scrollbars */
::-webkit-scrollbar{width:9px;height:9px}
::-webkit-scrollbar-track{background:rgba(148,163,184,.1)}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#8ea0d8,#5f6fb8);border-radius:99px;border:2px solid rgba(238,241,247,.8);background-clip:padding-box}
::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#5f6fb8,#2b3f9e);background-clip:padding-box}
*{scrollbar-width:thin;scrollbar-color:#8ea0d8 rgba(148,163,184,.1)}
/* overlays & motion */
[class*="bg-slate-900/60"],[class*="bg-black/45"],[class*="bg-black/20"]{-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
[class*="fixed inset-0"]>*{animation:pvLIn .2s cubic-bezier(.34,1.3,.64,1)}
@keyframes pvLIn{from{opacity:0;transform:scale(.96) translateY(8px)}to{opacity:1;transform:scale(1) translateY(0)}}
/* calculator: ivory luxe */
.pv-card{border-color:#e4e8f2}
.pv-disp{background:#101c3f;border-top:1px solid rgba(148,163,184,.2)}
.pv-k{background:#fff;border-color:#e4e8f2}
.pv-k:hover{background:#f4f6fc}
.pv-k-op{background:rgba(59,76,178,.09);border-color:rgba(59,76,178,.3);color:#2b3f9e}
.pv-k-op.pv-on{background:#2b3f9e;border-color:#2b3f9e;color:#fff;box-shadow:0 4px 16px rgba(43,63,158,.4)}
.pv-k-fn{background:#f1f3f9;border-color:#e4e8f2;color:#475569}
.pv-k-cl{background:rgba(220,38,38,.08);border-color:rgba(220,38,38,.3);color:#dc2626}
.pv-k-eq{background:linear-gradient(180deg,#2b3f9e,#1e2a72);border-color:#1e2a72}
.pv-trig{background:#fff;border-color:#e4e8f2}
.pv-trig:hover{background:#f4f6fc}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
/* ═══════════ END SAPPHIRE LUXE ═══════════ */
"""


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    if "PARAVEDA SAPPHIRE LUXE" in s:
        print("luxe theme already applied — abort"); sys.exit(1)

    # 1) remove the dark theme block
    i = s.find(OLD_START)
    if i > -1:
        j = s.find(OLD_END, i)
        if j < 0:
            print("ABORT: dark end marker missing"); sys.exit(1)
        j += len(OLD_END)
        s = s[:i] + s[j:]
        print("removed v3.1 dark theme block")

    # 2) fonts: Tajawal → Cairo (keep Inter)
    old_link = "family=Tajawal:wght@400;500;700;800;900&family=Inter:wght@400;600;700;800"
    new_link = "family=Cairo:wght@400;500;600;700;800;900&family=Inter:wght@400;600;700;800"
    if old_link in s:
        s = s.replace(old_link, new_link, 1)
        print("font switched: Tajawal → Cairo")

    # 3) append luxe theme
    k = s.find("</style>")
    if k < 0:
        print("ABORT: </style>"); sys.exit(1)
    s = s[:k] + LUXE + s[k:]
    print("sapphire luxe theme appended (%d bytes)" % len(LUXE))

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — v4.0 SAPPHIRE LUXE applied")


if __name__ == "__main__":
    main()
