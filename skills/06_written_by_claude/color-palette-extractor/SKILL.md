---
name: color-palette-extractor
description: Extract a dominant color palette from an actual uploaded image (via k-means-style color clustering), instead of guessing hex codes by eye. Use whenever the user uploads a photo, logo, or screenshot and wants a color palette, brand colors, or a matching theme pulled from it.
---

# Color Palette Extractor

## Purpose
Guessing hex codes from looking at an image is unreliable — the same red can read as `#c0392b` or `#d63031` depending on lighting and screen. This skill runs actual pixel clustering on the image file to return real, measured colors.

## When to use
- User uploads an image and asks for "the colors in this", "a palette from this photo", "brand colors from this logo".
- Building a theme/design system that should visually match an existing image or screenshot.

## Workflow

1. Locate the uploaded image on disk (see file-handling rules — uploads live under `/mnt/user-data/uploads/`).

2. Run the extractor:
   ```bash
   python3 scripts/extract_palette.py /path/to/image.png --n 6
   ```
   `--n` sets how many dominant colors to extract (default 6).

3. The script prints each color as hex + RGB + the percentage of pixels it represents, sorted by prevalence.

4. Present the palette to the user. If they want it as design tokens, format as CSS custom properties or a JSON theme file using the exact hex values returned — never round or "prettify" a measured hex value into a rounder-looking one, since that defeats the purpose of extracting from the real image.

5. If the user wants accessible text/background pairings from the palette, check contrast ratios between candidate pairs (a simple WCAG contrast formula) rather than assuming any two extracted colors are readable together.

## Notes
- Uses Pillow + pure-Python k-means (no extra ML dependencies) so it works in a minimal environment.
- Downsamples large images internally for speed — this doesn't change which colors are dominant, just speeds up clustering.
- If the image has a transparent background, transparent pixels are excluded from clustering so they don't skew results toward white/black.
