# Coding, Finance, Banking & Crypto Skills Pack — 171 Skills

A collection of "Agent Skills" (folders with a `SKILL.md` and often bundled
scripts) — pulled from real public GitHub repositories, plus 5 original ones
written and tested from scratch. Every folder is self-contained and usable
as-is with Claude Code, the Claude API skills feature, or any other
Agent-Skills-compatible tool.

## Folder structure

| Folder | # Skills | Minimum requested |
|---|---|---|
| `01_coding_main/` | **60** | 50 |
| `02_finance/` | **46** | 10 |
| `03_banking/` | **27** | 10 |
| `04_crypto/` | **32** | 10 |
| `05_written_by_claude/` | **5** | — (original, bonus) |

**Total: 171 skill folders.**

---

## `01_coding_main/` (60 skills)
Sources:
- **[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)** — `engineering/skills/*` (37): `agent-designer`, `api-design-reviewer`, `api-test-suite-builder`, `browser-automation`, `changelog-generator`, `chaos-engineering`, `ci-cd-pipeline-builder`, `codebase-onboarding`, `database-designer`, `database-schema-designer`, `dependency-auditor`, `env-secrets-manager`, `feature-flags-architect`, `focused-fix`, `full-page-screenshot`, `git-worktree-manager`, `interview-system-designer`, `kubernetes-operator`, `mcp-server-builder`, `migration-architect`, `monorepo-navigator`, `observability-designer`, `performance-profiler`, `pr-review-expert`, `rag-architect`, `runbook-generator`, `secrets-vault-manager`, `self-eval`, `ship-gate`, `skill-security-auditor`, `skill-tester`, `slo-architect`, `spec-driven-workflow`, `sql-database-assistant`, `tc-tracker`, `tech-debt-tracker`, `agent-workflow-designer`.
- **[obra/superpowers](https://github.com/obra/superpowers)** (14): TDD, systematic-debugging, code review, git worktrees, brainstorming, writing/executing plans, subagent-driven development, verification-before-completion, etc.
- **[anthropics/skills](https://github.com/anthropics/skills)** (4): `mcp-builder`, `webapp-testing`, `claude-api`, `skill-creator`.
- **[sanjay3290/ai-skills](https://github.com/sanjay3290/ai-skills)** (5, bonus): `mysql`, `postgres`, `mssql`, `azure-devops`, `jules`.

## `02_finance/` (46 skills)
Sources:
- **[JoelLewis/finance_skills](https://github.com/JoelLewis/finance_skills)** (27): asset allocation, portfolio management systems, equities, fixed income (corporate/municipal/sovereign/structured), currencies & FX, commodities, alternatives, rebalancing, performance attribution/metrics/reporting, tax-loss harvesting, tax efficiency, retirement decumulation, financial planning (workflow + integration), investment policy, investment suitability, diversification, factor investing, time value of money, statistics fundamentals, quantitative/qualitative valuation.
- **[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)** (12): `finance-skills`, `financial-analyst`, `saas-metrics-coach`, `business-investment-advisor`, plus the full `commercial/` suite (`channel-economics`, `commercial-forecaster`, `commercial-policy`, `commercial-skills`, `deal-desk`, `partnerships-architect`, `pricing-strategist`, `rfp-responder`).
- **[agiprolabs/claude-trading-skills](https://github.com/agiprolabs/claude-trading-skills)** (7 quant): `options-pricing`, `risk-management`, `kelly-criterion`, `volatility-modeling`, `market-microstructure-traditional`, `position-sizing`, `portfolio-analytics`.

## `03_banking/` (27 skills)
Sources:
- **[JoelLewis/finance_skills](https://github.com/JoelLewis/finance_skills)** (17, banking operations): `account-opening-compliance`, `account-opening-workflow`, `account-transfers`, `account-maintenance`, `anti-money-laundering`, `know-your-customer`, `lending`, `margin-operations`, `settlement-clearing`, `reconciliation`, `counterparty-risk`, `operational-risk`, `client-onboarding`, `trade-execution`, `order-management-advisor`, `examination-readiness`, `books-and-records`.
- **[G-P-S/claude-knowledge-work-plugins](https://github.com/G-P-S/claude-knowledge-work-plugins)** (8): `journal-entry`, `close-management`, `sox-testing`, `audit-support`, `variance-analysis`, `journal-entry-prep`, `financial-statements`, `gl-reconciliation`.
- **[openaccountant/skills](https://github.com/openaccountant/skills)** (1): `bank-sync`.
- **[singularityhacker/bank-skills](https://github.com/singularityhacker/bank-skills)** (1): `wise-bank-account-agent` — a real bank-account API skill (balances, international transfers, receive details) via Wise.

## `04_crypto/` (32 skills)
Sources:
- **[agiprolabs/claude-trading-skills](https://github.com/agiprolabs/claude-trading-skills)** (30): on-chain analysis (`wallet-profiling`, `whale-tracking`, `sybil-detection`, `mev-analysis`), Solana infra (`solana-rpc`, `solana-tx-building`, `jito-bundles`, `yellowstone-grpc`, `shredstream`, `pumpfun-mechanics`, `raptor-dex`), DEX/data APIs (`dex-execution`, `dex-pool-analysis`, `dexscreener-api`, `defillama-api`, `helius-api`, `birdeye-api`, `coingecko-api`, `solanatracker-api`), DeFi math (`impermanent-loss`, `lp-math`, `yield-analysis`, `token-economics`, `copy-trading`), and tax/accounting (`crypto-tax-export`, `cost-basis-engine`, `tax-liability-tracking`, `wash-sale-detection`, `trade-accounting`, `regulatory-reporting`).
- **[quiknode-labs/blockchain-skills](https://github.com/quiknode-labs/blockchain-skills)** (1): `quicknode-blockchain-api`.
- **[JoelLewis/finance_skills](https://github.com/JoelLewis/finance_skills)** (1): `digital-assets`.

## `05_written_by_claude/` (5 original skills, each with a tested Python script)
- **`sql-migration-safety-checker`** — flags production-breaking migration patterns (DROP without backup, `NOT NULL` with no `DEFAULT`, renames, non-concurrent index creation). Tested against a deliberately hazardous migration file; caught all 4 planted issues correctly.
- **`api-rate-limit-designer`** — validates a multi-tier rate-limit scheme's internal arithmetic (burst vs. window budget, tier monotonicity). Tested against both a consistent and a deliberately broken tier scheme.
- **`financial-ratio-calculator`** — computes 13 standard financial ratios from whatever balance-sheet/income-statement figures are given, explicitly listing any ratio it can't compute rather than guessing. Verified against a full test figure set.
- **`crypto-address-validator`** — real Base58Check / Bech32 / Bech32m / EIP-55-format checksum validation for Bitcoin, Ethereum, and Solana addresses (pure Python, no external libraries). Tested against a real historic Bitcoin address, a deliberately typo'd version of it (correctly rejected), a real Bech32 test vector, and a real Ethereum address.
- **`loan-amortization-calculator`** — generates a full period-by-period amortization schedule and computes total interest from the real schedule (not an estimate), including the effect of extra principal payments. Tested on a 30-year mortgage scenario with and without extra payments.

All five scripts were actually executed against real test inputs while building
this pack. The migration checker, rate-limit validator, and address validator
in particular were tested against intentionally broken/malicious-pattern inputs
to confirm they catch real problems, not just well-formed happy-path cases.

---

## How to use these

- **Claude Code / Claude.ai (paid plans with code execution):** drop a skill folder into
  `~/.claude/skills/<skill-name>/` (personal) or your project's `.claude/skills/` folder,
  or upload it as a custom skill in Claude.ai settings.
- **Claude API:** use the Skills API to upload a skill folder.
- **Any other Agent-Skills-compatible tool** (Cursor, OpenAI Codex, Gemini CLI, etc.):
  most read the same `SKILL.md` + folder convention directly.

## Important notes

- **Finance/banking/crypto skills are informational, not advice.** Every finance-
  and crypto-related skill in this pack (upstream and original) is meant to help
  analyze, calculate, or explain — not to make investment, trading, or legal/
  compliance decisions on anyone's behalf. Several upstream repos state this
  explicitly (e.g. `finance_skills`' disclaimer that nothing in it constitutes
  financial, legal, tax, or investment advice); treat that as true of the whole
  finance/banking/crypto portion of this pack.
- **Crypto address/wallet skills never guess.** The address validator and the
  on-chain analysis skills are for verification and analysis; none of them
  should be used to auto-generate or "correct" a real address someone will send
  funds to — always re-verify against the original source.
- Folders in `01`–`04` are copied verbatim from their source repos at the commit
  fetched on 2026-07-22 — nothing altered.
- Licenses vary by upstream repo (mostly MIT; check each repo's own LICENSE file
  if redistributing further).
