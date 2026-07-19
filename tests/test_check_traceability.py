#!/usr/bin/env python3
"""Tests for tools/check_traceability.py (issue #12).

The traceability gate must fail closed when CI passes --require-specs
(set when a PR changes product code under src/ - Feature/Fix class,
constitution 3.1) and no spec exists; the pass-on-empty behavior must
survive for chore/local runs; the existing covered/uncovered paths must
keep working.

NOTE for maintainers: fixture strings below build the coverage
annotation by concatenation ("Covers" + ": ...") so this file's own
source never contains the literal pattern the scanner matches -
otherwise, in a cloned project, this template-shipped test would count
as covering that project's real acceptance criteria.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "check_traceability.py"

# Built by concatenation on purpose - see module docstring.
COVERS_AC1 = "Covers" + ": AC-001"


def run_check(cwd, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd, capture_output=True, text=True,
    )


def make_project(tmp, spec=False, covering_test=False):
    root = Path(tmp)
    if spec:
        spec_dir = root / "specs" / "demo"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text(
            "# Demo spec\n\n- AC-001 Given a thing, When poked, Then it beeps.\n",
            encoding="utf-8",
        )
    tests_dir = root / "tests"
    tests_dir.mkdir(exist_ok=True)
    if covering_test:
        (tests_dir / "test_demo.py").write_text(
            f"# {COVERS_AC1}\ndef test_beep():\n    assert True\n",
            encoding="utf-8",
        )
    return root


class NoSpecsBehavior(unittest.TestCase):
    def test_require_specs_fails_closed_when_no_specs_exist(self):
        """Feature/Fix-class run with zero specs must exit nonzero (issue #12)."""
        with tempfile.TemporaryDirectory() as tmp:
            make_project(tmp)
            result = run_check(tmp, "--require-specs")
            self.assertNotEqual(
                result.returncode, 0,
                "--require-specs with no specs must fail closed, got pass:\n"
                + result.stdout + result.stderr,
            )
            self.assertIn("spec", (result.stdout + result.stderr).lower())

    def test_default_still_passes_when_no_specs_exist(self):
        """Chore-class and local runs keep pass-on-empty."""
        with tempfile.TemporaryDirectory() as tmp:
            make_project(tmp)
            result = run_check(tmp)
            self.assertEqual(
                result.returncode, 0,
                "default run with no specs must pass:\n" + result.stdout + result.stderr,
            )


class ExistingPathsStillWork(unittest.TestCase):
    def test_covered_spec_passes_in_both_modes(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_project(tmp, spec=True, covering_test=True)
            for args in ((), ("--require-specs",)):
                result = run_check(tmp, *args)
                self.assertEqual(
                    result.returncode, 0,
                    f"covered spec must pass with args={args}:\n"
                    + result.stdout + result.stderr,
                )

    def test_uncovered_criterion_still_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_project(tmp, spec=True, covering_test=False)
            result = run_check(tmp)
            self.assertNotEqual(
                result.returncode, 0,
                "uncovered criterion must fail:\n" + result.stdout + result.stderr,
            )


if __name__ == "__main__":
    unittest.main()
