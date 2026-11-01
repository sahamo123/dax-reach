# Open Knowledge Format

Dax Reach uses two complementary file interfaces:

- `skills/dax-reach/SKILL.md`: Agent Skills entry point for task routing and execution guidance.
- `skills/dax-reach/references/`: OKF v0.2 knowledge bundle for browsing and consuming the same concepts as portable knowledge.

The reference files retain their existing paths. Each concept has typed YAML frontmatter, a title/description, and provenance where applicable. The root index declares the version and lists concepts; the log uses dated entries. No second knowledge copy, server, SDK, or database is introduced. LICENSE.txt carries the notices needed to redistribute the reference bundle.

For maintainability without a YAML dependency, authored frontmatter uses one key per line with JSON values (a YAML-compatible subset). The local validator checks this authored convention, type fields, source resources, links, index, and log. It is not a universal OKF consumer or an official Google certification tool. No human verification or attestation event is fabricated. Review dates mean the recorded package review, not perpetual currency.

The primary [Google Cloud specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) was reviewed on 2026-11-01 at version 0.2. The [Google Cloud announcement](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) describes the initial v0.1 release. The current specification governs this implementation. No Google implementation code was copied.

OKF carries knowledge; it does not grant search indexing, rankings, citations, model capabilities, or permission to publish private context. Consumer-specific knowledge belongs in the consumer's private workspace, not this reusable library.
