import sys
from window import Window
from log import Log

def main():
    # call for main window creation whit checks for existence of required files and start loging
    log = Log()
    log.checklog()
    loging = log.return_log_file()
    sys.stdout = loging
    window = Window()
    window.create_main_window()
    loging.close()


if __name__ == "__main__":
    main()
