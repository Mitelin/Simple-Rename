"""Tkinter window composition and high-level app actions."""

from tkinter import ttk
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = None
    TkinterDnD = None

from config import APP_NAME, APP_VERSION, AppState, TEXTS
from rename_logic import CollisionError, RenameError, RenameService, ValidationError
from widget_logic import WidgetController

class Tooltip:
    """Display a small hover tooltip next to a widget."""

    def __init__(self, widget, text, *, wraplength=260):
        """Bind a tooltip window to the given widget."""
        self.widget = widget
        self.text = text
        self.wraplength = wraplength
        self.tooltip_window = None

        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)
        self.widget.bind("<ButtonPress>", self.hide)

    def update_text(self, text):
        """Replace the tooltip content and refresh an already open tooltip."""
        self.text = text
        if self.tooltip_window is not None:
            label = self.tooltip_window.winfo_children()[0]
            label.config(text=text)

    def show(self, _event=None):
        """Create and show the tooltip window if it is not visible yet."""
        if self.tooltip_window is not None:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 10
        y = self.widget.winfo_rooty() - 4
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        self.tooltip_window.configure(bg="#cfdad6")

        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            justify="left",
            wraplength=self.wraplength,
            bg="#f8fbfa",
            fg="#23343b",
            relief="solid",
            bd=1,
            padx=10,
            pady=8,
            font=("Segoe UI", 9),
        )
        label.pack()

    def hide(self, _event=None):
        """Destroy the tooltip window if it is currently visible."""
        if self.tooltip_window is None:
            return

        self.tooltip_window.destroy()
        self.tooltip_window = None


class Window:
    """Build the main UI and coordinate rename and undo actions."""

    WINDOW_WIDTH = 1040
    WINDOW_HEIGHT = 770
    CONTENT_WIDTH = 984
    CONTENT_HEIGHT = 670
    FILE_PANEL_WIDTH = 650
    SIDE_PANEL_WIDTH = 300
    HEADER_SUBTITLE_WRAP = 640
    FILE_HINT_WRAP = 520
    SIDE_HINT_WRAP = 250
    TIPS_WRAP = 250
    SETTINGS_CARD_HEIGHT = 430
    TIPS_CARD_HEIGHT = 220

    PALETTE = {
        "app_bg": "#eef3f1",
        "card_bg": "#f8fbfa",
        "card_border": "#d8e1dd",
        "text_primary": "#23343b",
        "text_secondary": "#60757c",
        "text_muted": "#72868c",
        "accent": "#4e7c74",
        "accent_active": "#416b64",
        "accent_pressed": "#355952",
        "secondary": "#dde7e3",
        "secondary_active": "#d0ddd8",
        "secondary_pressed": "#c2d1cb",
        "ghost_active": "#eef4f2",
        "ghost_pressed": "#e2ebe8",
        "surface": "#ffffff",
        "surface_select": "#d9ebe5",
        "surface_select_text": "#1f3737",
    }

    def __init__(self):
        """Create shared state, services, and widget controller objects."""
        self.state = AppState()
        self.rename_service = RenameService()
        self.widgets = WidgetController(self.state)
        self.widgets.method_tooltip = None
        self.last_rename_operation = []

    def _register_drop_target(self, widget):
        """Register a widget as a file drop target when TkDND is available."""
        if DND_FILES is None:
            return False

        try:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind(
                "<<Drop>>",
                lambda event: self.widgets.handle_file_drop(event, self.widgets.part1_entry)
            )
        except (tk.TclError, RuntimeError):
            return False

        return True

    def _configure_styles(self, root):
        """Create the ttk styles used by the application."""
        colors = self.PALETTE
        root.configure(bg=colors["app_bg"])

        title_font = tkfont.Font(family="Segoe UI Semibold", size=20)
        subtitle_font = tkfont.Font(family="Segoe UI", size=10)
        section_font = tkfont.Font(family="Segoe UI Semibold", size=12)
        body_font = tkfont.Font(family="Segoe UI", size=10)
        button_font = tkfont.Font(family="Segoe UI Semibold", size=10)

        root.option_add("*Font", body_font)

        style = ttk.Style(root)
        style.theme_use("clam")

        style.configure("App.TFrame", background=colors["app_bg"])
        style.configure("Card.TFrame", background=colors["card_bg"], relief="flat")
        style.configure(
            "Title.TLabel",
            background=colors["app_bg"],
            foreground=colors["text_primary"],
            font=title_font
        )
        style.configure(
            "Subtitle.TLabel",
            background=colors["app_bg"],
            foreground=colors["text_secondary"],
            font=subtitle_font
        )
        style.configure(
            "Section.TLabel",
            background=colors["card_bg"],
            foreground=colors["text_primary"],
            font=section_font
        )
        style.configure(
            "Hint.TLabel",
            background=colors["card_bg"],
            foreground=colors["text_muted"],
            font=body_font
        )
        style.configure(
            "Field.TLabel",
            background=colors["card_bg"],
            foreground=colors["text_primary"],
            font=body_font
        )
        style.configure(
            "Accent.TButton",
            background=colors["accent"],
            foreground="#ffffff",
            borderwidth=0,
            focusthickness=0,
            focuscolor=colors["accent"],
            padding=(16, 10),
            font=button_font
        )
        style.map(
            "Accent.TButton",
            background=[("active", colors["accent_active"]), ("pressed", colors["accent_pressed"])],
            foreground=[("disabled", "#d7dfdd")]
        )
        style.configure(
            "Secondary.TButton",
            background=colors["secondary"],
            foreground=colors["text_primary"],
            borderwidth=0,
            focusthickness=0,
            focuscolor=colors["secondary"],
            padding=(14, 9),
            font=button_font
        )
        style.map(
            "Secondary.TButton",
            background=[("active", colors["secondary_active"]), ("pressed", colors["secondary_pressed"])]
        )
        style.configure(
            "Outline.TButton",
            background=colors["card_bg"],
            foreground=colors["text_primary"],
            borderwidth=1,
            focusthickness=1,
            focuscolor=colors["card_bg"],
            lightcolor=colors["card_border"],
            darkcolor=colors["card_border"],
            padding=(16, 10),
            font=button_font
        )
        style.map(
            "Outline.TButton",
            background=[("active", colors["ghost_active"]), ("pressed", colors["ghost_pressed"])],
            foreground=[("disabled", colors["text_muted"])],
        )
        style.configure(
            "Ghost.TButton",
            background=colors["card_bg"],
            foreground=colors["text_primary"],
            borderwidth=0,
            focusthickness=0,
            focuscolor=colors["card_bg"],
            padding=(10, 8),
            font=button_font
        )
        style.map(
            "Ghost.TButton",
            background=[("active", colors["ghost_active"]), ("pressed", colors["ghost_pressed"])]
        )
        style.configure(
            "App.TEntry",
            fieldbackground=colors["surface"],
            foreground=colors["text_primary"],
            bordercolor=colors["card_border"],
            lightcolor=colors["card_border"],
            darkcolor=colors["card_border"],
            insertcolor=colors["text_primary"],
            padding=8
        )
        style.configure(
            "App.TCombobox",
            fieldbackground=colors["surface"],
            background=colors["surface"],
            foreground=colors["text_primary"],
            bordercolor=colors["card_border"],
            lightcolor=colors["card_border"],
            darkcolor=colors["card_border"],
            padding=6
        )

    def _build_header(self, root):
        """Create the top application header with title and quick actions."""
        header = ttk.Frame(root, style="App.TFrame", padding=(28, 24, 28, 16))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        header.rowconfigure(0, minsize=72)

        title_wrap = ttk.Frame(header, style="App.TFrame")
        title_wrap.grid(row=0, column=0, sticky="w")
        title_wrap.rowconfigure(1, minsize=34)

        self.widgets.app_title_label = ttk.Label(title_wrap, style="Title.TLabel")
        self.widgets.app_title_label.grid(row=0, column=0, sticky="w")

        self.widgets.app_subtitle_label = ttk.Label(
            title_wrap,
            style="Subtitle.TLabel",
            wraplength=self.HEADER_SUBTITLE_WRAP,
            justify="left"
        )
        self.widgets.app_subtitle_label.grid(row=1, column=0, sticky="w", pady=(6, 0))

        actions = ttk.Frame(header, style="App.TFrame")
        actions.grid(row=0, column=1, sticky="e")
        actions.columnconfigure((0, 1), weight=0)

        self.widgets.open_log_button = ttk.Button(
            actions,
            style="Ghost.TButton",
            command=self.widgets.open_log_viewer,
            width=12
        )
        self.widgets.open_log_button.grid(row=0, column=0, padx=(0, 8))

        self.widgets.toggle_button = ttk.Button(
            actions,
            style="Secondary.TButton",
            command=self.widgets.toggle_language,
            width=8
        )
        self.widgets.toggle_button.grid(row=0, column=1)

    def _build_file_panel(self, parent):
        """Create the left panel with the file list and ordering controls."""
        colors = self.PALETTE
        file_panel = ttk.Frame(
            parent,
            style="Card.TFrame",
            padding=20,
            width=self.FILE_PANEL_WIDTH,
            height=self.CONTENT_HEIGHT
        )
        file_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        file_panel.grid_propagate(False)
        file_panel.columnconfigure(0, weight=1)
        file_panel.rowconfigure(1, minsize=54)
        file_panel.rowconfigure(2, weight=1)
        file_panel.rowconfigure(3, minsize=56)

        self.widgets.files_panel_title_label = ttk.Label(file_panel, style="Section.TLabel")
        self.widgets.files_panel_title_label.grid(row=0, column=0, sticky="w")

        self.widgets.files_panel_hint_label = ttk.Label(
            file_panel,
            style="Hint.TLabel",
            wraplength=self.FILE_HINT_WRAP,
            justify="left"
        )
        self.widgets.files_panel_hint_label.grid(row=1, column=0, sticky="ew", pady=(6, 14))

        list_wrap = ttk.Frame(file_panel, style="Card.TFrame")
        list_wrap.grid(row=2, column=0, sticky="nsew")
        list_wrap.columnconfigure(0, weight=1)
        list_wrap.rowconfigure(0, weight=1)

        list_surface = tk.Frame(
            list_wrap,
            bg=colors["surface"],
            highlightthickness=1,
            highlightbackground=colors["card_border"]
        )
        list_surface.grid(row=0, column=0, sticky="nsew")
        list_surface.columnconfigure(0, weight=1)
        list_surface.rowconfigure(0, weight=1)

        self.widgets.file_listbox = tk.Listbox(
            list_surface,
            selectmode=tk.MULTIPLE,
            activestyle="none",
            borderwidth=0,
            highlightthickness=0,
            background=colors["surface"],
            foreground=colors["text_primary"],
            selectbackground=colors["surface_select"],
            selectforeground=colors["surface_select_text"],
            font=("Segoe UI", 10),
            yscrollcommand=lambda first, last: None
        )
        self.widgets.file_listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_surface, orient=tk.VERTICAL, command=self.widgets.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.widgets.file_listbox.config(yscrollcommand=scrollbar.set)

        self._register_drop_target(list_surface)
        self._register_drop_target(self.widgets.file_listbox)

        move_controls = ttk.Frame(list_wrap, style="Card.TFrame")
        move_controls.grid(row=0, column=1, sticky="ns", padx=(12, 0))
        for row_index in range(5):
            move_controls.rowconfigure(row_index, weight=1)

        self.widgets.move_up_button = ttk.Button(move_controls, text="△", style="Ghost.TButton", command=self.widgets.move_up, width=4)
        self.widgets.move_up_button.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.widgets.move_to_top_button = ttk.Button(move_controls, style="Secondary.TButton", command=self.widgets.move_to_top, width=12)
        self.widgets.move_to_top_button.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        self.widgets.flip_order_button = ttk.Button(move_controls, style="Secondary.TButton", command=self.widgets.flip_order, width=12)
        self.widgets.flip_order_button.grid(row=2, column=0, sticky="ew", pady=(0, 8))

        self.widgets.move_to_bottom_button = ttk.Button(move_controls, style="Secondary.TButton", command=self.widgets.move_to_bottom, width=12)
        self.widgets.move_to_bottom_button.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        self.widgets.move_down_button = ttk.Button(move_controls, text="▽", style="Ghost.TButton", command=self.widgets.move_down, width=4)
        self.widgets.move_down_button.grid(row=4, column=0, sticky="ew")

        actions = ttk.Frame(file_panel, style="Card.TFrame")
        actions.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        actions.columnconfigure(0, weight=2)
        actions.columnconfigure(1, weight=2)
        actions.columnconfigure(2, weight=3)

        self.widgets.select_file_button = ttk.Button(
            actions,
            style="Accent.TButton",
            command=lambda: self.widgets.select_files(self.widgets.file_listbox, self.widgets.part1_entry)
        )
        self.widgets.select_file_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.widgets.remove_button = ttk.Button(
            actions,
            style="Secondary.TButton",
            command=lambda: self.widgets.remove_selected(self.widgets.file_listbox, self.widgets.part1_entry)
        )
        self.widgets.remove_button.grid(row=0, column=1, sticky="ew", padx=4)

        self.widgets.remove_all_button = ttk.Button(
            actions,
            style="Secondary.TButton",
            command=lambda: self.widgets.remove_all_files(self.widgets.part1_entry)
        )
        self.widgets.remove_all_button.grid(row=0, column=2, sticky="ew", padx=(8, 0))

    def _build_settings_panel(self, parent):
        """Create the right panel with rename settings and usage hints."""
        side_panel = ttk.Frame(
            parent,
            style="App.TFrame",
            width=self.SIDE_PANEL_WIDTH,
            height=self.CONTENT_HEIGHT
        )
        side_panel.grid(row=0, column=1, sticky="nsew")
        side_panel.grid_propagate(False)
        side_panel.columnconfigure(0, weight=1)
        side_panel.rowconfigure(0, minsize=self.SETTINGS_CARD_HEIGHT)
        side_panel.rowconfigure(1, minsize=self.TIPS_CARD_HEIGHT)

        settings_card = ttk.Frame(
            side_panel,
            style="Card.TFrame",
            padding=20,
            width=self.SIDE_PANEL_WIDTH,
            height=self.SETTINGS_CARD_HEIGHT
        )
        settings_card.grid(row=0, column=0, sticky="ew")
        settings_card.grid_propagate(False)
        settings_card.columnconfigure(0, weight=1)
        settings_card.rowconfigure(1, minsize=92)
        settings_card.rowconfigure(3, minsize=46)
        settings_card.rowconfigure(5, minsize=50)
        settings_card.rowconfigure(6, minsize=66)
        settings_card.rowconfigure(7, minsize=56)

        self.widgets.settings_panel_title_label = ttk.Label(settings_card, style="Section.TLabel")
        self.widgets.settings_panel_title_label.grid(row=0, column=0, sticky="w")

        self.widgets.settings_panel_hint_label = ttk.Label(
            settings_card,
            style="Hint.TLabel",
            wraplength=self.SIDE_HINT_WRAP,
            justify="left"
        )
        self.widgets.settings_panel_hint_label.grid(row=1, column=0, sticky="ew", pady=(6, 18))

        self.widgets.part1_label = ttk.Label(settings_card, style="Field.TLabel")
        self.widgets.part1_label.grid(row=2, column=0, sticky="w")

        self.widgets.part1_entry = ttk.Entry(settings_card, style="App.TEntry")
        self.widgets.part1_entry.grid(row=3, column=0, sticky="ew", pady=(6, 18))

        method_row = ttk.Frame(settings_card, style="Card.TFrame")
        method_row.grid(row=4, column=0, sticky="w")
        method_row.columnconfigure(0, weight=0)
        method_row.columnconfigure(1, weight=0)

        self.widgets.part2_label = ttk.Label(method_row, style="Field.TLabel")
        self.widgets.part2_label.grid(row=0, column=0, sticky="w")

        self.widgets.method_info_button = tk.Label(
            method_row,
            text="i",
            bg=self.PALETTE["accent"],
            fg="#ffffff",
            width=2,
            cursor="hand2",
            font=("Segoe UI Semibold", 9),
        )
        self.widgets.method_info_button.grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.widgets.method_tooltip = Tooltip(self.widgets.method_info_button, "")

        self.widgets.counter_type = tk.StringVar(value="Čísla")
        self.widgets.counter_menu = ttk.Combobox(
            settings_card,
            textvariable=self.widgets.counter_type,
            state="readonly",
            style="App.TCombobox"
        )
        self.widgets.counter_menu["values"] = ("Čísla", "Písmena")
        self.widgets.counter_menu.grid(row=5, column=0, sticky="ew", pady=(6, 22))

        self.widgets.rename_button = ttk.Button(settings_card, style="Accent.TButton", command=self.rename_and_refresh)
        self.widgets.rename_button.grid(row=6, column=0, sticky="ew", pady=(8, 8))

        self.widgets.undo_button = ttk.Button(settings_card, style="Outline.TButton", command=self.undo_last_rename)
        self.widgets.undo_button.grid(row=7, column=0, sticky="ew")
        self._set_undo_button_enabled(False)

        tips_card = ttk.Frame(
            side_panel,
            style="Card.TFrame",
            padding=20,
            width=self.SIDE_PANEL_WIDTH,
            height=self.TIPS_CARD_HEIGHT
        )
        tips_card.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        tips_card.grid_propagate(False)
        tips_card.columnconfigure(0, weight=1)
        tips_card.rowconfigure(1, minsize=44)
        tips_card.rowconfigure(2, minsize=48)
        tips_card.rowconfigure(3, minsize=58)

        self.widgets.tips_panel_title_label = ttk.Label(tips_card, style="Section.TLabel")
        self.widgets.tips_panel_title_label.grid(row=0, column=0, sticky="w")

        self.widgets.tips_line_1_label = ttk.Label(tips_card, style="Hint.TLabel", wraplength=self.TIPS_WRAP, justify="left")
        self.widgets.tips_line_1_label.grid(row=1, column=0, sticky="w", pady=(10, 6))

        self.widgets.tips_line_2_label = ttk.Label(tips_card, style="Hint.TLabel", wraplength=self.TIPS_WRAP, justify="left")
        self.widgets.tips_line_2_label.grid(row=2, column=0, sticky="w", pady=6)

        self.widgets.tips_line_3_label = ttk.Label(tips_card, style="Hint.TLabel", wraplength=self.TIPS_WRAP, justify="left")
        self.widgets.tips_line_3_label.grid(row=3, column=0, sticky="w", pady=(6, 0))

    def rename_and_refresh(self):
        """Run the rename service and reflect the result back into the UI."""
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

        self.last_rename_operation = list(result.operations)
        self._set_undo_button_enabled(bool(self.last_rename_operation))
        self.widgets.update_file_listbox(result.renamed_paths)
        success_message = self._current_texts()["rename_success_message"].format(count=len(result.renamed_paths))
        print(success_message)

    def undo_last_rename(self):
        """Attempt to restore the last successful batch rename."""
        if not self.last_rename_operation:
            messagebox.showinfo(
                self._current_texts()["undo_nothing_title"],
                self._current_texts()["undo_nothing_message"]
            )
            return

        try:
            result = self.rename_service.rollback_files(self.last_rename_operation)
        except ValidationError as error:
            messagebox.showwarning(self._current_texts()["undo_nothing_title"], str(error))
            return
        except RenameError as error:
            messagebox.showerror("Chyba vrácení", str(error))
            return

        self.last_rename_operation = list(result.retryable_operations)
        self._set_undo_button_enabled(bool(self.last_rename_operation))
        self.widgets.update_file_listbox(result.current_paths)

        if result.restored_count == result.total_count:
            success_message = self._current_texts()["undo_success_message"].format(count=result.restored_count)
            print(success_message)
            messagebox.showinfo(self._current_texts()["undo_success_title"], success_message)
            return

        details = self._format_result_details(result.skipped_messages)
        partial_message = self._current_texts()["undo_partial_message"].format(
            restored=result.restored_count,
            total=result.total_count,
        )
        if details:
            partial_message = f"{partial_message}\n\n{details}"

        print(partial_message)
        messagebox.showwarning(self._current_texts()["undo_partial_title"], partial_message)

    def _current_texts(self):
        """Return the currently active localization dictionary."""
        return TEXTS[self.state.current_lang]

    def _set_undo_button_enabled(self, enabled):
        """Enable or disable the undo button if it has been created."""
        if self.widgets.undo_button is None:
            return

        if enabled:
            self.widgets.undo_button.state(["!disabled"])
        else:
            self.widgets.undo_button.state(["disabled"])

    def _format_result_details(self, messages):
        """Limit verbose rollback warnings to a short readable preview."""
        if not messages:
            return ""

        preview = messages[:4]
        details = "\n\n".join(preview)
        if len(messages) > len(preview):
            details = f"{details}\n\n+{len(messages) - len(preview)} dalších položek"
        return details

    def create_main_window(self):
        """Create the Tk root window, build the layout, and enter the event loop."""
        root = TkinterDnD.Tk() if TkinterDnD is not None else tk.Tk()
        root.title(f"{APP_NAME} {APP_VERSION}")

        self._configure_styles(root)
        root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        root.minsize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        root.resizable(False, False)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        self._build_header(root)

        content = ttk.Frame(
            root,
            style="App.TFrame",
            padding=(28, 0, 28, 28),
            width=self.CONTENT_WIDTH,
            height=self.CONTENT_HEIGHT
        )
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_propagate(False)
        content.columnconfigure(0, minsize=self.FILE_PANEL_WIDTH, weight=0)
        content.columnconfigure(1, minsize=self.SIDE_PANEL_WIDTH, weight=0)
        content.rowconfigure(0, minsize=self.CONTENT_HEIGHT, weight=0)

        self._build_file_panel(content)
        self._build_settings_panel(content)

        self.widgets.update_texts()

        root.protocol("WM_DELETE_WINDOW", lambda: self.widgets.on_closing(root))
        root.mainloop()


