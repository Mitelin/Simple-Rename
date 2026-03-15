import tkinter as tk
import unittest
from tkinter import ttk
from unittest.mock import patch

from config import AppState
from widget_logic import WidgetController


class WidgetControllerTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.addCleanup(self._cleanup_root)
        self.state = AppState()
        self.controller = WidgetController(self.state)
        self.controller.file_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.controller.part1_entry = tk.Entry(self.root)
        self.controller.toggle_button = tk.Button(self.root)
        self.controller.rename_button = tk.Button(self.root)
        self.controller.select_file_button = tk.Button(self.root)
        self.controller.remove_button = tk.Button(self.root)
        self.controller.remove_all_button = tk.Button(self.root)
        self.controller.move_to_top_button = tk.Button(self.root)
        self.controller.flip_order_button = tk.Button(self.root)
        self.controller.move_to_bottom_button = tk.Button(self.root)
        self.controller.part1_label = tk.Label(self.root)
        self.controller.part2_label = tk.Label(self.root)
        self.controller.app_title_label = tk.Label(self.root)
        self.controller.app_subtitle_label = tk.Label(self.root)
        self.controller.files_panel_title_label = tk.Label(self.root)
        self.controller.files_panel_hint_label = tk.Label(self.root)
        self.controller.settings_panel_title_label = tk.Label(self.root)
        self.controller.settings_panel_hint_label = tk.Label(self.root)
        self.controller.tips_panel_title_label = tk.Label(self.root)
        self.controller.tips_line_1_label = tk.Label(self.root)
        self.controller.tips_line_2_label = tk.Label(self.root)
        self.controller.tips_line_3_label = tk.Label(self.root)
        self.controller.open_log_button = tk.Button(self.root)
        self.controller.counter_type = tk.StringVar(value="Čísla")
        self.controller.counter_menu = ttk.Combobox(self.root, textvariable=self.controller.counter_type, state="readonly")

    def _cleanup_root(self):
        if self.root.winfo_exists():
            self.root.destroy()

    def test_build_display_labels_disambiguates_duplicate_basenames(self):
        labels = self.controller.build_display_labels([
            r"C:\folder-one\episode.txt",
            r"D:\folder-two\episode.txt",
            r"D:\folder-two\unique.txt",
        ])

        self.assertEqual([
            "episode.txt [folder-one]",
            "episode.txt [folder-two]",
            "unique.txt",
        ], labels)

    def test_get_common_prefix_returns_first_basename_when_prefix_missing(self):
        prefix = self.controller.get_common_prefix([
            r"C:\files\alpha.txt",
            r"C:\files\beta.txt",
        ])

        self.assertEqual("alpha", prefix)

    def test_select_files_populates_state_listbox_and_prefix(self):
        selected = (
            r"C:\files\scene_01.png",
            r"C:\files\scene_02.png",
        )

        with patch("widget_logic.filedialog.askopenfilenames", return_value=selected):
            self.controller.select_files(self.controller.file_listbox, self.controller.part1_entry)

        self.assertEqual(list(selected), self.state.selected_files)
        self.assertEqual(["scene_01.png", "scene_02.png"], list(self.controller.file_listbox.get(0, tk.END)))
        self.assertEqual("scene_0", self.controller.part1_entry.get())

    def test_remove_selected_clears_entry_when_last_file_is_removed(self):
        self.state.selected_files = [r"C:\files\only.txt"]
        self.controller.update_file_listbox(self.state.selected_files)
        self.controller.part1_entry.insert(0, "only")
        self.controller.file_listbox.select_set(0)

        self.controller.remove_selected(self.controller.file_listbox, self.controller.part1_entry)

        self.assertEqual([], self.state.selected_files)
        self.assertEqual("", self.controller.part1_entry.get())

    def test_move_up_updates_order_and_selection(self):
        self.controller.update_file_listbox(["a", "b", "c", "d"])
        self.controller.file_listbox.select_set(1)
        self.controller.file_listbox.select_set(3)

        self.controller.move_up()

        self.assertEqual(["b", "a", "d", "c"], self.state.selected_files)
        self.assertEqual((0, 2), self.controller.file_listbox.curselection())

    def test_move_down_updates_order_and_selection(self):
        self.controller.update_file_listbox(["a", "b", "c", "d"])
        self.controller.file_listbox.select_set(0)
        self.controller.file_listbox.select_set(2)

        self.controller.move_down()

        self.assertEqual(["b", "a", "d", "c"], self.state.selected_files)
        self.assertEqual((1, 3), self.controller.file_listbox.curselection())

    def test_move_to_top_keeps_relative_order_of_selected_items(self):
        self.controller.update_file_listbox(["a", "b", "c", "d"])
        self.controller.file_listbox.select_set(1)
        self.controller.file_listbox.select_set(3)

        self.controller.move_to_top()

        self.assertEqual(["b", "d", "a", "c"], self.state.selected_files)
        self.assertEqual((0, 1), self.controller.file_listbox.curselection())

    def test_move_to_bottom_keeps_relative_order_of_selected_items(self):
        self.controller.update_file_listbox(["a", "b", "c", "d"])
        self.controller.file_listbox.select_set(1)
        self.controller.file_listbox.select_set(3)

        self.controller.move_to_bottom()

        self.assertEqual(["a", "c", "b", "d"], self.state.selected_files)
        self.assertEqual((2, 3), self.controller.file_listbox.curselection())

    def test_flip_order_reverses_entire_list_and_mirrors_selection(self):
        self.controller.update_file_listbox(["a", "b", "c", "d"])
        self.controller.file_listbox.select_set(0)
        self.controller.file_listbox.select_set(2)

        self.controller.flip_order()

        self.assertEqual(["d", "c", "b", "a"], self.state.selected_files)
        self.assertEqual((1, 3), self.controller.file_listbox.curselection())

    def test_update_texts_switches_labels_and_counter_values(self):
        self.state.current_lang = "EN"
        self.controller.counter_type.set("Numbers")

        self.controller.update_texts()

        self.assertEqual("CZ", self.controller.toggle_button.cget("text"))
        self.assertEqual("Rename Files", self.controller.rename_button.cget("text"))
        self.assertEqual("Reverse", self.controller.flip_order_button.cget("text"))
        self.assertEqual(("Numbers", "Letters"), self.controller.counter_menu.cget("values"))

        self.state.current_lang = "CZ"
        self.controller.update_texts()

        self.assertEqual("EN", self.controller.toggle_button.cget("text"))
        self.assertEqual("Přejmenuj soubory", self.controller.rename_button.cget("text"))
        self.assertEqual("Obrátit", self.controller.flip_order_button.cget("text"))
        self.assertEqual(("Čísla", "Písmena"), self.controller.counter_menu.cget("values"))

    def test_toggle_language_updates_state_and_next_toggle_label(self):
        self.state.current_lang = "CZ"
        self.controller.counter_type.set("Čísla")

        self.controller.toggle_language()

        self.assertEqual("EN", self.state.current_lang)
        self.assertEqual("CZ", self.controller.toggle_button.cget("text"))


if __name__ == "__main__":
    unittest.main()