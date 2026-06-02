# Pulling Envato assets (Claude Code step, runs on James's machine)

The chat environment can't reach Envato. Claude Code can, through the connected
Envato Elements MCP. This is how concept `asset` blocks become real files on disk.

## What a concept asks for
A concept that wants a real layered asset carries:
```json
"asset": {
  "type": "interface_panel",
  "envato_query": "credit score report dashboard ui mockup",
  "itemType": "graphic-templates",
  "id": "bankruptcies_panel",
  "zone": "right",
  "scale": 0.40
}
```

## The pull procedure (per asset)
1. Read concepts_<video>.json and collect every object that has an `asset` block.
2. For each, call the Envato MCP `search_items` with:
   - itemType = the asset's `itemType` (graphic-templates, graphics, photos…)
   - searchTerms = the asset's `envato_query`
3. Pick the result that best fits the Godiva look: clean, documentary, transparent or
   white background, no loud branding, no clip-art. Prefer PNG / transparent.
4. Download that item's preview/asset and save it to: assets/envato/<id>.png
   (use the EXACT `id` string from the asset block as the filename).
5. Repeat for all assets. Then run the normal build; finish_text.py will layer each
   asset into its zone automatically, razor-sharp, with text on top.

## Choosing well (this is the whole game)
- interface_panel  -> a credit/score dashboard or app-screen mockup, flat and clean
- stamped_document -> a transparent rubber-stamp PNG (APPROVED / DELETED / BLOCKED) or a blank form
- before_after_card-> a chart / score-gauge / data card with no fake paragraph text
Reject anything with garbled latin filler text on it; a blank or icon-only asset beats a
busy one. The asset is a trust signal only if it looks real, not stocky.

## If no good asset exists
Leave the file out. The build degrades gracefully: it renders the NB2 scene and notes the
missing layer. A clean NB2 prop beats a cheap stock comp.
