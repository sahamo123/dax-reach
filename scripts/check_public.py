#!/usr/bin/env python3
"""Offline public-release guard. Reports locations and rule IDs, never matched values."""
import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'private-key': rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    'github-token': rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b',
    'api-secret': rb'\bsk-(?:proj-|live_|test_)?[A-Za-z0-9_-]{24,}\b',
    'aws-key': rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    'google-key': rb'\bAIza[A-Za-z0-9_-]{35}\b',
    'credential-url': rb'https?://[^\s/:]+:[^\s/@]+@',
    'secret-assignment': rb'(?i)(?:api[_-]?key|client[_-]?secret|password|access[_-]?token)\s*[=:]\s*[\"\'][A-Za-z0-9+/=_-]{16,}[\"\']',
    'service-account': rb'"type"\s*:\s*"service_account"',
    'internal-project-path': rb'/(?:home|Users)/[^\s/]+/(?:projects|\.codex)/',
    'private-preview': rb'(?i)daxable[^\s/]*\.web\.app',
}


def findings_for(path, data):
    findings = [rule for rule, pattern in PATTERNS.items() if re.search(pattern, data)]
    p = Path(path)
    if (p.name.startswith('.env') and p.name != '.env.example') or p.suffix.lower() in ('.pem', '.p12', '.pfx', '.key'):
        findings.append('credential-filename')
    if ('local-context' in p.parts and p.name != '.gitignore') or p.name == 'profile.json':
        findings.append('private-context')
    return findings


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def check(root=ROOT, history=False):
    findings, checked = [], 0
    # Include untracked deliverables; ignore only generated/cache directories, not secrets.
    for path in root.rglob('*'):
        if any(part in ('.git', '__pycache__', '.venv') for part in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            findings.append((str(path.relative_to(root)), 'symlink'))
        elif path.is_file():
            checked += 1
            findings.extend((str(path.relative_to(root)), rule) for rule in findings_for(str(path.relative_to(root)), path.read_bytes()))
    if history:
        if git(root, 'rev-parse', '--is-shallow-repository').strip() == b'true':
            raise ValueError('Full history scan requires a non-shallow checkout')
        for line in git(root, 'rev-list', '--objects', '--all').decode().splitlines():
            oid, _, name = line.partition(' ')
            if git(root, 'cat-file', '-t', oid).strip() != b'blob':
                continue
            checked += 1
            findings.extend((oid[:12] + ':' + name, rule) for rule in findings_for(name, git(root, 'cat-file', 'blob', oid)))
        # Filenames are also checked per commit: the same blob can have more than one path.
        for revision in git(root, 'rev-list', '--all').decode().splitlines():
            for name in git(root, 'ls-tree', '-r', '--name-only', '-z', revision).decode().split('\0'):
                findings.extend((revision[:12] + ':' + name, rule) for rule in findings_for(name, b''))
        metadata = git(root, 'log', '--all', '--format=%B%n%an <%ae>%n%cn <%ce>')
        findings.extend(('commit-metadata', rule) for rule in findings_for('', metadata))
    return sorted(set(findings)), checked


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--history', action='store_true')
    args = parser.parse_args()
    try:
        findings, checked = check(history=args.history)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, 'Public-release check could not complete: ' + type(error).__name__ + '\n')
    for path, rule in findings:
        print('REVIEW: ' + rule + ' at ' + path)
    print(f'{"REVIEW REQUIRED" if findings else "PASS"}: {checked} working files/history blobs checked; no matched values printed.')
    print('Pattern checks cannot recognize all confidential prose. Inspect content, history metadata, issues, PRs, and build artifacts before public release.')
    sys.exit(bool(findings))
