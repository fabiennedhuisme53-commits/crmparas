#!/usr/bin/env python3
"""
Paraveda CRM — client-side sync fix (surgical patches on the built bundle).

Fixes the "data resurrection / user wipe" bug at the source:
  P1: pushes (aa) are queued until the first successful sync (GET) completes,
      so a browser with empty/cleared localStorage can NEVER push the built-in
      factory seed over the server's real data.
  P2: the initial sync (S4) now (a) refreshes React state via the registered
      callbacks exactly like the 12s poll does, and (b) retries every 5s on
      failure instead of giving up for the whole session.
  P3: the users store registers a sync callback so the UI adopts the server's
      users after sync instead of staying stuck on the [admin] factory seed.

Each anchor must match EXACTLY ONCE or the script aborts without writing.
"""
import sys

PATH = "/home/user/crmparas/app/index.html"

PATCHES = [
    # (name, anchor, replacement)
    (
        "P1-queue-push-until-synced",
        "function aa(e){if(!$c||!sg.includes(e))return;if(wl.has(e)){setTimeout(()=>aa(e),1200);return}",
        "var __pvq=new Set;function __pvqTick(){if($c){var a=Array.from(__pvq);"
        "__pvq.clear(),a.forEach(x=>aa(x))}else setTimeout(__pvqTick,3e3)}"
        "function aa(e){if(!$c){if(!__pvq.has(e)){__pvq.add(e),"
        "__pvq.size===1&&setTimeout(__pvqTick,3e3)}return}"
        "if(!sg.includes(e))return;if(wl.has(e)){setTimeout(()=>aa(e),1200);return}",
    ),
    (
        "P2-initial-sync-refresh-and-retry",
        "ig(n),$c=!0,E4()}catch{$c=!1}}let wl=new Set",
        "ig(n).forEach(i=>lg.get(i)?.()),$c=!0,E4()}catch{$c=!1,setTimeout(S4,5e3)}}let wl=new Set",
    ),
    (
        "P3-users-store-sync-callback",
        "ee.useEffect(()=>{localStorage.setItem(Yu,JSON.stringify(n)),aa(Yu)},[n])",
        "ee.useEffect(()=>{localStorage.setItem(Yu,JSON.stringify(n)),aa(Yu)},[n]),"
        "ee.useEffect(()=>{Ms(Yu,()=>{try{const d=localStorage.getItem(Yu);if(!d)return;"
        "const v=JSON.parse(d);Array.isArray(v)&&"
        "a(q=>JSON.stringify(q)===JSON.stringify(v)?q:v)}catch{}})},[])",
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
    print("OK — index.html patched")


if __name__ == "__main__":
    main()
