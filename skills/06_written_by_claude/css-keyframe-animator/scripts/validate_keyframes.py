#!/usr/bin/env python3
"""Validate CSS @keyframes blocks: non-animatable properties, malformed
selectors, out-of-range percentages, and duplicate selectors.

Usage:
    python3 validate_keyframes.py path/to/styles.css
"""
import argparse
import re
import sys

# Properties that CANNOT be smoothly animated (discrete or non-interpolable)
NON_ANIMATABLE = {
    "display", "visibility", "position", "float", "overflow",
    "font-family", "white-space", "cursor", "content", "z-index",
}

# Properties that trigger layout (expensive) vs. compositor-only (cheap)
LAYOUT_TRIGGERING = {
    "width", "height", "top", "left", "right", "bottom",
    "margin", "margin-top", "margin-left", "margin-right", "margin-bottom",
    "padding", "padding-top", "padding-left", "padding-right", "padding-bottom",
    "font-size", "line-height",
}


def find_keyframe_blocks(css: str):
    """Find @keyframes blocks using manual brace matching (regex can't
    reliably handle nested braces of unknown depth)."""
    blocks = []
    for m in re.finditer(r"@keyframes\s+([\w-]+)\s*\{", css):
        name = m.group(1)
        start = m.end()  # just after the opening {
        depth = 1
        i = start
        while i < len(css) and depth > 0:
            if css[i] == "{":
                depth += 1
            elif css[i] == "}":
                depth -= 1
            i += 1
        body = css[start:i - 1]  # exclude the final closing brace
        blocks.append((name, body))
    return blocks


def parse_selectors(body: str):
    # matches "0%", "50%", "from", "to" selector blocks with their declarations
    return re.finditer(r"([\d.]+%|from|to)\s*\{([^}]*)\}", body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    args = ap.parse_args()

    with open(args.path, "r") as f:
        css = f.read()

    blocks = list(find_keyframe_blocks(css))
    if not blocks:
        print("No @keyframes blocks found in this file.")
        return

    issues = 0
    for name, body in blocks:
        print(f"--- @keyframes {name} ---")

        selectors_seen = []
        has_start = has_end = False
        layout_props = set()
        animatable_ok = True

        for m in parse_selectors(body):
            sel, decls = m.group(1), m.group(2)
            norm = "0%" if sel == "from" else "100%" if sel == "to" else sel

            if norm in selectors_seen:
                print(f"  [ISSUE] duplicate selector {sel!r} — later one silently wins, earlier rules are dead code")
                issues += 1
            selectors_seen.append(norm)

            if norm == "0%":
                has_start = True
            if norm == "100%":
                has_end = True

            if sel not in ("from", "to"):
                try:
                    pct = float(sel.rstrip("%"))
                    if not (0 <= pct <= 100):
                        print(f"  [ISSUE] selector {sel!r} is out of the valid 0%-100% range")
                        issues += 1
                except ValueError:
                    print(f"  [ISSUE] malformed selector {sel!r}")
                    issues += 1

            for prop_match in re.finditer(r"([\w-]+)\s*:", decls):
                prop = prop_match.group(1).strip().lower()
                if prop in NON_ANIMATABLE:
                    print(f"  [ISSUE] '{prop}' in {sel!r} is not smoothly animatable (discrete property)")
                    issues += 1
                    animatable_ok = False
                if prop in LAYOUT_TRIGGERING:
                    layout_props.add(prop)

        if not has_start:
            print("  [ISSUE] missing a 0%/from starting keyframe")
            issues += 1
        if not has_end:
            print("  [ISSUE] missing a 100%/to ending keyframe")
            issues += 1
        if layout_props:
            print(f"  [PERF NOTE] animates layout-triggering propert{'y' if len(layout_props)==1 else 'ies'}: {sorted(layout_props)} — consider transform/opacity equivalents for smoother animation")
        if animatable_ok and not layout_props:
            print("  OK — animates only compositor-friendly properties")
        print()

    print(f"Total issues found: {issues}")
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
