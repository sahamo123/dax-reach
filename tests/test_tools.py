import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load('installer', 'scripts/install.py')
inspector = load('inspector', 'skills/daxable-marketing-search/scripts/inspect_html.py')
validator = load('validator', 'scripts/validate.py')


class InstallationTests(unittest.TestCase):
    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as path:
            result = installer.install(path, 'codex')
            self.assertEqual(result['status'], 'dry-run')
            self.assertEqual(list(Path(path).iterdir()), [])

    def test_all_hosts_get_complete_package_without_settings_changes(self):
        for agent, location in installer.LOCATIONS.items():
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as path:
                root = Path(path)
                (root / 'AGENTS.md').write_text('Existing project instructions')
                (root / 'CLAUDE.md').write_text('Existing Claude instructions')
                result = installer.install(path, agent, True)
                destination = root / location / installer.SOURCE.name
                self.assertEqual(Path(result['destination']), destination)
                self.assertEqual(installer.inventory(destination), installer.inventory(installer.SOURCE))
                self.assertEqual((root / 'AGENTS.md').read_text(), 'Existing project instructions')
                self.assertEqual((root / 'CLAUDE.md').read_text(), 'Existing Claude instructions')
                self.assertFalse((destination / 'upstream').exists())
                self.assertEqual(installer.install(path, agent, True)['status'], 'unchanged')

    def test_existing_customization_is_preserved(self):
        with tempfile.TemporaryDirectory() as path:
            result = installer.install(path, 'codex', True)
            skill = Path(result['destination']) / 'SKILL.md'
            skill.write_text('User customization')
            with self.assertRaises(ValueError):
                installer.install(path, 'codex', True)
            self.assertEqual(skill.read_text(), 'User customization')

    def test_symlink_escape_refused(self):
        with tempfile.TemporaryDirectory() as path, tempfile.TemporaryDirectory() as outside:
            (Path(path) / '.agents').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                installer.install(path, 'codex', True)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_missing_project_refused(self):
        with tempfile.TemporaryDirectory() as path:
            with self.assertRaises(ValueError):
                installer.install(Path(path) / 'absent', 'claude', True)


class HtmlEvidenceTests(unittest.TestCase):
    def test_fixture_preserves_preview_noindex_as_fact(self):
        report = inspector.inspect_file(ROOT / 'tests/fixtures/example.html')
        self.assertEqual(report['robots_meta'][0]['content'], 'noindex, nofollow')
        self.assertEqual(report['findings'], [])
        self.assertEqual(len(report['headings']), 2)
        self.assertEqual(report['anchor_hrefs'], ['/academy/'])
        self.assertIn('Google eligibility/indexing', report['not_checked'])

    def test_nested_graph_and_multiple_documents(self):
        report = inspector.inspect_html('<script type="application/ld+json">{"@graph":[{"@type":"Organization"}]}</script><script type="application/ld+json">[{"@type":"Service"}]</script>')
        self.assertEqual(len(report['jsonld_documents']), 2)
        self.assertEqual(report['jsonld_parse_errors'], [])

    def test_invalid_json_does_not_discard_valid_document(self):
        report = inspector.inspect_html('<script type="application/ld+json">{oops}</script><script type="application/ld+json">{}</script>')
        self.assertEqual(len(report['jsonld_documents']), 1)
        self.assertEqual(len(report['jsonld_parse_errors']), 1)

    def test_scalar_json_is_not_schema(self):
        report = inspector.inspect_html('<script type="application/ld+json">true</script>')
        self.assertEqual(report['jsonld_documents'], [])
        self.assertEqual(len(report['jsonld_parse_errors']), 1)

    def test_non_json_numeric_constant_is_rejected(self):
        report = inspector.inspect_html('<script type="application/ld+json">{"ratingValue": NaN}</script>')
        self.assertEqual(report['jsonld_documents'], [])
        self.assertEqual(len(report['jsonld_parse_errors']), 1)

    def test_valueless_attributes_do_not_crash(self):
        report = inspector.inspect_html('<meta name><link rel><script type></script><h1>Service</h1>')
        self.assertEqual(report['headings'][0]['text'], 'Service')

    def test_unclosed_jsonld_is_reported(self):
        report = inspector.inspect_html('<script type="application/ld+json">{}')
        self.assertIn('Unclosed JSON-LD script element', report['jsonld_parse_errors'])

    def test_canonical_conflict_and_case_handling(self):
        report = inspector.inspect_html('<TITLE>Example &amp; Test</TITLE><link rel="CANONICAL" href="/one"><link rel="canonical" href="/two"><meta name="Googlebot" content="noindex">')
        self.assertEqual(report['titles'], ['Example & Test'])
        self.assertEqual(report['robots_meta'][0]['name'], 'googlebot')
        self.assertIn('Conflicting canonical URLs in this HTML file', report['findings'])

    def test_script_text_is_not_executed(self):
        report = inspector.inspect_html('<script>fetch("https://example.com")</script><h1>Plain <em>Heading</em></h1>')
        self.assertEqual(report['headings'], [{'level': 'h1', 'text': 'Plain Heading'}])
        self.assertEqual(report['jsonld_documents'], [])

    def test_oversized_file_refused(self):
        with tempfile.TemporaryDirectory() as path:
            file = Path(path) / 'large.html'
            file.write_bytes(b' ' * (inspector.MAX_BYTES + 1))
            with self.assertRaises(ValueError):
                inspector.inspect_file(file)


class PackageTests(unittest.TestCase):
    def test_package_contracts(self):
        errors, _ = validator.validate()
        self.assertEqual(errors, [])

    def test_archive_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path) / 'repository'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            source = root / 'upstream/AgriciDaniel--claude-seo/skills/seo-content/SKILL.md'
            source.write_text(source.read_text() + '\nChanged source\n')
            errors, _ = validator.validate(root)
            self.assertTrue(any('SHA-256 mismatch' in error for error in errors))
            self.assertTrue(any('Git blob mismatch' in error for error in errors))

    def test_artifact_links_do_not_hide_broken_active_references(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path) / 'repository'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            result = root / 'evals/results/example.md'
            result.parent.mkdir(exist_ok=True)
            result.write_text('[Example website destination](/services/example/)')
            errors, _ = validator.validate(root)
            self.assertEqual(errors, [])
            entry = root / 'skills/daxable-marketing-search/SKILL.md'
            entry.write_text(entry.read_text() + '\n[Broken reference](absent.md)\n')
            errors, _ = validator.validate(root)
            self.assertTrue(any('absent.md' in error for error in errors))


if __name__ == '__main__':
    unittest.main()
