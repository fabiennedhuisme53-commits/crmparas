#!/usr/bin/env python3
"""
Paraveda CRM v5.0 — "PARAVEDA ONE": a real unified Design System (UI/UX only).

Built on the audit findings. Zero JS changes — the system is enforced through
design tokens + semantic color folding + component layers:

T1 TOKENS        : one brand scale, semantic roles, radii, 3 shadow levels
T2 PALETTE FOLD  : 17 scattered color families fold into 4 semantic roles
                   (primary/success/warning/danger) + neutral slate — every
                   page, pill, button and chart inherits the same language
T3 NAVIGATION    : premium light sidebar (desktop) / clean pill bar (mobile)
T4 BUTTONS       : gradients flattened into uniform solid/soft/ghost variants
T5 TABLE         : readable orders grid — light separators, sticky blurred
                   header, hover row, aligned numerals, quiet actions
T6 SURFACES      : cards/modals/dropdowns/popovers share radius+shadow+border
T7 FORMS         : unified inputs, selects, focus rings, checkboxes
T8 MOTION/RTL    : subtle 150ms transitions, logical properties, slim
                   scrollbars, reduced-motion respected
Replaces the v4.0 SAPPHIRE LUXE block. Idempotent.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

OLD_START = "/* ═══════════ PARAVEDA SAPPHIRE LUXE v4.0"
OLD_END = "END SAPPHIRE LUXE ═══════════ */"

ONE = r"""
/* ═══════════ PARAVEDA ONE — Unified Design System v5.0 ═══════════ */
:root{
  color-scheme:light;
  /* T1 — tokens */
  --pv-primary:#3b5bdb;--pv-primary-strong:#2f4bc0;--pv-primary-soft:#eef2ff;--pv-primary-border:#c7d2fe;
  --pv-ok:#0e9f6e;--pv-ok-strong:#087f5b;--pv-ok-soft:#ecfdf5;
  --pv-warn:#b7791f;--pv-warn-strong:#9a6a15;--pv-warn-soft:#fffbeb;
  --pv-danger:#dc2626;--pv-danger-strong:#b91c1c;--pv-danger-soft:#fef2f2;
  --pv-ink:#0f172a;--pv-ink-2:#334155;--pv-mute:#64748b;
  --pv-line:#e6eaf2;--pv-line-soft:#eef1f7;
  --pv-surface:#ffffff;--pv-canvas:#f4f6fb;
  --pv-r-sm:8px;--pv-r:12px;--pv-r-lg:16px;
  --pv-sh-1:0 1px 2px rgba(15,23,42,.06);
  --pv-sh-2:0 1px 2px rgba(15,23,42,.05),0 10px 28px -14px rgba(30,41,110,.16);
  --pv-sh-3:0 30px 80px -22px rgba(15,23,42,.32);

  /* T2 — semantic folding of every Tailwind family */
  --color-indigo-400:#748ffc;--color-indigo-500:var(--pv-primary);--color-indigo-600:var(--pv-primary);
  --color-indigo-700:var(--pv-primary-strong);--color-indigo-800:#28359a;--color-indigo-900:#1e2a6e;
  --color-indigo-50:var(--pv-primary-soft);--color-indigo-100:#e0e7ff;--color-indigo-200:var(--pv-primary-border);
  --color-indigo-300:#a5b4fc;--color-indigo-100\/70:rgba(224,231,255,.7);--color-indigo-100\/60:rgba(224,231,255,.6);--color-indigo-50\/60:rgba(238,242,255,.6);--color-indigo-50\/40:rgba(238,242,255,.4);
  --color-violet-400:#748ffc;--color-violet-500:var(--pv-primary);--color-violet-600:var(--pv-primary);
  --color-violet-700:var(--pv-primary-strong);--color-violet-800:#28359a;
  --color-violet-50:var(--pv-primary-soft);--color-violet-100:#e0e7ff;--color-violet-200:var(--pv-primary-border);
  --color-violet-300:#a5b4fc;--color-violet-50\/60:rgba(238,242,255,.6);--color-violet-50\/30:rgba(238,242,255,.3);
  --color-purple-400:#748ffc;--color-purple-600:var(--pv-primary);--color-purple-700:var(--pv-primary-strong);
  --color-fuchsia-600:var(--pv-primary-strong);--color-fuchsia-700:var(--pv-primary-strong);
  --color-pink-600:#e11d6b;
  --color-blue-400:#6d8dfa;--color-blue-500:var(--pv-primary);--color-blue-600:var(--pv-primary);
  --color-blue-700:var(--pv-primary-strong);--color-blue-800:#28359a;--color-blue-900:#1e2a6e;
  --color-blue-50:#eef2ff;--color-blue-100:#e0e7ff;--color-blue-200:var(--pv-primary-border);--color-blue-300:#a5b4fc;
  --color-blue-50\/60:rgba(238,242,255,.6);--color-blue-50\/40:rgba(238,242,255,.4);--color-blue-200\/60:rgba(199,210,254,.6);
  --color-sky-500:var(--pv-primary);--color-sky-700:var(--pv-primary-strong);--color-sky-50:#eef2ff;
  --color-cyan-500:#0e9db8;
  --color-emerald-400:#38c990;--color-emerald-500:var(--pv-ok);--color-emerald-600:var(--pv-ok);
  --color-emerald-700:var(--pv-ok-strong);--color-emerald-800:#065f46;--color-emerald-900:#064e3b;
  --color-emerald-50:var(--pv-ok-soft);--color-emerald-100:#d1fae5;--color-emerald-200:#a7f3d0;--color-emerald-300:#6ee7b7;
  --color-emerald-50\/50:rgba(236,253,245,.5);--color-emerald-50\/30:rgba(236,253,245,.3);--color-emerald-50\/40:rgba(236,253,245,.4);--color-emerald-200\/60:rgba(167,243,208,.6);
  --color-teal-400:#2dd4bf;--color-teal-500:#14b8a6;--color-teal-600:var(--pv-ok);--color-teal-700:var(--pv-ok-strong);
  --color-teal-50:var(--pv-ok-soft);--color-teal-200:#a7f3d0;--color-teal-300:#6ee7b7;
  --color-green-600:var(--pv-ok);
  --color-amber-400:#f5b73d;--color-amber-500:#e8a91d;--color-amber-600:var(--pv-warn);
  --color-amber-700:var(--pv-warn-strong);--color-amber-800:#8a5d10;--color-amber-900:#7a5209;
  --color-amber-50:var(--pv-warn-soft);--color-amber-100:#fdeeba;--color-amber-200:#fbe58c;--color-amber-300:#f7d774;
  --color-amber-50\/70:rgba(255,251,235,.7);--color-amber-50\/40:rgba(255,251,235,.4);--color-amber-50\/30:rgba(255,251,235,.3);--color-amber-200\/60:rgba(251,229,140,.6);--color-amber-950\/30:rgba(69,26,3,.3);
  --color-orange-400:#f58f3c;--color-orange-500:#e97d22;--color-orange-600:var(--pv-warn);
  --color-orange-700:var(--pv-warn-strong);--color-orange-800:#8a5d10;--color-orange-900:#7a5209;
  --color-orange-50:var(--pv-warn-soft);--color-orange-100:#fdeeba;--color-orange-200:#fbe58c;--color-orange-300:#f7d774;
  --color-orange-500\/20:rgba(233,125,34,.2);--color-orange-200:var(--pv-warn-soft);
  --color-yellow-50:var(--pv-warn-soft);--color-yellow-500:#e8a91d;--color-yellow-600:var(--pv-warn);
  --color-red-400:#f36c6c;--color-red-500:var(--pv-danger);--color-red-600:var(--pv-danger);
  --color-red-700:var(--pv-danger-strong);--color-red-800:#991b1b;--color-red-900:#8f1d1d;
  --color-red-50:var(--pv-danger-soft);--color-red-100:#fee2e2;--color-red-200:#fecaca);--color-red-300:#fca5a5;
  --color-red-50\/70:rgba(254,242,242,.7);--color-red-50\/50:rgba(254,242,242,.5);--color-red-50\/30:rgba(254,242,242,.3);--color-red-950\/30:rgba(69,10,10,.3);
  --color-rose-400:#f36c8a;--color-rose-500:#e11d48;--color-rose-600:#dc2626;--color-rose-700:var(--pv-danger-strong);
  --color-rose-50:var(--pv-danger-soft);--color-rose-50\/90:rgba(254,242,242,.9);--color-rose-50\/30:rgba(254,242,242,.3);--color-rose-300:#fda4af;
  --color-slate-50:var(--pv-canvas);--color-slate-100:#eef1f7;--color-slate-200:var(--pv-line);--color-slate-300:#d6dce8;
  --color-slate-400:#94a3b8;--color-slate-500:var(--pv-mute);--color-slate-600:var(--pv-ink-2);--color-slate-700:#1e293b;
  --color-slate-800:var(--pv-ink);--color-slate-900:#0b1222;
  --color-slate-50\/60:rgba(244,246,251,.6);--color-slate-50\/70:rgba(244,246,251,.7);--color-slate-50\/90:rgba(244,246,251,.9);
  --color-slate-100\/80:rgba(238,241,247,.8);--color-slate-200\/80:rgba(230,234,242,.8);
  --color-slate-800\/60:rgba(30,41,59,.6);--color-slate-900\/60:rgba(11,18,34,.6);
  --color-black:#0b1222;--color-white:#ffffff;
}

/* ── typography (Cairo + Inter) ── */
*{-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
html,body{font-family:'Cairo','Inter',system-ui,-apple-system,'Segoe UI',Tahoma,sans-serif}
[dir="ltr"]{font-family:'Inter','Cairo',system-ui,sans-serif}
body{font-variant-numeric:tabular-nums;background:var(--pv-canvas);color:var(--pv-ink);letter-spacing:.1px}
b,strong{font-weight:800}.font-extrabold,.font-black{letter-spacing:-.2px}
::selection{background:#dbe4ff;color:#1e2a6e}

/* ── canvas ── */
.h-dvh.bg-slate-100,.min-h-screen{background:
  radial-gradient(880px 400px at 90% -12%,rgba(59,91,219,.06),transparent 60%),
  radial-gradient(700px 360px at -8% 110%,rgba(14,159,110,.05),transparent 55%),
  linear-gradient(178deg,#f6f8fc 0%,#f2f5fa 60%,#f4f6fb 100%)}

/* ═══════ T3 — NAVIGATION ═════════ */
@media (min-width:1024px){
  .flex.h-dvh.flex-col.bg-slate-100{flex-direction:row}
  .flex.h-dvh.flex-col.bg-slate-100>header{
    display:flex;flex-direction:column;width:268px;min-width:268px;height:100dvh;
    background:rgba(255,255,255,.94)!important;border-bottom:0!important;
    border-inline-end:1px solid var(--pv-line);box-shadow:var(--pv-sh-1);padding-bottom:8px;
  }
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child{flex-wrap:wrap;gap:10px;padding:14px 14px 10px;border-bottom:1px solid var(--pv-line-soft)}
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child>div[class*="md:flex"]{display:none!important}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav{flex:1;min-height:0;margin-top:6px;display:flex;flex-direction:column;overflow:hidden}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div{flex-direction:column!important;align-items:stretch!important;gap:2px!important;
    overflow-y:auto!important;overflow-x:hidden!important;padding:8px 10px!important;
    scrollbar-width:thin;scrollbar-color:var(--pv-line) transparent}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div::-webkit-scrollbar{width:5px}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div::-webkit-scrollbar-thumb{background:var(--pv-line);border-radius:99px}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>div[class*="w-px"]{display:none!important}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button{
    width:100%;justify-content:flex-start!important;gap:10px!important;padding:8px 12px!important;
    border-radius:10px;font-size:12.5px;letter-spacing:.1px;
    background:transparent!important;border-color:transparent!important;box-shadow:none!important;color:var(--pv-ink-2)}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button:hover{background:var(--pv-line-soft)!important;color:var(--pv-ink)!important;transform:none!important}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button[class*="ring-2"]{
    background:var(--pv-primary-soft)!important;color:var(--pv-primary-strong)!important;font-weight:800;
    box-shadow:none!important;position:relative}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button[class*="ring-2"]::before{
    content:"";position:absolute;inset-inline-start:3px;top:24%;bottom:24%;width:3px;border-radius:99px;
    background:var(--pv-primary)}
  .flex.h-dvh.flex-col.bg-slate-100>footer{
    position:fixed;bottom:10px;inset-inline-start:280px;inset-inline-end:12px;z-index:40;
    border-radius:14px;border:1px solid var(--pv-line);background:rgba(255,255,255,.9);
    -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
    box-shadow:var(--pv-sh-2);padding:5px 10px}
  .flex.h-dvh.flex-col.bg-slate-100>.flex-1.overflow-hidden{padding-bottom:54px}
}
/* girls + mobile header */
header.bg-white,.shrink-0.border-b.bg-white{background:rgba(255,255,255,.88)!important;-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom:1px solid var(--pv-line)!important;box-shadow:none!important}
div.sticky.top-0{background:rgba(255,255,255,.92);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}

/* ═══════ T4 — BUTTONS: flatten every gradient into semantic solids ═════════ */
button{cursor:pointer;transition:transform .1s ease,box-shadow .16s ease,background-color .16s ease,filter .16s ease,color .16s ease}
button:not(.pv-k):not(.pv-trig):not(.pv-x):active{transform:scale(.968)}
button:focus-visible,a:focus-visible{outline:2px solid var(--pv-primary);outline-offset:2px;border-radius:8px}
button[class*="bg-gradient-to"]{background-image:none!important}
button[class*="from-blue-"],button[class*="from-indigo-"],button[class*="from-violet-"],button[class*="from-purple-"]{background-color:var(--pv-primary)!important;border-color:var(--pv-primary-strong)!important}
button[class*="from-emerald-"],button[class*="from-teal-"],button[class*="from-green-"]{background-color:var(--pv-ok)!important;border-color:var(--pv-ok-strong)!important}
button[class*="from-amber-"],button[class*="from-orange-"],button[class*="from-yellow-"]{background-color:var(--pv-warn)!important;border-color:var(--pv-warn-strong)!important}
button[class*="from-red-"],button[class*="from-rose-"]{background-color:var(--pv-danger)!important;border-color:var(--pv-danger-strong)!important}
button[class*="from-slate-"],button[class*="from-slate-500"]{background-color:var(--pv-ink-2)!important;border-color:var(--pv-ink)!important}
button[class*="bg-gradient-to"]:not([class*="variant"]):hover{filter:brightness(.94)}
button[class*="bg-gradient-to"]{box-shadow:var(--pv-sh-1)}
button[class*="ring-2"]{--tw-ring-shadow:0 0 0 0 transparent!important;box-shadow:var(--pv-sh-1)!important}
/* ghost chips (soft) unify */
button[class*="bg-"][class*="/"]{border-color:var(--pv-line)!important}

/* ═══════ T5 — TABLE (orders grid readability) ═════════ */
table{font-variant-numeric:tabular-nums;border-collapse:collapse}
table td,table th{border-color:var(--pv-line-soft)!important}
thead th{font-weight:800;letter-spacing:.4px;font-size:10.5px;text-transform:uppercase;color:var(--pv-mute)}
thead tr{border-bottom:1px solid var(--pv-line)!important}
tbody tr{transition:background-color .13s ease}
tbody tr:hover{background-color:rgba(59,91,219,.045)}
/* quiet row actions: visible on hover only */
tbody tr td button{opacity:.55;transition:opacity .15s ease}
tbody tr:hover td button{opacity:1}
tbody tr td button:hover{transform:scale(1.06)}

/* ═══════ T6 — SURFACES: cards, modals, dropdowns, popovers ═════════ */
.rounded-2xl,.rounded-3xl{border-radius:var(--pv-r-lg)!important}
.rounded-xl{border-radius:var(--pv-r)!important}
.rounded-md{border-radius:var(--pv-r-sm)!important}
.rounded-2xl.border,.rounded-xl.border,.rounded-3xl.border{border-color:var(--pv-line)!important;box-shadow:var(--pv-sh-2)}
.rounded-2xl.border:hover{box-shadow:0 1px 2px rgba(15,23,42,.05),0 16px 36px -16px rgba(30,41,110,.22)}
[class*="shadow-2xl"]{box-shadow:var(--pv-sh-3)!important}
[class*="shadow-xl"],[class*="shadow-lg"]{box-shadow:var(--pv-sh-2)!important}
[class*="shadow-md"],[class*="shadow-sm"]{box-shadow:var(--pv-sh-1)!important}
/* dropdown/popover menus */
[class*="fixed z-50"],[class*="z-[70]"]>[class*="rounded-xl"]{border:1px solid var(--pv-line);box-shadow:var(--pv-sh-3)}
/* overlays */
[class*="bg-slate-900/60"],[class*="bg-black/45"],[class*="bg-black/20"],[class*="bg-slate-900/45"]{background-color:rgba(11,18,34,.5)!important;-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px)}
[class*="fixed inset-0"]>*{animation:pvOIn .18s cubic-bezier(.32,1.25,.6,1)}
@keyframes pvOIn{from{opacity:0;transform:scale(.97) translateY(6px)}to{opacity:1;transform:scale(1) translateY(0)}}

/* ═══════ T7 — FORMS ═════════ */
input,select,textarea{font-family:inherit;border-radius:10px;border-color:var(--pv-line)}
input::placeholder,textarea::placeholder{color:#94a3b8}
input:focus,select:focus,textarea:focus{outline:none;border-color:#a5b4fc;box-shadow:0 0 0 3px rgba(59,91,219,.14)}
input[type="checkbox"],input[type="radio"]{accent-color:var(--pv-primary);border-radius:4px}
select{background-image:none}
.bg-transparent{background-color:transparent}

/* KPI figures */
.text-3xl.font-extrabold,.text-2xl.font-extrabold{color:var(--pv-ink)}

/* ═══════ T8 — motion, scrollbars, a11y ═════════ */
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#c3cbdd;border-radius:99px;border:2px solid rgba(244,246,251,.9);background-clip:padding-box}
::-webkit-scrollbar-thumb:hover{background:#9aa6c0;background-clip:padding-box}
*{scrollbar-width:thin;scrollbar-color:#c3cbdd transparent}
/* calculator aligns to tokens */
.pv-card{border-radius:var(--pv-r-lg)!important;border-color:var(--pv-line)!important;box-shadow:var(--pv-sh-3)!important}
.pv-disp{background:#101a33;border-top:1px solid rgba(148,163,184,.18)}
.pv-k{border-radius:10px;background:#fff;border-color:var(--pv-line)}
.pv-k:hover{background:#f4f6fb}
.pv-k-op{background:var(--pv-primary-soft);border-color:var(--pv-primary-border);color:var(--pv-primary-strong)}
.pv-k-op.pv-on{background:var(--pv-primary);border-color:var(--pv-primary);color:#fff;box-shadow:0 4px 14px rgba(59,91,219,.35)}
.pv-k-fn{background:var(--pv-line-soft);border-color:var(--pv-line);color:var(--pv-ink-2)}
.pv-k-cl{background:var(--pv-danger-soft);border-color:#fecaca;color:var(--pv-danger)}
.pv-k-eq{background:var(--pv-primary);border-color:var(--pv-primary-strong)}
.pv-trig{background:#fff;border-color:var(--pv-line)}
.pv-trig:hover{background:#f4f6fb}
.pv-hist{border-top-color:var(--pv-line-soft)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
/* ═══════════ END PARAVEDA ONE ═══════════ */
"""


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    if "PARAVEDA ONE" in s:
        print("ONE already applied — abort"); sys.exit(1)

    i = s.find(OLD_START)
    if i > -1:
        j = s.find(OLD_END, i)
        if j < 0:
            print("ABORT: luxe end marker missing"); sys.exit(1)
        j += len(OLD_END)
        s = s[:i] + s[j:]
        print("removed v4.0 sapphire luxe block")

    k = s.find("</style>")
    if k < 0:
        print("ABORT: </style>"); sys.exit(1)
    s = s[:k] + ONE + s[k:]
    print("PARAVEDA ONE design system appended (%d bytes)" % len(ONE))

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — v5.0 PARAVEDA ONE applied")


if __name__ == "__main__":
    main()
