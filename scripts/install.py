#!/usr/bin/env python3
"""Install Dax Reach. Dry-run by default; local context stays in the target project."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from business_profile import build_profile
from check_public import findings_for

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills' / 'dax-reach'
LOCATIONS = {'codex': '.agents/skills', 'claude': '.claude/skills', 'antigravity': '.agents/skills',
             'cursor': '.cursor/skills', 'grok': '.grok/skills', 'portable': 'skills'}
PROJECT_ROOTS = tuple(dict.fromkeys((*LOCATIONS.values(), '.codex/skills', '.agent/skills', '_agents/skills', '_agent/skills')))
USER_ROOTS = ('.agents/skills', '.claude/skills', '.codex/skills', '.cursor/skills', '.grok/skills',
              '.gemini/config/skills', '.gemini/skills', '.gemini/antigravity-cli/skills')
ALIASES = {'dax-reach', 'daxreach', 'daxable-marketing-search', 'daxable-marketing-skill'}
OVERLAPS = {'seo', 'seo-technical', 'seo-content', 'seo-schema', 'seo-geo', 'ai-seo',
            'copywriting', 'content-strategy', 'product-marketing', 'cro', 'seo-audit', 'impeccable', 'frontend-design'}
PROFILE_PATH = 'local-context/profile.json'


def inventory(directory):
    result = {}
    for path in directory.rglob('*'):
        if path.is_symlink():
            raise ValueError('Package or installation contains a symlink: ' + str(path))
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            result[str(path.relative_to(directory))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def project_scopes(project):
    project = Path(project).resolve()
    parents = [project, *project.parents]
    for index, path in enumerate(parents):
        if (path / '.git').exists():
            return parents[:index + 1]
    return [project]


def detect_agents(project, environ=None):
    environ = os.environ if environ is None else environ
    markers = {'codex': ('.codex',), 'claude': ('.claude', 'CLAUDE.md'), 'cursor': ('.cursor',),
               'antigravity': ('.agent', 'GEMINI.md', '.gemini'), 'grok': ('.grok',)}
    found = {agent for agent, paths in markers.items()
             if any((scope / marker).exists() for scope in project_scopes(project) for marker in paths)}
    # Presence only; never print environment values or read credentials.
    for agent, keys in {'codex': ('CODEX_THREAD_ID',), 'claude': ('CLAUDECODE',), 'cursor': ('CURSOR_TRACE_ID',)}.items():
        if any(environ.get(key) for key in keys):
            found.add(agent)
    if environ.get('TERM_PROGRAM', '').lower() == 'cursor':
        found.add('cursor')
    return sorted(found)


def scan_conflicts(project, destination, home=None, extra_roots=()):
    """Bounded read-only metadata scan; does not execute third-party skills."""
    home = Path.home() if home is None else Path(home)
    roots = [scope / name for scope in project_scopes(project) for name in PROJECT_ROOTS]
    roots += [home / name for name in USER_ROOTS]
    roots += [Path(path).expanduser().absolute() for path in extra_roots]
    findings, visited, scanned = [], set(), []

    def blocked(path, detail):
        findings.append({'severity': 'block', 'path': str(path), 'reason': detail})

    for root in dict.fromkeys(roots):
        scanned.append(str(root))
        if root.is_symlink() or any(parent.is_symlink() for parent in root.parents):
            blocked(root, 'Symlinked scan root cannot be verified; inspect it explicitly')
            continue
        try:
            if not root.exists():
                continue
            if not root.is_dir():
                blocked(root, 'Skill root is not a directory')
                continue
            count = 0
            for base, directories, files in os.walk(root, followlinks=False, onerror=lambda e: blocked(root, 'Unreadable skill root')):
                base = Path(base)
                count += len(directories) + len(files)
                if count > 5000:
                    blocked(root, 'Scan limit exceeded; inspect and narrow this skill root')
                    break
                for directory in list(directories):
                    child = base / directory
                    if child.is_symlink():
                        blocked(child, 'Symlinked skill directory cannot be verified')
                        directories.remove(directory)
                    elif directory in ('.git', '__pycache__', 'node_modules', 'local-context'):
                        directories.remove(directory)
                if base == destination or base in visited:
                    directories[:] = []
                    continue
                visited.add(base)
                if base.name.lower() in ALIASES:
                    blocked(base, 'Duplicate or legacy Dax Reach directory; migrate explicitly')
                    directories[:] = []
                    continue
                if 'SKILL.md' not in files:
                    continue
                entry = base / 'SKILL.md'
                if entry.is_symlink() or entry.stat().st_size > 131072:
                    blocked(entry, 'Symlinked or oversized skill metadata cannot be verified')
                    continue
                content = entry.read_text(encoding='utf-8')
                header = re.match(r'\A---\s*\n(.*?)\n---', content, re.S)
                declared = re.search(r'^name:\s*[\"\']?([a-zA-Z0-9_-]+)', header[1], re.M) if header else None
                names = {base.name.lower(), declared[1].lower() if declared else ''}
                if names & ALIASES:
                    blocked(entry, 'Duplicate or legacy Dax Reach identity')
                elif names & OVERLAPS:
                    findings.append({'severity': 'overlap', 'path': str(entry),
                                     'reason': 'Related marketing/SEO workflow; choose which skill owns each task'})
        except (OSError, UnicodeError):
            blocked(root, 'Cannot read skill metadata; scan is incomplete')
    return findings, scanned


def install(project, agent, apply=False, *, industry, business_type, home=None, extra_roots=(), allow_overlap=False):
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError('Project must be an existing directory')
    if agent not in LOCATIONS:
        raise ValueError('Select a supported host or portable')
    destination = project / LOCATIONS[agent] / SOURCE.name
    if not destination.resolve().is_relative_to(project):
        raise ValueError('Destination escapes the project through a symlink')
    if destination.resolve().is_relative_to(ROOT):
        raise ValueError('Install in a separate consumer project, never inside the public pack repository')
    if any(path.is_symlink() for path in (destination, *destination.parents)):
        raise ValueError('Refusing a symlink installation path')
    profile = build_profile(industry, business_type)
    profile_bytes = (json.dumps(profile, indent=2, ensure_ascii=True) + '\n').encode()
    expected = inventory(SOURCE)
    for name in expected:
        if findings_for(name, (SOURCE / name).read_bytes()):
            raise ValueError('Source package contains private context or a sensitive-file indicator; refusing to distribute it')
    expected[PROFILE_PATH] = hashlib.sha256(profile_bytes).hexdigest()
    unchanged = False
    if destination.exists():
        if destination.is_dir() and inventory(destination) == expected:
            unchanged = True
        else:
            raise ValueError('Existing installation differs; review and back it up before reinstalling')
    conflicts, scanned = scan_conflicts(project, destination, home, extra_roots)
    blocked = any(item['severity'] == 'block' or not allow_overlap for item in conflicts)
    result = {'status': 'blocked' if blocked else 'unchanged' if unchanged else 'dry-run',
              'agent': agent, 'destination': str(destination), 'profile': profile,
              'conflicts': conflicts, 'scanned_roots': scanned}
    if blocked or unchanged or not apply:
        return result
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.dax-reach-', dir=destination.parent) as temporary:
        staged = Path(temporary) / SOURCE.name
        shutil.copytree(SOURCE, staged, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        (staged / PROFILE_PATH).write_bytes(profile_bytes)
        if inventory(staged) != expected:
            raise ValueError('Staged installation failed integrity verification')
        if destination.exists() or destination.is_symlink():
            raise ValueError('Destination appeared during installation; refusing to overwrite')
        staged.rename(destination)
    result['status'] = 'installed'
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=['auto', *LOCATIONS], default='auto')
    parser.add_argument('--project', required=True)
    parser.add_argument('--industry', help='Broad industry label only; no secrets or client data')
    parser.add_argument('--business-type', choices=['service', 'product'])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--interactive', action='store_true', help='Prompt even with piped stdin')
    mode.add_argument('--non-interactive', action='store_true')
    parser.add_argument('--extra-skill-root', action='append', default=[], help='Also scan a custom or plugin skill directory (repeatable)')
    parser.add_argument('--allow-overlap', action='store_true', help='Acknowledge related workflows; never bypass duplicate or conflicting copies')
    parser.add_argument('--apply', action='store_true', help='Copy files after checks; default is dry-run')
    parser.add_argument('--json', action='store_true', help='Structured results; pass explicit inputs for clean JSON')
    args = parser.parse_args(argv)
    interactive = args.interactive or (sys.stdin.isatty() and not args.non_interactive)
    try:
        project = Path(args.project).expanduser().resolve()
        if not project.is_dir():
            raise ValueError('Project must be an existing directory')
        detected = detect_agents(project)
        agent = args.agent
        if agent == 'auto':
            if len(detected) == 1:
                agent = detected[0]
            elif interactive:
                print('Detected hosts: ' + (', '.join(detected) or 'none') + '. Shared .agents folders are not host-specific.')
                agent = input('Host (codex/claude/antigravity/cursor/grok/portable): ').strip().lower()
            else:
                raise ValueError('Host detection is ambiguous or empty: ' + ', '.join(detected) + '; pass --agent explicitly')
        industry = args.industry
        business_type = args.business_type
        if not industry and interactive:
            industry = input('Industry (broad label, no confidential information): ').strip()
        if not business_type and interactive:
            business_type = input('Business type (service/product): ').strip().lower()
        if not industry or not business_type:
            raise ValueError('Pass --industry and --business-type, or run interactively')
        result = install(project, agent, args.apply, industry=industry, business_type=business_type,
                         extra_roots=args.extra_skill_root, allow_overlap=args.allow_overlap)
        result['detected_agents'] = detected
    except (ValueError, OSError, EOFError) as error:
        parser.exit(1, str(error) + '\n')
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result['status'] + ': ' + result['destination'])
        print('Host: ' + agent + '; business: ' + business_type + '; industry: ' + industry)
        for item in result['conflicts']:
            print(item['severity'].upper() + ': ' + item['path'] + ' — ' + item['reason'])
        print('Workflow order: ' + ' → '.join(result['profile']['workflow_order']))
        for note in [result['profile']['recommendations']['journey'], *result['profile']['recommendations']['industry']]:
            print(note)
        if result['status'] in ('installed', 'unchanged'):
            print('Reload the host and invoke ' + ('$dax-reach' if agent == 'codex' else '/dax-reach' if agent != 'portable' else 'SKILL.md through your host'))
        print('Private context: local-context/profile.json inside the installed skill; excluded by its own .gitignore. Never add it with git add -f.')
    return 1 if result['status'] == 'blocked' else 0


if __name__ == '__main__':
    sys.exit(main())
