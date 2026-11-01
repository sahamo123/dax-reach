---
type: "Playbook"
title: "Backlinks and Free Tools"
description: "Analyze supplied link evidence and choose free or optional paid tools without claiming a complete backlink index."
sources: [{"id":"gsc-links","resource":"https://support.google.com/webmasters/answer/9049606"},{"id":"lychee","resource":"https://github.com/lycheeverse/lychee"},{"id":"seonaut","resource":"https://github.com/StJudeWasHere/seonaut"},{"id":"openseo","resource":"https://github.com/every-app/open-seo"}]
reviewed_on: "2026-11-01"
---

# Backlinks and Free Tools

Distinguish discovery (which pages link to a site), presence verification (a known page currently contains a link), and availability checking (a URL responds). A site crawler or broken-link checker does not provide a complete web-wide backlink index. Referring hostnames are not necessarily distinct registrable domains.

Start with authorized Search Console Links exports for the site's verified property. Google describes this as sampled, potentially historical data, not an exhaustive current inventory; it does not specify nofollow. Keep the export date, property, report/filter, and row limits with the result. A top-linking-domains summary is not a list of source/target page pairs. Do not invent those pairs or treat missing rows as proof a link was lost.

For supplied page-pair CSVs, run the bundled `scripts/inspect_backlinks.py` from the installed skill directory. Set the source and target column names to the actual export; for a page-specific source list, explicitly pass the known target URL. It normalizes HTTP(S) URLs, rejects credential-bearing URLs, deduplicates pairs, and counts referring hostnames. It does not fetch URLs, score authority, label toxicity, or discover new links.

For a known linking page, inspect authorized current HTML using the host's browser, or run the helper on saved HTML with its source URL and target domain. Record whether links appear, their anchor text and rel values, the capture time, and whether JavaScript rendering was included. An absent link in raw HTML is not proof it is absent after rendering. Verify redirects and response status separately. No accounts, crawls, or paid requests are created by this pack.

## Tool choices

When paid DataForSEO access is already available, the bundled `scripts/dataforseo_backlinks.py` supports summary and bounded link-list requests. It reads only local DATAFORSEO_LOGIN/DATAFORSEO_PASSWORD variables and defaults to a dry-run. Only use `--execute-paid` within the user's spending authorization; owning credentials alone is not authorization to spend. There is one request, no pagination or automatic retry, no redirect following, and no credential logging. Check current account pricing and preserve the provider's coverage limits. API details: [authentication](https://docs.dataforseo.com/v3/auth/), [summary](https://docs.dataforseo.com/v3/backlinks/summary/live/), [links](https://docs.dataforseo.com/v3/backlinks/backlinks/live/).

| Tool | Useful for | Cost/access boundary |
|---|---|---|
| Google Search Console Links | First-party sampled backlinks for an authorized property | Free service; account/property access needed; not open-source software |
| Lychee | Checking known links in files/sites | MIT/Apache-2.0 open source; run an existing reviewed installation within the allowed URL scope |
| SEOnaut | Self-hosted technical site crawl and issue reports | MIT open source; compute/database setup is separate; not a web-wide backlink database |
| OpenSEO | Optional broader SEO/backlink data through its MCP/application | Open-source app; its DataForSEO data requires a paid key; never describe it as free backlink coverage |
| Bundled offline helpers | Local HTML evidence and supplied export analysis | Python standard library; no account, network calls, or API key |

Do not silently install third-party software, run an unpinned remote script, change host/MCP settings, or upload exports. If a suitable tool is already authorized and available, use its documented read-only capability. Otherwise give a concrete scoped setup plan and continue with local evidence. Tool availability, versions, fees, and quotas must be checked at use time.

Prioritize relevant earned references, useful original resources, accurate business listings, and genuine editorial relationships. Avoid bought/manipulative links, mass-generated outreach, or automatic disavow recommendations based on third-party scores. Outreach remains separately authorized. Choose substantive work through [decisions](decisions.md), then measure with [measurement](measurement.md).
