#!/usr/bin/env python3
"""
Paraveda CRM — live-sync & empty-state patches (applied on top of patch-client.py P1-P3).

Fixes the "demo orders keep coming back for every user" complaint at the UI layer:
  P5: the orders store treated an EMPTY saved list as "no data" and fell back to the
      168-demo factory seed on every boot (if(Array.isArray(A)&&A.length)). Empty is
      now respected as a real state (user deleted all orders).
  P4: live-refresh callbacks for orders (qu), agent names (Xu) and history (bd) —
      previously only users/worktimes/villes/chat/remarques/avances/adspend/perfrows
      had them. Without a callback the React state stayed on whatever it booted with
      (seed on a fresh browser / stale data on an open tab).
  P6: background poll 12s -> 5s for a near-live feel.
  P7: live-refresh callbacks for tabs list (pd) and custom sheets (gd).
  P8: live-refresh callback for team photos (cd).

Each anchor must match EXACTLY ONCE or the script aborts without writing.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

PATCHES = [
    # (name, anchor, replacement)
    (
        "P5-orders-empty-state-respected",
        "if(Array.isArray(A)&&A.length)return F4(A)}}catch{}return dp()",
        "if(Array.isArray(A))return F4(A)}}catch{}return dp()",
    ),
    (
        "P4-orders-agents-history-live-callbacks",
        'ee.useEffect(()=>{L4(u),aa("afrizon_history_v1")},[u]);',
        'ee.useEffect(()=>{L4(u),aa("afrizon_history_v1")},[u]);'
        'ee.useEffect(()=>{'
        'Ms(qu,()=>{try{const v=localStorage.getItem(qu);if(!v)return;'
        'const A=JSON.parse(v);if(!Array.isArray(A))return;const D=F4(A);'
        'i(T=>{try{return JSON.stringify(T)===JSON.stringify(D)?T:D}catch{return D}})}catch{}}),'
        'Ms(Xu,()=>{try{const v=localStorage.getItem(Xu);if(!v)return;'
        'const A=JSON.parse(v);if(Array.isArray(A)&&A.every(D=>typeof D=="string"))'
        'f(T=>JSON.stringify(T)===JSON.stringify(A)?T:A)}catch{}}),'
        'Ms(bd,()=>{try{const v=localStorage.getItem(bd);if(!v)return;'
        'const A=JSON.parse(v);if(Array.isArray(A))'
        'd(T=>JSON.stringify(T)===JSON.stringify(A)?T:A)}catch{}})'
        '},[]);',
    ),
    (
        "P6-poll-12s-to-5s",
        "},12e3))}",
        "},5e3))}",
    ),
    (
        "P7-tabs-customsheets-live-callbacks",
        "localStorage.setItem(pd,JSON.stringify(h)),aa(pd)},[h]),"
        "ee.useEffect(()=>{localStorage.setItem(gd,JSON.stringify(b)),aa(gd)},[b])",
        "localStorage.setItem(pd,JSON.stringify(h)),aa(pd)},[h]),"
        "ee.useEffect(()=>{localStorage.setItem(gd,JSON.stringify(b)),aa(gd)},[b]),"
        "ee.useEffect(()=>{"
        "Ms(pd,()=>{try{const C=localStorage.getItem(pd);if(C){const P=JSON.parse(C);"
        "g(q=>JSON.stringify(q)===JSON.stringify(P)?q:P)}}catch{}}),"
        "Ms(gd,()=>{try{const C=localStorage.getItem(gd);if(C){const P=JSON.parse(C);"
        "y(q=>JSON.stringify(q)===JSON.stringify(P)?q:P)}}catch{}})"
        "},[])",
    ),
]


def build_p8(s):
    """P8 positional: locate the team-photos (cd) save effect precisely
    (avoids escaping headaches with the apostrophe inside the alert text)."""
    core = 'aa(cd)}catch{alert('
    i = s.find(core)
    if i < 0:
        return None, None, "core not found"
    j = s.find('}},[w])', i)
    if j < 0 or j - i > 220:
        return None, None, "effect end not found"
    end = j + len('}},[w])')
    segment = s[i:end]
    if s.count(core) != 1 or 'photo' not in segment:
        return None, None, "core not unique or segment unexpected"
    replacement = segment + (
        ',ee.useEffect(()=>{'
        'Ms(cd,()=>{try{const C=localStorage.getItem(cd);if(C){const P=JSON.parse(C);'
        'N(q=>JSON.stringify(q)===JSON.stringify(P)?q:P)}}catch{}})'
        '},[])'
    )
    return segment, replacement, None


def main():
    with open(PATH, encoding="utf-8") as f:
        s = f.read()

    seg8, repl8, err8 = build_p8(s)
    if err8:
        print(f"ABORT: P8 positional failed: {err8}")
        sys.exit(1)
    patches = PATCHES + [("P8-teamphotos-live-callback", seg8, repl8)]

    for name, anchor, repl in patches:
        n = s.count(anchor)
        if n != 1:
            print(f"ABORT: anchor {name} matched {n} times (expected 1)")
            sys.exit(1)

    for name, anchor, repl in patches:
        s = s.replace(anchor, repl, 1)
        print(f"applied: {name}")

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK — index.html patched (live)")


if __name__ == "__main__":
    main()
