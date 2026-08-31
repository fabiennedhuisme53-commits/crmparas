#!/usr/bin/env python3
"""
Paraveda CRM v3.0 — PRO THEME (complete visual overhaul, zero logic changes).

Strategy: the built bundle's Tailwind utilities all reference CSS variables
(--color-indigo-600, ...) — so redefining the variables recolors EVERY page,
menu, button, table and card at once. On top of that, a structural polish layer
(glass header, premium shadows, refined tables/inputs/buttons, custom
scrollbars, focus states, Tajawal+Inter typography) is appended AFTER the
compiled stylesheet so it wins the cascade.

Result: 100% new look everywhere (login, tabs bar, sidebar menus, orders grid,
Ranking, Dashboard, Work Team, modals, calculator...) with ZERO risk to data
logic — nothing in the JS is touched.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">\n'
)

THEME = """
/* ═══════════ PARAVEDA PRO THEME v3.0 — full visual overhaul ═══════════ */
:root{
  /* richer executive palette (same lightness → contrast-safe) */
  --color-indigo-400:#818cf8;--color-indigo-500:#5457ea;--color-indigo-600:#4338ca;--color-indigo-700:#362fae;--color-indigo-800:#2c2585;
  --color-violet-400:#a78bfa;--color-violet-500:#8b5cf6;--color-violet-600:#7c3aed;--color-violet-700:#6d28d9;--color-violet-800:#5b21b6;
  --color-blue-500:#3b82f6;--color-blue-600:#2563eb;--color-blue-700:#1d4ed8;
  --color-emerald-500:#10b981;--color-emerald-600:#059669;--color-emerald-700:#047857;
  --color-amber-400:#fbbf24;--color-amber-500:#f59e0b;--color-amber-600:#d97706;--color-amber-700:#b45309;
  --color-red-500:#ef4444;--color-red-600:#dc2626;--color-red-700:#b91c1c;
  --color-teal-600:#0d9488;--color-teal-700:#0f766e;
  --color-slate-800:#1e293b;--color-slate-900:#0f172a;
}
*{-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
html,body{font-family:'Tajawal','Inter',system-ui,-apple-system,'Segoe UI',Tahoma,sans-serif}
[dir="ltr"]{font-family:'Inter','Tajawal',system-ui,sans-serif}
body{font-variant-numeric:tabular-nums;letter-spacing:.1px}
b,strong{font-weight:800}
.font-extrabold,.font-black{letter-spacing:-.2px}
::selection{background:#c7d2fe;color:#1e1b4b}

/* ── app shell: soft premium backdrop ── */
.h-dvh.bg-slate-100{background:linear-gradient(175deg,#eef2f8 0%,#e8edf5 45%,#eef1f7 100%)}
.min-h-screen{background:linear-gradient(165deg,#eef2f8,#e6ebf4)}

/* ── glass header (every layout) ── */
header.bg-white{background:rgba(255,255,255,.82)!important;-webkit-backdrop-filter:blur(16px) saturate(1.4);backdrop-filter:blur(16px) saturate(1.4);border-bottom:1px solid rgba(148,163,184,.28)!important;box-shadow:0 1px 0 rgba(255,255,255,.6) inset,0 4px 24px -16px rgba(15,23,42,.25)}

/* ── cards: elevated, crisp ── */
.rounded-2xl.border{box-shadow:0 1px 2px rgba(15,23,42,.05),0 10px 30px -14px rgba(30,41,120,.14);border-color:#e2e8f0!important}
.rounded-2xl.border:hover{box-shadow:0 2px 4px rgba(15,23,42,.06),0 16px 40px -16px rgba(30,41,120,.2)}
.rounded-2xl{scrollbar-width:thin}

/* ── buttons: unified micro-interactions ── */
button{cursor:pointer;transition:transform .09s ease,box-shadow .2s ease,background-color .18s ease,filter .18s ease}
button:not(.pv-k):not(.pv-trig):not(.pv-x):not(.fill-handle):active{transform:scale(.965)}
button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,a:focus-visible{outline:2px solid #6366f1;outline-offset:2px;border-radius:8px}
input:focus-visible,select:focus-visible,textarea:focus-visible{outline:none;box-shadow:0 0 0 3px rgba(99,102,241,.16);border-color:#818cf8}

/* ── tables: executive grid ── */
table{font-variant-numeric:tabular-nums}
thead th{font-weight:800;letter-spacing:.35px}
tbody tr{transition:background-color .13s ease}
tbody tr:hover{background-color:rgba(99,102,241,.05)}
table td,table th{border-color:#e6eaf2}

/* ── inputs ── */
input,select,textarea{font-family:inherit}
input[type="checkbox"]{accent-color:#4f46e5;cursor:pointer}
input[type="radio"]{accent-color:#4f46e5;cursor:pointer}

/* ── slim elegant scrollbars ── */
::-webkit-scrollbar{width:9px;height:9px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#c7d2fe,#a5b4fc);border-radius:99px;border:2px solid rgba(255,255,255,.6);background-clip:padding-box}
::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#a5b4fc,#818cf8);background-clip:padding-box}
*{scrollbar-width:thin;scrollbar-color:#b6c1f8 transparent}

/* ── modals & overlays ── */
[class*="bg-slate-900/60"],[class*="bg-slate-900/45"],[class*="bg-black/45"],[class*="bg-black/20"]{-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
[class*="shadow-2xl"]{box-shadow:0 30px 80px -18px rgba(15,23,42,.45)!important}

/* ── pills, chips, badges ── */
.rounded-full{font-variant-numeric:tabular-nums}

/* ── sticky inner bars (page toolbars) get a hint of glass ── */
div.sticky.top-0{background:rgba(255,255,255,.9);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}

/* ── subtle entrance for modals/menus (GPU-cheap) ── */
[class*="fixed inset-0"]>*{animation:pvTIn .2s cubic-bezier(.34,1.3,.64,1)}
@keyframes pvTIn{from{opacity:0;transform:scale(.96) translateY(8px)}to{opacity:1;transform:scale(1) translateY(0)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
/* ═══════════ END PRO THEME ═══════════ */
"""


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    if "PARAVEDA PRO THEME" in s:
        print("theme already applied — aborting to stay idempotent"); sys.exit(1)

    # 1) fonts in <head> (the REAL document head = last </head>; the other one
    # lives inside a SheetJS export string)
    import re as _re
    heads = list(_re.finditer(r"</head>", s))
    if not heads:
        print("ABORT: no </head>"); sys.exit(1)
    h = heads[-1].start()
    s = s[:h] + FONT_LINKS + s[h:]
    print("fonts linked (Tajawal + Inter)")

    # 2) theme CSS at the end of the stylesheet (wins the cascade)
    k = s.find("</style>")
    if k < 0:
        print("ABORT: </style> not found"); sys.exit(1)
    s = s[:k] + THEME + s[k:]
    print("pro theme appended (%d bytes)" % len(THEME))

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — v3.0 PRO THEME applied")


if __name__ == "__main__":
    main()
