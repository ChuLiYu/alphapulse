"""Exercise broken authority/link/import cases in isolated repositories."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/verify_context.py"
SPEC = spec_from_file_location("verify_context", SCRIPT)
verifier = module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class ContextVerifierTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for name in verifier.REQUIRED:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# fixture\n", encoding="utf-8")

    def test_valid_fixture_and_external_links(self):
        (self.root / "README.md").write_text(
            "[router](docs/INDEX.md) [web](https://example.com/a) [anchor](#local)\n"
            "```md\n[template](uncreated.md)\n```\n",
            encoding="utf-8",
        )
        self.assertEqual(verifier.collect_errors(self.root), [])

    def test_missing_authority_is_reported(self):
        (self.root / "docs/domain/investment-operations.md").unlink()
        self.assertTrue(
            any("Missing authority" in e for e in verifier.collect_errors(self.root))
        )

    def test_broken_link_fails_cli_with_nonzero_exit(self):
        (self.root / "README.md").write_text(
            "[lost](docs/missing.md)\n", encoding="utf-8"
        )
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Broken local link", result.stderr)

    def test_framework_and_cross_domain_imports_are_rejected(self):
        path = self.root / "src/alphapulse/portfolio/valuation.py"
        for statement in (
            "import sqlalchemy",
            "from fastapi import FastAPI",
            "from alphapulse.api import models",
            "from ..api import models",
        ):
            with self.subTest(statement=statement):
                path.write_text(statement + "\n", encoding="utf-8")
                self.assertTrue(
                    any(
                        "boundary violation" in e
                        for e in verifier.collect_errors(self.root)
                    )
                )

    def test_stale_identity_and_invalid_python_are_reported(self):
        (self.root / "README.md").write_text(
            "alphapulse-mlops-platform", encoding="utf-8"
        )
        (self.root / "src/alphapulse/portfolio/valuation.py").write_text(
            "def (", encoding="utf-8"
        )
        errors = verifier.collect_errors(self.root)
        self.assertTrue(any("Stale active" in e for e in errors))
        self.assertTrue(any("Invalid Python" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
