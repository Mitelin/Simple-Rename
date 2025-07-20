from os import path, rename
from config import DynamicConfig, StaticConfig
from widget_logic import Widget
import uuid, os
from tkinter import messagebox
from os import path, rename
from config import DynamicConfig, StaticConfig
from widget_logic import Widget
import uuid, os

class Rename(DynamicConfig, StaticConfig):
    def __init__(self):
        super().__init__()

    def rename_file(self, old_path, new_name):
        try:
            directory = path.dirname(old_path)
            extension = path.splitext(old_path)[1]
            new_path = path.join(directory, new_name + extension)
            rename(old_path, new_path)
            print(f"Soubor byl úspěšně přejmenován na {new_path}.")
        except FileNotFoundError:
            print(f"Soubor {old_path} nebyl nalezen.")
        except PermissionError:
            print(f"Nemáte oprávnění k přejmenování souboru {old_path}.")
        except Exception as e:
            print(f"Nastala chyba: {e}")

    def rename_files(self, part1, counter_type, file_list):
        if not file_list:
            print("[CHYBA] Seznam souborů je prázdný.")
            return []

        # 1️⃣ Vygeneruj cílové názvy podle číslování s paddingem
        width = len(str(len(file_list)))
        if counter_type == "Čísla":
            new_names = [f"{part1}{str(i + 1).zfill(width)}" for i in range(len(file_list))]
        elif counter_type == "Písmena":
            new_names = [f"{part1}{chr(65 + i)}" for i in range(len(file_list))]
        else:
            print("[CHYBA] Neplatný typ číslování.")
            return []

        # 2️⃣ Kontrola kolizí mimo seznam
        directory = path.dirname(file_list[0])
        existing_files = set(os.listdir(directory))
        extensions = [path.splitext(p)[1] for p in file_list]
        intended_targets = {new + ext for new, ext in zip(new_names, extensions)}
        file_names_in_list = {path.basename(p) for p in file_list}

        for target in intended_targets:
            if target in existing_files and target not in file_names_in_list:
                messagebox.showerror(
                    "Kolize souboru",
                    f"Nelze přejmenovat: v cílové složce už existuje soubor '{target}', který není součástí vybraného seznamu."
                )
                return []

        # 3️⃣ Fáze 1 – přejmenuj vše na dočasná unikátní jména
        temp_map = {}
        for original_path in file_list:
            ext = path.splitext(original_path)[1]
            temp_name = str(uuid.uuid4()) + ext
            temp_path = path.join(directory, temp_name)
            rename(original_path, temp_path)
            temp_map[temp_path] = original_path

        # 4️⃣ Fáze 2 – přejmenuj na finální jména (řeší kolize v rámci seznamu)
        final_paths = []
        for temp_path, new_name in zip(temp_map.keys(), new_names):
            ext = path.splitext(temp_path)[1]
            final_path = path.join(directory, new_name + ext)

            if path.exists(final_path):
                backup_path = path.join(directory, new_name + "_X" + ext)
                counter = 2
                while path.exists(backup_path):
                    backup_path = path.join(directory, f"{new_name}_X{counter}{ext}")
                    counter += 1
                rename(final_path, backup_path)
                print(f"[KOLIZE] Přesunuto: {final_path} → {backup_path}")

            rename(temp_path, final_path)
            final_paths.append(final_path)

            # ✅ Přehledný zápis do logu
            original_name = os.path.basename(temp_map[temp_path])
            new_name = os.path.basename(final_path)
            print(f"Přejmenováno: {original_name} -> {new_name}")

        return final_paths


    def base_numbering(self, part1, file_list):
        new_file_list = []
        count = 1
        file_count = len(file_list)
        zero_padding = len(str(file_count))
        for file_path in file_list:
            new_name: str = f"{part1}{count:0{zero_padding}d}"
            self.rename_file(file_path, new_name)
            new_file_list.append(
                path.join(path.dirname(file_path), new_name + path.splitext(file_path)[1]))
            count += 1
        self.file_list_update(file_list, new_file_list)

    def base_alphabet(self, part1, file_list):
        new_file_list = []
        total_files = len(file_list)
        string_chain = self.generate_string_chain(total_files)

        for i, file_path in enumerate(file_list):
            new_name = f"{part1}{string_chain[i]}"
            self.rename_file(file_path, new_name)
            new_file_list.append(
                path.join(path.dirname(file_path), new_name + path.splitext(file_path)[1]))

        self.file_list_update(file_list, new_file_list)

    def generate_string_chain(self, size):
        string_chain = []
        n = 1
        while 26 * (26 ** (n - 1)) < size:
            n += 1

        for i in range(size):
            chain = ""
            num = i
            for _ in range(n):
                chain = chr(num % 26 + ord('A')) + chain
                num //= 26
            string_chain.append(chain)

        return string_chain

    def file_list_update(self, file_list, new_file_list):
        if not isinstance(file_list, list):
            raise ValueError("file_list musí být seznam.")
        file_list.clear()
        file_list.extend(new_file_list)
        self.update_file_listbox(file_list)

