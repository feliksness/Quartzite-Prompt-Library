---
name: regex-builder
description: Build and verify a regular expression against real sample strings before handing it to the user, instead of guessing a pattern from memory. Use whenever the user asks for a regex, wants to validate/extract/replace text with a pattern, or reports that "my regex isn't matching."
---

# Regex Builder & Verifier

## Purpose
Regexes are easy to get subtly wrong (anchors, greedy vs lazy, escaping). This skill forces every proposed pattern through an actual test run against sample strings — both strings that should match and strings that shouldn't — before it's presented as the answer.

## When to use
- User asks "write a regex that matches X".
- User has a broken regex and wants it fixed.
- User wants to extract/replace substrings by pattern.

## Workflow

1. **Gather examples.** If the user hasn't given sample strings, ask for or infer 2-3 positive examples (should match) and 1-2 negative examples (should NOT match) — edge cases matter more than the happy path.

2. **Draft the pattern**, choosing the right flavor (Python `re`, JavaScript, PCRE, POSIX) based on where the user will use it.

3. **Verify it**, don't just eyeball it:
   ```bash
   python3 scripts/test_regex.py --pattern '<pattern>' --flags i --match "foo123" "foo456" --no-match "bar" "foo"
   ```
   The script reports PASS/FAIL per example plus, for matches, the captured groups.

4. **Iterate** until every positive example matches (with correct groups) and every negative example does not. Don't present a pattern that failed verification.

5. **Explain briefly** what the pattern does in plain English (anchors, quantifiers, groups) — not a character-by-character breakdown unless asked.

## Notes
- Python's `re` module differs from JS/PCRE in a few ways (e.g. lookbehind support, named group syntax `(?P<name>...)` vs `(?<name>...)`) — the script defaults to Python syntax; mention the syntax difference if the target language differs.
- For catastrophic backtracking risk (nested quantifiers like `(a+)+`), flag it and prefer a possessive/atomic-safe rewrite rather than shipping a pattern that could hang.
