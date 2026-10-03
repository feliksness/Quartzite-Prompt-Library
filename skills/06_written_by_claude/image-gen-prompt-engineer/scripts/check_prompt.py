#!/usr/bin/env python3
"""Check an AI image-generation prompt draft against common failure patterns.

Usage:
    python3 check_prompt.py "a photorealistic cartoon of a dog running on the beach at sunset"
"""
import argparse
import re

CONFLICTING_STYLE_GROUPS = [
    {"photorealistic", "photo-realistic", "realistic photo", "hyperrealistic"},
    {"cartoon", "anime", "cel-shaded", "toon"},
    {"3d render", "cgi", "octane render", "unreal engine"},
    {"oil painting", "watercolor", "pencil sketch", "line drawing"},
]

VAGUE_QUANTITY_WORDS = {"some", "a few", "several", "many", "various", "a bunch of"}

ABSTRACT_NOUNS = {
    "innovation", "synergy", "disruption", "excellence", "success",
    "growth", "efficiency", "leadership", "empowerment", "sustainability",
}

COMPOSITION_KEYWORDS = {
    "close-up", "close up", "wide shot", "bird's-eye", "birds eye", "aerial",
    "portrait", "landscape orientation", "square", "over-the-shoulder",
    "low angle", "high angle", "macro", "full body", "medium shot",
}


def find_style_conflicts(prompt_lower):
    hits = []
    for group in CONFLICTING_STYLE_GROUPS:
        matched = [term for term in group if term in prompt_lower]
        if matched:
            hits.append(matched)
    conflicting_pairs = []
    for i in range(len(hits)):
        for j in range(i + 1, len(hits)):
            # only a real conflict if terms come from *different* style groups
            conflicting_pairs.append((hits[i], hits[j]))
    return conflicting_pairs if len(hits) > 1 else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    args = ap.parse_args()
    prompt = args.prompt
    lower = prompt.lower()

    issues = []

    conflicts = find_style_conflicts(lower)
    for a, b in conflicts:
        issues.append(f"conflicting style cues: {a} vs {b} — pick one medium/style, not both")

    vague_hits = [w for w in VAGUE_QUANTITY_WORDS if re.search(rf"\b{re.escape(w)}\b", lower)]
    if vague_hits:
        issues.append(f"vague quantity word(s) {vague_hits} — models handle exact counts more reliably than fuzzy amounts")

    abstract_hits = [w for w in ABSTRACT_NOUNS if re.search(rf"\b{w}\b", lower)]
    if abstract_hits:
        issues.append(f"abstract, non-visual noun(s) {abstract_hits} — nothing for the model to actually render; replace with a concrete visual metaphor")

    has_composition = any(kw in lower for kw in COMPOSITION_KEYWORDS)
    if not has_composition:
        issues.append("no composition/framing specified (e.g. close-up, wide shot, low angle) — the model will pick an arbitrary default")

    word_count = len(prompt.split())
    if word_count < 6:
        issues.append(f"prompt is very short ({word_count} words) — likely under-specifies subject, setting, and style")

    print(f"Prompt: {prompt}\n")
    if not issues:
        print("No issues found — prompt looks well-specified.")
    else:
        print(f"{len(issues)} issue(s) found:")
        for i in issues:
            print(f"  - {i}")


if __name__ == "__main__":
    main()
