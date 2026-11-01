---
type: "Playbook"
title: "Design and UX"
description: "Apply Impeccable-derived visual assessment and refinement with accessible, crawlable content."
sources: [{"id":"impeccable","resource":"https://github.com/pbakaus/impeccable/tree/4f956490f0056ae1ff5ea80372cf56e83c001d3c"}]
reviewed_on: "2026-11-01"
---

# Design and UX

Adapted and modified from Impeccable's layout, typeset, audit, and polish playbooks (Apache-2.0). Dax Reach removes engine, hook, and forced orchestration requirements, reconciles design with search/content, and preserves scoped authorization. This is an integrated design workflow, not the complete Impeccable runtime or its deterministic detector. Licensing is preserved in [LICENSE.txt](LICENSE.txt).

Identify the exact surface and task: critique, refinement, or redesign. Read available design tokens, shared components, brand/context files, approved copy, and current rendered pages. Refinement keeps the existing identity; a requested redesign can replace it while preserving factual content, essential behavior, and constraints. Do not force a new visual system or require a context document for a small edit.

Choose the visitor mode: deciding and buying, operating a tool, or reading and learning. A marketing page may benefit from a strong visual focal point; a form or article usually needs stable structure and comfortable reading. Explain the intended reading path before changing layout.

Assess the rendered composition first, then inspect implementation evidence. Check what leads, what supports it, which information belongs together, whether repeated cards represent equivalent items, and whether density suits the task. A checker output does not establish visual quality. Record screenshots/viewport and selectors when available; label a source-only review accurately.

Use meaningful grouping, deliberate spacing rhythm, consistent type roles, and the project's existing tokens. Keep prose at a readable measure, contrast strong, and headings distinguishable. Test long headings, font fallback, text zoom, narrow widths, and intermediate layouts. Preserve DOM reading and keyboard order when rearranging the visual composition. Prefer real, relevant assets over decorative UI containers; use verified claims and genuine proof near the decision they support.

For marketing pages, connect a clear offer to benefits, process, proof, comparisons where justified, and a useful CTA. Make different audiences and service/product routes explicit. Keep details on linked pages where appropriate, while retaining enough visible content to understand the offer. Avoid sacrificing usable design for keyword repetition or hiding the sole service explanation in animation.

Fix blocked tasks and accessibility defects before spacing polish. Inspect labels, focus, keyboard navigation, error/success/loading states, contrast, touch behavior, responsive overflow, and visual stability. Use native semantics before ARIA. Distinguish measured accessibility findings from design preferences; do not declare WCAG conformance from one automated score.

Implement within existing components and dependencies. Use [motion](motion.md) only where it explains a relationship or provides useful feedback. Recheck the full visitor path with representative sizes and inputs, inspect console/runtime behavior, and report what remained untested. If upstream Impeccable is already installed, agree which workflow owns the design pass; do not overwrite it or run duplicate hooks.

Output: the visual diagnosis, a concise layout/direction, scoped implementation when requested, and evidence of the final experience. For competing approaches use [decisions](decisions.md); for wording use [copy](copy.md).
