import importlib.util
import html
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "harden_site", Path(__file__).parents[1] / "scripts" / "harden_site.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SecurityPolicyTests(unittest.TestCase):
    def test_scripts_and_handlers_are_hashed_without_allowing_arbitrary_scripts(self):
        source = ('<html><head><meta charset="utf-8"><script>hello();</script>'
                  '</head><body><button onclick="toggle();">Menu</button></body></html>')
        result = module.harden(source)
        decoded = html.unescape(result)
        self.assertIn(module.script_hash("hello();"), decoded)
        self.assertIn(module.script_hash("toggle();"), decoded)
        self.assertNotIn("script-src 'self' 'unsafe-inline'", decoded)
        self.assertLess(result.index('id="site-security-csp"'), result.index('<script>'))
        self.assertIn('<script>hello();</script>', result)

    def test_hash_changes_with_script_content(self):
        template = '<html><head><meta charset="utf-8"><script>{}</script></head></html>'
        self.assertNotEqual(module.harden(template.format("a();")),
                            module.harden(template.format("b();")))

    def test_repeated_processing_does_not_duplicate_policy(self):
        source = '<html><head><meta charset="utf-8"></head><body>CV</body></html>'
        result = module.harden(module.harden(source))
        self.assertEqual(result.count('id="site-security-csp"'), 1)
        self.assertEqual(result.count('id="site-security-referrer"'), 1)
        self.assertIn('<body>CV</body>', result)


if __name__ == "__main__":
    unittest.main()
