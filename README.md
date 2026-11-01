# Daxable Marketing Search Skills

A portable marketing, content, conversion, SEO, and AI visibility skill. It combines selected workflows from **Corey Haines' Marketing Skills** and **AgriciDaniel's claude-seo**, reconciled with official Google guidance reviewed **November 1, 2026**.

This is a curated derivative with an explicit evidence standard, not a full union of both toolkits. It is independent of and not endorsed by the upstream authors, Google, Anthropic, or OpenAI. Improved organization and portability are engineering goals; better rankings, leads, or model outputs have not been established by a comparative outcome benchmark.

## Included workflows

| Workflow | Delivers |
|---|---|
| Strategy | Audience/offer map, service hierarchy, content priorities |
| Technical SEO | Evidence-backed crawl, index, render, metadata, and experience findings |
| Content | Article briefs, drafts, refreshes, source and quality review |
| Copy | Headlines, benefits, service/landing-page copy, editing |
| Conversion | CTA hierarchy, objections, trust, forms, experiments |
| AI visibility | Platform-specific access, citations, brand accuracy, measurement plan |
| Schema | Fact-matched structured data and explicit validation scope |
| Measurement | Search-to-lead diagnosis and reproducible comparisons |

The [active skill](skills/daxable-marketing-search/SKILL.md) loads only the references needed. No paid API, model-specific orchestration, automatic hooks, telemetry, or runtime package dependencies are required. Optional Python helpers use the standard library.

## Install in a project

Clone this repository using your authorized GitHub access, then run from its root. Python 3.10+ is needed only for the installer and helpers.

```bash
git clone https://github.com/sahamo123/daxable-marketing-search-skills.git
cd daxable-marketing-search-skills

# Inspect the destination without writing anything
python3 scripts/install.py --agent codex --project /absolute/path/to/project

# Install the self-contained package for Codex
python3 scripts/install.py --agent codex --project /absolute/path/to/project --apply

# Or install for Claude Code
python3 scripts/install.py --agent claude --project /absolute/path/to/project --apply

# Or create a portable folder for another agent
python3 scripts/install.py --agent portable --project /absolute/path/to/project --apply
```

| Host | Project destination | Invocation |
|---|---|---|
| Codex | `.agents/skills/daxable-marketing-search/` | `$daxable-marketing-search` or a matching task |
| Claude Code | `.claude/skills/daxable-marketing-search/` | `/daxable-marketing-search` or a matching task |
| Other Agent Skills host | `skills/daxable-marketing-search/` using portable mode | Configure the host to load the folder |
| Chat interface without skill loading | Read/paste SKILL.md plus the relevant reference files | Explicitly provide the context and desired task |

The installer preserves existing AGENTS.md, CLAUDE.md, settings, and skills. A different existing installation causes a refusal rather than an overwrite. For updates, review the diff and back up/remove that package directory explicitly, then reinstall. For uninstall, remove only the installed `daxable-marketing-search` directory.

Manual installation: copy the entire active skill folder, including references and licenses, to the appropriate destination. Do not install the archival upstream directory. If a host caches its skill list, reload its session. A plain LLM can use the instructions but cannot gain browsing or execution tools merely from reading them.

## Examples

```text
Use daxable-marketing-search to review this local homepage for service clarity,
qualified leads, and search visibility. Keep changes local. Preserve offers.
```

```text
Use daxable-marketing-search to write a source-backed article from this brief.
Use our approved facts; mark missing evidence instead of inventing it.
```

```text
Use daxable-marketing-search to diagnose this lead decline from the attached
analytics exports. Separate observations from hypotheses and tracking gaps.
```

## Verification and limits

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 skills/daxable-marketing-search/scripts/inspect_html.py tests/fixtures/example.html
```

Read [verification results](Docs/verification.md) for what actually ran. Installation layout tests are not proof of runtime behavior in every agent. [Behavior cases](evals/README.md) define a repeatable quality comparison without inventing a benchmark score. The offline HTML helper only extracts evidence from a local file; it does not crawl, render JavaScript, or establish rich-result eligibility.

## Sources, maintenance, and licenses

- [Upstream lock](upstream.lock.json): exact source versions and hashes.
- [Merge decisions](skills/daxable-marketing-search/references/merge-decisions.md): retained, changed, and excluded behavior.
- [Google guidance](skills/daxable-marketing-search/references/google-guidance.md): dated rules and a documented reporting conflict.
- [Maintenance](Docs/maintenance.md): review updates without automatically importing upstream instructions.
- [Attribution](skills/daxable-marketing-search/NOTICE.md): original authors and licenses, included in every installation.

Original additions and MIT-derived workflows are MIT licensed. Google-derived documentation notes retain CC BY 4.0 attribution. Upstream MIT notices are preserved verbatim. Repository visibility is private initially; access is managed through GitHub, not by the license.
