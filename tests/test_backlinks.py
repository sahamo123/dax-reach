import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from test_tools import load

backlinks = load('backlinks', 'skills/dax-reach/scripts/inspect_backlinks.py')


class BacklinkEvidenceTests(unittest.TestCase):
    def test_csv_deduplicates_keeps_queries_and_reports_coverage(self):
        text = 'source_url,target_url\nhttps://News.example/a#one,https://example.com/p\nhttps://news.example/a#two,https://example.com/p\nhttps://news.example/a?q=1,https://example.com/p\n'
        result = backlinks.summarize_csv(text)
        self.assertEqual(result['input_rows'], 3)
        self.assertEqual(result['unique_page_pairs'], 2)
        self.assertEqual(result['referring_hostnames'], 1)
        self.assertFalse(result['network_performed'])

    def test_domain_summary_cannot_masquerade_as_page_pairs(self):
        with self.assertRaises(ValueError):
            backlinks.summarize_csv('Top linking sites,Links\nexample.com,100\n')

    def test_page_specific_export_with_custom_column(self):
        result = backlinks.summarize_csv('Linking page\nhttps://publisher.example/a\n', 'Linking page', target_url='https://example.com/page')
        self.assertEqual(result['links'][0]['target_url'], 'https://example.com/page')

    def test_invalid_and_credential_urls_and_same_host_are_not_counted(self):
        credential_url = 'https://' + 'user:pass' + '@bad.example/a'
        result = backlinks.summarize_csv('source_url,target_url\nftp://bad.example/a,https://example.com\n' + credential_url + ',https://example.com\nhttps://example.com/a,https://example.com/b\n')
        self.assertEqual(result['unique_page_pairs'], 0)
        self.assertEqual(result['rejected_rows'], 2)
        self.assertEqual(result['same_hostname_rows'], 1)
        self.assertNotIn('user:pass', str(result))

    def test_html_extracts_anchor_rel_and_rejects_lookalike_domain(self):
        html = '<a href="https://www.example.com/report" rel="nofollow sponsored">A <b>report</b></a><a href="https://evil-example.com/">Wrong</a><template><a href="https://example.com/fake">Hidden</a></template><script>fetch("https://example.com/js")</script>'
        result = backlinks.inspect_html(html, 'https://publisher.example/story', 'example.com')
        self.assertEqual(len(result['matching_links']), 1)
        self.assertEqual(result['matching_links'][0]['anchor'], 'A report')
        self.assertEqual(result['matching_links'][0]['rel'], ['nofollow', 'sponsored'])

    def test_html_base_relative_and_absent_attributes(self):
        result = backlinks.inspect_html('<base href="https://example.com/reports/"><a href="one" rel>One</a><a href>Empty</a>', 'https://publisher.example/story', 'example.com')
        self.assertEqual(result['matching_links'][0]['target_url'], 'https://example.com/reports/one')
        self.assertEqual(result['matching_links'][0]['rel'], [])

    def test_row_and_file_limits(self):
        with patch.object(backlinks, 'MAX_ROWS', 1), self.assertRaises(ValueError):
            backlinks.summarize_csv('source_url,target_url\nhttps://a.example,https://b.example\nhttps://c.example,https://b.example\n')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'large.csv'
            path.write_bytes(b'x' * (backlinks.MAX_BYTES + 1))
            with self.assertRaises(ValueError):
                backlinks.read_input(path)
