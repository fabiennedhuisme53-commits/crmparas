#!/usr/bin/env python3
"""
Paraveda CRM v5.1 — ONE / GRAPHITE SIDEBAR: dark graphite vertical sidebar +
pristine light content, the classic premium SaaS-CRM composition.
Keeps the whole PARAVEDA ONE token system (semantic palette, unified buttons,
readable table) and only overrides the sidebar's visual identity.
Zero JS changes. Appended AFTER the ONE block (cascade wins). Idempotent.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

GRAPHITE = r"""
/* ═══════════ PARAVEDA ONE · GRAPHITE SIDEBAR v5.1 ═══════════ */
@media (min-width:1024px){
  /* sidebar surface: deep graphite */
  .flex.h-dvh.flex-col.bg-slate-100>header{
    background:linear-gradient(196deg,#171e2e 0%,#121828 55%,#151d30 100%)!important;
    border-inline-end:1px solid rgba(148,163,184,.14);
    box-shadow:14px 0 44px -26px rgba(10,14,30,.6);
  }
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child{border-bottom:1px solid rgba(148,163,184,.12)}
  /* logo row: light text inside the dark sidebar */
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child .text-slate-800,
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child .text-slate-400,
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child .text-slate-600{color:#dbe3f4!important}
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child .bg-white,
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child [class*="bg-white/"]{background-color:rgba(255,255,255,.06)!important}
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child .border-slate-200{border-color:rgba(148,163,184,.2)!important}
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child input{background-color:rgba(255,255,255,.06);color:#e6ebf7;border-color:rgba(148,163,184,.2)}
  .flex.h-dvh.flex-col.bg-slate-100>header>div:first-child input::placeholder{color:#8b98b4}
  /* nav items */
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div::-webkit-scrollbar-thumb{background:rgba(148,163,184,.25)}
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button{
    color:#b9c4dc!important;border-radius:11px;letter-spacing:.15px;
  }
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button:hover{
    background:rgba(255,255,255,.06)!important;color:#ffffff!important;
  }
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button[class*="ring-2"]{
    background:rgba(59,91,219,.22)!important;color:#ffffff!important;
    box-shadow:inset 0 0 0 1px rgba(129,156,255,.35),0 8px 20px -10px rgba(59,91,219,.55)!important;
  }
  .flex.h-dvh.flex-col.bg-slate-100>header>nav>div>button[class*="ring-2"]::before{
    background:linear-gradient(180deg,#9db1ff,#5c7cfa);width:3.5px;
  }
  /* floating shortcut bar stays glass-light over the content */
}
/* ═══════════ END GRAPHITE SIDEBAR ═══════════ */
"""


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()
    if "GRAPHITE SIDEBAR" in s:
        print("already applied — abort"); sys.exit(1)
    k = s.find("</style>")
    if k < 0:
        print("ABORT: </style>"); sys.exit(1)
    s = s[:k] + GRAPHITE + s[k:]
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — v5.1 GRAPHITE SIDEBAR applied")


if __name__ == "__main__":
    main()
