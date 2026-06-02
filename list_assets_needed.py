#!/usr/bin/env python3
"""list_assets_needed.py <concepts.json>
Prints every asset a concepts file wants, so Claude Code knows exactly what to pull
from Envato and what filename to save. Pure read-only; no network."""
import json, sys
f = sys.argv[1] if len(sys.argv) > 1 else "concepts_video1.json"
concepts = json.load(open(f))
need = [(c["name"], c["asset"]) for c in concepts if c.get("asset")]
if not need:
    print(f"No assets requested in {f}."); raise SystemExit
print(f"Assets to pull for {f}:\n")
for name, a in need:
    print(f"  concept: {name}")
    print(f"    search Envato itemType={a.get('itemType','graphics')}  query=\"{a.get('envato_query','')}\"")
    print(f"    save chosen file as: assets/envato/{a['id']}.png")
    print(f"    will place in zone={a.get('zone','right')} scale={a.get('scale',0.42)}\n")
