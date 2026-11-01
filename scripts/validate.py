#!/usr/bin/env python3
"""Offline structural validation; this does not test LLM quality or SEO outcomes."""

from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'daxable-marketing-search'


def validate(root=ROOT):
    errors, warnings = [], []
    skill = root / 'skills' / 'daxable-marketing-search'
    text = (skill / 'SKILL.md').read_text()
    frontmatter = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not frontmatter:
        errors.append('Missing skill frontmatter')
    else:
        fields = dict(re.findall(r'^([a-z-]+): (.+)$', frontmatter[1], re.M))
        name = fields.get('name', '')
        if name != skill.name or len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            errors.append('Invalid skill name')
        if not 1 <= len(fields.get('description', '')) <= 1024:
            errors.append('Invalid skill description')
        if len(fields.get('compatibility', '')) > 500:
            errors.append('Compatibility description too long')
    for path in root.rglob('*.md'):
        if any(part in ('.git', 'upstream', '__pycache__') for part in path.relative_to(root).parts):
            continue
        # Raw model outputs contain example website links, not repository references.
        # Authored docs linking to these artifacts are still checked below.
        if path.is_relative_to(root / 'evals' / 'results'):
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f'Broken/escaping reference in {path.relative_to(root)}: {target}')
            if path.is_relative_to(skill) and not resolved.is_relative_to(skill):
                errors.append(f'Installed package reference escapes package: {target}')
    manifest = json.loads((root / 'upstream.lock.json').read_text())
    for item in manifest['sources']:
        snapshot = (root / item['snapshot']).resolve()
        if not snapshot.is_relative_to(root / 'upstream'):
            errors.append('Upstream path outside archive')
            continue
        data = snapshot.read_bytes()
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            errors.append('Upstream SHA-256 mismatch: ' + item['snapshot'])
        blob = b'blob ' + str(len(data)).encode() + b'\0' + data
        if hashlib.sha1(blob).hexdigest() != item['git_blob_sha']:
            errors.append('Upstream Git blob mismatch: ' + item['snapshot'])
        if not re.fullmatch(r'[a-f0-9]{40}', item['commit']):
            errors.append('Unpinned upstream source')
    licenses = [('coreyhaines31--marketingskills', 'corey-haines-MIT.txt'),
                ('AgriciDaniel--claude-seo', 'agricidaniel-MIT.txt')]
    for archive, installed in licenses:
        if (root / 'upstream' / archive / 'LICENSE').read_bytes() != (skill / 'licenses' / installed).read_bytes():
            errors.append('License notice changed: ' + installed)
    sources = json.loads((skill / 'references/sources.json').read_text())
    ids = [item['id'] for item in sources['sources']]
    if len(ids) != len(set(ids)):
        errors.append('Duplicate source IDs')
    for item in sources['sources']:
        parsed = urlsplit(item['url'])
        if parsed.scheme != 'https' or parsed.hostname not in ('developers.google.com', 'support.google.com'):
            errors.append('Non-official Google source: ' + item['id'])
        reviewed = date.fromisoformat(item['reviewed_on'])
        age = (date.today() - reviewed).days
        if age < 0:
            errors.append('Future source review date: ' + item['id'])
        elif age > sources['review_interval_days']:
            warnings.append('Review freshness: ' + item['id'])
    for path in skill.rglob('*.md'):
        for source_id in re.findall(r'\bG\d{2}\b', path.read_text()):
            if source_id not in ids:
                errors.append('Unknown source ID: ' + source_id)
    for path in skill.rglob('*'):
        if path.is_symlink():
            errors.append('Symlink in active package: ' + str(path))
    return errors, warnings


if __name__ == '__main__':
    try:
        errors, warnings = validate()
    except (OSError, ValueError, KeyError) as error:
        errors, warnings = [str(error)], []
    for warning in warnings:
        print('WARNING: ' + warning)
    for error in errors:
        print('ERROR: ' + error)
    if not errors:
        print('PASS: package structure, local references, source pins, hashes, and license integrity')
    sys.exit(bool(errors))
