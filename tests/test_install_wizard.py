from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


INSTALLER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install.py"
SPEC = importlib.util.spec_from_file_location("pitcrew_install", INSTALLER_PATH)
assert SPEC is not None
pitcrew_install = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = pitcrew_install
SPEC.loader.exec_module(pitcrew_install)


class InstallWizardTest(unittest.TestCase):
    def test_scan_recommends_new_for_missing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "new-project"
            scan = pitcrew_install.scan_repository(target)

            self.assertFalse(scan.exists)
            self.assertEqual(pitcrew_install.suggest_mode(scan, "auto"), "new")

    def test_scan_recommends_append_for_existing_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / ".git").mkdir()
            (target / "README.md").write_text("# Existing\n", encoding="utf-8")
            (target / "pyproject.toml").write_text("[project]\n", encoding="utf-8")

            scan = pitcrew_install.scan_repository(target)

            self.assertTrue(scan.exists)
            self.assertTrue(scan.is_git_repo)
            self.assertTrue(scan.has_readme)
            self.assertIn("Python", scan.languages)
            self.assertEqual(pitcrew_install.suggest_mode(scan, "auto"), "append")

    def test_new_plan_creates_clean_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "fresh"
            options = pitcrew_install.InstallOptions(
                mode="new",
                tools=("claude", "copilot"),
                force=False,
                update_readme=False,
                project_name="Fresh App",
            )

            plan = pitcrew_install.build_plan(pitcrew_install.template_root(), target, options)
            action_paths = {action.path.relative_to(target).as_posix() for action in plan.actions}

            self.assertEqual(plan.mode, "new")
            self.assertIn("AGENTS.md", action_paths)
            self.assertIn("TASKS.md", action_paths)
            self.assertIn(".agent-workflow.md", action_paths)
            self.assertIn("docs/product.md", action_paths)
            self.assertIn(".github/copilot-instructions.md", action_paths)
            self.assertIn(".claude/agents/developer.md", action_paths)
            self.assertIn("src/.gitkeep", action_paths)
            self.assertIn("README.md", action_paths)
            self.assertNotIn("GEMINI.md", action_paths)

    def test_append_plan_skips_existing_files_and_updates_readme(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "AGENTS.md").write_text("# Custom agents\n", encoding="utf-8")
            (target / "README.md").write_text("# Existing\n", encoding="utf-8")
            options = pitcrew_install.InstallOptions(
                mode="append",
                tools=(),
                force=False,
                update_readme=True,
            )

            plan = pitcrew_install.build_plan(pitcrew_install.template_root(), target, options)

            self.assertIn(f"{target / 'AGENTS.md'}: already exists", plan.skipped)
            self.assertTrue(
                any(action.kind == "append" and action.path == target / "README.md"
                    for action in plan.actions)
            )

    def test_apply_plan_writes_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "fresh"
            options = pitcrew_install.InstallOptions(
                mode="new",
                tools=("gemini",),
                force=False,
                update_readme=False,
                project_name="Fresh App",
            )
            plan = pitcrew_install.build_plan(pitcrew_install.template_root(), target, options)

            pitcrew_install.apply_plan(plan)

            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "TASKS.md").exists())
            self.assertTrue((target / "GEMINI.md").exists())
            self.assertFalse((target / "CLAUDE.md").exists())
            self.assertIn("Fresh App", (target / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
