from dataclasses import dataclass, field


@dataclass
class AppState:
    current_lang: str = "CZ"
    selected_files: list[str] = field(default_factory=list)


TEXTS = {
    "EN": {
        "app_title": "Simple Rename",
        "app_subtitle": "Bulk rename files safely with clear ordering and predictable numbering.",
        "files_panel_title": "Selected Files",
        "files_panel_hint": "Reorder the list before renaming, or drag files from Explorer into the white area. The order here decides the final sequence.",
        "settings_panel_title": "Rename Setup",
        "settings_panel_hint": "Choose a base name and numbering style. Existing files outside your selection are protected.",
        "tips_panel_title": "How It Works",
        "tips_line_1": "1. Select files from one or more folders.",
        "tips_line_2": "2. Adjust the order with the move buttons.",
        "tips_line_3": "3. Rename safely in one batch.",
        "log_button": "Open Log",
        "remove_all": "Remove all files",
        "remove_file": "Remove selected",
        "name_label": "File name:",
        "method_label": "Method:",
        "method_tooltip": "Numbers: adds a numeric suffix in the current list order. The width adapts to the number of selected files, so 9 files become 1-9, while 12 files become 01-12.\n\nLetters: adds A, B, C in the current list order and continues as Z, AA, AB, AC like Excel columns.\n\nThe text you enter becomes the base name, the original file extension is kept, and each file stays in its original folder.",
        "move_to_top_button": "Top",
        "flip_order_button": "Reverse",
        "move_to_bottom_button": "Bottom",
        "rename_button": "Rename Files",
        "undo_button": "Undo",
        "select_file_button": "Select Files",
        "rename_success_title": "Rename Complete",
        "rename_success_message": "Renamed {count} files.",
        "undo_success_title": "Undo Complete",
        "undo_success_message": "Restored {count} files.",
        "undo_partial_title": "Undo Partially Complete",
        "undo_partial_message": "Restored {restored} of {total} files, some could not be restored.",
        "undo_nothing_title": "Nothing To Undo",
        "undo_nothing_message": "There is no successful rename batch to undo.",
        "counter_menu_label": {
            "values": ("Numbers", "Letters"),
            "default": "Numbers"
        },
    },
    "CZ": {
        "app_title": "Simple Rename",
        "app_subtitle": "Hromadne prejmenuj soubory bezpecne, prehledne a ve spravnem poradi.",
        "files_panel_title": "Vybrane soubory",
        "files_panel_hint": "Pred prejmenovanim si uprav poradi, nebo sem pretahni soubory z Exploreru. Prave to urci vyslednou sekvenci.",
        "settings_panel_title": "Nastaveni prejmenovani",
        "settings_panel_hint": "Zvol zaklad nazvu a typ sekvence. Existujici cizi soubory zustanou chranene.",
        "tips_panel_title": "Jak to funguje",
        "tips_line_1": "1. Vyber soubory z jedne nebo vice slozek.",
        "tips_line_2": "2. Uprav poradi pomoci tlacitek pro presun.",
        "tips_line_3": "3. Prejmenuj vse bezpecne jednim krokem.",
        "log_button": "Otevrit log",
        "remove_all": "Odebrat všechny soubory",
        "remove_file": "Odebrat vybrané",
        "name_label": "Název souboru:",
        "method_label": "Metoda:",
        "method_tooltip": "Čísla: přidají číselný suffix podle aktuálního pořadí v seznamu. Šířka čísel se mění podle počtu vybraných souborů, takže při 9 souborech bude řada 1-9, ale při 12 souborech 01-12.\n\nPísmena: přidají A, B, C podle aktuálního pořadí v seznamu a pokračují jako Z, AA, AB, AC podobně jako sloupce v Excelu.\n\nText, který zadáš, se použije jako základ názvu, původní přípona souboru zůstane zachovaná a každý soubor zůstane ve své původní složce.",
        "move_to_top_button": "Nahoru",
        "flip_order_button": "Obrátit",
        "move_to_bottom_button": "Dolů",
        "rename_button": "Přejmenuj soubory",
        "undo_button": "Vrátit zpět",
        "select_file_button": "Vyber soubory",
        "rename_success_title": "Přejmenování dokončeno",
        "rename_success_message": "Přejmenováno {count} souborů.",
        "undo_success_title": "Obnovení dokončeno",
        "undo_success_message": "Obnoveno {count} souborů.",
        "undo_partial_title": "Obnovení dokončeno jen částečně",
        "undo_partial_message": "Obnoveno {restored} z {total} souborů, některé nešlo vrátit.",
        "undo_nothing_title": "Není co vrátit zpět",
        "undo_nothing_message": "Není k dispozici žádné poslední úspěšné přejmenování pro vrácení.",
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
