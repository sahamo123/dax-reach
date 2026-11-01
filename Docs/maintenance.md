# Maintenance

1. Review the current upstream default-branch commits and source diffs. Keep the existing pinned snapshots until the new version has been evaluated; never automatically merge remote instructions.
2. Re-open relevant official Google sources and the update log. Record the actual review date and changes in the source registry. A successful HTTP response alone does not count as a substantive review.
3. Resolve conflicts explicitly in merge-decisions.md. Distinguish documented policy, implementation advice, local convention, and hypotheses. Verify provider-specific AI behavior against that provider's current documentation.
4. If replacing a source snapshot, update its commit URL, Git blob hash and SHA-256. Preserve licenses and any attribution embedded in the source. Update the active workflow only where the change improves a supported task.
5. Run package validation, unit tests, and the affected behavior cases. Log model, tools, source versions, raw output, reviewer, and limitations. Update verification.md and the changelog.
6. Deliver through a reviewed branch/PR for existing releases. Do not turn a source update into authorization to deploy websites, send outreach, change budgets, or alter account controls.
7. Preserve the separation from company-internal skills. Run the public/history guard and review [public-release boundaries](public-release.md) before publishing. Update third-party licenses when adding sources; Impeccable-derived files remain Apache-2.0.

No automatic update or publication job is installed. A 90-day freshness warning is a maintenance prompt, not proof that advice became invalid on day 91. Recheck volatile claims at the point of use.

## Compatibility sources

- Agent Skills structure: https://agentskills.io/specification
- Claude Code skills: https://code.claude.com/docs/en/skills
- Codex project skills: https://learn.chatgpt.com/docs/customization/overview
- [Current host paths and conflict scope](installation.md)
- [OKF knowledge layout](knowledge-format.md)
- [Optional paid adapter and offline backlinks](backlinks-and-dataforseo.md)

The package uses only common frontmatter in SKILL.md. Optional agents/openai.yaml provides Codex UI metadata. Other hosts can ignore it. Do not claim that every model has passed behavior testing merely because it reads Markdown.
