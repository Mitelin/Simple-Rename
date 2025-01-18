# Main global variables
class DynamicConfig:
    _instance = None

    # Proměnné pro widgety
    counter_menu = None
    file_listbox = None
    toggle_button = None
    remove_all_button = None
    remove_button = None
    select_file_button = None
    part1_label = None
    part2_label = None
    move_up_button = None
    move_down_button = None
    move_to_top_button = None
    move_to_bottom_button = None
    rename_button = None
    counter_type = None
    part1_entry = None
    open_log_button = None
    current_lang = "CZ"
    file_list = []

    def __init__(self):
        if not DynamicConfig._instance:
            DynamicConfig._instance = self
        else:
            raise Exception("Instance already exists, use get_instance() to access it.")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls()
        return cls._instance


# Text variables for multilanguage support
class StaticConfig:
    _instance = None

    # Texty pro více jazyků
    texts = {
        "EN": {
            "remove_all": "Remove all files",
            "remove_file": "   Remove file    ",
            "name_label": "File name:  ",
            "method_label": "Method:",
            "move_to_top_button": " Top  ",
            "move_to_bottom_button": "Bottom",
            "rename_button": "     Rename Files      ",
            "select_file_button": "   Select Files    ",
            "counter_menu_label": {
                "values": ("Numbers", "Letters"),
                "default": "Numbers"},
        },
        "CZ": {
            "remove_all": "Odebrat všechny soubory",
            "remove_file": "Odebrat soubor",
            "name_label": "Název souboru:",
            "method_label": "Metoda:",
            "move_to_top_button": "Nahoru",
            "move_to_bottom_button": "Dolů",
            "rename_button": "Přejmenuj Soubory",
            "select_file_button": "Vyber soubory",
            "counter_menu_label": {
                "values": ("Čísla", "Písmena"),
                "default": "Čísla"},
        }
    }

    def __init__(self):
        if not StaticConfig._instance:
            StaticConfig._instance = self
        else:
            raise Exception("Instance already exists, use get_instance() to access it.")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls()
        return cls._instance
