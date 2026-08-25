#!/usr/bin/env python3
"""
Paraveda CRM — feature patches (on top of P1-P8).

F1: PROTECT MAIN TABS — hide the ✕ (delete) mark on the core CRM pages and block
    their deletion. Previously only COMONDES/PRODUITS/Work Team/Les villes/Work
    Times were protected; now also: Dashboard performance, suivi confirmation,
    pièce, statistique, suivi rentabilité. (The tab bar renders ✕ only when
    !tg.includes(tab) and the delete handler refuses tg tabs — one array drives
    both, so extending it covers both.)

F2: BULK DELETE ORDERS — the orders table already has row selection, select-all
    (selects all FILTERED rows) and bulk-copy buttons. This adds a red
    "🗑️ حذف المحدد (N)" button to that same toolbar which deletes every selected
    order through the store's del() (so history/audit entries and the
    delivered-order protection for non-admins still apply).

Each anchor must match EXACTLY ONCE or the script aborts without writing.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

PATCHES = [
    (
        "F1-protect-main-tabs",
        'tg=["COMONDES","PRODUITS","Work Team","Les villes","Work Times"]',
        'tg=["COMONDES","PRODUITS","Work Team","Les villes","Work Times",'
        '"Dashboard performance","suivi confirmation","pièce","statistique","suivi rentabilité"]',
    ),
    (
        "F2-bulk-delete-selected-orders",
        's.jsx(yt,{icon:"📋",color:"slate",onClick:Va,title:"نسخ بجميع الخانات (Excel/Sheets)",children:"نسخ الكل"})',
        's.jsx(yt,{icon:"📋",color:"slate",onClick:Va,title:"نسخ بجميع الخانات (Excel/Sheets)",children:"نسخ الكل"})'
        ',s.jsx(yt,{icon:"🗑️",color:"red",onClick:()=>{'
        'const se=La;'
        'if(!se||!se.length)return;'
        'confirm(`مسح ${se.length} طلبية نهائياً؟`)&&'
        '(se.forEach(Ce=>c(Ce.id)),T(new Set),Sa(`🗑️ تم مسح ${se.length} طلبية`))'
        '},title:"مسح الطلبيات المحددة نهائياً (مع الحفاظ على حماية الطلبيات الموصلة)",'
        'children:["حذف المحدد (",La.length,")"]})',
    ),
]


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    for name, anchor, repl in PATCHES:
        n = s.count(anchor)
        if n != 1:
            print(f"ABORT: anchor {name} matched {n} times (expected 1)")
            sys.exit(1)

    for name, anchor, repl in PATCHES:
        s = s.replace(anchor, repl, 1)
        print(f"applied: {name}")

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — index.html patched (features)")


if __name__ == "__main__":
    main()
