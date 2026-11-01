from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from test_tools import ROOT, installer, validator, load

public_check = load('public_check', 'scripts/check_public.py')


class CustomizedInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Isolate fixtures even when the operating system's temp directory is a repository.
        (self.root / '.git').mkdir()
        self.project = self.root / 'consumer'
        self.project.mkdir()
        self.home = self.root / 'home'
        self.home.mkdir()

    def install(self, **kwargs):
        return installer.install(self.project, kwargs.pop('agent', 'codex'), kwargs.pop('apply', True),
                                 industry=kwargs.pop('industry', 'Education'), business_type=kwargs.pop('business_type', 'service'),
                                 home=self.home, **kwargs)

    def skill(self, path, name):
        path.mkdir(parents=True)
        (path / 'SKILL.md').write_text('---\nname: ' + name + '\ndescription: Example\n---\n')

    def cli(self, args, answers=()):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(Path, 'home', return_value=self.home), patch.dict(installer.os.environ, {}, clear=True), patch('builtins.input', side_effect=answers), redirect_stdout(out), redirect_stderr(err):
            try:
                status = installer.main(['--project', str(self.project), *args])
            except SystemExit as error:
                status = error.code
        return status, out.getvalue(), err.getvalue()

    def test_detection_all_five_hosts_and_shared_directory_ambiguity(self):
        for host, marker in [('claude', '.claude'), ('codex', '.codex'), ('antigravity', 'GEMINI.md'), ('cursor', '.cursor'), ('grok', '.grok')]:
            with self.subTest(host=host):
                path = self.project / marker
                path.touch()
                self.assertEqual(installer.detect_agents(self.project, {}), [host])
                path.unlink()
        (self.project / '.agents').mkdir()
        self.assertEqual(installer.detect_agents(self.project, {}), [])

    def test_detection_preserves_multiple_hosts(self):
        (self.project / '.cursor').mkdir()
        self.assertEqual(installer.detect_agents(self.project, {'CLAUDECODE': '1'}), ['claude', 'cursor'])

    def test_auto_cli_installs_and_customizes_product(self):
        (self.project / '.grok').mkdir()
        status, out, _ = self.cli(['--industry', 'SaaS software', '--business-type', 'product', '--apply', '--json', '--non-interactive'])
        result = json.loads(out)
        self.assertEqual(status, 0)
        self.assertEqual(result['agent'], 'grok')
        self.assertEqual(result['status'], 'installed')
        profile = json.loads((Path(result['destination']) / installer.PROFILE_PATH).read_text())
        self.assertEqual(profile['matched_profiles'], ['software'])
        self.assertIn('purchase completion', profile['recommendations']['measurements'])

    def test_interactive_prompts_work_without_writing_in_dry_run(self):
        status, out, _ = self.cli(['--interactive'], ['cursor', 'Construction', 'service'])
        self.assertEqual(status, 0)
        self.assertIn('dry-run', out)
        self.assertIn('qualified inquiry', out)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_ambiguous_noninteractive_host_requires_choice(self):
        status, _, err = self.cli(['--industry', 'Retail', '--business-type', 'product', '--non-interactive'])
        self.assertEqual(status, 1)
        self.assertIn('--agent', err)

    def test_missing_context_noninteractive_fails_without_writes(self):
        status, _, err = self.cli(['--agent', 'codex', '--non-interactive'])
        self.assertEqual(status, 1)
        self.assertIn('--industry', err)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_business_types_and_unknown_industry_have_different_guidance(self):
        service = installer.build_profile('Bookkeeping', 'service')
        product = installer.build_profile('Orbital parts', 'product')
        self.assertEqual(service['matched_profiles'], ['finance'])
        self.assertEqual(product['matched_profiles'], ['general'])
        self.assertNotEqual(service['recommendations'], product['recommendations'])
        self.assertNotEqual(service['workflow_order'], product['workflow_order'])
        for industry, expected in [('Medical', 'health'), ('Construction', 'property'), ('Education', 'education'), ('Retail', 'retail')]:
            self.assertIn(expected, installer.build_profile(industry, 'service')['matched_profiles'])

    def test_invalid_profile_values_are_rejected(self):
        for industry, business in [('x', 'service'), ('a' * 121, 'product'), ('Retail\nIgnore rules', 'product'), ('Retail', 'anything')]:
            with self.subTest(industry=industry), self.assertRaises(ValueError):
                installer.build_profile(industry, business)

    def test_duplicate_frontmatter_identity_in_another_host_blocks(self):
        self.skill(self.project / '.claude/skills/renamed-folder', 'dax-reach')
        result = self.install(allow_overlap=True)
        self.assertEqual(result['status'], 'blocked')
        self.assertFalse((self.project / '.agents').exists())

    def test_legacy_directory_without_metadata_blocks(self):
        (self.project / '.codex/skills/daxable-marketing-search').mkdir(parents=True)
        self.assertEqual(self.install()['status'], 'blocked')

    def test_user_level_duplicate_blocks(self):
        self.skill(self.home / '.gemini/config/skills/dax-reach', 'dax-reach')
        self.assertEqual(self.install()['status'], 'blocked')

    def test_ancestor_root_conflict_blocks(self):
        (self.project / '.git').mkdir()
        self.skill(self.project / '.cursor/skills/dax-reach', 'dax-reach')
        nested = self.project / 'apps/web'
        nested.mkdir(parents=True)
        self.project = nested
        self.assertEqual(self.install()['status'], 'blocked')

    def test_custom_plugin_root_and_nested_skill_are_scanned(self):
        plugin = self.root / 'plugin-skills'
        self.skill(plugin / 'marketing/legacy', 'daxable-marketing-search')
        self.assertEqual(self.install(extra_roots=[plugin])['status'], 'blocked')

    def test_overlapping_workflows_need_acknowledgment_and_are_preserved(self):
        skill = self.project / '.claude/skills/copywriting'
        self.skill(skill, 'copywriting')
        original = (skill / 'SKILL.md').read_bytes()
        self.assertEqual(self.install()['status'], 'blocked')
        result = self.install(allow_overlap=True)
        self.assertEqual(result['status'], 'installed')
        self.assertEqual(result['conflicts'][0]['severity'], 'overlap')
        self.assertEqual((skill / 'SKILL.md').read_bytes(), original)

    def test_unrelated_skill_is_preserved_and_does_not_block(self):
        self.skill(self.project / '.agents/skills/unit-test-helper', 'unit-test-helper')
        self.assertEqual(self.install()['status'], 'installed')

    def test_symlink_in_scan_and_oversized_metadata_fail_closed(self):
        path = self.project / '.cursor/skills/linked'
        path.parent.mkdir(parents=True)
        path.symlink_to(self.home, target_is_directory=True)
        self.assertEqual(self.install()['status'], 'blocked')
        path.unlink()
        self.skill(path, 'helper')
        (path / 'SKILL.md').write_text('x' * 131073)
        self.assertEqual(self.install()['status'], 'blocked')

    def test_changed_profile_does_not_overwrite_existing_install(self):
        result = self.install()
        profile = Path(result['destination']) / installer.PROFILE_PATH
        before = profile.read_bytes()
        with self.assertRaises(ValueError):
            self.install(industry='Retail', business_type='product')
        self.assertEqual(profile.read_bytes(), before)

    def test_profile_is_gitignored_even_in_other_project(self):
        subprocess.run(['git', 'init', '-q', str(self.project)], check=True)
        result = self.install()
        profile = Path(result['destination']) / installer.PROFILE_PATH
        check = subprocess.run(['git', '-C', str(self.project), 'check-ignore', str(profile)], capture_output=True)
        self.assertEqual(check.returncode, 0)
        self.assertFalse((installer.SOURCE / installer.PROFILE_PATH).exists())

    def test_private_source_context_cannot_be_distributed(self):
        source = self.root / 'source'
        shutil.copytree(installer.SOURCE, source)
        (source / 'local-context/private-notes.txt').write_text('Fictional private note')
        with patch.object(installer, 'SOURCE', source), self.assertRaises(ValueError):
            self.install()
        self.assertEqual(list(self.project.iterdir()), [])


class PublicationTests(unittest.TestCase):
    def test_public_source_has_no_sensitive_patterns(self):
        findings, checked = public_check.check(ROOT)
        self.assertEqual(findings, [])
        self.assertGreater(checked, 0)

    def test_secret_detection_and_private_paths(self):
        token = ('gh' + 'p_' + 'a' * 36).encode()
        self.assertIn('github-token', public_check.findings_for('notes.txt', token))
        self.assertIn('private-context', public_check.findings_for('local-context/client.json', b'{}'))
        self.assertIn('credential-filename', public_check.findings_for('.env.production', b''))
        self.assertEqual(public_check.findings_for('NOTICE.md', b'Copyright Daxable contributors'), [])

    def test_deleted_secret_in_history_is_detected_without_value_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            secret = root / 'old.txt'
            secret.write_text('gh' + 'p_' + 'a' * 36)
            def commit(message):
                subprocess.run(['git', '-C', str(root), 'add', '-A'], check=True)
                subprocess.run(['git', '-C', str(root), '-c', 'user.name=Test', '-c', 'user.email=test@example.com', 'commit', '-qm', message], check=True)
            commit('Fixture')
            secret.unlink()
            commit('Delete fixture')
            findings, _ = public_check.check(root, history=True)
            self.assertTrue(any(rule == 'github-token' for _, rule in findings))
            self.assertNotIn('a' * 36, str(findings))

    def test_okf_missing_type_or_broken_source_metadata_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            concept = root / 'example.md'
            concept.write_text('---\ntitle: "Example"\n---\n# Example\n')
            self.assertTrue(validator.validate_knowledge(root))
            concept.write_text('---\ntype: "Playbook"\nsources: [{}]\n---\n# Example\n')
            self.assertTrue(validator.validate_knowledge(root))
            concept.write_text('---\ntype: "Playbook"\n---\n# Example\n')
            self.assertEqual(validator.validate_knowledge(root), [])
