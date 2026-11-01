#!/usr/bin/env python3
"""Extract evidence from a local HTML file. No networking or JavaScript execution."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path

MAX_BYTES = 5 * 1024 * 1024


def reject_non_json_constant(value):
    raise ValueError('Invalid JSON constant: ' + value)


class EvidenceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titles = []
        self.headings = []
        self.canonicals = []
        self.robots = []
        self.descriptions = []
        self.links = []
        self.jsonld = []
        self.errors = []
        self._title = None
        self._heading = None
        self._jsonld = None
        self._template_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = {key: value or '' for key, value in attrs}
        if tag == 'template':
            self._template_depth += 1
        if self._template_depth:
            return
        if tag == 'title':
            self._title = []
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self._heading = [tag, []]
        elif tag == 'meta':
            name = attrs.get('name', '').lower()
            content = attrs.get('content', '')
            if name in ('robots', 'googlebot'):
                self.robots.append({'name': name, 'content': content})
            elif name == 'description':
                self.descriptions.append(content)
        elif tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonicals.append(attrs.get('href', ''))
        elif tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        elif tag == 'script' and attrs.get('type', '').lower().split(';')[0].strip() == 'application/ld+json':
            self._jsonld = []

    def handle_data(self, data):
        if self._template_depth:
            return
        if self._jsonld is not None:
            self._jsonld.append(data)
        elif self._title is not None:
            self._title.append(data)
        elif self._heading is not None:
            self._heading[1].append(data)

    def handle_endtag(self, tag):
        if tag == 'template':
            self._template_depth = max(0, self._template_depth - 1)
            return
        if self._template_depth:
            return
        if tag == 'title' and self._title is not None:
            self.titles.append(' '.join(''.join(self._title).split()))
            self._title = None
        elif self._heading is not None and tag == self._heading[0]:
            self.headings.append({'level': tag, 'text': ' '.join(''.join(self._heading[1]).split())})
            self._heading = None
        elif tag == 'script' and self._jsonld is not None:
            try:
                value = json.loads(''.join(self._jsonld), parse_constant=reject_non_json_constant)
                if not isinstance(value, (dict, list)):
                    self.errors.append('JSON-LD root must be an object or array')
                else:
                    self.jsonld.append(value)
            except (ValueError, RecursionError) as error:
                self.errors.append(str(error))
            self._jsonld = None

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)


def inspect_html(html):
    parser = EvidenceParser()
    parser.feed(html)
    parser.close()
    if parser._jsonld is not None:
        parser.errors.append('Unclosed JSON-LD script element')
    findings = []
    if not parser.titles or not any(parser.titles):
        findings.append('Missing or empty title in this HTML file')
    if len(parser.titles) > 1:
        findings.append('Multiple title elements in this HTML file')
    if len(set(parser.canonicals)) > 1:
        findings.append('Conflicting canonical URLs in this HTML file')
    if parser.errors:
        findings.append('JSON-LD syntax/shape errors in this HTML file')
    return {
        'scope': 'local-html-only',
        'titles': parser.titles,
        'descriptions': parser.descriptions,
        'headings': parser.headings,
        'canonicals': parser.canonicals,
        'robots_meta': parser.robots,
        'anchor_hrefs': parser.links,
        'jsonld_documents': parser.jsonld,
        'jsonld_parse_errors': parser.errors,
        'findings': findings,
        'not_checked': ['HTTP status/headers', 'robots.txt', 'rendered DOM or CSS visibility',
                        'Schema.org vocabulary', 'Google eligibility/indexing',
                        'performance', 'live links', 'AI citations', 'conversions'],
    }


def inspect_file(path):
    path = Path(path)
    with path.open('rb') as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('HTML exceeds the 5 MiB helper limit; this is not a Google limit')
    result = inspect_html(data.decode('utf-8-sig', errors='replace'))
    result['file'] = str(path)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html_file')
    args = parser.parse_args()
    try:
        result = inspect_file(args.html_file)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
