"""Application entry point for the Simple Rename desktop app."""

import atexit
import sys

from window import Window
from log import Log


def main():
    """Initialize logging, redirect console output, and start the main window."""
    log = Log()
    log.checklog()
    loging = log.return_log_file()
    sys.stdout = loging
    sys.stderr = loging

    atexit.register(loging.close)

    Window().create_main_window()


if __name__ == "__main__":
    main()
