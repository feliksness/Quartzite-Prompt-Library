---
name: api-rate-limit-designer
description: Design and validate a rate-limiting scheme (limits, windows, burst allowance, and headers) for a REST API, checking the numbers actually add up (burst never exceeds the window budget, tiers stay consistent) rather than picking round numbers by feel. Use whenever the user is adding rate limiting to an API, choosing limits for a paid-tier system, or debugging why clients are getting rate-limited unexpectedly.
---

# API Rate Limit Designer

## Purpose
Rate limit numbers interact in ways that are easy to get subtly wrong: a "burst" allowance bigger than the window budget makes the window limit meaningless; tiers that don't scale monotonically create paradoxes (a "pro" tier stricter than "free" on some dimension); and returning the wrong headers breaks well-behaved clients that back off correctly. This skill checks the actual arithmetic before the scheme ships.

## When to use
- User is adding rate limiting to an API for the first time and wants sane numbers.
- User has an existing scheme and something's misbehaving (clients getting limited too early/late).
- User is designing a multi-tier (free/pro/enterprise) limit structure.

## Workflow

1. Gather the inputs: requests-per-window for each tier, window length, burst/concurrency allowance, and which algorithm (fixed window, sliding window, token bucket, leaky bucket).

2. Validate the numbers:
   ```bash
   python3 scripts/validate_limits.py --tiers "free:60:60,pro:600:60,enterprise:6000:60" --burst 20
   ```
   Format per tier is `name:requests:window_seconds`. The script checks:
   - burst allowance doesn't exceed any tier's per-window budget (a burst bigger than the window limit means the "limit" never actually triggers)
   - tiers are monotonically increasing (a higher tier is never stricter than a lower one)
   - the requests-per-second implied by each tier is reported, so tier gaps make sense relative to each other

3. Recommend the standard response headers so well-behaved clients can self-throttle: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (or `Retry-After` on a 429).

4. Recommend the algorithm based on the use case:
   - **Token bucket**: best default — allows bursts while enforcing an average rate.
   - **Fixed window**: simplest to implement, but allows a 2x burst at window boundaries (client can send full quota at 11:59:59 and again at 12:00:00).
   - **Sliding window log/counter**: smooths the boundary problem, more accurate, more storage/compute cost.

5. Always return `429 Too Many Requests` with a `Retry-After` header, not a silent drop or a generic 4xx/5xx — this is what lets clients back off correctly instead of hammering the API.

## Notes
- Per-IP limiting alone under-protects behind shared NAT/corporate proxies and over-protects legitimate high-volume single users; prefer per-API-key/per-account limiting with a separate, more generous per-IP ceiling as a secondary guard.
- Don't silently vary limits by undocumented internal logic (e.g., different limits for "suspicious" traffic) without telling the user that's part of the design — that makes debugging client complaints much harder later.
