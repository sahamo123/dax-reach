# Backlinks and DataForSEO

Run these helpers from the repository root, or adjust the script path to the installed skill. Keep exports and reports in the consumer project's private working area.

## Free, offline evidence

```bash
python3 skills/dax-reach/scripts/inspect_backlinks.py --csv /path/to/links.csv

python3 skills/dax-reach/scripts/inspect_backlinks.py --csv /path/to/page-links.csv \
  --source-column "Linking page" --target-url https://example.com/product

python3 skills/dax-reach/scripts/inspect_backlinks.py --html /path/to/saved-page.html \
  --source-url https://publisher.example/article --target-domain example.com
```

CSV defaults are `source_url,target_url`; map actual headers using `--source-column` and `--target-column`. Supply a fixed target only when the export actually pertains to that page. Domain-summary reports cannot be treated as page-pair exports. Input limits are 5 MB and 50,000 CSV rows. Results preserve query strings, deduplicate exact normalized pairs, and count referring hostnames. They do not establish live status, all backlinks, registrable-domain counts, or authority scores.

The HTML path inspects saved anchors, rel values, and anchor text without executing JavaScript or fetching pages. Verify capture date, rendering, redirects, and current HTTP status separately. See [tool choices](../skills/dax-reach/references/backlinks.md) for Lychee, SEOnaut, Search Console, and optional OpenSEO.

## Optional paid DataForSEO adapter

The provider uses an **API login and API password**, available in its API Access dashboard; the API password differs from the account password. Set `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` through a local secret manager or your process environment. Do not paste credentials into prompts, command arguments, public files, issues, PRs, or logs. The helper does not load `.env` files or store credentials.

```bash
# Prepare a request: no credential access, network call, or charge
python3 skills/dax-reach/scripts/dataforseo_backlinks.py --target example.com

# Only after reviewing the target, account pricing, and permission to spend:
python3 skills/dax-reach/scripts/dataforseo_backlinks.py --target example.com --execute-paid

# One bounded link-list request; 1–100 records, no automatic pagination
python3 skills/dax-reach/scripts/dataforseo_backlinks.py --target example.com \
  --mode links --limit 20 --execute-paid
```

The adapter uses HTTPS to a fixed DataForSEO hostname, follows no redirects, makes one request with a 30-second timeout, and never retries automatically. It checks both API and task status, limits response size, suppresses raw errors, and redacts credential echoes. The result records retrieval time, provider-reported cost, and coverage limits. A response timeout can occur after the provider has charged: check usage before retrying. The record limit is not a dollar spending cap. No exact price or account entitlement is assumed.

Summary and link-list endpoints are supported; keyword research and paid AI-mention endpoints are not implemented in this adapter. Provider-index records are not proof every link is still present. No paid request was used in package testing; mocks cover transport boundaries and failures.

Primary docs reviewed 2026-11-01: [Authentication](https://docs.dataforseo.com/v3/auth/), [summary endpoint](https://docs.dataforseo.com/v3/backlinks/summary/live/), [link-list endpoint](https://docs.dataforseo.com/v3/backlinks/backlinks/live/). Recheck provider pricing and access at use time.
