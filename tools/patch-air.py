#!/usr/bin/env python3
"""
Paraveda CRM v6.0 — AIR: the depth layer that makes ONE feel truly designed.
Appended AFTER ONE+Graphite (wins the cascade). Zero JS changes.

A1 NAV PILLS DE-RAINBOW : every horizontal pill nav (sources, inner tabs)
                          becomes neutral; active = solid primary. The
                          rainbow selector rows disappear.
A2 TABLE REBUILD        : Airtable-style grid — horizontal hairlines only
                          (no vertical cell borders), solid uppercase micro
                          header, quiet hover.
A3 CONFIDENT TITLES     : page toolbars get small, tight, letter-spaced
                          headings (SaaS convention) instead of shouty h1s.
A4 CHIP / BUTTON VOICE  : uniform 700-weight chips, consistent button type.
A5 MODAL REFINEMENT     : 18px radius, softer overlay.
A6 SIDEBAR RE-ASSERT    : graphite sidebar rules re-applied after A1 so the
                          sidebar keeps its identity.
Idempotent.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

AIR = r"""
/* ═══════════ PARAVEDA AIR v6.0 — depth layer ═══════════ */
/* A1 · de-rainbow all horizontal pill navs */
nav button[class*="from-"]{background-color:#ffffff!important;color:var(--pv-ink-2)!important;
  border-color:var(--pv-line)!important;box-shadow:var(--pv-sh-1)!important;font-weight:700;letter-spacing:.1px}
nav button[class*="from-"]:hover{background-color:var(--pv-canvas)!important;color:var(--pv-ink)!important;transform:none!important}
nav button[class*="from-"][class*="ring-2"]{background-color:var(--pv-primary)!important;color:#ffffff!important;
  border-color:var(--pv-primary-strong)!important;box-shadow:0 6px 16px -8px rgba(59,91,219,.55)!important}

/* A2 · table rebuild: hairline rows, clean header */
table{border-collapse:collapse}
table td{border-inline-start:0!important;border-inline-end:0!important;border-top:0!important;
  border-bottom:1px solid var(--pv-line-soft)!important}
table th{border-inline-start:0!important;border-inline-end:0!important;border-top:0!important;
  border-bottom:1px solid var(--pv-line)!important}
thead th{background:#ffffff;color:var(--pv-mute);font-size:10px;font-weight:800;
  letter-spacing:.7px;text-transform:uppercase;white-space:nowrap}
thead{box-shadow:0 1px 0 var(--pv-line)}
tbody tr:last-child td{border-bottom:0!important}

/* A3 · confident small page titles */
div[class*="sticky"] h1,header h1{font-size:1.07rem!important;letter-spacing:-.25px;font-weight:800!important}
div[class*="sticky"] .text-2xl,header .text-2xl{font-size:1.07rem!important}
div[class*="sticky"] .text-lg{font-size:.98rem!important}
.text-3xl.font-extrabold{letter-spacing:-.5px}

/* A4 · chips & buttons voice */
[class*="rounded-full"][class*="bg-"]{font-weight:700;letter-spacing:.2px}
button[class*="from-"]{font-weight:700;letter-spacing:.1px}
button .text-2xl,button .text-3xl{font-weight:800}

/* A5 · modal refinement */
[class*="fixed inset-0"] [class*="rounded-2xl"]{border-radius:18px}
[class*="fixed inset-0"]{background-color:rgba(11,18,34,.42)!important}

/* A6 · re-assert graphite sidebar (after A1) */
@media (min-width:1024px){
  .flex.h-dvh.flex-col.bg-slate-100>header nav button{
    color:#b9c4dc!important;background:transparent!important;border-color:transparent!important;box-shadow:none!important}
  .flex.h-dvh.flex-col.bg-slate-100>header nav button:hover{background:rgba(255,255,255,.06)!important;color:#fff!important}
  .flex.h-dvh.flex-col.bg-slate-100>header nav button[class*="ring-2"]{
    background:rgba(59,91,219,.22)!important;color:#ffffff!important;
    box-shadow:inset 0 0 0 1px rgba(129,156,255,.35),0 8px 20px -10px rgba(59,91,219,.55)!important}
}
/* ═══════════ END PARAVEDA AIR ═══════════ */
"""


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()
    if "PARAVEDA AIR" in s:
        print("AIR already applied — abort"); sys.exit(1)
    k = s.find("</style>")
    if k < 0:
        print("ABORT: </style>"); sys.exit(1)
    s = s[:k] + AIR + s[k:]
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — v6.0 AIR depth layer applied")


if __name__ == "__main__":
    main()
