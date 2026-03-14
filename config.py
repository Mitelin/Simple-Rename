from dataclasses import dataclass, field


@dataclass
class AppState:
    current_lang: str = "CZ"
    selected_files: list[str] = field(default_factory=list)


TEXTS = {
    "EN": {
        "remove_all": "Remove all files",
        "remove_file": "Remove selected",
        "name_label": "File name:",
        "method_label": "Method:",
        "move_to_top_button": "Top",
        "move_to_bottom_button": "Bottom",
        "rename_button": "Rename Files",
        "select_file_button": "Select Files",
        "counter_menu_label": {
            "values": ("Numbers", "Letters"),
            "default": "Numbers"
        },
    },
    "CZ": {
        "remove_all": "Odebrat všechny soubory",
        "remove_file": "Odebrat vybrané",
        "name_label": "Název souboru:",
        "method_label": "Metoda:",
        "move_to_top_button": "Nahoru",
        "move_to_bottom_button": "Dolů",
        "rename_button": "Přejmenuj soubory",
        "select_file_button": "Vyber soubory",
        "counter_menu_label": {
            "values": ("Čísla", "Písmena"),
            "default": "Čísla"
        },
    }
}

COUNTER_TYPE_ALIASES = {
    "Čísla": "numbers",
    "Numbers": "numbers",
    "Písmena": "letters",
    "Letters": "letters",
}

COUNTER_TYPE_LABELS = {
    "CZ": {
        "numbers": "Čísla",
        "letters": "Písmena",
    },
    "EN": {
        "numbers": "Numbers",
        "letters": "Letters",
    },
}


def normalize_counter_type(value):
    return COUNTER_TYPE_ALIASES.get(value)


def get_counter_type_label(counter_kind, lang):
    normalized_kind = counter_kind if counter_kind in {"numbers", "letters"} else "numbers"
    return COUNTER_TYPE_LABELS[lang][normalized_kind]
