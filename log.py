import os
from datetime import datetime
import tkinter as tk


class Log:

    # Function that make sure that LOG folder and current LOG file exist
    def checklog(self):
        today_date = datetime.now().strftime('%Y-%m-%d')
        log_file_name = f"{today_date}.log"
        log_path = "log/"
        log_folder = "log"
        log_file = f"{log_path}{today_date}.log"

        # Check for existence of log file
        if os.path.isdir(log_path):
            file_location = os.path.join(log_path, log_file_name)
            # return bolean on check
            if os.path.isfile(file_location):
                return True
            # if file does not exist its created and return bolean
            else:
                with open(log_file, "w") as f:
                    f.write("Toto je první řádek v logu.\n")
                return False
        else:
            # If folder does not exist we create it.
            os.mkdir(log_folder)
            with open(log_file, "w") as f:
                f.write("Toto je první řádek v logu.\n")
            return False

    # Function that return current logfile name location and make it writable for system messages.
    def return_log_file(self):
        today_date = datetime.now().strftime('%Y-%m-%d')
        log_file = f"log/{today_date}.log"
        return open(log_file, "a", buffering=1)

    # function for loading last 1000 lines from current log file for displaing in log wiever
    def get_last_lines(self, log_file, num_lines=1000):
        try:
            with open(log_file, 'r') as file:
                lines = file.readlines()  # Načteme všechny řádky
                return lines[-num_lines:]  # Vezmeme posledních 'num_lines' řádků
        except FileNotFoundError:
            return ["Log file not found.\n"]
        except Exception as e:
            return [f"Error reading log file: {e}\n"]

    # function for refresh button in log wiever.
    def update_log_text(self, log_file, text_widget):
        lines = self.get_last_lines(log_file)
        text_widget.delete(1.0, tk.END)  # Vymažeme předchozí obsah
        text_widget.insert(tk.END, ''.join(lines))  # Vložíme nové řádky

    # creates Main window of log wiever.
    def create_ui(self):
        today_date = datetime.now().strftime('%Y-%m-%d')
        log_file = f"log/{today_date}.log"
        root = tk.Tk()
        root.title("Log Viewer")

        # Vytvoření Text widgetu pro zobrazení logu
        log_text = tk.Text(root, width=80, height=20)
        log_text.pack(padx=10, pady=10)

        # Zobrazíme poslední 10 řádků
        self.update_log_text(log_file, log_text)

        # Vytvoření tlačítka pro manuální aktualizaci
        refresh_button = tk.Button(root, text="Refresh", command=lambda: self.update_log_text(log_file, log_text))
        refresh_button.pack(pady=5)

        # Spuštění aplikace
        root.mainloop()



