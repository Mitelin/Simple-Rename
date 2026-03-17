"""Utilities for creating, reading, and displaying application log files."""

import os
from datetime import datetime
import tkinter as tk


class Log:
    """Manage the daily log file and its simple viewer window."""

    def checklog(self):
        """Ensure that the log directory and today's log file exist."""
        today_date = datetime.now().strftime('%Y-%m-%d')
        log_file_name = f"{today_date}.log"
        log_path = "log/"
        log_folder = "log"
        log_file = f"{log_path}{today_date}.log"

        if os.path.isdir(log_path):
            file_location = os.path.join(log_path, log_file_name)
            if os.path.isfile(file_location):
                return True
            else:
                with open(log_file, "w") as f:
                    f.write("Toto je první řádek v logu.\n")
                return False
        else:
            os.mkdir(log_folder)
            with open(log_file, "w") as f:
                f.write("Toto je první řádek v logu.\n")
            return False

    def return_log_file(self):
        """Open today's log file in append mode for stdout and stderr redirection."""
        today_date = datetime.now().strftime('%Y-%m-%d')
        log_file = f"log/{today_date}.log"
        return open(log_file, "a", buffering=1, encoding="utf-8")

    def get_last_lines(self, log_file, num_lines=1000):
        """Return up to the latest ``num_lines`` lines from a log file."""
        try:
            with open(log_file, 'r') as file:
                lines = file.readlines()
                return lines[-num_lines:]
        except FileNotFoundError:
            return ["Log file not found.\n"]
        except Exception as e:
            return [f"Error reading log file: {e}\n"]

    def update_log_text(self, log_file, text_widget):
        """Reload the visible contents of the log viewer text widget."""
        lines = self.get_last_lines(log_file)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, ''.join(lines))

    def create_ui(self):
        """Open a lightweight viewer window for today's log file."""
        today_date = datetime.now().strftime('%Y-%m-%d')
        log_file = f"log/{today_date}.log"
        parent = tk._default_root
        root = tk.Toplevel(parent) if parent is not None else tk.Tk()
        root.title("Log Viewer")

        log_text = tk.Text(root, width=80, height=20)
        log_text.pack(padx=10, pady=10)

        self.update_log_text(log_file, log_text)

        refresh_button = tk.Button(root, text="Refresh", command=lambda: self.update_log_text(log_file, log_text))
        refresh_button.pack(pady=5)

        if parent is None:
            root.mainloop()



