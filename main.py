from window import Window
from config import StaticConfig


def main():
    # call for main window creation
    static_configuration = StaticConfig()
    window = Window(static_configuration)
    window.create_main_window()


if __name__ == "__main__":
    main()

