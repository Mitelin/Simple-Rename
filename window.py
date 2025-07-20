from tkinter import ttk
import tkinter as tk
from widget_logic import Widget
from rename_logic import Rename
import os

# # This is for app dev precision widget moving
# def display_coordinates(event):
#     x, y = event.x, event.y
#     print(f"Clicked at coordinates: ({x}, {y})")


class Window(Rename, Widget):

    def __init__(self):
        super().__init__()

    def rename_and_refresh(self):
        # Vezmeme aktuální pořadí z GUI a přemapujeme zpět na cesty
        sorted_names = list(self.file_listbox.get(0, tk.END))
        name_to_path = {os.path.basename(p): p for p in self.selected_files}
        sorted_paths = [name_to_path[name] for name in sorted_names if name in name_to_path]

        new_paths = self.rename_files(
            self.part1_entry.get(),
            self.counter_type.get(),
            sorted_paths
        )

        if new_paths:
            self.update_file_listbox(new_paths)

    def create_main_window(self):
        # Main window creation
        root = tk.Tk()

        # Window name
        root.title("Simple Mass Rename")
        root.geometry("580x500")
        root.resizable(False, False)

        # Frame for Listbox and scrollbar
        listbox_frame = ttk.Frame(root, width=500, height=350)
        listbox_frame.place(x=20, y=60)

        # Listbox
        self.file_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, yscrollcommand=lambda first, last: None)
        self.file_listbox.place(x=0, y=0, width=480, height=350)

        # Scrollbar
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.place(x=480, y=0, height=350)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Odebrat všechny
        self.remove_all_button = tk.Button(root, text="Odebrat všechny soubory",
                                           command=lambda: self.remove_all_files(self.part1_entry), width=19)
        self.remove_all_button.place(x=428, y=420)

        # Odebrat vybrané
        self.remove_button = tk.Button(root, text="Odebrat soubor",
                                       command=lambda: self.remove_selected(
                                           self.file_listbox,
                                           self.part1_entry
                                       ))
        self.remove_button.place(x=316, y=420)

        # Vyber soubory
        self.select_file_button = tk.Button(root, text="Vyber soubory",
                                            command=lambda: self.select_files(self.file_listbox, self.part1_entry))
        self.select_file_button.place(x=20, y=420)

        # Název souboru
        self.part1_label = tk.Label(root, text="Název souboru:")
        self.part1_label.place(x=20, y=10)

        self.part1_entry = tk.Entry(root, width=40)
        self.part1_entry.place(x=20, y=30)

        # Metoda
        self.part2_label = tk.Label(root, text="Metoda:")
        self.part2_label.place(x=300, y=10)

        self.counter_type = tk.StringVar()
        self.counter_type.set("Čísla")

        self.counter_menu = ttk.Combobox(root, textvariable=self.counter_type)
        self.counter_menu['values'] = ("Čísla", "Písmena")
        self.counter_menu.place(x=300, y=29)

        # Přejmenovat
        self.rename_button = tk.Button(root, text="Přejmenuj Soubory", command=self.rename_and_refresh)
        self.rename_button.place(x=115, y=420)

        # Tlačítka pro řazení
        self.move_up_button = tk.Button(root, text="△", command=self.move_up)
        self.move_up_button.place(x=525, y=60, width=30, height=30)

        self.move_down_button = tk.Button(root, text="▽", command=self.move_down)
        self.move_down_button.place(x=525, y=385, width=30, height=30)

        self.move_to_top_button = tk.Button(root, text="Nahoru", command=self.move_to_top)
        self.move_to_top_button.place(x=525, y=90, width=50, height=30)

        self.move_to_bottom_button = tk.Button(root, text="Dolů", command=self.move_to_bottom)
        self.move_to_bottom_button.place(x=525, y=355, width=50, height=30)

        # Jazykový přepínač
        self.toggle_button = tk.Button(root, text="EN", command=self.toggle_language)
        self.toggle_button.place(x=550, y=1)

        # Zobrazení logu
        self.open_log_button = tk.Button(root, text="Log", command=self.open_log_viewer)
        self.open_log_button.place(x=428, y=450)

        # Zavření okna
        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))
        root.mainloop()


