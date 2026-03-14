from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

from config import AppState
from rename_logic import CollisionError, RenameError, RenameService, ValidationError
from widget_logic import WidgetController

# # This is for app dev precision widget moving
# def display_coordinates(event):
#     x, y = event.x, event.y
#     print(f"Clicked at coordinates: ({x}, {y})")


class Window:

    def __init__(self):
        self.state = AppState()
        self.rename_service = RenameService()
        self.widgets = WidgetController(self.state)

    def rename_and_refresh(self):
        try:
            result = self.rename_service.rename_files(
                self.widgets.part1_entry.get(),
                self.widgets.counter_type.get(),
                self.state.selected_files
            )
        except ValidationError as error:
            messagebox.showwarning("Neplatný vstup", str(error))
            return
        except CollisionError as error:
            messagebox.showerror("Kolize souboru", str(error))
            return
        except RenameError as error:
            messagebox.showerror("Chyba přejmenování", str(error))
            return

        self.widgets.update_file_listbox(result.renamed_paths)

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
        self.widgets.file_listbox = tk.Listbox(
            listbox_frame,
            selectmode=tk.MULTIPLE,
            yscrollcommand=lambda first, last: None
        )
        self.widgets.file_listbox.place(x=0, y=0, width=480, height=350)

        # Scrollbar
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.widgets.file_listbox.yview)
        scrollbar.place(x=480, y=0, height=350)
        self.widgets.file_listbox.config(yscrollcommand=scrollbar.set)

        # Odebrat všechny
        self.widgets.remove_all_button = tk.Button(
            root,
            text="Odebrat všechny soubory",
            command=lambda: self.widgets.remove_all_files(self.widgets.part1_entry),
            width=19
        )
        self.widgets.remove_all_button.place(x=428, y=420)

        # Odebrat vybrané
        self.widgets.remove_button = tk.Button(
            root,
            text="Odebrat soubor",
            command=lambda: self.widgets.remove_selected(
                self.widgets.file_listbox,
                self.widgets.part1_entry
            )
        )
        self.widgets.remove_button.place(x=316, y=420)

        # Vyber soubory
        self.widgets.select_file_button = tk.Button(
            root,
            text="Vyber soubory",
            command=lambda: self.widgets.select_files(self.widgets.file_listbox, self.widgets.part1_entry)
        )
        self.widgets.select_file_button.place(x=20, y=420)

        # Název souboru
        self.widgets.part1_label = tk.Label(root, text="Název souboru:")
        self.widgets.part1_label.place(x=20, y=10)

        self.widgets.part1_entry = tk.Entry(root, width=40)
        self.widgets.part1_entry.place(x=20, y=30)

        # Metoda
        self.widgets.part2_label = tk.Label(root, text="Metoda:")
        self.widgets.part2_label.place(x=300, y=10)

        self.widgets.counter_type = tk.StringVar()
        self.widgets.counter_type.set("Čísla")

        self.widgets.counter_menu = ttk.Combobox(root, textvariable=self.widgets.counter_type, state="readonly")
        self.widgets.counter_menu['values'] = ("Čísla", "Písmena")
        self.widgets.counter_menu.place(x=300, y=29)

        # Přejmenovat
        self.widgets.rename_button = tk.Button(root, text="Přejmenuj Soubory", command=self.rename_and_refresh)
        self.widgets.rename_button.place(x=115, y=420)

        # Tlačítka pro řazení
        self.widgets.move_up_button = tk.Button(root, text="△", command=self.widgets.move_up)
        self.widgets.move_up_button.place(x=525, y=60, width=30, height=30)

        self.widgets.move_down_button = tk.Button(root, text="▽", command=self.widgets.move_down)
        self.widgets.move_down_button.place(x=525, y=385, width=30, height=30)

        self.widgets.move_to_top_button = tk.Button(root, text="Nahoru", command=self.widgets.move_to_top)
        self.widgets.move_to_top_button.place(x=525, y=90, width=50, height=30)

        self.widgets.move_to_bottom_button = tk.Button(root, text="Dolů", command=self.widgets.move_to_bottom)
        self.widgets.move_to_bottom_button.place(x=525, y=355, width=50, height=30)

        # Jazykový přepínač
        self.widgets.toggle_button = tk.Button(root, text="EN", command=self.widgets.toggle_language)
        self.widgets.toggle_button.place(x=550, y=1)

        # Zobrazení logu
        self.widgets.open_log_button = tk.Button(root, text="Log", command=self.widgets.open_log_viewer)
        self.widgets.open_log_button.place(x=428, y=450)

        self.widgets.update_texts()

        # Zavření okna
        root.protocol("WM_DELETE_WINDOW", lambda: self.widgets.on_closing(root))
        root.mainloop()


