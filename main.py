import sys, atexit
from window import Window
from log import Log

def main():
    log = Log()
    log.checklog()
    loging = log.return_log_file()
    sys.stdout = loging
    sys.stderr = loging  # volitelně logni i chyby

    atexit.register(loging.close)

    Window().create_main_window()


if __name__ == "__main__":
    main()
