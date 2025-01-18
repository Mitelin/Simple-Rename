from config import DynamicConfig, StaticConfig
from tkinter import ttk, filedialog
import tkinter as tk
from os import path
from log import Log
import sys

class Widget(DynamicConfig, StaticConfig):
    def __init__(self):
        super().__init__()

    def select_files(self, file_list, part1_entry):
        files = filedialog.askopenfilenames()
        if files:
            file_list.clear()
            file_list.extend(files)
            self.update_file_listbox(file_list)

            # Call and activation of prepopulate entry for creating common name of selected files.
            self.prepopulate_entry(file_list, part1_entry)

    # Function for prepopulate entry
    def prepopulate_entry(self, file_list, part1_entry):
        common_prefix = self.get_common_prefix(file_list)
        part1_entry.delete(0, tk.END)
        part1_entry.insert(0, common_prefix)

    # Function for updating and displaying selected files into the filebox

    def update_file_listbox(self, file_list, selected_indices=None):
        self.file_listbox.delete(0, tk.END)
        for file in file_list:
            self.file_listbox.insert(tk.END, path.basename(file))  # Show only the file name
        if selected_indices:
            for index in selected_indices:
                self.file_listbox.select_set(index)

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
        self.file_listbox.delete(0, tk.END)
        part1_entry.delete(0, tk.END)

    # Remove selected files
    def remove_selected(self, file_list, file_listbox, part1_entry):
        selected_indices = file_listbox.curselection()
        for index in reversed(selected_indices):
            file_list.pop(index)
        self.update_file_listbox(file_list)
        self.prepopulate_entry(file_list, part1_entry)

    # Move selected files one up
    def move_up(self, file_list, file_listbox):
        selected_indices = file_listbox.curselection()
        if not selected_indices:
            return
        for index in selected_indices:
            if index == 0:
                continue
            file_list[index], file_list[index - 1] = file_list[index - 1], file_list[index]
        self.update_file_listbox(file_list, [index - 1 if index > 0 else index for index in selected_indices])

    # Moving selected files one down
    def move_down(self, file_list, file_listbox):
        selected_indices = file_listbox.curselection()
        if not selected_indices:
            return
        for index in reversed(selected_indices):
            if index == len(file_list) - 1:
                continue
            file_list[index], file_list[index + 1] = file_list[index + 1], file_list[index]
        self.update_file_listbox(file_list,
                                 [index + 1 if index < len(file_list) - 1 else index for index in selected_indices])

    # Moving selected top
    def move_to_top(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            return
        selected_files = [self.file_listbox.get(i) for i in selected_indices]
        for i in reversed(selected_indices):
            self.file_listbox.delete(i)
        for i, file in enumerate(selected_files):
            self.file_listbox.insert(i, file)
            self.file_listbox.selection_set(i)

    # Moving selected files one bottom
    def move_to_bottom(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            return
        selected_files = [self.file_listbox.get(i) for i in selected_indices]
        for i in reversed(selected_indices):
            self.file_listbox.delete(i)
        for file in selected_files:
            self.file_listbox.insert(tk.END, file)
            self.file_listbox.selection_set(tk.END)

    # Language toggle button
    def toggle_language(self):
        if self.toggle_button.config('text')[-1] == 'CZ':
            self.toggle_button.config(text='EN')
            self.current_lang = 'CZ'
            print("Přepnuto na češtinu")
        else:
            self.toggle_button.config(text='CZ')
            self.current_lang = 'EN'
            print("Switched to English")
        self.update_texts()

    # List and map of widgets
    def update_texts(self):

        widgets = {
            self.remove_all_button: "remove_all",
            self.remove_button: "remove_file",
            self.part1_label: "name_label",
            self.part2_label: "method_label",
            self.move_to_top_button: "move_to_top_button",
            self.move_to_bottom_button: "move_to_bottom_button",
            self.rename_button: "rename_button",
            self.select_file_button: "select_file_button",
            self.counter_menu: "counter_menu_label",
        }

        # Text update for all widgets
        for widget, text_key in widgets.items():
            if isinstance(widget, ttk.Combobox):
                # This part is for rolling menu text update
                widget['values'] = self.texts[self.current_lang][text_key]['values']
                widget.set(
                    self.texts[self.current_lang][text_key]['default'])  # Setting default value
            else:
                widget.config(text=self.texts[self.current_lang][text_key])

    # Create main instance of Log wiever and rechecks if everything exist / solve problems.
    def open_log_viewer(self):
        log = Log()
        log.checklog()  # Recheck of log folder and files / fixes if they do not.
        log.create_ui()  # Create main window UI

    # This is called on end of the main window to close all the remaining windows and application.
    def on_closing(self, root):
        sys.exit()
