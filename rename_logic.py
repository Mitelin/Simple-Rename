# import os
from os import path, rename


# Renames each file based of the logic
def rename_file(old_path, new_name):
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


# Rename files method switch
def rename_files(part1, counter_type, file_list):
    if file_list:
        if counter_type == "Čísla":
            base_numbering(part1, file_list)
        elif counter_type == "Písmena":
            base_alphabet(part1, file_list)
        else:
            print("Neplatný typ počítadla.")
    else:
        print("Žádné soubory k přejmenování.")


# Method for base numbering scheme while the size of numbering 0 , 00 , 000 is based on total file count
def base_numbering(part1, file_list):
    new_file_list = []
    count = 1
    file_count = len(file_list)  # Find the number of selected files
    zero_padding = len(str(file_count))  # Length of the biggest number set the default number of zeroes.
    for file_path in file_list:
        new_name: str = f"{part1}{count:0{zero_padding}d}"
        rename_file(file_path, new_name)
        new_file_list.append(
            path.join(path.dirname(file_path), new_name + path.splitext(file_path)[1]))
        count += 1
    file_list_update(file_list, new_file_list)


# Method for base alphabet acting like numbers (e.g., 'a' -> 'b', 'z' -> 'aa', 'az' -> 'ba', 'zz' -> 'aaa')
def base_alphabet(part1, file_list):
    new_file_list = []
    total_files = len(file_list)
    string_chain = generate_string_chain(total_files)

    for i, file_path in enumerate(file_list):
        new_name = f"{part1}{string_chain[i]}"
        rename_file(file_path, new_name)
        new_file_list.append(
            path.join(path.dirname(file_path), new_name + path.splitext(file_path)[1]))

    file_list_update(file_list, new_file_list)


# Generates a list of alphabetical strings, starting from 'A', 'AA', 'AAA', etc., based on the number of files.
def generate_string_chain(size):
    string_chain = []
    n = 1  # Number of strings in chain

    # Define number of letters based on number of files
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


# calls for updating of file list box after renaming is done
def file_list_update(file_list, new_file_list):
    file_list.clear()
    file_list.extend(new_file_list)
    # update_file_listbox(file_list)
