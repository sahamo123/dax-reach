# Installation and Compatibility

Dax Reach uses the common Agent Skills folder structure. Review date: 2026-11-01.

## Host selection

`--agent auto` is the default. The installer checks `.claude`/CLAUDE.md, `.codex`, `.cursor`, `.grok`, and Antigravity-oriented `.agent`/GEMINI.md/`.gemini` markers in the project and its repository ancestors. Known Claude/Codex/Cursor session indicators supplement them. Shared `.agents` and AGENTS.md do not identify one host. Markers are heuristics; `--agent` overrides detection. Existing skills or plugins may cause more than one match.

In a terminal, missing host/industry/type inputs prompt automatically. Use `--interactive` to force prompts, or `--non-interactive` with explicit inputs in automation. A missing required input exits without writing. A dry-run prints the destination, customized recommendations, and conflicts; `--json` also includes scanned roots. Explicit inputs plus `--json --non-interactive` produce clean JSON.

Industry is a broad label, not a company name or confidential brief. Matching profiles cover finance, health, property/construction, education, software, and retail; custom industries get a general research workflow. Service vs product changes the journey, schema candidates, workflow order, and measurement suggestions. These are recommendations, not claims that the business holds credentials, serves a location, or delivers a particular result. No module is removed.

## Conflict checks

The scanner reads SKILL.md metadata without executing installed code. It examines known project folders through the nearest repository root and standard user folders for all supported hosts. This conservative cross-host scan prevents copies that compatibility loaders may also discover. It identifies folder names and declared identities, including `daxable-marketing-search` as a legacy migration name.

Same package and same profile at the intended destination are idempotent. A different copy is never overwritten. Duplicate names elsewhere block; known related SEO/design workflows require explicit `--allow-overlap` after deciding ownership. This flag cannot bypass duplicates, unreadable metadata, oversized entries, or symlinks. Unrelated skills stay untouched.

Use `--extra-skill-root /path/to/skills` for custom discovery paths, plugin skill folders, or additional workspace roots. The scan does not parse every host's settings, discover all remote/plugin locations, or prove semantic compatibility. It does not traverse unrelated child projects from the selected workspace. Symlinked scan locations are reported as incomplete rather than followed; review and use a regular project/installation layout. Neither a clean scan nor explicit coexistence certifies arbitrary third-party code.

## Updates and private context

Review changes, back up the current installed package outside the public source checkout, and remove only the copy being replaced. Reinstall with the intended profile. There is no force-overwrite option. Never overwrite AGENTS.md, CLAUDE.md, PRODUCT.md, DESIGN.md, host settings, or internal company skills as part of this operation.

The installed package's local-context/.gitignore excludes its profile in any consumer repository. Git ignores prevent accidental adds, not deliberate force-adds or external uploads. The public pack's installer refuses to install into its own source checkout. Manual installation must copy the complete skill folder, licenses included, and keep private context outside the public repository.

## Primary compatibility references

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code](https://code.claude.com/docs/en/skills)
- [Codex](https://learn.chatgpt.com/docs/customization/overview)
- [Antigravity discovery](https://antigravity.google/docs/customization-discovery): current shared `.agents/skills` layout; legacy variants also scanned.
- [Cursor skills](https://cursor.com/docs/skills): shared/native directories plus Claude/Codex compatibility.
- [Grok Build](https://docs.x.ai/build/features/skills-plugins-marketplaces): `.grok/skills`, Claude compatibility, and user `.agents` discovery.

No host runtime, browser, paid API, or model is installed. Reload the host after installation. Chat interfaces without filesystem skill support can read the entry point and relevant references, but do not gain execution or browsing capabilities from Markdown.
