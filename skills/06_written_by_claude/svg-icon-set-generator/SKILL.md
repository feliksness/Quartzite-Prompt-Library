---
name: svg-icon-set-generator
description: Generate a consistent, validated set of SVG icons that all share the same viewBox, stroke width, and stroke style — instead of one-off icons that look mismatched next to each other. Use whenever the user wants a custom icon, a small icon set, or asks to "match the style of" an existing icon.
---

# SVG Icon Set Generator

## Purpose
A single hand-drawn SVG icon is easy; a *set* that looks like it belongs together is not — inconsistent viewBoxes, stroke widths, or corner-rounding make icons look like they came from different libraries even when a person drew them all. This skill enforces one shared style spec across every icon in a request and validates each SVG against it.

## When to use
- User wants 1 or more custom icons (not photographic images — for line icons/pictograms, this is the right tool; for photorealistic images use the image-generation skill instead).
- User wants new icons to visually match an existing set (e.g. "add a settings icon that matches my nav icons").

## Workflow

1. **Establish (or infer) the style spec** before drawing anything:
   - `viewBox` (commonly `0 0 24 24`)
   - stroke width (commonly `1.5` or `2`)
   - `stroke-linecap` / `stroke-linejoin` (`round` is most common for friendly icon sets, `square` for sharper/technical ones)
   - filled vs. outline style — don't mix within one set
   - corner radius convention if the icon uses rounded rects

   If the user is matching an existing icon, inspect it first and extract these values rather than guessing.

2. **Draw each icon** as an SVG using only simple primitives (`path`, `circle`, `rect`, `line`) at the agreed viewBox, using `currentColor` for stroke/fill so the icon inherits color from CSS rather than being hardcoded.

3. **Validate the whole set** before presenting it:
   ```bash
   python3 scripts/validate_icon_set.py icons/*.svg
   ```
   This checks: all files share the same `viewBox`, same stroke-width, same linecap/linejoin, no hardcoded colors (should use `currentColor` or no fill/stroke color at all), and that the SVG is well-formed XML.

4. Fix any icon flagged as inconsistent with the rest of the set before delivering.

## Notes
- Keep icons on a consistent visual weight (similar amount of "ink" per icon) — a very dense icon next to a very sparse one in the same set looks unbalanced even if technically valid.
- For a design-system deliverable, also produce a single `sprite.svg` with each icon as a `<symbol id="icon-name">` so the set can be referenced via `<use href="#icon-name">`.
