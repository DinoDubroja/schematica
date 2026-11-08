"""Behavior checks for authored variants and generated gallery preservation.

Run: python -m unittest discover -s tests
"""
from pathlib import Path
import sys
import shutil
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_preference_galleries import Builder, GalleryError


class PreferenceGalleryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.leaf = self.root / 'preferences/connections/crossings/README.md'
        self.category = self.root / 'preferences/connections/README.md'
        self.write('README.md', '# Example\n\n<!-- preference-gallery:start level=3 -->\n<!-- preference-gallery:end -->\n')
        self.write('preferences/README.md', '# Preferences\n\n<!-- preference-gallery:start level=2 -->\n<!-- preference-gallery:end -->\n')
        self.write('preferences/GENERAL.md', '[Crossings](connections/crossings/RULE.md)\n')
        self.write('preferences/connections/README.md', '# Connections\n\nManual intro.\n\n<!-- preference-representative: crossings/README.md -->\n<!-- preference-gallery:start level=2 -->\n<!-- preference-gallery:end -->\n\nManual ending.\n')
        self.write('preferences/connections/crossings/RULE.md', '# Crossings\n\nID: G-TEST\nStatus: accepted\n')
        for name in ('good-label.svg', 'bad-label.svg'):
            self.write('preferences/assets/' + name, '<svg/>')
        for stem in ('good', 'bridge', 'bad'):
            for extension in ('-light.svg', '-dark.svg', '.png'):
                self.write('preferences/connections/crossings/' + stem + extension, 'fixture')
        self.write('preferences/connections/crossings/README.md', self.variants())

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    @staticmethod
    def images(stem, marker):
        return (f'<!-- preference-{marker}:start -->\n' +
                '\n'.join(f'<a href="{stem}-{theme}.svg#gh-{theme}-mode-only"><img src="{stem}-{theme}.svg" alt="Example"></a>' for theme in ('light', 'dark')) +
                f'\n<!-- preference-{marker}:end -->')

    @staticmethod
    def downloads(stem):
        return f'<a href="{stem}.png">PNG</a> · <a href="{stem}-light.svg">Light</a> · <a href="{stem}-dark.svg">Dark</a>'

    def variants(self):
        return ('<!-- preference-visual:start -->\n# Crossings\n\n'
                '<!-- preference-comparison:start -->\n<table>\n'
                '<tr><th><img src="../../assets/good-label.svg" alt="Good"></th>'
                '<th><img src="../../assets/bad-label.svg" alt="Bad"></th></tr>\n'
                f'<tr><td>{self.images("good", "good")}</td><td>{self.images("bad", "bad")}</td></tr>\n'
                '<tr><td>straight wire crossing (default); bridged wire crossing.</td><td>Gap.</td></tr>\n'
                f'<tr><td>{self.downloads("good")}</td><td>{self.downloads("bad")}</td></tr>\n'
                '</table>\n<!-- preference-comparison:end -->\n'
                '<!-- preference-visual:end -->\n\n[Back](../README.md)\n')

    def mutate(self, old, new):
        self.leaf.write_text(self.leaf.read_text(encoding='utf-8').replace(old, new), encoding='utf-8')

    def test_variants_propagate_with_default_preview_and_stable_manual_text(self):
        before = self.category.read_text(encoding='utf-8')
        self.category.write_bytes(before.replace('\n', '\r\n').encode())
        before = self.category.read_bytes()
        self.assertTrue(Builder(self.root).build(True))
        self.assertEqual(before, self.category.read_bytes())
        Builder(self.root).build()
        text = self.category.read_text(encoding='utf-8')
        self.assertIn('straight wire crossing (default)', text)
        self.assertIn('crossings/good-dark.svg#gh-dark-mode-only', text)
        self.assertLess(text.index('alt="Good"'), text.index('alt="Bad"'))
        self.assertIn('<td>straight wire crossing (default); bridged wire crossing.</td><td>Gap.</td>', text)
        self.assertIn('## [Crossings](crossings/README.md)', text)
        after = self.category.read_bytes()
        for marker, part in [(b'<!-- preference-gallery:start level=2 -->', 0), (b'<!-- preference-gallery:end -->', 1)]:
            self.assertEqual(before.split(marker)[part], after.split(marker)[part])
        main = (self.root / 'README.md').read_text(encoding='utf-8')
        self.assertIn('crossings/good-light.svg', main)
        self.assertNotIn('bridge-light.svg', main)
        self.assertFalse(Builder(self.root).build(True))

    def test_invalid_variants_reject_without_writing(self):
        cases = [
            ('alt="Good"', 'alt="Bad"', 'Good left and Bad right'),
            ('<td>Gap.</td>', '', 'four rows of two'),
            ('#gh-dark-mode-only"><img src="good-dark.svg"', '#other"><img src="good-dark.svg"', 'good preview missing dark'),
            ('<!-- preference-good:end -->', '', 'good marker pair'),
            ('preference-comparison:', 'preference-variants:', 'inside the Good column'),
        ]
        for old, new, error in cases:
            with self.subTest(error=error):
                self.leaf.write_text(self.variants().replace(old, new), encoding='utf-8')
                before = self.category.read_bytes()
                with self.assertRaisesRegex(GalleryError, error):
                    Builder(self.root).build()
                self.assertEqual(before, self.category.read_bytes())

    def test_missing_comparison_asset_rejects_before_writing(self):
        (self.leaf.parent / 'bad-dark.svg').unlink()
        before = self.category.read_bytes()
        with self.assertRaisesRegex(GalleryError, 'missing reference'):
            Builder(self.root).build()
        self.assertEqual(before, self.category.read_bytes())

    def test_optional_bad_and_inactive_rules(self):
        text = ('<!-- preference-visual:start -->\n# Crossings\n\n'
                '## ![Good](../../assets/good-label.svg)\n' + self.images('good', 'good') +
                '\n' + self.downloads('good') + '\n<!-- preference-visual:end -->\n')
        self.leaf.write_text(text, encoding='utf-8')
        for status in ('proposed', 'deferred', 'rejected', 'superseded'):
            self.write(f'preferences/connections/{status}/RULE.md', f'# Pending\nID: G-{status}\nStatus: {status}\n')
        Builder(self.root).build()
        self.assertNotIn('Pending', self.category.read_text(encoding='utf-8'))
        self.assertFalse(Builder(self.root).build(True))

    def test_nested_category_rebases_variants_and_keeps_representative(self):
        routing = self.category.parent / 'routing'
        routing.mkdir()
        shutil.move(str(self.leaf.parent), routing / 'crossings')
        moved = routing / 'crossings/README.md'
        moved.write_text(moved.read_text(encoding='utf-8').replace('../../assets/', '../../../assets/'), encoding='utf-8')
        self.write('preferences/connections/routing/README.md', '# Routing\n\n<!-- preference-representative: crossings/README.md -->\n<!-- preference-gallery:start level=2 -->\n<!-- preference-gallery:end -->\n')
        self.category.write_text(self.category.read_text(encoding='utf-8').replace('preference-representative: crossings/', 'preference-representative: routing/crossings/'), encoding='utf-8')
        self.write('preferences/GENERAL.md', '[Crossings](connections/routing/crossings/RULE.md)\n')
        Builder(self.root).build()
        self.assertIn('## [Routing](routing/README.md)', self.category.read_text(encoding='utf-8'))
        text = (routing / 'README.md').read_text(encoding='utf-8')
        self.assertIn('bridged wire crossing', text)
        self.assertIn('crossings/good-dark.svg#gh-dark-mode-only', text)
        self.assertIn('../../assets/good-label.svg', text)
        self.assertFalse(Builder(self.root).build(True))

    def test_missing_anchor_rejects_before_writing(self):
        with self.leaf.open('a', encoding='utf-8') as file:
            file.write('\n[Details](RULE.md#missing)\n')
        before = self.category.read_bytes()
        with self.assertRaisesRegex(GalleryError, 'missing anchor'):
            Builder(self.root).build()
        self.assertEqual(before, self.category.read_bytes())

    def test_single_good_and_good_bad_comparison_still_work(self):
        good = self.images('good', 'good')
        self.leaf.write_text(f'<!-- preference-visual:start -->\n# Crossings\n\n## ![Good](../../assets/good-label.svg)\n{good}\n{self.downloads("good")}\n<!-- preference-visual:end -->', encoding='utf-8')
        Builder(self.root).build()
        comparison = ('<!-- preference-visual:start -->\n# Crossings\n\n<!-- preference-comparison:start -->\n<table>'
                      '<tr><th><img src="../../assets/good-label.svg" alt="Good"></th><th><img src="../../assets/bad-label.svg" alt="Bad"></th></tr>'
                      f'<tr><td>{good}</td><td>{self.images("bad", "bad")}</td></tr>'
                      '<tr><td>Clear.</td><td>Ambiguous.</td></tr>'
                      f'<tr><td>{self.downloads("good")}</td><td>{self.downloads("bad")}</td></tr>'
                      '</table>\n<!-- preference-comparison:end -->\n<!-- preference-visual:end -->')
        self.leaf.write_text(comparison, encoding='utf-8')
        Builder(self.root).build()
        self.assertFalse(Builder(self.root).build(True))


if __name__ == '__main__':
    unittest.main()
