#!/usr/bin/env python3
"""Inspect supplied backlink CSV or saved HTML offline. No crawling or link discovery."""
import argparse
import csv
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import sys
from urllib.parse import urljoin, urlsplit, urlunsplit

MAX_BYTES = 5_000_000
MAX_ROWS = 50_000


def normalized_url(value):
    value = value.strip()
    if not value or any(c.isspace() or ord(c) < 32 for c in value):
        raise ValueError('Expected an HTTP(S) URL without whitespace')
    parts = urlsplit(value)
    if parts.scheme.lower() not in ('http', 'https') or not parts.hostname or parts.username is not None or parts.password is not None:
        raise ValueError('Expected an HTTP(S) URL without credentials')
    host = parts.hostname.lower().encode('idna').decode('ascii')
    if ':' in host:
        host = '[' + host + ']'
    port = parts.port
    if port is not None and (parts.scheme.lower(), port) not in (('http', 80), ('https', 443)):
        host += ':' + str(port)
    return urlunsplit((parts.scheme.lower(), host, parts.path or '/', parts.query, ''))


def read_input(path):
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('Input exceeds the 5 MB limit')
    return path.read_text(encoding='utf-8-sig')


def summarize_csv(text, source_column='source_url', target_column='target_url', target_url=None):
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or source_column not in reader.fieldnames or (target_url is None and target_column not in reader.fieldnames):
        raise ValueError('Missing source/target columns; map actual export columns or supply --target-url for a page-specific source list')
    fixed_target = normalized_url(target_url) if target_url is not None else None
    pairs, rejected, internal, rows = set(), 0, 0, 0
    for row in reader:
        rows += 1
        if rows > MAX_ROWS:
            raise ValueError('Input exceeds the 50000-row limit')
        try:
            source = normalized_url(row.get(source_column) or '')
            target = fixed_target or normalized_url(row.get(target_column) or '')
        except (ValueError, UnicodeError):
            rejected += 1
            continue
        if urlsplit(source).hostname == urlsplit(target).hostname:
            internal += 1
            continue
        pairs.add((source, target))
    return {'input_rows': rows, 'rejected_rows': rejected, 'same_hostname_rows': internal,
            'unique_page_pairs': len(pairs), 'referring_hostnames': len({urlsplit(s).hostname for s, _ in pairs}),
            'links': [{'source_url': s, 'target_url': t} for s, t in sorted(pairs)],
            'scope': 'Supplied export only; hostnames are not registrable domains. Coverage, recency, rel attributes, and live status are unknown.',
            'network_performed': False}


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.current, self.ignored, self.base = [], None, 0, None

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'template'):
            self.ignored += 1
        if self.ignored:
            return
        attributes = dict(attrs)
        if tag == 'base' and self.base is None:
            self.base = attributes.get('href')
        if tag == 'a' and attributes.get('href'):
            self.current = {'href': attributes['href'], 'rel': (attributes.get('rel') or '').lower().split(), 'text': ''}

    def handle_data(self, data):
        if self.current is not None and not self.ignored:
            self.current['text'] += data

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'template') and self.ignored:
            self.ignored -= 1
        if tag == 'a' and self.current is not None and not self.ignored:
            self.links.append(self.current)
            self.current = None


def inspect_html(text, source_url, target_domain):
    source_url = normalized_url(source_url)
    target_domain = target_domain.lower().rstrip('.')
    if not target_domain or any(c in target_domain for c in '/:@?#') or any(c.isspace() for c in target_domain):
        raise ValueError('Use a bare target domain, such as example.com')
    target_domain = target_domain.encode('idna').decode('ascii')
    parser = Links()
    parser.feed(text)
    parser.close()
    base = urljoin(source_url, parser.base) if parser.base else source_url
    matches = []
    for link in parser.links:
        try:
            target = normalized_url(urljoin(base, link['href']))
        except (ValueError, UnicodeError):
            continue
        host = urlsplit(target).hostname
        if host == target_domain or host.endswith('.' + target_domain):
            matches.append({'target_url': target, 'anchor': ' '.join(link['text'].split()), 'rel': sorted(set(link['rel']))})
    return {'source_url': source_url, 'target_domain': target_domain, 'matching_links': matches,
            'scope': 'Saved HTML only, including target subdomains. Capture time, HTTP status, current presence, and JavaScript-rendered links are not established.',
            'network_performed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--csv', type=Path)
    mode.add_argument('--html', type=Path)
    parser.add_argument('--source-column', default='source_url')
    parser.add_argument('--target-column', default='target_url')
    parser.add_argument('--target-url')
    parser.add_argument('--source-url')
    parser.add_argument('--target-domain')
    args = parser.parse_args()
    try:
        if args.csv:
            report = summarize_csv(read_input(args.csv), args.source_column, args.target_column, args.target_url)
        else:
            if not args.source_url or not args.target_domain:
                raise ValueError('HTML mode requires --source-url and --target-domain')
            report = inspect_html(read_input(args.html), args.source_url, args.target_domain)
    except (OSError, ValueError, UnicodeError, csv.Error) as error:
        parser.exit(1, type(error).__name__ + ': unable to inspect input; check format, columns, URLs, and size limits\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
