from os import path, rename
from config import DynamicConfig, StaticConfig
from widget_logic import Widget


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
        if file_list:
            if counter_type == "Čísla":
                self.base_numbering(part1, file_list)
            elif counter_type == "Písmena":
                self.base_alphabet(part1, file_list)
            else:
                print("Neplatný typ počítadla.")
        else:
            print("Žádné soubory k přejmenování.")

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

