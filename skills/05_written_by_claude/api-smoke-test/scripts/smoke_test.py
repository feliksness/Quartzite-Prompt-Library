#!/usr/bin/env python3
"""Read-only REST API smoke test using only the Python standard library.

Usage:
    python3 smoke_test.py https://api.example.com/health https://api.example.com/status \
        --headers "Authorization: Bearer xyz" --method GET --timeout 10
"""
import argparse
import json
import time
import urllib.request
import urllib.error


def parse_header(h: str):
    if ":" not in h:
        return None
    k, v = h.split(":", 1)
    return k.strip(), v.strip()


def check(url: str, method: str, headers: list, timeout: float):
    hdrs = {}
    for h in headers:
        kv = parse_header(h)
        if kv:
            hdrs[kv[0]] = kv[1]

    req = urllib.request.Request(url, method=method, headers=hdrs)
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed_ms = (time.time() - start) * 1000
            body = resp.read()
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            summary = summarize_body(body, content_type)
            return {
                "url": url, "status": status, "ms": round(elapsed_ms, 1),
                "content_type": content_type, "summary": summary, "error": None,
            }
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.time() - start) * 1000
        return {
            "url": url, "status": e.code, "ms": round(elapsed_ms, 1),
            "content_type": e.headers.get("Content-Type", "") if e.headers else "",
            "summary": None, "error": str(e),
        }
    except Exception as e:
        elapsed_ms = (time.time() - start) * 1000
        return {"url": url, "status": None, "ms": round(elapsed_ms, 1), "content_type": None, "summary": None, "error": str(e)}


def summarize_body(body: bytes, content_type: str):
    if "json" not in (content_type or "").lower():
        return f"non-JSON body, {len(body)} bytes"
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "malformed JSON body"
    if isinstance(data, list):
        return f"JSON array, {len(data)} items"
    if isinstance(data, dict):
        keys = list(data.keys())[:10]
        return f"JSON object, top-level keys: {keys}"
    return f"JSON scalar: {data!r}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--method", default="GET", choices=["GET", "HEAD"])
    ap.add_argument("--headers", action="append", default=[])
    ap.add_argument("--timeout", type=float, default=10.0)
    args = ap.parse_args()

    for url in args.urls:
        r = check(url, args.method, args.headers, args.timeout)
        if r["error"] and r["status"] is None:
            print(f"[FAIL]  {url}\n        error: {r['error']}  ({r['ms']}ms)")
            continue
        flag = "OK" if r["status"] and 200 <= r["status"] < 300 else "WARN"
        slow = "  [SLOW]" if r["ms"] > 2000 else ""
        print(f"[{flag}]  {url}")
        print(f"        status={r['status']}  latency={r['ms']}ms{slow}  content-type={r['content_type']}")
        if r["summary"]:
            print(f"        body: {r['summary']}")
        if r["error"]:
            print(f"        note: {r['error']}")
        print()


if __name__ == "__main__":
    main()
