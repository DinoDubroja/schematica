"""Exercise Windows registration without touching the user's real skill folders."""

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
HELPER = REPO / "scripts" / "install-codex.ps1"
REQUIRED = (
    "skills/schematica-preferences/SKILL.md",
    "skills/schematica-preferences/agents/openai.yaml",
    "skills/schematica-preferences/references/example-record.md",
    "skills/schematica-preferences/references/preference-record.md",
    "agents/BEHAVIOR.md",
    "agents/PROJECT_RULES.md",
    "preferences/GENERAL.md",
    "styles/INDEX.md",
    "scripts/PRESENTATION.md",
    "scripts/build_preference_galleries.py",
)


@unittest.skipUnless(os.name == "nt", "Windows junction installer")
class InstallCodexTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="schematica-install-test-")
        self.scratch = Path(self.temporary.name).resolve()
        self.assertEqual(self.scratch.parent, Path(tempfile.gettempdir()).resolve())
        self.shells = [p for p in (shutil.which("pwsh.exe"),) if p]
        self.assertTrue(self.shells, "PowerShell 7 is required on Windows")

    def tearDown(self):
        # Only this test's newly-created temporary directory is recursively removed.
        self.assertEqual(self.scratch.parent, Path(tempfile.gettempdir()).resolve())
        self.temporary.cleanup()

    def fixture(self, index):
        root = self.scratch / str(index)
        library = root / "Schematica download [test]"
        for relative in REQUIRED:
            target = library / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, target)
        shutil.copyfile(HELPER, library / "scripts/install-codex.ps1")
        skills = root / "user skills [test]"
        return library, skills

    def run_helper(self, shell, library, skills, *args, succeeds=True):
        result = subprocess.run(
            [shell, "-NoProfile", "-NonInteractive", "-File",
             str(library / "scripts/install-codex.ps1"),
             "-SkillsDirectory", str(skills), *args],
            capture_output=True, text=True, timeout=20,
        )
        output = result.stdout + result.stderr
        if succeeds:
            self.assertEqual(result.returncode, 0, output)
        else:
            self.assertNotEqual(result.returncode, 0, output)
        return output

    def junction(self, shell, path, target):
        path.parent.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, SCHEMATICA_TEST_LINK=str(path), SCHEMATICA_TEST_TARGET=str(target))
        result = subprocess.run(
            [shell, "-NoProfile", "-NonInteractive", "-Command",
             "New-Item -ItemType Junction -Path $env:SCHEMATICA_TEST_LINK "
             "-Target $env:SCHEMATICA_TEST_TARGET | Out-Null"],
            capture_output=True, text=True, env=env, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @staticmethod
    def hashes(library):
        return {p.relative_to(library).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in library.rglob("*") if p.is_file()}

    def test_install_repeat_check_uninstall_preserves_library(self):
        for i, shell in enumerate(self.shells):
            with self.subTest(shell=shell):
                library, skills = self.fixture(i)
                before = self.hashes(library)
                output = self.run_helper(shell, library, skills, "-Check", succeeds=False)
                self.assertIn("Setup is not complete", output)
                self.assertFalse(skills.exists(), "Check must not create directories")
                self.run_helper(shell, library, skills)
                link = skills / "schematica-preferences"
                self.assertEqual(link.resolve(), (library / "skills/schematica-preferences").resolve())
                self.run_helper(shell, library, skills)
                self.run_helper(shell, library, skills, "-Check")
                self.run_helper(shell, library, skills, "-Uninstall")
                self.assertFalse(link.exists())
                self.run_helper(shell, library, skills, "-Uninstall")
                self.assertEqual(self.hashes(library), before)

    def test_migrate_legacy_link_preserves_both_source_folders(self):
        for i, shell in enumerate(self.shells):
            with self.subTest(shell=shell):
                library, skills = self.fixture(i)
                old_source = library / "skills/schematica-examples"
                old_source.mkdir()
                (old_source / "keep.txt").write_text("preserve legacy source")
                old_link = skills / "schematica-examples"
                self.junction(shell, old_link, old_source)
                before = self.hashes(library)
                self.run_helper(shell, library, skills)
                self.assertFalse(old_link.exists())
                self.run_helper(shell, library, skills, "-Check")
                self.run_helper(shell, library, skills, "-Uninstall")
                self.assertEqual(self.hashes(library), before)

    def test_conflicting_folder_or_foreign_link_is_untouched(self):
        for i, shell in enumerate(self.shells):
            for kind in ("folder", "foreign_link"):
                with self.subTest(shell=shell, kind=kind):
                    library, skills = self.fixture(f"{i}-{kind}")
                    link = skills / "schematica-preferences"
                    if kind == "folder":
                        target = link
                        target.mkdir(parents=True)
                    else:
                        target = self.scratch / f"foreign-{i}"
                        target.mkdir()
                        self.junction(shell, link, target)
                    (target / "keep.txt").write_text("untouched")
                    for args in ((), ("-Check",), ("-Uninstall",)):
                        output = self.run_helper(shell, library, skills, *args, succeeds=False)
                        self.assertIn("ordinary or unsupported" if kind == "folder" else "Another installation", output)
                        self.assertEqual((target / "keep.txt").read_text(), "untouched")
                        self.assertEqual(link.resolve(), target.resolve())

    def test_incomplete_download_and_internal_destination_are_rejected(self):
        for i, shell in enumerate(self.shells):
            with self.subTest(shell=shell):
                library, skills = self.fixture(i)
                output = self.run_helper(shell, library, library / "registration", succeeds=False)
                self.assertIn("must be outside this download", output)
                self.assertFalse((library / "registration").exists())
                (library / "styles/INDEX.md").unlink()
                output = self.run_helper(shell, library, skills, succeeds=False)
                self.assertIn("Incomplete Schematica download", output)
                self.assertFalse(skills.exists())


if __name__ == "__main__":
    unittest.main()
