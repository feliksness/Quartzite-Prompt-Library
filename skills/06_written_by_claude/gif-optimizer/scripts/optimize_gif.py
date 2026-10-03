#!/usr/bin/env python3
"""Optimize an animated GIF: reduce palette size, drop duplicate consecutive
frames, and optionally resize. Reports real before/after file sizes.

Usage:
    python3 optimize_gif.py input.gif output.gif --max-colors 128 --max-width 480
"""
import argparse
import os
from PIL import Image, ImageChops, ImageSequence


def load_frames(path):
    im = Image.open(path)
    durations = []
    frames = []
    for frame in ImageSequence.Iterator(im):
        frames.append(frame.convert("RGBA"))
        durations.append(frame.info.get("duration", 100))
    loop = im.info.get("loop", 0)
    return frames, durations, loop


def frames_near_equal(a, b, threshold=3.0):
    """True if two frames are visually indistinguishable. GIF re-encoding
    (per-frame local palettes) means truly-duplicate-looking frames are
    rarely byte-identical, so this uses a mean-pixel-difference threshold
    rather than exact equality."""
    diff = ImageChops.difference(a.convert("RGB"), b.convert("RGB"))
    if diff.getbbox() is None:
        return True
    hist = diff.histogram()  # 256 buckets per channel, R+G+B concatenated
    total_pixels = a.size[0] * a.size[1]
    total_diff = sum(i * v for i, v in enumerate(hist[0:256]))
    total_diff += sum(i * v for i, v in enumerate(hist[256:512]))
    total_diff += sum(i * v for i, v in enumerate(hist[512:768]))
    mean_diff = total_diff / (total_pixels * 3)
    return mean_diff < threshold


def dedupe_consecutive(frames, durations, threshold=3.0):
    """Merge frames that are visually identical to the immediately preceding
    frame, combining their duration into the kept frame instead."""
    if not frames:
        return frames, durations
    out_frames = [frames[0]]
    out_durations = [durations[0]]
    for f, d in zip(frames[1:], durations[1:]):
        if frames_near_equal(f, out_frames[-1], threshold):
            out_durations[-1] += d
        else:
            out_frames.append(f)
            out_durations.append(d)
    return out_frames, out_durations


def resize_frames(frames, max_width):
    if not max_width:
        return frames
    w, h = frames[0].size
    if w <= max_width:
        return frames
    scale = max_width / w
    new_size = (max_width, max(1, int(h * scale)))
    return [f.resize(new_size, Image.LANCZOS) for f in frames]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--max-colors", type=int, default=256)
    ap.add_argument("--max-width", type=int, default=None)
    args = ap.parse_args()

    orig_size = os.path.getsize(args.input)
    frames, durations, loop = load_frames(args.input)
    orig_frame_count = len(frames)

    frames, durations = dedupe_consecutive(frames, durations)
    frames = resize_frames(frames, args.max_width)

    # Quantize each frame to the target palette size, converting via 'P' mode
    quantized = [
        f.convert("RGB").quantize(colors=args.max_colors, method=Image.MEDIANCUT)
        for f in frames
    ]

    quantized[0].save(
        args.output,
        save_all=True,
        append_images=quantized[1:],
        duration=durations,
        loop=loop,
        optimize=True,
    )

    new_size = os.path.getsize(args.output)
    reduction = 100 * (1 - new_size / orig_size) if orig_size else 0

    print(f"Input:  {args.input}  ({orig_size/1024:.1f} KB, {orig_frame_count} frames)")
    print(f"Output: {args.output}  ({new_size/1024:.1f} KB, {len(frames)} frames)")
    print(f"Size reduction: {reduction:.1f}%")
    print(f"Palette: {args.max_colors} colors" + (f", resized to max width {args.max_width}px" if args.max_width else ""))
    if new_size >= orig_size:
        print("NOTE: output is not smaller than the input — the source may already be well-optimized, or try lowering --max-colors/--max-width further.")


if __name__ == "__main__":
    main()
