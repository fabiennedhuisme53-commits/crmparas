#!/usr/bin/env python3
"""
Paraveda CRM v3.1 — DARK PRO: TOTAL visual transformation.

Replaces the v3.0 light-polish theme with a full EXECUTIVE DARK redesign:
every page, menu, table, card, input, chip and modal is transformed.
Technique (zero JS changes):
  - Tailwind utilities resolve via CSS variables → the soft surfaces
    (slate-50..300, all *-50/-100/-200 tints) are redefined as dark
    translucency, recoloring chips/gradients/borders app-wide
  - explicit class overrides for text (bright on dark), solid greys,
    white surfaces, hovers, inputs, tables, glass header, aurora shell
  - calculator (pv-*) restyled dark too
Idempotent: aborts if the marker is already present.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

OLD_START = "/* ═══════════ PARAVEDA PRO THEME v3.0"
OLD_END = "END PRO THEME ═══════════ */"

DARK = r"""
/* ═══════════ PARAVEDA DARK PRO v3.1 — total transformation ═══════════ */
:root{
  color-scheme:dark;
  /* soft surfaces → deep navy (drives bg, borders, gradient stops) */
  --color-slate-50:#0d1424;--color-slate-100:#0b111f;--color-slate-200:#1a2440;--color-slate-300:#263354;
  /* soft tints → translucent dark (chips, badges, soft cards, gradients) */
  --color-indigo-50:rgba(99,102,241,.12);--color-indigo-100:rgba(99,102,241,.18);--color-indigo-200:rgba(99,102,241,.24);
  --color-violet-50:rgba(139,92,246,.12);--color-violet-100:rgba(139,92,246,.18);--color-violet-200:rgba(139,92,246,.24);
  --color-blue-50:rgba(59,130,246,.12);--color-blue-100:rgba(59,130,246,.18);--color-blue-200:rgba(59,130,246,.24);
  --color-emerald-50:rgba(16,185,129,.12);--color-emerald-100:rgba(16,185,129,.18);--color-emerald-200:rgba(16,185,129,.24);
  --color-red-50:rgba(239,68,68,.11);--color-red-100:rgba(239,68,68,.17);--color-red-200:rgba(239,68,68,.23);
  --color-amber-50:rgba(245,158,11,.11);--color-amber-100:rgba(245,158,11,.17);--color-amber-200:rgba(245,158,11,.23);
  --color-orange-50:rgba(249,115,22,.12);--color-orange-100:rgba(249,115,22,.18);--color-orange-200:rgba(249,115,22,.24);
  --color-teal-50:rgba(13,148,136,.12);--color-teal-200:rgba(13,148,136,.2);
  --color-rose-50:rgba(244,63,94,.11);--color-rose-100:rgba(244,63,94,.17);
  --color-yellow-50:rgba(234,179,8,.11);--color-yellow-500:#eab308;--color-yellow-600:#ca8a04;
  --color-sky-50:rgba(14,165,233,.12);--color-sky-700:#38bdf8;
  --color-fuchsia-700:#e879f9;--color-pink-600:#f472b6;--color-green-600:#22c55e;
  --color-purple-400:#c084fc;--color-purple-600:#9333ea;--color-purple-700:#7e22ce;
  --color-cyan-500:#22d3ee;--color-black:#020617;
  /* saturated accents kept rich */
  --color-indigo-500:#6366f1;--color-indigo-600:#4f46e5;--color-indigo-700:#4338ca;--color-indigo-800:#3730a3;
  --color-violet-500:#8b5cf6;--color-violet-600:#7c3aed;--color-violet-700:#6d28d9;
  --color-blue-500:#3b82f6;--color-blue-600:#2563eb;--color-blue-700:#1d4ed8;
  --color-emerald-500:#10b981;--color-emerald-600:#059669;--color-emerald-700:#047857;--color-emerald-300:#34d399;
  --color-red-500:#ef4444;--color-red-600:#dc2626;--color-red-700:#b91c1c;
  --color-amber-400:#fbbf24;--color-amber-500:#f59e0b;--color-amber-600:#d97706;--color-amber-700:#b45309;
  --color-teal-600:#14b8a6;--color-teal-700:#0d9488;--color-orange-400:#fb923c;--color-orange-500:#f97316;
}

/* ── typography ── */
*{-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
html,body{font-family:'Tajawal','Inter',system-ui,-apple-system,'Segoe UI',Tahoma,sans-serif}
[dir="ltr"]{font-family:'Inter','Tajawal',system-ui,sans-serif}
body{font-variant-numeric:tabular-nums;letter-spacing:.1px}
b,strong{font-weight:800}.font-extrabold,.font-black{letter-spacing:-.2px}
::selection{background:#4338ca;color:#eef2ff}

/* ── aurora shell ── */
body{background:#080d1a;color:#e2e8f0}
.h-dvh.bg-slate-100,.min-h-screen{background:
  radial-gradient(1100px 520px at 88% -12%,rgba(99,102,241,.20),transparent 62%),
  radial-gradient(900px 460px at -12% 112%,rgba(139,92,246,.15),transparent 58%),
  radial-gradient(700px 380px at 45% 118%,rgba(14,165,233,.07),transparent 60%),
  linear-gradient(178deg,#0a101f 0%,#0b1322 52%,#080d1a 100%)}

/* ── glass header + sticky bars ── */
header.bg-white{background:rgba(10,16,31,.78)!important;-webkit-backdrop-filter:blur(18px) saturate(1.5);backdrop-filter:blur(18px) saturate(1.5);border-bottom:1px solid rgba(148,163,184,.16)!important;box-shadow:0 8px 32px -18px rgba(0,0,0,.7)}
div.sticky.top-0{background:rgba(10,16,31,.86);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}

/* ── surfaces ── */
.bg-white{background-color:#111a2e}
[class*="bg-white/"]{background-color:rgba(17,26,46,.9)}
.bg-slate-500{background-color:#64748b}.bg-slate-600{background-color:#475569}
.bg-slate-700{background-color:#334155}.bg-slate-800{background-color:#1e293b}
.bg-slate-900{background-color:#0f172a}
[class*="bg-slate-900/"]{background-color:rgba(2,6,23,.74)}
[class*="bg-slate-50/"]{background-color:rgba(13,20,36,.9)}
[class*="bg-slate-100/"]{background-color:rgba(11,17,31,.92)}
[class*="bg-slate-200/"]{background-color:rgba(26,36,64,.92)}
.bg-[#f8f9fa]{background-color:#0d1424}[class*="bg-[#f8f9fa]"]{background-color:#0d1424}
.bg-[#e8e8e8]{background-color:#151f36}[class*="bg-[#e8e8e8]"]{background-color:#151f36}
.bg-[#434343]{background-color:#1f2a44}
.from-white{--tw-gradient-from:#111a2e}.to-white{--tw-gradient-to:#111a2e}
.to-slate-50{--tw-gradient-to:#0d1424}.to-transparent{--tw-gradient-to:transparent}

/* ── cards ── */
.rounded-2xl.border,.rounded-xl.border{border-color:rgba(148,163,184,.16)!important;box-shadow:0 1px 0 rgba(255,255,255,.03) inset,0 14px 40px -18px rgba(0,0,0,.55)}
.rounded-2xl.border:hover{box-shadow:0 1px 0 rgba(255,255,255,.05) inset,0 20px 50px -18px rgba(0,0,0,.65)}
[class*="shadow-2xl"]{box-shadow:0 30px 80px -18px rgba(0,0,0,.75)!important}
[class*="shadow-lg"],[class*="shadow-xl"]{box-shadow:0 18px 44px -16px rgba(0,0,0,.6)!important}

/* ── text on dark ── */
.text-slate-900{color:#f8fafc}.text-slate-800{color:#f1f5f9}.text-slate-700{color:#e2e8f0}
.text-slate-600{color:#cbd5e1}.text-slate-500{color:#94a3b8}.text-slate-400{color:#8296b4}.text-slate-300{color:#a9b8d0}
.text-indigo-600,.text-indigo-700,.text-indigo-800,.text-indigo-900{color:#a5b4fc}
.text-violet-600,.text-violet-700,.text-violet-800{color:#c4b5fd}
.text-blue-600,.text-blue-700,.text-blue-800,.text-blue-900{color:#93c5fd}
.text-emerald-600,.text-emerald-700,.text-emerald-800,.text-emerald-900{color:#6ee7b7}
.text-red-600,.text-red-700,.text-red-800,.text-red-900{color:#fca5a5}
.text-amber-600,.text-amber-700,.text-amber-800{color:#fcd34d}
.text-teal-600,.text-teal-700{color:#5eead4}
.text-orange-600,.text-orange-700,.text-orange-800,.text-orange-900{color:#fdba74}
.text-rose-600,.text-rose-700{color:#fda4af}
.text-indigo-900\/70{color:rgba(199,210,254,.8)}
[class*="text-white/"]{color:rgba(255,255,255,.85)}

/* ── hovers / focus ── */
.hover\:bg-slate-50:hover,.hover\:bg-slate-100:hover,.hover\:bg-slate-200:hover{background-color:#1a2440}
.hover\:bg-white:hover,.hover\:bg-white\/80:hover,.hover\:bg-white\/90:hover{background-color:rgba(30,41,59,.92)}
.hover\:bg-white\/25:hover,.hover\:bg-white\/30:hover,.hover\:bg-white\/40:hover{background-color:rgba(148,163,184,.2)}
.hover\:bg-indigo-50:hover,.hover\:bg-indigo-100:hover{background-color:rgba(99,102,241,.18)}
.hover\:bg-emerald-50:hover,.hover\:bg-emerald-100:hover,.hover\:bg-emerald-200:hover{background-color:rgba(16,185,129,.18)}
.hover\:bg-red-50:hover,.hover\:bg-red-100:hover{background-color:rgba(239,68,68,.17)}
.hover\:bg-amber-50:hover,.hover\:bg-amber-50\/30:hover{background-color:rgba(245,158,11,.15)}
.hover\:bg-blue-50:hover,.hover\:bg-blue-50\/40:hover{background-color:rgba(59,130,246,.16)}
.hover\:bg-indigo-50\/40:hover,.hover\:bg-indigo-50\/60:hover{background-color:rgba(99,102,241,.14)}
.hover\:bg-violet-50:hover,.hover\:bg-violet-50\/30:hover{background-color:rgba(139,92,246,.16)}
.hover\:bg-teal-50:hover{background-color:rgba(13,148,136,.16)}
.hover\:bg-rose-50\/30:hover{background-color:rgba(244,63,94,.13)}
.hover\:bg-emerald-50\/30:hover,.hover\:bg-emerald-50\/40:hover{background-color:rgba(16,185,129,.13)}
.hover\:bg-red-50\/30:hover,.hover\:bg-red-50\/50:hover,.hover\:bg-red-50\/70:hover{background-color:rgba(239,68,68,.13)}
.hover\:bg-amber-50\/70:hover{background-color:rgba(245,158,11,.2)}
.focus\:bg-white:focus,.focus\:bg-white\/80:focus{background-color:rgba(15,23,42,.95)}
button{cursor:pointer;transition:transform .09s ease,box-shadow .2s ease,background-color .18s ease}
button:not(.pv-k):not(.pv-trig):not(.pv-x):active{transform:scale(.965)}
button:focus-visible,a:focus-visible{outline:2px solid #818cf8;outline-offset:2px;border-radius:8px}

/* ── inputs ── */
input,select,textarea{color:#e5e7eb;background-color:rgba(13,20,36,.9);border-color:rgba(148,163,184,.25);color-scheme:dark}
input::placeholder,textarea::placeholder{color:#64748b}
input:focus,select:focus,textarea:focus{outline:none;border-color:#818cf8;box-shadow:0 0 0 3px rgba(99,102,241,.22)}
input[type="date"]::-webkit-calendar-picker-indicator{filter:invert(.75)}
input[type="checkbox"],input[type="radio"]{accent-color:#6366f1}
.bg-transparent{background-color:transparent}
select option{background-color:#0f172a;color:#e5e7eb}

/* ── tables ── */
table td,table th{border-color:rgba(148,163,184,.15)}
thead th{font-weight:800;letter-spacing:.35px}
tbody tr{transition:background-color .13s}
tbody tr:hover{background-color:rgba(99,102,241,.07)}
.divide-slate-50>:not(:last-child){border-color:rgba(148,163,184,.12)}

/* ── overlays & motion ── */
[class*="bg-slate-900/60"],[class*="bg-black/45"],[class*="bg-black/20"]{-webkit-backdrop-filter:blur(7px);backdrop-filter:blur(7px)}
[class*="fixed inset-0"]>*{animation:pvDIn .2s cubic-bezier(.34,1.3,.64,1)}
@keyframes pvDIn{from{opacity:0;transform:scale(.96) translateY(8px)}to{opacity:1;transform:scale(1) translateY(0)}}

/* ── scrollbars ── */
::-webkit-scrollbar{width:9px;height:9px}
::-webkit-scrollbar-track{background:rgba(148,163,184,.06)}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#4f46e5,#6d28d9);border-radius:99px;border:2px solid rgba(8,13,26,.8);background-clip:padding-box}
::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#6366f1,#8b5cf6);background-clip:padding-box}
*{scrollbar-width:thin;scrollbar-color:#4f46e5 rgba(148,163,184,.06)}

/* ── calculator dark ── */
.pv-card{background:#0e1526;border-color:rgba(148,163,184,.2)}
.pv-disp{background:#060b16;border-top:1px solid rgba(148,163,184,.12)}
.pv-k{background:#182238;border-color:rgba(148,163,184,.2);color:#e2e8f0}
.pv-k:hover{background:#1f2a44;box-shadow:none}
.pv-k-op{background:rgba(99,102,241,.16);border-color:rgba(99,102,241,.4);color:#a5b4fc}
.pv-k-op.pv-on{background:#6366f1;border-color:#818cf8;color:#fff;box-shadow:0 4px 16px rgba(99,102,241,.45)}
.pv-k-fn{background:rgba(148,163,184,.12);border-color:rgba(148,163,184,.22);color:#cbd5e1}
.pv-k-cl{background:rgba(239,68,68,.14);border-color:rgba(239,68,68,.4);color:#fca5a5}
.pv-hist{border-top-color:rgba(148,163,184,.14)}
.pv-h{color:#7c8aa5}
.pv-hist-clear{background:rgba(148,163,184,.14);color:#94a3b8}
.pv-hist-clear:hover{background:rgba(148,163,184,.24)}
.pv-trig{background:#131c31;border-color:rgba(148,163,184,.24)}
.pv-trig:hover{background:#1c2742}
.pv-expr{color:#7c8aa5}

@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
/* ═══════════ END PARAVEDA DARK PRO ═══════════ */
"""


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    if "PARAVEDA DARK PRO" in s:
        print("dark theme already applied — abort"); sys.exit(1)

    # remove the v3.0 light-polish block (fonts link stays)
    i = s.find(OLD_START)
    if i > -1:
        j = s.find(OLD_END, i)
        if j < 0:
            print("ABORT: old theme end marker missing"); sys.exit(1)
        j += len(OLD_END)
        s = s[:i] + s[j:]
        print("removed v3.0 light theme block")

    k = s.find("</style>")
    if k < 0:
        print("ABORT: </style>"); sys.exit(1)
    s = s[:k] + DARK + s[k:]
    print("dark pro theme appended (%d bytes)" % len(DARK))

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — v3.1 DARK PRO applied")


if __name__ == "__main__":
    main()
