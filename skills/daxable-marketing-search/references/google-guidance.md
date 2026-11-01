# Google Guidance — Reviewed 2026-11-01

These are Daxable's concise, adapted notes on official documentation, not Google endorsement. Source IDs and review dates live in [sources.json](sources.json). Google-derived notes are attributed to Google and licensed CC BY 4.0; other package content remains under its stated license. Re-open the primary source for changing policy before implementation. If sources disagree, document the conflict and prefer the current specific documentation; do not silently combine incompatible claims.

| ID | Decision rule | Source |
|---|---|---|
| G01 | Google AI search uses core SEO foundations. Do not require llms.txt, special AI markup, tiny content chunks, or invented mention campaigns. | [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) |
| G02 | Prefer useful original expertise and evidence. There is no Google minimum word count; cosmetic date changes do not establish freshness. | [Helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) |
| G03 | AI-assisted content requires accuracy and added value, including its metadata. Rater guidance does not directly determine rankings. | [Generative AI content](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) |
| G04 | Do not create scaled low-value pages, deceptive doorway variants, keyword stuffing, or manipulative content merely to gain rankings. | [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) |
| G05 | Structured data must represent the actual content. Eligibility and valid markup do not guarantee a rich result. | [Structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) |
| G06 | FAQ rich results ceased in May 2026; useful visible FAQs can remain. Check feature status before promising enhancements. | [Documentation updates, May 8 and June 15](https://developers.google.com/search/updates) |
| G07 | robots.txt controls crawling, not privacy or reliable removal from search. Access control and indexing directives solve different problems. | [Robots introduction](https://developers.google.com/search/docs/crawling-indexing/robots/intro) |
| G08 | Check the intended use of noindex, snippet controls, and access protection. Preserve intentional preview restrictions. | [Control what you share](https://developers.google.com/search/docs/crawling-indexing/control-what-you-share) |
| G09 | Google can render JavaScript; inspect actual rendering and metadata consistency. Do not diagnose an indexing failure solely from the framework. | [JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) |
| G10 | Evaluate the overall visitor experience, including mobile, stability, speed, and unobstructed content. A perfect tool score is not the objective. | [Page experience](https://developers.google.com/search/docs/appearance/page-experience) |
| G11 | Search Console has a Search generative AI inclusion control, separate from training controls and general Search indexing. Inspect the actual property when authorized. | [Search generative AI control](https://support.google.com/webmasters/answer/16908024) |
| G12 | The Generative AI performance report measures impressions. Missing reports can reflect insufficient impressions; don't fabricate AI clicks or infer zero visibility. | [Generative AI performance report](https://support.google.com/webmasters/answer/16984139) |
| G13 | Third-party scores and predictions are not Google's internal metrics. Use first-party evidence and identify judgment as judgment. | [Third-party SEO advice](https://developers.google.com/search/docs/fundamentals/third-party-seo) |
| G14 | Use sensible crawlable URL structures. Avoid unnecessary migrations just to cosmetically change existing working URLs. | [URL structure](https://developers.google.com/search/docs/crawling-indexing/url-structure) |

## Resolved documentation conflict

The older [AI features overview](https://developers.google.com/search/docs/appearance/ai-features) describes AI traffic within the aggregate Web performance report. The more specific current G11/G12 documentation describes a dedicated inclusion control and AI impressions report, rolled out August 31, 2026. Use the specific control/report documentation for those capabilities. Aggregate search traffic and the dedicated impressions report are different views. Neither source proves the user's property has data, nor supplies a dedicated AI click metric.

## Freshness

The date above records review, not automatic updating. Check [Google's update log](https://developers.google.com/search/updates) during policy maintenance and before time-sensitive recommendations. The validator warns when the review is older than 90 days; this is this project's maintenance convention, not a Google requirement. Update sources, decisions, behavioral cases, and the changelog together.
