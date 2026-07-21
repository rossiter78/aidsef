#!/usr/bin/env python3
"""Tests for the project/ workspace layout (issue #22, feature project-workspace).

These assert against the REAL repository tree (not a temp fixture): the
migration creates project/ with inputs/, specs/, adr/, traceability/, and
retros/, each carrying a plain-language README that says who writes there
and during which lifecycle phase (AC-001), plus the inputs README's
absorption rules (AC-006, AC-009).

NOTE for maintainers: the coverage annotations below are built by
concatenation ("Covers" + ": AC-...") so this file's own source never
contains the literal pattern the traceability scanner matches -
otherwise, in a cloned project, this template-shipped test would count
as covering that project's real acceptance criteria. This mirrors the
convention in tests/test_check_traceability.py.
"""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT = REPO_ROOT / "project"
INPUTS_README = PROJECT / "inputs" / "README.md"

# Built by concatenation on purpose - see module docstring.
COVERS_AC001 = "Covers" + ": AC-001"
COVERS_AC006 = "Covers" + ": AC-006"
COVERS_AC009 = "Covers" + ": AC-009"

# The five subdirectories AC-001 requires, each with a README.
SUBDIRS = ("inputs", "specs", "adr", "traceability", "retros")

# A README must name at least one role/actor who writes there. Kept broad
# so wording is not brittle: any one of these signals satisfies the check.
ROLE_SIGNALS = (
    "analyst", "architect", "retro", "coder", "planner", "reviewer",
    "ci", "human", "agent", "you", "project",
)


def read_lower(path):
    return path.read_text(encoding="utf-8").lower()


class WorkspaceStructure(unittest.TestCase):
    """AC-001: project/ holds the five subdirs, each with a plain-language
    README stating who writes there and during which lifecycle phase."""

    # COVERS_AC001

    def test_project_directory_exists(self):
        self.assertTrue(
            PROJECT.is_dir(),
            f"expected a project/ directory at {PROJECT}",
        )

    def test_each_subdir_exists_with_readme(self):
        for name in SUBDIRS:
            sub = PROJECT / name
            with self.subTest(subdir=name):
                self.assertTrue(sub.is_dir(), f"missing project/{name}/")
                readme = sub / "README.md"
                self.assertTrue(
                    readme.is_file(), f"missing project/{name}/README.md"
                )

    def test_each_readme_is_non_trivial(self):
        for name in SUBDIRS:
            readme = PROJECT / name / "README.md"
            with self.subTest(subdir=name):
                if not readme.is_file():
                    self.skipTest(f"project/{name}/README.md not present")
                text = readme.read_text(encoding="utf-8").strip()
                self.assertGreaterEqual(
                    len(text), 80,
                    f"project/{name}/README.md is too short to explain "
                    "who writes there and when",
                )

    def test_each_readme_names_who_writes_there(self):
        for name in SUBDIRS:
            readme = PROJECT / name / "README.md"
            with self.subTest(subdir=name):
                if not readme.is_file():
                    self.skipTest(f"project/{name}/README.md not present")
                lower = read_lower(readme)
                self.assertTrue(
                    any(sig in lower for sig in ROLE_SIGNALS),
                    f"project/{name}/README.md names no role/actor who "
                    f"writes there (looked for any of {ROLE_SIGNALS})",
                )

    def test_each_readme_states_lifecycle_phase(self):
        for name in SUBDIRS:
            readme = PROJECT / name / "README.md"
            with self.subTest(subdir=name):
                if not readme.is_file():
                    self.skipTest(f"project/{name}/README.md not present")
                lower = read_lower(readme)
                self.assertIn(
                    "phase", lower,
                    f"project/{name}/README.md does not mention the "
                    "lifecycle phase it belongs to",
                )


class InputsReadmeExplainsAbsorption(unittest.TestCase):
    """AC-006: inputs README explains intake, when agents read inputs,
    that specs cite what they used, and that the merged spec governs."""

    # COVERS_AC006

    def test_inputs_readme_exists(self):
        self.assertTrue(
            INPUTS_README.is_file(),
            f"expected project/inputs/README.md at {INPUTS_README}",
        )

    def test_inputs_readme_describes_intake(self):
        if not INPUTS_README.is_file():
            self.skipTest("project/inputs/README.md not present")
        lower = read_lower(INPUTS_README)
        self.assertTrue(
            "pre-existing" in lower or "existing" in lower or "prior" in lower,
            "inputs README should say to put pre-existing/prior documents here",
        )

    def test_inputs_readme_says_agents_read_during_spec_and_design(self):
        if not INPUTS_README.is_file():
            self.skipTest("project/inputs/README.md not present")
        lower = read_lower(INPUTS_README)
        self.assertIn("read", lower, "inputs README should say agents read them")
        self.assertIn(
            "spec", lower,
            "inputs README should say inputs are read during spec",
        )
        self.assertIn(
            "design", lower,
            "inputs README should say inputs are read during design",
        )

    def test_inputs_readme_says_specs_cite_what_they_used(self):
        if not INPUTS_README.is_file():
            self.skipTest("project/inputs/README.md not present")
        lower = read_lower(INPUTS_README)
        self.assertTrue(
            "cite" in lower or "cited" in lower or "source" in lower,
            "inputs README should say specs cite (Sources) what they used",
        )

    def test_inputs_readme_says_merged_spec_governs(self):
        if not INPUTS_README.is_file():
            self.skipTest("project/inputs/README.md not present")
        lower = read_lower(INPUTS_README)
        self.assertIn(
            "govern", lower,
            "inputs README should state that the merged spec governs "
            "once it covers the material",
        )


class InputsReadmeStatesAbsorptionRule(unittest.TestCase):
    """AC-009 (inputs-README half): the precedence rule is stated verbatim
    in project/inputs/README.md."""

    # COVERS_AC009

    def test_inputs_readme_states_merged_spec_wins_rule(self):
        if not INPUTS_README.is_file():
            self.fail(f"expected project/inputs/README.md at {INPUTS_README}")
        lower = read_lower(INPUTS_README)
        self.assertIn(
            "merged spec wins", lower,
            'inputs README must state the rule "the merged spec wins; '
            'inputs are historical once absorbed"',
        )
        self.assertIn(
            "historical", lower,
            "inputs README must say inputs are historical once absorbed",
        )


if __name__ == "__main__":
    unittest.main()
