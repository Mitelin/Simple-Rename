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
class RenameOperation:
    original_path: str
    renamed_path: str


@dataclass(frozen=True)
class RenameResult:
    renamed_paths: list[str]
    operations: list[RenameOperation]


@dataclass(frozen=True)
class RollbackResult:
    current_paths: list[str]
    restored_paths: list[str]
    retryable_operations: list[RenameOperation]
    skipped_messages: list[str]
    restored_count: int
    total_count: int


class RenameService:
    INVALID_WINDOWS_FILENAME_CHARS = set('<>:"/\\|?*')
    RESERVED_WINDOWS_NAMES = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
    }

    def rename_files(self, part1, counter_type, file_list):
        normalized_files = [path.abspath(file_path) for file_path in file_list]
        self._validate_request(normalized_files, part1, counter_type)

        counter_kind = normalize_counter_type(counter_type)
        new_names = self._build_target_names(part1, counter_kind, len(normalized_files))
        self._validate_target_names(new_names)
        rename_plan = self._build_rename_plan(normalized_files, new_names)
        collision = self._find_external_collision(rename_plan)
        if collision:
            raise CollisionError(
                "Nelze pokračovat, protože v cílové složce už existuje jiný soubor s výsledným názvem:\n\n"
                f"{collision}"
            )

        renamed_paths = self._execute_move_plan(
            rename_plan,
            success_label="Přejmenováno",
            failure_message="Přejmenování se nepodařilo bezpečně dokončit. Původní názvy byly obnoveny."
        )
        operations = [
            RenameOperation(original_path=original_path, renamed_path=renamed_path)
            for original_path, renamed_path in rename_plan
        ]
        return RenameResult(renamed_paths=renamed_paths, operations=operations)

    def rollback_files(self, operations):
        if not operations:
            raise ValidationError("Není co vrátit zpět.")

        normalized_operations = [
            RenameOperation(
                original_path=path.abspath(operation.original_path),
                renamed_path=path.abspath(operation.renamed_path),
            )
            for operation in operations
        ]
        eligible_operations, skipped_messages, retryable_operations = self._build_rollback_plan(normalized_operations)
        restored_paths = []

        if eligible_operations:
            restored_paths = self._execute_move_plan(
                [(operation.renamed_path, operation.original_path) for operation in eligible_operations],
                success_label="Obnoveno",
                failure_message="Vrácení posledního přejmenování se nepodařilo bezpečně dokončit. Aktuální názvy byly zachovány."
            )

        restored_targets = {path.normcase(path.abspath(restored_path)) for restored_path in restored_paths}
        current_paths = []
        for operation in normalized_operations:
            normalized_original = path.normcase(path.abspath(operation.original_path))
            if normalized_original in restored_targets:
                current_paths.append(operation.original_path)
            elif path.exists(operation.renamed_path):
                current_paths.append(operation.renamed_path)

        return RollbackResult(
            current_paths=current_paths,
            restored_paths=restored_paths,
            retryable_operations=retryable_operations,
            skipped_messages=skipped_messages,
            restored_count=len(restored_paths),
            total_count=len(normalized_operations),
        )

    def _validate_request(self, file_list, part1, counter_type):
        if not file_list:
            raise ValidationError("Nejdřív vyber soubory k přejmenování.")

        if not part1:
            raise ValidationError("Zadej základ názvu pro přejmenování.")

        missing_files = [file_path for file_path in file_list if not path.exists(file_path)]
        if missing_files:
            missing_preview = "\n".join(missing_files[:5])
            raise ValidationError(
                f"Některé vybrané soubory už neexistují:\n\n{missing_preview}"
            )

        if normalize_counter_type(counter_type) is None:
            raise ValidationError(f"Neznámá metoda číslování: {counter_type}")

    def _validate_target_names(self, new_names):
        for new_name in new_names:
            control_chars = sorted({repr(char)[1:-1] for char in new_name if ord(char) < 32})
            if control_chars:
                control_preview = " ".join(control_chars)
                raise ValidationError(
                    "Výsledný název souboru obsahuje nepovolené řídicí znaky:\n\n"
                    f"{new_name}\n\nNepovolené znaky: {control_preview}"
                )

            stripped_name = new_name.rstrip(" .")
            if stripped_name != new_name:
                raise ValidationError(
                    "Výsledný název souboru nesmí končit mezerou ani tečkou:\n\n"
                    f"{new_name}"
                )

            invalid_chars = sorted({char for char in new_name if char in self.INVALID_WINDOWS_FILENAME_CHARS})
            if invalid_chars:
                invalid_preview = " ".join(invalid_chars)
                raise ValidationError(
                    "Výsledný název souboru obsahuje znaky, které Windows nepovoluje:\n\n"
                    f"{new_name}\n\nNepovolené znaky: {invalid_preview}"
                )

            reserved_name = path.splitext(new_name)[0].upper()
            if reserved_name in self.RESERVED_WINDOWS_NAMES:
                raise ValidationError(
                    "Výsledný název souboru používá rezervovaný název Windows:\n\n"
                    f"{new_name}"
                )

    def _build_rollback_plan(self, operations):
        missing_messages = []
        existing_operations = []

        for operation in operations:
            if not path.exists(operation.renamed_path):
                message = (
                    "Přeskočeno, protože soubor s posledním přejmenovaným názvem už neexistuje:\n"
                    f"{operation.renamed_path}"
                )
                print(message)
                missing_messages.append(message)
                continue

            existing_operations.append(operation)

        eligible_operations = list(existing_operations)
        changed = True
        while changed:
            changed = False
            eligible_sources = {
                path.normcase(path.abspath(operation.renamed_path)) for operation in eligible_operations
            }
            filtered_operations = []

            for operation in eligible_operations:
                normalized_original = path.normcase(path.abspath(operation.original_path))
                if path.exists(operation.original_path) and normalized_original not in eligible_sources:
                    changed = True
                    continue

                filtered_operations.append(operation)

            eligible_operations = filtered_operations

        eligible_originals = {
            path.normcase(path.abspath(operation.original_path)) for operation in eligible_operations
        }
        skipped_messages = list(missing_messages)
        retryable_operations = []

        for operation in existing_operations:
            if operation in eligible_operations:
                continue

            normalized_original = path.normcase(path.abspath(operation.original_path))
            if path.exists(operation.original_path) and normalized_original not in eligible_originals:
                message = (
                    "Přeskočeno, protože původní název je už obsazený jiným souborem:\n"
                    f"{operation.original_path}"
                )
            else:
                message = (
                    "Přeskočeno, protože soubor nelze bezpečně vrátit v aktuálním stavu:\n"
                    f"{operation.renamed_path}"
                )

            print(message)
            skipped_messages.append(message)
            retryable_operations.append(operation)

        return eligible_operations, skipped_messages, retryable_operations

    def _execute_move_plan(self, move_plan, success_label, failure_message):
        staged_moves = []
        final_paths = []
        completed_moves = []

        try:
            for original_path, final_path in move_plan:
                temp_path = self._build_temp_path(original_path)
                os.replace(original_path, temp_path)
                staged_moves.append((original_path, temp_path, final_path))

            for original_path, temp_path, final_path in staged_moves:
                os.replace(temp_path, final_path)
                completed_moves.append((original_path, temp_path, final_path))
                final_paths.append(final_path)
                print(f"{success_label}: {path.basename(original_path)} -> {path.basename(final_path)}")
        except OSError as error:
            self._rollback_moves(staged_moves, completed_moves)
            raise RenameError(f"{failure_message}\n\n{error}") from error

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

