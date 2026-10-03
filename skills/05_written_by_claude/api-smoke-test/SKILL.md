---
name: api-smoke-test
description: Run a quick, read-only smoke test against a REST API endpoint — status code, latency, and response shape — using only Python's standard library (no requests/curl dependency assumed). Use whenever the user wants to check "is this API up", verify an endpoint after deployment, or sanity-check a URL before writing integration code against it.
---

# API Smoke Test

## Purpose
Before writing real integration code against an API, or after a deploy, do a fast read-only check: does the endpoint respond, with what status code, how fast, and does the body look like valid JSON with the expected top-level keys.

## When to use
- "Is this endpoint up?" / "check if the API is responding"
- Post-deploy sanity check on a set of endpoints
- Before building a client against an unfamiliar API, to see what a real response looks like

## Do NOT use for
- Load testing or performance benchmarking at scale (use a proper tool like k6/locust)
- Any request that mutates data (POST/PUT/DELETE against production) unless the user explicitly confirms it's safe — default to GET/HEAD only
- Writing or explaining exploit code against an API you don't control

## Workflow

1. Confirm the target is something the user owns or has explicit permission to test — never smoke-test third-party APIs without clear authorization context.

2. Run the check:
   ```bash
   python3 scripts/smoke_test.py https://api.example.com/health https://api.example.com/v1/status
   ```
   Add `--headers "Authorization: Bearer <token>"` if auth is needed. Multiple `--headers` flags are allowed.

3. The script reports, per URL: HTTP status, latency in ms, content-type, and (if JSON) the top-level keys and array length if it's a list.

4. Summarize results plainly: which endpoints are healthy (2xx), which are slow (flag anything over ~2s), and which returned unexpected status codes or malformed JSON.

5. If something looks broken, suggest the next concrete step (check server logs, verify auth token, check DNS) rather than guessing at the root cause.

## Notes
- Uses `urllib` from the standard library only — works in bare environments with no pip installs.
- Defaults to a 10-second timeout per request; won't hang on unresponsive endpoints.
- Only ever issues GET/HEAD unless `--method` is explicitly passed by the user.
