#!/usr/bin/env python3
"""
Paraveda CRM — v2.4 "clean start + auto-save" patches (on top of P1-P8, F1-F2).

User requests:
  * demo orders must NEVER come back (even via Reset) — CRM starts and stays EMPTY
  * remove ALL Reset buttons (accidental press brought old/demo orders back)
  * no Save button needed — Google-Sheets style auto-save

P9  dp() returns [] — the 168-demo factory seed is dead at the source. A fresh
    install starts with ZERO orders; nothing can ever render/push the demo again.
P10 reset() neutered — pressing any leftover restore path does nothing.
B1  "Save CMD" button removed (was a manual checkpoint — checkpoints now happen
    automatically, see P12).
B2  admin "↺ Reset" button removed (this was THE bug: it restored an old
    checkpoint, or fell back to dp() = 168 demo orders when no checkpoint).
B3  girls' "Save" button removed (same reason as B1).
B4  second "↺ Reset" button (sheet admin bar) removed.
P12 auto-checkpoint: 3s after any orders/agents change the snapshot updates
    silently in the background (the "✓ saved" badge keeps working).

Each anchor must match EXACTLY ONCE (positional extraction used where template
literals make literal anchors fragile) or the script aborts without writing.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"


def slice_span(s, start_marker, end_marker):
    """Return (start,end) span of the single element from start_marker to the
    FIRST end_marker after it. Both markers must occur exactly once."""
    if s.count(start_marker) != 1:
        return None, f"start marker not unique ({s.count(start_marker)}): {start_marker[:60]}"
    i = s.find(start_marker)
    j = s.find(end_marker, i)
    if j < 0:
        return None, "end marker not found for " + start_marker[:40]
    return (i, j + len(end_marker)), None


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    # ---------- literal patches ----------
    lit = [
        ("P9-demo-seed-disabled",
         "function dp(){return A4.map(",
         "function dp(){return[].map("),
        ("P10-reset-neutered",
         'reset:()=>{try{const v=localStorage.getItem(Mi);if(v){const A=JSON.parse(v);if(Array.isArray(A)){i(A);const D=localStorage.getItem(Mi+"_agents");D&&f(JSON.parse(D));return}}}catch{}i(dp()),f(vp)}',
         'reset:()=>{}'),
        ("P12-auto-checkpoint",
         'ee.useEffect(()=>{localStorage.setItem(Xu,JSON.stringify(c)),aa(Xu)},[c])',
         'ee.useEffect(()=>{localStorage.setItem(Xu,JSON.stringify(c)),aa(Xu)},[c]),'
         'ee.useEffect(()=>{const __t=setTimeout(()=>{try{'
         'const v=new Date().toISOString();'
         'localStorage.setItem(Mi,JSON.stringify(a)),'
         'localStorage.setItem(gp,v),'
         'localStorage.setItem(Mi+"_agents",JSON.stringify(c)),'
         'h(v),b(a.length)}catch{}},3e3);'
         'return()=>clearTimeout(__t)},[a,c])'),
    ]

    # ---------- positional button removals ----------
    btn = [
        ("B1-savecmd-button-removed",
         's.jsx(yt,{icon:"💾",color:"emerald",onClick:()=>{const se=u();',
         'children:"Save CMD"})'),
        ("B2-admin-reset-button-removed",
         's.jsx(yt,{icon:"↺",color:"red",variant:"ghost",onClick:()=>confirm(d?',
         'children:"Reset"})'),
        ("B3-girls-save-button-removed",
         's.jsx(yt,{icon:"💾",color:"emerald",onClick:()=>{const H=u();',
         'children:"Save"})'),
        ("B4-sheet-reset-button-removed",
         's.jsx("button",{onClick:R,className:"rounded-lg bg-red-600',
         'children:"↺ Reset"})'),
    ]

    # validate all first
    for name, a, r in lit:
        n = s.count(a)
        if n != 1:
            print(f"ABORT: {name} anchor matched {n} times"); sys.exit(1)

    # apply literals FIRST (they shift offsets)
    for name, a, r in lit:
        s = s.replace(a, r, 1)
        print("applied:", name)

    # compute spans on the UPDATED string
    spans = {}
    for name, a, e in btn:
        sp, err = slice_span(s, a, e)
        if err:
            print(f"ABORT: {name}: {err}"); sys.exit(1)
        i, j = sp
        seg = s[i:j]
        if len(seg) > 900 or seg.count('s.jsx(') != 1:
            print(f"ABORT: {name}: suspicious span (len={len(seg)}, s.jsx count={seg.count('s.jsx(')})")
            print("       span head:", seg[:120]); sys.exit(1)
        spans[name] = sp
        print("span ok:", name, f"({len(seg)} chars)")

    # apply removals (from the end backwards to keep offsets valid)
    for name in sorted(spans, key=lambda k: -spans[k][0]):
        i, j = spans[name]
        s = s[:i] + "null" + s[j:]
        print("applied:", name)

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — index.html patched (v2.4 clean-start + auto-save)")


if __name__ == "__main__":
    main()
