---
type: "Playbook"
title: "Evidence-Led Decisions"
description: "Choose scoped actions through explicit alternatives, evidence, consequences, and verification."
sources: [{"id":"madr","resource":"https://github.com/adr/madr/blob/ba75bb1b20d42af5746b246ad348c202419ae681/template/adr-template.md"}]
reviewed_on: "2026-11-01"
---

# Evidence-Led Decisions

Adapted from Markdown Architectural Decision Records (MADR), using its MIT license. Dax Reach applies it to design, marketing, and search decisions and adds evidence, reversibility, and measurement. This is a decision framework usable by any capable model, not an extra model, autonomous agent service, or guarantee of better judgment.

For a consequential choice, state the concrete problem and decision boundary. List established constraints and desired outcomes. Compare plausible alternatives, including keeping the current implementation when that is reasonable. For each, note the evidence, expected visitor benefit, effort, dependencies, risks, and uncertainty. Do not manufacture numerical confidence or estimates to populate a table.

Reject options that break access controls, accessibility, truthful claims, or the user's publication boundary. Prioritize demonstrated failures that block people or discovery, then high-confidence improvements, then experiments and polish. Separate measured facts from recommendations. If options cannot be distinguished with available evidence, choose the smallest reversible test and define what result would change the choice.

Record only what the decision needs:

- Problem and scope.
- Drivers and evidence, with date/source when material.
- Alternatives and their trade-offs.
- Chosen action and rationale.
- Consequences and unresolved uncertainty.
- Verification, success measure, and revisit/rollback trigger.

Use this record for substantive trade-offs; a typo fix does not need a formal decision document. Keep private business evidence inside the consumer project. Do not publish decision logs as a side effect. For observed outcomes use [measurement](measurement.md).
