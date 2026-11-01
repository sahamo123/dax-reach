# DaxReach AI Visibility Pack

**Dax Reach** is a portable pack for **design, marketing, copy, content, conversion, SEO, GEO, and AEO**. It combines selected licensed workflows from Corey Haines' Marketing Skills, AgriciDaniel's claude-seo, and Impeccable, reconciles search guidance with Google's official documentation, and uses MADR for consequential decisions.

One entry point loads only the references a task needs. The knowledge library also uses **Google Cloud's Open Knowledge Format (OKF) v0.2**. No model, paid subscription, runtime dependency, or background service is required. Optional Python helpers use Python 3.10+ and the standard library.

This is the reusable public package. Company-specific internal skills, project rules, business facts, customer data, and credentials stay in their private projects. The installer never copies them into this repository. Public license and author attribution is retained.

## What is included

| Module | Outcome |
|---|---|
| Design and motion | Impeccable-derived hierarchy, typography, responsive UX, accessible animation, and polish |
| Strategy and conversion | Audience/offer architecture, CTAs, proof, forms, and experiments |
| Copy and content | Headlines, landing pages, article briefs, complete drafts, and refreshes |
| Technical SEO and schema | Crawl/render/index evidence, metadata, internal links, and fact-matched structured data |
| GEO / AEO / AI visibility | Clear answers, accurate entities, engine-specific access, citations, and repeatable measurement |
| Backlinks | Offline CSV analysis and saved-HTML verification; optional DataForSEO summary/link queries |
| Free tools | Guidance for Search Console exports, Lychee, and SEOnaut; costs and limits distinguished |
| Decisions | MADR-derived alternatives, evidence, consequences, reversible tests, and revisit criteria |

[Start with the skill](skills/dax-reach/SKILL.md) or browse the [OKF knowledge index](skills/dax-reach/references/index.md). Impeccable's full engine, detector binary, hooks, and command suite are not bundled. Its selected design workflows are adapted into this pack with attribution.

## Install

```bash
git clone https://github.com/sahamo123/dax-reach.git
cd dax-reach

# Detect the host, ask for broad industry and service/product type; dry-run
python3 scripts/install.py --project /absolute/path/to/your-project

# Explicit, reproducible installation
python3 scripts/install.py --project /absolute/path/to/your-project \
  --agent codex --industry "Software" --business-type product --apply
```

| Host | Project destination | Invocation after reloading the host |
|---|---|---|
| Codex | `.agents/skills/dax-reach/` | `$dax-reach` |
| Claude Code | `.claude/skills/dax-reach/` | `/dax-reach` |
| Google Antigravity | `.agents/skills/dax-reach/` | Select/invoke Dax Reach in the host |
| Cursor | `.cursor/skills/dax-reach/` | `/dax-reach` |
| Grok Build | `.grok/skills/dax-reach/` | `/dax-reach` |
| Other hosts | `skills/dax-reach/` via `--agent portable` | Configure the host or provide SKILL.md and relevant references |

Choose the **host**, not the underlying model: Grok running inside Cursor uses the Cursor destination. Detection uses project markers and a few session indicators; ambiguous/unknown environments require a selection. Noninteractive installs accept explicit flags. See [installation details](Docs/installation.md).

The installer scans standard project, ancestor, and user skill folders, plus optional `--extra-skill-root` paths. Duplicate/legacy identities and incomplete scans block installation. Related workflows such as Impeccable or copywriting are reported separately; `--allow-overlap` acknowledges coexistence without bypassing duplicate protection. Existing settings and divergent installed copies are never overwritten.

Your broad industry and business type generate a local `local-context/profile.json` inside the installed skill. That directory contains its own Git exclusion. Do not put secrets in the labels or force-add private context. The source pack cannot be installed into itself and refuses source files flagged as private/sensitive. For updates, review and back up the installed copy, then explicitly remove only that copy before reinstalling.

## Use

```text
Use Dax Reach to refresh this homepage's hierarchy and motion while preserving
its approved content, accessibility, working forms, and publication boundary.
```

```text
Use Dax Reach to create a source-backed product comparison and article brief.
Distinguish verified features from claims still needing evidence.
```

```text
Use Dax Reach to analyze this supplied backlink export and recommend the next
three actions. Explain coverage limits and the evidence for each decision.
```

See [backlink and DataForSEO usage](Docs/backlinks-and-dataforseo.md). DataForSEO is optional and paid: credentials are read from local environment variables, never passed as CLI arguments or committed. The adapter makes no network request unless `--execute-paid` is explicitly supplied. Tests use mocked responses and no paid account.

## Verify and maintain

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/check_public.py --history
```

Read [verification](Docs/verification.md), [public/private separation](Docs/public-release.md), [OKF format notes](Docs/knowledge-format.md), and [maintenance](Docs/maintenance.md). Source snapshots are pinned and hash-checked in [upstream.lock.json](upstream.lock.json). Historical evaluation records retain the original name so the evidence is not rewritten as a test of the new version.

The pack improves packaging, workflow coverage, evidence handling, and installation safeguards. Better rankings, citations, conversions, or model output quality require actual comparative measurement; no superiority benchmark is claimed. Native host execution is distinct from installer testing.

## License and credit

Original additions and MIT-derived workflows use MIT. Impeccable-derived design/motion uses Apache-2.0. Google-derived documentation notes use CC BY 4.0 where applicable. Preserve the [full notices and licenses](skills/dax-reach/NOTICE.md). The project is independent and is not endorsed by Google, upstream authors, or model/tool providers.
