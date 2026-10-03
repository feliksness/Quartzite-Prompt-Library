#!/usr/bin/env python3
"""Extract a dominant color palette from an image using simple k-means
clustering on pixel RGB values. Standard library + Pillow only.

Usage:
    python3 extract_palette.py path/to/image.png --n 6
"""
import argparse
import random
from PIL import Image


def load_pixels(path: str, max_dim: int = 200):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))))
    pixels = []
    for r, g, b, a in img.getdata():
        if a < 32:  # skip near-fully-transparent pixels
            continue
        pixels.append((r, g, b))
    return pixels


def init_centroids_farthest_point(pixels, k, seed=42):
    """Farthest-point (k-means++-style) seeding. Plain random.sample can pick
    the same repeated color multiple times when an image has few flat color
    regions, which collapses distinct clusters together. This spreads the
    initial centroids out instead."""
    rnd = random.Random(seed)
    unique_pixels = list(set(pixels))
    if len(unique_pixels) <= k:
        return [list(p) for p in unique_pixels] + [list(unique_pixels[0])] * (k - len(unique_pixels))

    centroids = [list(rnd.choice(unique_pixels))]
    for _ in range(k - 1):
        best_pixel, best_dist = None, -1
        # sample a subset of candidates for speed on large unique-color counts
        candidates = unique_pixels if len(unique_pixels) <= 2000 else rnd.sample(unique_pixels, 2000)
        for p in candidates:
            d = min((p[0]-c[0])**2 + (p[1]-c[1])**2 + (p[2]-c[2])**2 for c in centroids)
            if d > best_dist:
                best_dist, best_pixel = d, p
        centroids.append(list(best_pixel))
    return centroids


def kmeans(pixels, k, iterations=12, seed=42):
    rnd = random.Random(seed)
    centroids = init_centroids_farthest_point(pixels, k, seed)

    for _ in range(iterations):
        clusters = [[] for _ in centroids]
        for p in pixels:
            best_i, best_d = 0, float("inf")
            for i, c in enumerate(centroids):
                d = (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 + (p[2] - c[2]) ** 2
                if d < best_d:
                    best_d, best_i = d, i
            clusters[best_i].append(p)

        new_centroids = []
        for i, cluster in enumerate(clusters):
            if cluster:
                r = sum(p[0] for p in cluster) / len(cluster)
                g = sum(p[1] for p in cluster) / len(cluster)
                b = sum(p[2] for p in cluster) / len(cluster)
                new_centroids.append([r, g, b])
            else:
                # empty cluster: respawn at the point farthest from all current centroids
                candidates = pixels if len(pixels) <= 2000 else rnd.sample(pixels, 2000)
                best_pixel, best_dist = candidates[0], -1
                for p in candidates:
                    d = min((p[0]-c[0])**2 + (p[1]-c[1])**2 + (p[2]-c[2])**2 for c in centroids)
                    if d > best_dist:
                        best_dist, best_pixel = d, p
                new_centroids.append(list(best_pixel))
        centroids = new_centroids

    # final assignment for percentage counts
    counts = [0] * len(centroids)
    for p in pixels:
        best_i, best_d = 0, float("inf")
        for i, c in enumerate(centroids):
            d = (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 + (p[2] - c[2]) ** 2
            if d < best_d:
                best_d, best_i = d, i
        counts[best_i] += 1

    total = sum(counts) or 1
    results = []
    for c, cnt in zip(centroids, counts):
        r, g, b = round(c[0]), round(c[1]), round(c[2])
        results.append({
            "hex": f"#{r:02x}{g:02x}{b:02x}",
            "rgb": (r, g, b),
            "pct": round(100 * cnt / total, 1),
        })
    results.sort(key=lambda x: -x["pct"])
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--n", type=int, default=6)
    args = ap.parse_args()

    pixels = load_pixels(args.path)
    if not pixels:
        print("No non-transparent pixels found in this image.")
        return

    palette = kmeans(pixels, args.n)
    print(f"Dominant colors in {args.path} (n={args.n}):\n")
    for c in palette:
        bar = "#" * max(1, round(c["pct"] / 2))
        print(f"  {c['hex']}  rgb{c['rgb']}  {c['pct']:5.1f}%  {bar}")


if __name__ == "__main__":
    main()
