# Public and Private Boundaries

Dax Reach is a standalone reusable pack. Internal company skills, website configuration, production rules, customer records, analytics exports, commercial account settings, and credentials are not distribution inputs. No website or internal skill is changed by this release.

The public tree contains generic workflows, fictional fixtures, source/license snapshots from public upstream repositories, tests, and package maintenance records. The author name in copyright notices and the public GitHub owner are attribution, not business configuration. Historical offline evidence retains its original artifact name and generic process references; it is not evidence of testing the renamed version.

## Checks before visibility changes

Run `python3 scripts/check_public.py --history` from a complete checkout. It scans current files and reachable historical blobs, checks paths in every commit, and inspects commit text for known sensitive patterns. Reports show rule IDs and paths, never matched secret values. A shallow clone is rejected for this release check. Review all branches/tags intended for publication.

Also inspect authored content, commit authors/messages, repository metadata, issues, PRs, releases, and workflow artifacts for private prose or attachments. Pattern checks cannot recognize all confidential information. If sensitive material appears, stop publication, remove it from the intended public history/artifacts, and handle any exposed credential with its owner; deleting only the current file is insufficient.

The original repository was created separately from the production project. Its existing commit authors are an automated identity and GitHub noreply identity. Public upstream snapshots retain required source credits and license notices. No credential was retrieved or added for DataForSEO testing.

## Consumer data

The installer reads skill names/metadata to detect conflicts, but does not copy installed company skills, settings, or context into the public source. It writes only its package plus locally supplied broad industry/type recommendations to a consumer destination. Local context is protected against accidental Git adds by its own .gitignore; deliberate force-adds and external uploads remain the user's responsibility.

The installer blocks distribution of source files with private-context or sensitive indicators and rejects installation into the pack's own checkout. It never writes host settings or existing agent instruction files. Updates never overwrite a divergent installation.

The optional DataForSEO adapter reads API credentials from the process environment only when paid execution is explicitly selected. No command-line credential option, credential persistence, telemetry, automatic account setup, retry loop, or website deployment is included. Keep output reports private unless independently reviewed for sharing.
