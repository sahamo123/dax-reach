# CL-001 — Portable Marketing Search — Agent: Codex

Date: 2026-11-01. Plan: [IP-001](../implementation-plans/IP-001-portable-marketing-search.md).

## Summary

Created a separate portable package combining selected Corey Haines marketing and AgriciDaniel SEO workflows with current official Google guidance. The website and existing agent settings are unchanged.

## Changes

| Files | Change |
|---|---|
| skills/daxable-marketing-search | Shared routing, eight workflows, source registry, context/finding templates, licensing, HTML evidence helper |
| upstream and upstream.lock.json | Exact pinned source excerpts, licenses, Git blob and SHA-256 hashes |
| scripts and tests | Dependency-free installer, validator, and meaningful isolation/evidence tests |
| evals | Eight behavioral cases and comparative evaluation protocol |
| .github/workflows | Read-only CI validation with a pinned official checkout action |
| README and Docs | Installation, limitations, plan, attribution, maintenance, verification |

## Issues and resolutions

The local Codex validator rejects the optional Agent Skills compatibility field. Requirements now live in the body, retaining compatibility with that older validator. The package preserves both licenses and clearly separates archived source advice from the active reconciled workflow. Current specific Google Search Console sources resolve an older overview's aggregate-only AI reporting description.

## Accomplished

Eight active workflows, fifteen dated Google references, eleven pinned source/license snapshots, all three installation layouts, eighteen passing unit tests, two passing local validation paths, and three completed independent offline behavioral tasks with raw outputs.

## Next

The private repository is delivered and GitHub CI run 41290296157 passed on implementation commit a2a8269. A full cross-model comparative benchmark and real website outcome measurements remain future evaluation work, not promised results. See [verification](../verification.md).
