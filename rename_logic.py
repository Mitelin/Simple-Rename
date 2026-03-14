import os
import uuid
from dataclasses import dataclass
from os import path

from config import normalize_counter_type


class RenameError(Exception):
    pass


class ValidationError(RenameError):
    pass


class CollisionError(RenameError):
    pass


@dataclass(frozen=True)
class RenameResult:
    renamed_paths: list[str]


class RenameService:
    def rename_files(self, part1, counter_type, file_list):
        normalized_files = [path.abspath(file_path) for file_path in file_list]
        self._validate_request(normalized_files, counter_type)

        counter_kind = normalize_counter_type(counter_type)
        new_names = self._build_target_names(part1, counter_kind, len(normalized_files))
        rename_plan = self._build_rename_plan(normalized_files, new_names)
        collision = self._find_external_collision(rename_plan)
        if collision:
            raise CollisionError(
                "Nelze pokračovat, protože v cílové složce už existuje jiný soubor s výsledným názvem:\n\n"
                f"{collision}"
            )

        return RenameResult(renamed_paths=self._execute_rename_plan(rename_plan))

    def _validate_request(self, file_list, counter_type):
        if not file_list:
            raise ValidationError("Nejdřív vyber soubory k přejmenování.")

        missing_files = [file_path for file_path in file_list if not path.exists(file_path)]
        if missing_files:
            missing_preview = "\n".join(missing_files[:5])
            raise ValidationError(
                f"Některé vybrané soubory už neexistují:\n\n{missing_preview}"
            )

        if normalize_counter_type(counter_type) is None:
            raise ValidationError(f"Neznámá metoda číslování: {counter_type}")

    def _execute_rename_plan(self, rename_plan):
        staged_moves = []
        final_paths = []
        completed_moves = []

        try:
            for original_path, final_path in rename_plan:
                temp_path = self._build_temp_path(original_path)
                os.replace(original_path, temp_path)
                staged_moves.append((original_path, temp_path, final_path))

            for original_path, temp_path, final_path in staged_moves:
                os.replace(temp_path, final_path)
                completed_moves.append((original_path, temp_path, final_path))
                final_paths.append(final_path)
                print(f"Přejmenováno: {path.basename(original_path)} -> {path.basename(final_path)}")
        except OSError as error:
            self._rollback_moves(staged_moves, completed_moves)
            raise RenameError(
                f"Přejmenování se nepodařilo bezpečně dokončit. Původní názvy byly obnoveny.\n\n{error}"
            ) from error

        return final_paths

    def _build_target_names(self, part1, counter_kind, total_files):
        if counter_kind == "numbers":
            width = max(1, len(str(total_files)))
            return [f"{part1}{str(index + 1).zfill(width)}" for index in range(total_files)]

        return [f"{part1}{self._index_to_excel_label(index)}" for index in range(total_files)]

    def _build_rename_plan(self, file_list, new_names):
        rename_plan = []
        for original_path, new_name in zip(file_list, new_names):
            directory = path.dirname(original_path)
            extension = path.splitext(original_path)[1]
            final_path = path.join(directory, new_name + extension)
            rename_plan.append((original_path, final_path))
        return rename_plan

    def _find_external_collision(self, rename_plan):
        original_paths = {path.normcase(path.abspath(old_path)) for old_path, _ in rename_plan}
        planned_targets = set()

        for _, final_path in rename_plan:
            normalized_target = path.normcase(path.abspath(final_path))
            if normalized_target in planned_targets:
                return final_path
            planned_targets.add(normalized_target)

            if path.exists(final_path) and normalized_target not in original_paths:
                return final_path

        return None

    def _build_temp_path(self, original_path):
        directory = path.dirname(original_path)
        extension = path.splitext(original_path)[1]

        while True:
            candidate = path.join(directory, f".simple-rename-{uuid.uuid4().hex}{extension}")
            if not path.exists(candidate):
                return candidate

    def _rollback_moves(self, staged_moves, completed_moves):
        for original_path, _, final_path in reversed(completed_moves):
            if path.exists(final_path) and not path.exists(original_path):
                try:
                    os.replace(final_path, original_path)
                except OSError:
                    pass

        for original_path, temp_path, _ in reversed(staged_moves):
            if path.exists(temp_path) and not path.exists(original_path):
                try:
                    os.replace(temp_path, original_path)
                except OSError:
                    pass

    def _index_to_excel_label(self, index):
        label = ""
        current = index + 1

        while current > 0:
            current, remainder = divmod(current - 1, 26)
            label = chr(ord('A') + remainder) + label

        return label

