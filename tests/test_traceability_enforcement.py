#!/usr/bin/env python3
"""Tests for the --allow-uncovered mode of tools/check_traceability.py (issue #18).

The AIDSEF lifecycle merges a spec at Phase 1 but writes its covering
tests at Phase 4. The default strict gate would turn the first spec-only
pull request red and deadlock it. `--allow-uncovered` lets a spec-only
change (one that touches neither src/ nor tests/) report its criteria as
*pending* and still pass - without weakening any other guarantee:

  - an uncovered criterion under the flag is PENDING, not a failure;
  - a malformed spec (no AC IDs at all) stays fatal even under the flag -
    a missing ID is a mistake, not a not-yet-written test;
  - the flag does NOT bypass --require-specs (no spec at all still fails);
  - a fully covered spec still passes under the flag.

This is a NEW file on purpose (playbook 4.1.2 append-only rule): the
red proof must see net-new failing tests, not edits to the existing
tests/test_check_traceability.py. It reuses that file's helpers by import.

NOTE for maintainers: the covering-annotation fixture is built by
concatenation ("Covers" + ": ...") so this file's own source never
contains the literal pattern the scanner matches - see the sibling
file's module docstring for why that matters in a cloned project.
"""
import tempfile
import unittest
from pathlib import Path

from test_check_traceability import make_project, run_check

# Built by concatenation on purpose - see module docstring.
COVERS_AC1 = "Covers" + ": AC-001"


def make_malformed_spec(tmp):
    """A spec directory whose spec.md carries prose but no AC-### IDs."""
    root = Path(tmp)
    spec_dir = root / "specs" / "malformed"
    spec_dir.mkdir(parents=True)
    (spec_dir / "spec.md").write_text(
        "# Malformed spec\n\n- Given a thing, When poked, Then it beeps.\n",
        encoding="utf-8",
    )
    (root / "tests").mkdir(exist_ok=True)
    return root


class AllowUncoveredMode(unittest.TestCase):
    def test_uncovered_criterion_is_pending_not_failure(self):
        """Spec-only change: an uncovered criterion passes and is reported pending."""
        with tempfile.TemporaryDirectory() as tmp:
            make_project(tmp, spec=True, covering_test=False)
            result = run_check(tmp, "--allow-uncovered")
            self.assertEqual(
                result.returncode, 0,
                "--allow-uncovered must let an uncovered criterion pass:\n"
                + result.stdout + result.stderr,
            )
            self.assertIn(
                "pending", (result.stdout + result.stderr).lower(),
                "the run should name uncovered criteria as pending:\n"
                + result.stdout + result.stderr,
            )

    def test_covered_spec_still_passes_under_flag(self):
        """The flag must not disturb the normal fully-covered pass."""
        with tempfile.TemporaryDirectory() as tmp:
            make_project(tmp, spec=True, covering_test=True)
            result = run_check(tmp, "--allow-uncovered")
            self.assertEqual(
                result.returncode, 0,
                "covered spec must still pass under --allow-uncovered:\n"
                + result.stdout + result.stderr,
            )


class AllowUncoveredDoesNotHideRealFaults(unittest.TestCase):
    def test_malformed_spec_still_fails_under_flag(self):
        """A spec with no AC IDs is a mistake, not a pending test - stays fatal."""
        with tempfile.TemporaryDirectory() as tmp:
            make_malformed_spec(tmp)
            result = run_check(tmp, "--allow-uncovered")
            self.assertNotEqual(
                result.returncode, 0,
                "a spec with no AC IDs must fail even under --allow-uncovered:\n"
                + result.stdout + result.stderr,
            )

    def test_flag_does_not_bypass_require_specs(self):
        """--allow-uncovered forgives pending tests, never a missing spec."""
        with tempfile.TemporaryDirectory() as tmp:
            make_project(tmp)  # no spec at all
            result = run_check(tmp, "--require-specs", "--allow-uncovered")
            self.assertNotEqual(
                result.returncode, 0,
                "--require-specs must still fail closed when combined with "
                "--allow-uncovered:\n" + result.stdout + result.stderr,
            )
            self.assertIn("spec", (result.stdout + result.stderr).lower())


if __name__ == "__main__":
    unittest.main()
