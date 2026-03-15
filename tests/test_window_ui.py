import tkinter as tk
import unittest
from tkinter import ttk
from unittest.mock import Mock, patch

from rename_logic import CollisionError, RenameResult, RenameError, ValidationError
from window import Window


class WindowUiTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.addCleanup(self._cleanup_root)
        self.window = Window()
        self.window._configure_styles(self.root)
        self.root.geometry(f"{self.window.WINDOW_WIDTH}x{self.window.WINDOW_HEIGHT}")
        self.root.minsize(self.window.WINDOW_WIDTH, self.window.WINDOW_HEIGHT)
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.window._build_header(self.root)

        self.content = ttk.Frame(
            self.root,
            style="App.TFrame",
            padding=(28, 0, 28, 28),
            width=self.window.CONTENT_WIDTH,
            height=self.window.CONTENT_HEIGHT,
        )
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.grid_propagate(False)
        self.content.columnconfigure(0, minsize=self.window.FILE_PANEL_WIDTH, weight=0)
        self.content.columnconfigure(1, minsize=self.window.SIDE_PANEL_WIDTH, weight=0)
        self.content.rowconfigure(0, minsize=self.window.CONTENT_HEIGHT, weight=0)
        self.window._build_file_panel(self.content)
        self.window._build_settings_panel(self.content)
        self.window.widgets.update_texts()
        self.root.update_idletasks()

    def _cleanup_root(self):
        if self.root.winfo_exists():
            self.root.destroy()

    def test_settings_button_stays_above_tips_card_in_both_languages(self):
        for lang in ("CZ", "EN"):
            self.window.state.current_lang = lang
            self.window.widgets.update_texts()
            self.root.update_idletasks()

            rename_bottom = self.window.widgets.rename_button.winfo_y() + self.window.widgets.rename_button.winfo_height()
            tips_y = self.window.widgets.tips_panel_title_label.master.winfo_y()
            self.assertLess(rename_bottom, tips_y)

    def test_language_switch_keeps_key_panel_widths_stable(self):
        file_panel = self.window.widgets.select_file_button.master.master
        settings_card = self.window.widgets.part1_entry.master

        self.window.state.current_lang = "CZ"
        self.window.widgets.update_texts()
        self.root.update_idletasks()
        cz_widths = (file_panel.winfo_width(), settings_card.winfo_width())

        self.window.state.current_lang = "EN"
        self.window.widgets.update_texts()
        self.root.update_idletasks()
        en_widths = (file_panel.winfo_width(), settings_card.winfo_width())

        self.assertEqual(cz_widths, en_widths)

    def test_flip_button_is_present_between_top_and_bottom_controls(self):
        self.assertEqual("2", str(self.window.widgets.flip_order_button.grid_info()["row"]))
        self.assertEqual("1", str(self.window.widgets.move_to_top_button.grid_info()["row"]))
        self.assertEqual("3", str(self.window.widgets.move_to_bottom_button.grid_info()["row"]))

    def test_rename_and_refresh_updates_file_list_on_success(self):
        self.window.state.selected_files = ["a.txt"]
        self.window.widgets.part1_entry.insert(0, "episode")
        self.window.widgets.counter_type.set("Numbers")
        self.window.widgets.update_file_listbox = Mock()

        with patch.object(self.window.rename_service, "rename_files", return_value=RenameResult(["episode1.txt"])) as rename_mock:
            self.window.rename_and_refresh()

        rename_mock.assert_called_once_with("episode", "Numbers", ["a.txt"])
        self.window.widgets.update_file_listbox.assert_called_once_with(["episode1.txt"])

    def test_rename_and_refresh_shows_validation_warning(self):
        with patch.object(self.window.rename_service, "rename_files", side_effect=ValidationError("bad input")):
            with patch("window.messagebox.showwarning") as warning_mock:
                self.window.rename_and_refresh()

        warning_mock.assert_called_once()

    def test_rename_and_refresh_shows_collision_error(self):
        with patch.object(self.window.rename_service, "rename_files", side_effect=CollisionError("collision")):
            with patch("window.messagebox.showerror") as error_mock:
                self.window.rename_and_refresh()

        error_mock.assert_called_once()

    def test_rename_and_refresh_shows_generic_rename_error(self):
        with patch.object(self.window.rename_service, "rename_files", side_effect=RenameError("failed")):
            with patch("window.messagebox.showerror") as error_mock:
                self.window.rename_and_refresh()

        error_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()