from config import TEXTS, get_counter_type_label, normalize_counter_type
from tkinter import ttk, filedialog
import tkinter as tk
from os import path
from collections import Counter
from log import Log
import sys


class WidgetController:
    def __init__(self, state):
        self.state = state
        self.app_title_label = None
        self.app_subtitle_label = None
        self.files_panel_title_label = None
        self.files_panel_hint_label = None
        self.settings_panel_title_label = None
        self.settings_panel_hint_label = None
        self.tips_panel_title_label = None
        self.tips_line_1_label = None
        self.tips_line_2_label = None
        self.tips_line_3_label = None
        self.counter_menu = None
        self.file_listbox = None
        self.toggle_button = None
        self.remove_all_button = None
        self.remove_button = None
        self.select_file_button = None
        self.part1_label = None
        self.part1_entry = None
        self.part2_label = None
        self.method_info_button = None
        self.move_to_top_button = None
        self.flip_order_button = None
        self.move_up_button = None
        self.move_down_button = None
        self.move_to_bottom_button = None
        self.rename_button = None
        self.counter_type = None
        self.open_log_button = None

    def select_files(self, file_listbox, part1_entry):
        selected_files = filedialog.askopenfilenames(title="Vyber soubory")

        if selected_files:
            self.state.selected_files = list(selected_files)
            self.update_file_listbox(self.state.selected_files)
            self.prepopulate_entry(selected_files, part1_entry)

    def parse_drop_data(self, drop_data, splitlist):
        if not drop_data:
            return []

        try:
            return list(splitlist(drop_data))
        except tk.TclError:
            return [drop_data]

    def add_dropped_files(self, dropped_files, part1_entry):
        merged_files = list(self.state.selected_files)
        known_files = {path.normcase(path.abspath(file_path)) for file_path in merged_files}

        for file_path in dropped_files:
            absolute_path = path.abspath(file_path)
            normalized_path = path.normcase(absolute_path)
            if normalized_path in known_files or not path.isfile(absolute_path):
                continue

            merged_files.append(absolute_path)
            known_files.add(normalized_path)

        if merged_files == self.state.selected_files:
            return

        self.update_file_listbox(merged_files)
        self.prepopulate_entry(merged_files, part1_entry)

    def handle_file_drop(self, event, part1_entry):
        dropped_files = self.parse_drop_data(event.data, self.file_listbox.tk.splitlist)
        self.add_dropped_files(dropped_files, part1_entry)
        return "break"

    # Function for prepopulate entry
    def prepopulate_entry(self, file_list, part1_entry):
        common_prefix = self.get_common_prefix(file_list)
        part1_entry.delete(0, tk.END)
        part1_entry.insert(0, common_prefix)

    # Function for updating and displaying selected files into the filebox

    def update_file_listbox(self, file_list, selected_indices=None):
        self.file_listbox.delete(0, tk.END)
        self.state.selected_files = list(file_list)
        for label in self.build_display_labels(self.state.selected_files):
            self.file_listbox.insert(tk.END, label)

        if selected_indices is not None:
            for index in selected_indices:
                self.file_listbox.select_set(index)

    def build_display_labels(self, file_list):
        basenames = [path.basename(file_path) for file_path in file_list]
        basename_counts = Counter(basenames)
        labels = []

        for file_path in file_list:
            basename = path.basename(file_path)
            if basename_counts[basename] == 1:
                labels.append(basename)
                continue

            parent_name = path.basename(path.dirname(file_path)) or path.dirname(file_path)
            labels.append(f"{basename} [{parent_name}]")

        return labels

    # Short function for getting the common name of all selected files
    def get_common_prefix(self, file_list):
        if not file_list:
            return ""

        base_names = [path.splitext(path.basename(file))[0] for file in file_list]
        if len(base_names) == 1:
            return base_names[0]

        prefix = path.commonprefix(base_names)
        if prefix:
            return prefix

        else:
            # If there is no common prefix return the first selected file name
            return base_names[0]

    # Removing all files from selection box and clearing the common prefix
    def remove_all_files(self, part1_entry):
        self.state.selected_files = []
        self.file_listbox.delete(0, tk.END)
        part1_entry.delete(0, tk.END)

    # Remove selected files
    def remove_selected(self, file_listbox, part1_entry):
        selected_indices = set(file_listbox.curselection())

        if not selected_indices:
            return

        self.state.selected_files = [
            file_path for index, file_path in enumerate(self.state.selected_files) if index not in selected_indices
        ]
        self.update_file_listbox(self.state.selected_files)

        if not self.state.selected_files:
            part1_entry.delete(0, tk.END)

    # Move selected files one up
    def move_up(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            return

        selected_set = set(selected_indices)
        items = list(self.state.selected_files)
        new_selection = []

        for index in selected_indices:
            if index > 0 and (index - 1) not in selected_set:
                items[index - 1], items[index] = items[index], items[index - 1]
                new_selection.append(index - 1)
            else:
                new_selection.append(index)

        self.update_file_listbox(items, new_selection)

    # Moving selected files one down
    def move_down(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            return

        selected_set = set(selected_indices)
        items = list(self.state.selected_files)
        new_selection = []

        for index in reversed(selected_indices):
            if index < len(items) - 1 and (index + 1) not in selected_set:
                items[index + 1], items[index] = items[index], items[index + 1]
                new_selection.append(index + 1)
            else:
                new_selection.append(index)

        self.update_file_listbox(items, sorted(new_selection))

    # Moving selected top
    def move_to_top(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            return

        selected_set = set(selected_indices)
        selected_files = [self.state.selected_files[i] for i in selected_indices]
        remaining_files = [
            file_path for index, file_path in enumerate(self.state.selected_files) if index not in selected_set
        ]
        updated_files = selected_files + remaining_files
        new_selection = list(range(len(selected_files)))
        self.update_file_listbox(updated_files, new_selection)

    # Moving selected files one bottom
    def move_to_bottom(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            return

        selected_set = set(selected_indices)
        selected_files = [self.state.selected_files[i] for i in selected_indices]
        remaining_files = [
            file_path for index, file_path in enumerate(self.state.selected_files) if index not in selected_set
        ]
        updated_files = remaining_files + selected_files
        new_selection = list(range(len(remaining_files), len(updated_files)))
        self.update_file_listbox(updated_files, new_selection)

    def flip_order(self):
        items = list(self.state.selected_files)
        if not items:
            return

        selected_indices = list(self.file_listbox.curselection())
        reversed_items = list(reversed(items))
        new_selection = sorted((len(items) - 1 - index) for index in selected_indices)
        self.update_file_listbox(reversed_items, new_selection)

    # Language toggle button
    def toggle_language(self):
        if self.state.current_lang == 'CZ':
            self.state.current_lang = 'EN'
            self.toggle_button.config(text='CZ')
            print("Switched to English")
        else:
            self.state.current_lang = 'CZ'
            self.toggle_button.config(text='EN')
            print("Přepnuto na češtinu")

        self.update_texts()

    # List and map of widgets
    def update_texts(self):
        current_counter_kind = normalize_counter_type(self.counter_type.get()) or 'numbers'
        current_texts = TEXTS[self.state.current_lang]

        if self.toggle_button is not None:
            next_lang = 'CZ' if self.state.current_lang == 'EN' else 'EN'
            self.toggle_button.config(text=next_lang)

        if self.method_info_button is not None:
            self.method_info_button.config(text="i")

        if hasattr(self, "method_tooltip") and self.method_tooltip is not None:
            self.method_tooltip.update_text(current_texts["method_tooltip"])

        widgets = {
            self.app_title_label: "app_title",
            self.app_subtitle_label: "app_subtitle",
            self.files_panel_title_label: "files_panel_title",
            self.files_panel_hint_label: "files_panel_hint",
            self.settings_panel_title_label: "settings_panel_title",
            self.settings_panel_hint_label: "settings_panel_hint",
            self.tips_panel_title_label: "tips_panel_title",
            self.tips_line_1_label: "tips_line_1",
            self.tips_line_2_label: "tips_line_2",
            self.tips_line_3_label: "tips_line_3",
            self.remove_all_button: "remove_all",
            self.remove_button: "remove_file",
            self.part1_label: "name_label",
            self.part2_label: "method_label",
            self.move_to_top_button: "move_to_top_button",
            self.flip_order_button: "flip_order_button",
            self.move_to_bottom_button: "move_to_bottom_button",
            self.rename_button: "rename_button",
            self.select_file_button: "select_file_button",
            self.counter_menu: "counter_menu_label",
            self.open_log_button: "log_button",
        }

        for widget, text_key in widgets.items():
            if widget is None:
                continue

            if isinstance(widget, ttk.Combobox):
                widget['values'] = current_texts[text_key]['values']
                widget.set(get_counter_type_label(current_counter_kind, self.state.current_lang))
            else:
                widget.config(text=current_texts[text_key])

    # Create main instance of Log wiever and rechecks if everything exist / solve problems.
    def open_log_viewer(self):
        log = Log()
        log.checklog()  # Recheck of log folder and files / fixes if they do not.
        log.create_ui()  # Create main window UI

    # This is called on end of the main window to close all the remaining windows and application.
    def on_closing(self, root):
        root.destroy()
        sys.exit()
