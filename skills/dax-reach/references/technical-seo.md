---
type: "Playbook"
title: "Technical SEO"
description: "Playbook for technical seo."
reviewed_on: "2026-11-01"
sources: [{"id": "G07", "resource": "https://developers.google.com/search/docs/crawling-indexing/robots/intro"}, {"id": "G08", "resource": "https://developers.google.com/search/docs/crawling-indexing/control-what-you-share"}, {"id": "agrici", "resource": "https://github.com/AgriciDaniel/claude-seo/tree/6be93f45064ffbadced572b5d5c95f55fd263af0"}]
---

# Technical SEO

Adapted from AgriciDaniel's technical SEO workflow; local heuristics have been separated from Google requirements.

Start by identifying production, staging, or local preview and the authorized scope. Intentional noindex on a preview is correct behavior. Do not remove access restrictions or publish a preview to obtain an audit score.

Collect URL/status and response headers where tools permit, initial HTML, rendered DOM, robots directives, canonical, sitemap inclusion, internal links, and representative mobile behavior. Label each source and date. Distinguish observations about one file from statements about the live domain.

1. Crawlability: verify important URLs and resources are reachable through actual anchors and allowed by intended crawler/CDN rules. Review redirects, error responses, sitemap entries, and resource blocking.
2. Indexability: compare status, noindex/X-Robots-Tag, canonicals, sitemap URLs, and rendered directives. Inspect actual Search Console evidence when available. A self-canonical is a signal, not proof of Google's selected canonical.
3. Rendering: compare raw and rendered content. Confirm headings, service explanations, primary links, and metadata survive loading failures. Missing raw content is a portability/rendering concern; it does not by itself prove Google cannot index JavaScript.
4. Page experience: inspect mobile layout, loading, layout shifts, keyboard navigation, reduced motion, and unobstructed content. Separate real-user Core Web Vitals from lab measurements. Do not invent field measurements from a local screenshot.
5. URL consistency: check broken internal destinations, redirect chains, competing variants, unintended duplicates, and descriptive routes. Do not blanket-ban query strings or rename established URLs for cosmetic reasons.
6. Structured data: use the separate schema workflow. Syntax errors, semantic errors, eligibility, and actual appearance are different checks.

Robots controls manage crawling and are not access control. See Google G07 and G08. Verify current vendor documentation before changing any AI crawler policy; training and search access are separate choices.

Optional offline helper: `python3 scripts/inspect_html.py /path/to/page.html` relative to this skill directory. It reports HTML facts and JSON-LD parse errors only. It does not fetch, execute JavaScript, interpret robots.txt, inspect response headers, or validate Google eligibility. Use the host's authorized browser/data tools for those gaps.

Output each material finding with evidence, affected scope, business impact, proposed fix, confidence, and verification. Prioritize real failures over unsupported numerical scores. Implement scoped fixes when authorized and run the project's relevant checks.
