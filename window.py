from tkinter import ttk
import tkinter as tk
from widget_logic import Widget
from rename_logic import Rename


# # This is for app dev precision widget moving
# def display_coordinates(event):
#     x, y = event.x, event.y
#     print(f"Clicked at coordinates: ({x}, {y})")


class Window(Rename, Widget):

    def __init__(self):
        super().__init__()

    def create_main_window(self):
        # Main window creation
        root = tk.Tk()

        # Window name
        root.title("Simple Mass Rename")

        # Window size setting  (width x height)
        root.geometry("580x500")
        # Fixes window size
        root.resizable(False, False)

        # # This is for app dev precision widget moving
        # root.bind("<Button-1>", display_coordinates)

        # Creation of box for listbox and scroll bar
        listbox_frame = ttk.Frame(root, width=500, height=350)
        listbox_frame.place(x=20, y=60)

        # Creation of list box
        self.file_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, yscrollcommand=lambda first, last: None)
        self.file_listbox.place(x=0, y=0, width=480, height=350)  # Setting size and parameters of listbox

        # Creation of scroll barr
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.place(x=480, y=0, height=350)  # Setting of location and parameters of scroll bar

        # Creation of remove all selected files button
        self.remove_all_button = tk.Button(root, text="Odebrat všechny soubory",
                                           command=lambda: self.remove_all_files(self.part1_entry), width=19)
        self.remove_all_button.place(x=428, y=420)

        # Creation of remove selected files button
        self.remove_button = tk.Button(root, text="Odebrat soubor",
                                       command=lambda:
                                       self.remove_selected(self.file_list, self.file_listbox, self.part1_entry))
        self.remove_button.place(x=316, y=420)

        # Fixing scrollbar to listbox
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Creation of select file button
        self.select_file_button = tk.Button(root, text="Vyber soubory",
                                            command=lambda: self.select_files(self.file_list, self.part1_entry))
        self.select_file_button.place(x=20, y=420)

        # Creation of label on file name text field
        self.part1_label = tk.Label(root, text="Název souboru:")
        self.part1_label.place(x=20, y=10)

        # Creation of text field for file name
        self.part1_entry = tk.Entry(root, width=40)
        self.part1_entry.place(x=20, y=30)

        # Creation of button to move one up
        self.move_up_button = tk.Button(root, text="△", command=lambda: self.move_up(self.file_list, self.file_listbox))
        self.move_up_button.place(x=525, y=60, width=30, height=30)

        # Creation of button to move one down
        self.move_down_button = tk.Button(root, text="▽",
                                          command=lambda: self.move_down(self.file_list, self.file_listbox))
        self.move_down_button.place(x=525, y=385, width=30, height=30)

        # Creation of button to move top
        self.move_to_top_button = tk.Button(root, text="Nahoru",
                                            command=self.move_to_top)
        self.move_to_top_button.place(x=525, y=90, width=50, height=30)

        # Creation of button to move bottom
        self.move_to_bottom_button = tk.Button(root, text="Dolů", command=self.move_to_bottom)
        self.move_to_bottom_button.place(x=525, y=355, width=50, height=30)

        # Creation of label on rename type
        self.part2_label = tk.Label(root, text="Metoda:")
        self.part2_label.place(x=300, y=10)

        # Creation of rolling menu for rename type
        self.counter_type = tk.StringVar()
        self.counter_type.set("Čísla")  # Default settings

        self.counter_menu = ttk.Combobox(root, textvariable=self.counter_type)
        self.counter_menu['values'] = ("Čísla", "Písmena")
        self.counter_menu.place(x=300, y=29)

        # Creation of button for file rename
        self.rename_button = tk.Button(root, text="Přejmenuj Soubory",
                                       command=lambda: self.rename_files(self.part1_entry.get(),
                                                                    self.counter_type.get(), self.file_list))
        self.rename_button.place(x=115, y=420)

        # Button for language toggle
        self.toggle_button = tk.Button(root, text="EN", command=self.toggle_language)
        self.toggle_button.place(x=550, y=1)

        # Button for opening the log wiever
        self.open_log_button = tk.Button(root, text="Log", command=self.open_log_viewer)
        self.open_log_button.place(x=428, y=450)

        # main loop remover
        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))
        # Start main application loop so window stay open
        root.mainloop()


