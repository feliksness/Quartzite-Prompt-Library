---
name: changelog-generator
description: Generate a clean, categorized CHANGELOG.md from git commit history. Use this whenever the user asks to "generate a changelog", "summarize commits since last release", "write release notes", or wants commits grouped into Added/Fixed/Changed sections for a repo.
---

# Changelog Generator

## Purpose
Turn raw `git log` output into a categorized, human-readable changelog (Keep a Changelog style), grouped under headings like Added, Changed, Fixed, Removed, and Docs.

## When to use
- User wants release notes for a tag range or date range.
- User wants a CHANGELOG.md file generated or updated.
- User wants a summary of recent commits grouped by type.

## Workflow

1. **Identify the range.** Ask (or infer) the git ref range, e.g. `v1.2.0..HEAD` or `--since="2 weeks ago"`. Default to the last tag to HEAD if the user doesn't specify.

2. **Extract commits.** Run the bundled script:
   ```bash
   python3 scripts/extract_commits.py --range "v1.2.0..HEAD" --repo /path/to/repo
   ```
   This prints one JSON object per commit: `{hash, author, date, subject, body}`.

3. **Categorize.** Bucket each commit by its Conventional Commit prefix if present (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `perf:`, `test:`, `BREAKING CHANGE`). If the repo doesn't use Conventional Commits, categorize by reading the subject line's intent (adds a feature → Added, fixes a bug → Fixed, etc.).

4. **Write the changelog.** Produce Markdown with this structure, newest release on top:
   ```markdown
   ## [Unreleased]
   ### Added
   - ...
   ### Fixed
   - ...
   ### Changed
   - ...
   ```
   Squash duplicate/trivial commits (typo fixes, merge commits, "wip") rather than listing every one — a changelog is for humans, not a raw git log dump.

5. **Save or print.** If the user has an existing `CHANGELOG.md`, prepend the new section above the previous top entry rather than overwriting the whole file.

## Notes
- Never fabricate commit messages — only summarize what `git log` actually returned.
- If the repo has no tags, fall back to `--since` date ranges.
- Keep each bullet to one line; link commit hashes if the user gives a remote URL format (e.g. GitHub `/commit/<hash>`).
