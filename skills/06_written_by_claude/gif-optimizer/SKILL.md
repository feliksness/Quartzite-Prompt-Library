---
name: gif-optimizer
description: Shrink an animated GIF's file size (palette reduction, frame deduplication, resizing) while reporting the actual before/after size and a quality trade-off summary, instead of guessing at settings. Use whenever the user has a GIF that's too large for Slack/Discord/email/a size-limited upload, or asks to "compress" or "optimize" a GIF.
---

# GIF Optimizer

## Purpose
GIF file size is dominated by a few controllable factors: palette size (max 256 colors, often fewer needed), frame count/duplicate frames, and pixel dimensions. This skill actually measures the file and applies targeted reductions, rather than blindly re-saving it.

## When to use
- User has a GIF over a platform's size limit (e.g. Slack's classic ~2MB limit — pair with the `slack-gif-creator` skill's validator for the exact current limit).
- User wants a smaller GIF for email/web without visibly degrading it.
- Not for: converting GIF to MP4/WebM for further size savings — mention that as an alternative if the target platform accepts video, since video codecs compress motion far better than GIF's per-frame palette approach.

## Workflow

1. Run the optimizer on the file:
   ```bash
   python3 scripts/optimize_gif.py input.gif output.gif --max-colors 128 --max-width 480
   ```
   Omit `--max-width` to keep original dimensions; omit `--max-colors` to keep 256.

2. The script reports: original size, new size, percentage reduction, frame count before/after (duplicate consecutive frames are dropped), and final palette size actually used.

3. If the reduction isn't enough to hit the target limit, iterate: try fewer colors first (least visible impact), then reduce dimensions, and only reduce frame count / playback fps as a last resort since that changes the motion feel.

4. Report the final numbers plainly — don't claim a target was hit without checking the actual output file size.

## Notes
- Uses Pillow only; no external binaries (ffmpeg/gifsicle) required, so it works in a minimal environment. If gifsicle is available on the system, mention it as a further option since it can perform lossy compression Pillow can't.
- Reducing to under ~64 colors starts to visibly banding on photographic content; for illustrations/logos with flat colors, far fewer colors (16-32) usually looks identical.
