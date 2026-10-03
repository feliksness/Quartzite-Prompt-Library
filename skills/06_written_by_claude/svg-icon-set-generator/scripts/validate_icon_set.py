#!/usr/bin/env python3
"""Validate that a set of SVG icon files share a consistent style
(viewBox, stroke width, linecap/linejoin, currentColor usage).

Usage:
    python3 validate_icon_set.py icons/*.svg
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET


def get_svg_attrs(path):
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        return None, f"not well-formed XML: {e}"
    root = tree.getroot()
    tag = root.tag.split("}")[-1]
    if tag != "svg":
        return None, f"root element is <{tag}>, not <svg>"

    attrs = {"viewBox": root.get("viewBox")}

    stroke_widths = set()
    linecaps = set()
    linejoins = set()
    hardcoded_colors = []

    HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{3,8}$")
    NAMED_COLOR_BLOCKLIST = {"black", "white", "red", "blue", "green", "gray", "grey"}

    for el in root.iter():
        sw = el.get("stroke-width")
        if sw:
            stroke_widths.add(sw)
        lc = el.get("stroke-linecap")
        if lc:
            linecaps.add(lc)
        lj = el.get("stroke-linejoin")
        if lj:
            linejoins.add(lj)
        for prop in ("fill", "stroke"):
            v = el.get(prop)
            if v and v not in ("none", "currentColor") and (HEX_COLOR.match(v) or v.lower() in NAMED_COLOR_BLOCKLIST):
                hardcoded_colors.append((prop, v))

    attrs["stroke_widths"] = stroke_widths
    attrs["linecaps"] = linecaps
    attrs["linejoins"] = linejoins
    attrs["hardcoded_colors"] = hardcoded_colors
    return attrs, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()

    parsed = {}
    for path in args.files:
        attrs, err = get_svg_attrs(path)
        if err:
            print(f"[ERROR] {path}: {err}")
            continue
        parsed[path] = attrs

    if not parsed:
        print("No valid SVG files to compare.")
        sys.exit(1)

    viewboxes = {p: a["viewBox"] for p, a in parsed.items()}
    common_viewbox = max(set(viewboxes.values()), key=list(viewboxes.values()).count)

    issues = 0
    for path, attrs in parsed.items():
        file_issues = []
        if attrs["viewBox"] != common_viewbox:
            file_issues.append(f"viewBox={attrs['viewBox']!r} differs from set's common {common_viewbox!r}")
        if len(attrs["stroke_widths"]) > 1:
            file_issues.append(f"inconsistent stroke-width within this file: {attrs['stroke_widths']}")
        if len(attrs["linecaps"]) > 1:
            file_issues.append(f"inconsistent stroke-linecap within this file: {attrs['linecaps']}")
        if attrs["hardcoded_colors"]:
            colors = ", ".join(f"{p}={v}" for p, v in attrs["hardcoded_colors"])
            file_issues.append(f"hardcoded color(s) instead of currentColor: {colors}")

        if file_issues:
            print(f"[ISSUE] {path}")
            for fi in file_issues:
                print(f"    - {fi}")
            issues += len(file_issues)
        else:
            print(f"[OK] {path}")

    # cross-file stroke-width consistency
    all_widths = set()
    for attrs in parsed.values():
        all_widths |= attrs["stroke_widths"]
    if len(all_widths) > 1:
        print(f"\n[SET-LEVEL ISSUE] stroke-width varies across the set: {all_widths}")
        issues += 1

    print(f"\nTotal issues: {issues}")
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
