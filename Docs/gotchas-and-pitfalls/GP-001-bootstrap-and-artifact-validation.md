# GP-001 — Repository Bootstrap and Artifact Link Checks

Date: 2026-11-01. Agent: Codex. Severity: Medium.

## Problem and cause

The authenticated GitHub CLI could create a private repository, but its configured SSH transport lacked a usable key. HTTPS authentication worked, but that OAuth credential lacked workflow scope. The connected GitHub integration had authorized workflow-write access.

Separately, recording a raw writing evaluation introduced a website-relative link into an artifact. A repository-wide Markdown-link validator incorrectly interpreted that example destination as a repository file.

## Resolution

Used the existing GitHub CLI credential helper over HTTPS without exposing tokens. Created the workflow through the connected GitHub integration, fetched that commit, and merged it into the owned bootstrap history before a normal fast-forward push. No token permissions or global Git settings were changed.

Excluded only raw files under evals/results from repository-link interpretation. Authored documentation links to those artifacts and all active-package links remain validated. A regression test proves that an example website link can coexist with detection of a genuinely broken active reference.

## Prevention

Verify capabilities by credential path; repository creation permission does not imply workflow-write permission. Keep raw evidence separate from executable instructions and authored package references. Never claim a bootstrap or intermediate failed CI run is the final validation result.
