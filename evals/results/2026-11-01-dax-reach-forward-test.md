# Local homepage proposal — warehouse inventory software

Prepared 2026-11-01. Scope: copy, layout direction, motion specification, and analysis of the supplied CSV. No current page, logo asset, implementation, product demonstration, analytics, or live link evidence was supplied. This is a proposed direction, not an observed site audit.

**Recommend a clear, static-first homepage explaining CSV import → stock levels → report export, with one short animation showing records passing through the existing logo.** Do the free local CSV analysis now. Defer hook installation and paid scans. Add FAQs when actual buyer questions identify something the core page does not answer.

The only established product facts are user-provided: imports CSV stock records, displays stock levels, and exports reports. The proposed audience is warehouse software buyers. “Accurate inventory reports” is a desired outcome, not a verified product capability. Do not claim automatic correction, reconciliation, real-time tracking, guaranteed accuracy, integrations, supported export formats, or stockout prevention. Substantiate any accuracy claim with product behavior, documented limitations, and comparisons between known input records and displayed/exported results before using it.

## What to do next

| Option | Visitor benefit and evidence | Effort/dependencies and uncertainty | Decision |
|---|---|---|---|
| Clarify headline, three capabilities, and one CTA | Explains the verified offer directly. No evidence yet that the existing page has a specific defect. | Small reversible content/layout proposal; use current brand tokens and inspect the actual page before implementation. | First homepage change. |
| Add the requested logo-flow animation | May help visitors connect input, product, and outputs. This is a comprehension hypothesis. | Modest implementation and accessibility/performance checks; needs the approved logo. | Add after the static layout works. |
| Expand FAQs first | Useful if visitors have unanswered purchase questions. No such evidence was supplied. | Needs support/sales questions and confirmed answers; generic questions would repeat the three capabilities. | Defer expansion. Keep essential explanations visible in the page. |
| Install Impeccable hooks | No demonstrated visitor benefit from installation itself. Dax Reach already supplies adapted design guidance. | Changes developer tooling and may duplicate an existing workflow. This pack is not the complete Impeccable runtime. | Not required. Do not install hooks for this proposal. |
| Run paid backlink scans today | Could later answer a defined discovery question. The three supplied rows do not demonstrate that discovery is the current bottleneck. | Requires a defined scope, approved spend/access, current provider terms, and a decision the data would change. | Defer. Use the free offline result below first. |

Keeping the current implementation is a valid baseline until it can be inspected. Prepare the replacement locally; do not infer that a redesign will increase conversions. If the existing page already explains the workflow well, retain its strengths and test only the focal illustration.

After local implementation, show the static and animated versions to representative buyers. Ask what can be imported, what they can view, and what can be exported. Record misunderstandings and whether they can find the next step; do not declare statistical superiority from a few sessions. Preserve the static version if motion distracts, obscures content, or fails accessibility/performance checks. Review FAQs when real objections emerge. Revisit paid data only when a specific link-discovery question would change a marketing action.

## Ready-to-use homepage copy

Use the approved product name and logo in the site header. The primary CTA below links to a real section of this proposed page; it makes no unverified promise of a demo, account, or free trial.

**Eyebrow**
Warehouse inventory software

**H1**
From CSV stock records to inventory reports.

**Supporting text**
Import your warehouse stock records, view stock levels, and export reports.

**Primary CTA**
See the workflow → `#workflow`

**Illustration caption**
CSV import → stock levels → report export

**Small illustration label**
Illustrative workflow

**Section heading** (`id="workflow"`)
Import records. View stock. Export reports.

**1. Import your stock records**
Bring CSV stock records into the software.

**2. View stock levels**
See stock levels in the product.

**3. Export reports**
Export inventory reports from the software.

**Closing heading**
Your stock records, with a clear next step.

**Closing text**
Start with a CSV import. View stock levels. Export the reports you need.

**Closing CTA**
Review the workflow → `#workflow`

This is a product-explanation draft. When an existing approved sales destination is available, use a corresponding sales CTA such as “Request a demo” only if that action actually exists. Do not ship a dead button or imply a trial, pricing, or booking process that has not been confirmed.

Two headline alternatives considered: “Import stock records. View levels. Export reports.” is more literal but less fluid; “Keep warehouse stock in view.” emphasizes stock visibility but omits the CSV/report mechanism. The selected headline connects the starting material with a verified output. No testimonials or numerical proof are invented. A real product screenshot can replace the illustration’s sample panels after it is checked for accuracy.

## Layout and visual direction

Reading path: audience → plain-language offer → next action → visual workflow → three capability explanations. On wide screens, place the hero copy and CTA beside the illustration. On narrow screens, put copy and CTA first, then the illustration, then the workflow section. Keep the DOM and keyboard order consistent with that sequence.

Retain current brand colors, type, and logo. Use one brand accent for the moving records and connector; neutral surfaces and strong text contrast keep the offer dominant. Keep body copy to a comfortable measure, use distinct heading sizes, and provide generous spacing around the CTA. Do not add decorative dashboards, invented metrics, or unrelated feature cards. No chosen color combination is asserted to meet contrast requirements until measured.

The animation region has three stationary stations: **CSV stock records**, the existing logo with the product name, and **Stock levels / Export reports**. The final station has two simple labeled rows, not a fabricated screenshot. Keep the caption outside the animated artwork. At a narrow breakpoint, stack the stations vertically. Reserve the region’s dimensions from first paint so it does not move surrounding content.

## Implementable animation storyboard

**Purpose:** show a conceptual relationship between imported stock records, the product, and its two known outputs. The logo is a visual waypoint, not evidence of an accuracy check or automatic repair. No quantities change and no “verified,” “synced,” or “accurate” status appears.

Use existing CSS and the Web Animations API; no new runtime or Impeccable hooks are necessary. Put the decoration in a scoped component, for example `InventoryFlow`. Essential labels, copy, links, and the complete static flow are present in server-rendered HTML before JavaScript executes.

| Time from start | Visual behavior | Implementation detail |
|---|---|---|
| Before trigger | All three stations, connectors, and output labels are visible. Three small record marks sit beside the CSV station. | The base HTML/CSS is the complete static explanation. Mark decorative duplicates `aria-hidden="true"`; the visible text caption communicates the same relationship. |
| 0–800 ms | Three decorative stock-record marks travel toward the logo, staggered by 120 ms. | Each travels for 560 ms. Animate transform and opacity only; ease with `cubic-bezier(.2,.7,.2,1)`. Fade each out over its last 100 ms as it reaches the logo. |
| 500–950 ms | The logo gives one restrained acknowledgment as the records arrive. | Scale from 1 to 1.025 and back to 1 across 450 ms. No flash, bright halo, checkmark, or error-to-success transformation. |
| 850–1450 ms | One accent trace moves from the logo toward the output station. | Overlay the already visible connector and reveal with `scaleX(0→1)` using a left transform origin; use `scaleY` and top origin for the stacked layout. Do not animate its layout dimensions. |
| 1350–1800 ms | A thin accent outline appears around the two output labels. | Animate the opacity of a positioned border overlay. Keep all output text visible throughout. |
| 1800–2400 ms | Accent overlays settle into the static end state. | Fade the temporary emphasis; remove transient transforms and animation objects. Keep the same readable stations and connectors. |
| After 2400 ms | The illustration remains still. | No automatic loop. A native “Replay animation” button can explicitly restart the sequence. |

**Trigger and state model.** Use `idle → playing → complete`, with a separate reduced-motion state. Trigger at most once per component mount when at least 50% of the illustration enters the viewport, the document is visible, and reduced motion is not requested. If IntersectionObserver or animation APIs are unavailable, keep the static composition. Partial, fast, or reverse scroll must never scrub, rewind, trap scrolling, or hide the explanation.

**Coordinates.** Measure the three stationary element centers once immediately before playback. Animate positioned decorative marks within the illustration from the CSV center to the logo center. Use the measured offsets for transform keyframes; do not read layout inside every animation frame. A media query controls horizontal versus stacked arrangement. Use relative dimensions, not fixed desktop page coordinates.

**Controls and interruption.** Expose a native “Skip animation” button during playback and “Replay animation” afterward, using the same button element to retain focus. Skip, tab hidden, component unmount, leaving the viewport, or a layout-changing resize cancels active animations. For skip, hidden tab, viewport exit, and resize, commit the final static state and mark the automatic run complete; returning to the viewport never restarts it. An explicit replay measures fresh positions and starts from the beginning. Guard against repeated activation starting overlapping sequences. Do not change keyboard focus or announce decorative updates through a live region.

**Reduced motion.** With `prefers-reduced-motion: reduce`, render the complete static composition immediately: no spatial travel, logo scaling, tracing, or autoplay. Remove the animation-only control. Listen for preference changes; if reduction is enabled mid-sequence, cancel and show the static state immediately. If it is later disabled, leave the diagram still and offer explicit replay. The visitor never needs motion to understand the product.

**Performance and cleanup.** Reserve stage dimensions; prefer transform/opacity; avoid parallax, particles, animated filters, and permanent broad `will-change`. Disconnect observers and remove preference/visibility listeners on unmount; cancel every animation handle. Keep the implementation local to this component.

**Acceptance checks for implementation, not checks claimed completed here:** initial render with JavaScript disabled; keyboard reachability and visible focus; reduced motion before and during playback; skip/replay and repeated activation; touch; narrow, intermediate, and wide layouts; font fallback, text zoom, long product names, resize, and overflow; initial partial scroll, fast/reverse scroll, viewport exit, and hidden tabs. Verify actual contrast and inspect runtime errors. Measure animation timing and layout stability in a browser on representative devices before describing it as smooth or performant. If any essential content becomes unreadable or inaccessible, use the static version while fixing it.

## Free CSV result

The bundled offline helper processed the three user-provided source/target rows on 2026-11-01:

- 3 input rows; 0 rejected rows; 0 same-hostname rows.
- **2 unique normalized source/target page pairs.**
- **2 referring hostnames**: `news.example` and `blog.example`.
- The `news.example/review#section` row normalizes to the same page as `news.example/review`, so it is a duplicate pair under the helper’s fragment-removal rule.

| Normalized source | Target |
|---|---|
| `https://news.example/review` | `https://inventory.example/product` |
| `https://blog.example/story` | `https://inventory.example/product` |

These are supplied export rows, not two verified live backlinks or a complete backlink inventory. Referring hostnames are not necessarily registrable domains. No pages were fetched; link presence, HTTP status, redirects, anchor text, rel attributes, authority, completeness, and recency remain unknown. The CSV’s original capture date was not supplied. No negative inference can be made about links absent from this tiny export.

Discovery asks which pages link; presence verification checks whether a known page contains a link; availability checking tests whether a URL responds. This run only normalized and summarized supplied pairs. A free link checker would not establish web-wide coverage. If broader data later becomes justified, define that question and cost/access scope first. An open-source tool can still depend on paid data; OpenSEO’s optional DataForSEO-backed data is not free backlink coverage.

## References and tools actually used

Read the installed local Dax Reach skill at `/tmp/dax-reach-public-20261101/skills/dax-reach/SKILL.md`, plus `references/design.md`, `motion.md`, `copy.md`, `conversion.md`, `backlinks.md`, and `decisions.md`. Checked the optional `local-context/profile.json` path; no file was present. Read the bundled `scripts/inspect_backlinks.py` before executing it.

Tools used: `functions.exec` and its `exec_command` shell tool for local file reads and output creation; Python 3 standard-library execution of the bundled CSV helper with explicit `source_url` and `target_url` column mappings. The first output-creation attempt failed before executing because its requested working directory did not yet exist; it was rerun from `/tmp` successfully.

Command executed:

```sh
python3 -B /tmp/dax-reach-public-20261101/skills/dax-reach/scripts/inspect_backlinks.py \
  --csv /tmp/dax-reach-forward-check/backlinks.csv \
  --source-column source_url --target-column target_url
```

Artifacts: `proposal.md`, `backlinks.csv`, and `backlinks-report.json`, all under `/tmp/dax-reach-forward-check`. No pack/project files were modified, no services were contacted, no hooks or dependencies were installed, no paid scans or browser tests were run, and nothing was published. Local references are dated guidance; linked upstream websites were not opened, and current fees or platform rules were not verified. No Google-specific ranking or eligibility claim is made.
