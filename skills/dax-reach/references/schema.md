---
type: "Playbook"
title: "Structured Data"
description: "Playbook for schema."
reviewed_on: "2026-11-01"
sources: [{"id": "G05", "resource": "https://developers.google.com/search/docs/appearance/structured-data/sd-policies"}, {"id": "G06", "resource": "https://developers.google.com/search/updates"}, {"id": "agrici", "resource": "https://github.com/AgriciDaniel/claude-seo/tree/6be93f45064ffbadced572b5d5c95f55fd263af0"}]
---

# Structured Data

Adapted from AgriciDaniel's schema analysis workflow; see Google G05 and G06.

Inventory existing JSON-LD, Microdata, or RDFa before adding markup. Select types from the actual entity and visible content. A valid Schema.org type is not necessarily a Google rich-result feature. Do not label services as products or add reviews solely to obtain stars.

Generate a minimal consistent graph using real canonical URLs and stable identifiers when useful. Use only established organization/person identities, accurate service scope, real offers, and current visible course facts. Do not invent ratings, credentials, insurance, addresses, dates, prices, availability, partnerships, or outcomes. Keep organization identity and the entity delivering each service unambiguous.

JSON-LD is usually a practical implementation choice; existing valid Microdata/RDFa need not be rewritten purely for format preference. Use the project's established rendering and escaping patterns. Never interpolate raw user input into a script tag; include a test for script-closing characters when generating JSON-LD through code.

Check in this order: JSON syntax; Schema.org vocabulary/types; consistency with visible text and linked entities; current Google feature-specific eligibility; rendered output; actual Search Console observations if accessible. State which checks ran. Google's Rich Results Test does not cover every Schema.org vocabulary type; no recognized rich-result feature does not automatically make a Service graph invalid.

As reviewed 2026-11-01, Google retired FAQ rich results in May 2026. Keep useful visible FAQs. FAQPage may remain meaningful vocabulary, but do not add it to promise Google FAQ enhancements or AI inclusion. Confirm the live feature documentation before future recommendations.

Deliver the proposed markup plus a property-to-visible-evidence map, validation results, and any missing facts. If nothing meaningful is missing, avoid redundant schema additions.
