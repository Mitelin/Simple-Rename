import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rename_logic import CollisionError, RenameError, RenameService, ValidationError


class RenameServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.base_path = Path(self.temp_dir.name)
        self.service = RenameService()

    def create_file(self, relative_path, content="data"):
        file_path = self.base_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return str(file_path)

    def test_rejects_empty_file_list(self):
        with self.assertRaises(ValidationError):
            self.service.rename_files("episode", "Numbers", [])

    def test_rejects_missing_files(self):
        missing_path = str(self.base_path / "missing.txt")

        with self.assertRaises(ValidationError) as context:
            self.service.rename_files("episode", "Numbers", [missing_path])

        self.assertIn("neexistují", str(context.exception).lower())

    def test_rejects_unknown_counter_type(self):
        file_path = self.create_file("episode.txt")

        with self.assertRaises(ValidationError) as context:
            self.service.rename_files("episode", "Roman", [file_path])

        self.assertIn("neznámá metoda", str(context.exception).lower())

    def test_renames_with_number_sequence_and_padding(self):
        files = [self.create_file(f"season/file{index}.txt") for index in range(1, 13)]

        result = self.service.rename_files("shot", "Numbers", files)

        expected = [f"shot{index:02d}.txt" for index in range(1, 13)]
        self.assertEqual(expected, [Path(file_path).name for file_path in result.renamed_paths])
        self.assertTrue(all(Path(file_path).exists() for file_path in result.renamed_paths))

    def test_supports_english_counter_labels(self):
        files = [self.create_file("letters/a.txt"), self.create_file("letters/b.txt")]

        result = self.service.rename_files("part-", "Letters", files)

        self.assertEqual(["part-A.txt", "part-B.txt"], [Path(file_path).name for file_path in result.renamed_paths])

    def test_builds_excel_style_letter_sequence(self):
        files = [self.create_file(f"alphabet/file{index}.txt") for index in range(28)]

        result = self.service.rename_files("col-", "Písmena", files)

        expected = [
            "col-A.txt", "col-B.txt", "col-C.txt", "col-D.txt", "col-E.txt", "col-F.txt", "col-G.txt",
            "col-H.txt", "col-I.txt", "col-J.txt", "col-K.txt", "col-L.txt", "col-M.txt", "col-N.txt",
            "col-O.txt", "col-P.txt", "col-Q.txt", "col-R.txt", "col-S.txt", "col-T.txt", "col-U.txt",
            "col-V.txt", "col-W.txt", "col-X.txt", "col-Y.txt", "col-Z.txt", "col-AA.txt", "col-AB.txt",
        ]
        self.assertEqual(expected, [Path(file_path).name for file_path in result.renamed_paths])

    def test_keeps_each_file_in_its_original_directory(self):
        files = [
            self.create_file("folder_a/first.txt"),
            self.create_file("folder_b/second.txt"),
        ]

        result = self.service.rename_files("renamed-", "Numbers", files)

        self.assertEqual(self.base_path / "folder_a" / "renamed-1.txt", Path(result.renamed_paths[0]))
        self.assertEqual(self.base_path / "folder_b" / "renamed-2.txt", Path(result.renamed_paths[1]))

    def test_blocks_external_collision(self):
        selected_file = self.create_file("season/source.txt")
        self.create_file("season/episode1.txt")

        with self.assertRaises(CollisionError) as context:
            self.service.rename_files("episode", "Numbers", [selected_file])

        self.assertIn("episode1.txt", str(context.exception))
        self.assertTrue(Path(selected_file).exists())

    def test_rolls_back_when_final_move_fails(self):
        files = [
            self.create_file("rollback/a.txt", "A"),
            self.create_file("rollback/b.txt", "B"),
        ]
        real_replace = os.replace
        failing_target = str(self.base_path / "rollback" / "episode2.txt")
        failed = {"value": False}

        def flaky_replace(source, destination):
            if destination == failing_target and not failed["value"]:
                failed["value"] = True
                raise OSError("simulated failure")
            return real_replace(source, destination)

        with patch("rename_logic.os.replace", side_effect=flaky_replace):
            with self.assertRaises(RenameError):
                self.service.rename_files("episode", "Numbers", files)

        self.assertTrue((self.base_path / "rollback" / "a.txt").exists())
        self.assertTrue((self.base_path / "rollback" / "b.txt").exists())
        self.assertFalse((self.base_path / "rollback" / "episode1.txt").exists())
        self.assertFalse((self.base_path / "rollback" / "episode2.txt").exists())
        leftovers = list((self.base_path / "rollback").glob(".simple-rename-*"))
        self.assertEqual([], leftovers)


if __name__ == "__main__":
    unittest.main()