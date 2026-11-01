#!/usr/bin/env python3
"""Install only the portable package. Dry-run by default; never overwrite."""

import argparse
import hashlib
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills' / 'daxable-marketing-search'
LOCATIONS = {'codex': '.agents/skills', 'claude': '.claude/skills', 'portable': 'skills'}


def inventory(directory):
    result = {}
    for path in directory.rglob('*'):
        if path.is_symlink():
            raise ValueError('Package or installation contains a symlink: ' + str(path))
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            result[str(path.relative_to(directory))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def install(project, agent, apply=False):
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError('Project must be an existing directory')
    destination = project / LOCATIONS[agent] / SOURCE.name
    if not destination.resolve().is_relative_to(project):
        raise ValueError('Destination escapes the project through a symlink')
    if destination.resolve().is_relative_to(SOURCE):
        raise ValueError('Cannot install the package inside itself')
    expected = inventory(SOURCE)
    if destination.is_symlink():
        raise ValueError('Refusing a symlink installation')
    if destination.exists():
        if destination.is_dir() and inventory(destination) == expected:
            return {'status': 'unchanged', 'destination': str(destination)}
        raise ValueError('Existing installation differs; review and back it up before reinstalling')
    if not apply:
        return {'status': 'dry-run', 'destination': str(destination)}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.marketing-search-', dir=destination.parent) as temporary:
        staged = Path(temporary) / SOURCE.name
        shutil.copytree(SOURCE, staged, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        if inventory(staged) != expected:
            raise ValueError('Staged installation failed integrity verification')
        if destination.exists() or destination.is_symlink():
            raise ValueError('Destination appeared during installation; refusing to overwrite')
        staged.rename(destination)
    return {'status': 'installed', 'destination': str(destination)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=LOCATIONS, required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--apply', action='store_true', help='Copy files; default only reports the destination')
    args = parser.parse_args()
    try:
        result = install(args.project, args.agent, args.apply)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')
    print(result['status'] + ': ' + result['destination'])


if __name__ == '__main__':
    main()
