# Simple mass rename (Alpha Version)

This application is designed to facilitate the bulk renaming of files based on user-defined parameters. Currently in its alpha stage, the application is primarily focused on providing core functionality, with more advanced features planned for future releases.

## Features

- **Bulk File Renaming**: Rename multiple files at once according to specified rules.
- **Basic Numbering**: Supports simple sequential numbering of files.
- **Alphabetical Sequence Naming**: Automatically generates alphabetical file names (e.g., 'A', 'AA', 'AAA') based on the total number of files to be renamed, ensuring consistent and sequential naming similar to Excel column labeling.

## Why This Application?

While searching for a simple and intuitive file renaming tool, I found existing solutions to be overly complex and not user-friendly. This application is designed to be straightforward and focused on functionality, making it easier to rename large sets of files, such as TV show episodes, without unnecessary complications.

## Installation

To install and run this application:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Mitelin/Simple-Rename
    ```

2. **Navigate to the Project Directory**:
    ```bash
    cd Simple-Rename
    ```

3. **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Application**:
    ```bash
    python main.py
    ```

The app uses Tkinter from the standard library plus `tkinterdnd2` for drag-and-drop support on Windows.

## Testing

Run the automated test suite with:

```bash
python -m unittest discover -s tests -v
```

The suite covers rename safety rules, numbering variants, controller behavior, drag-and-drop parsing, and core UI layout regressions.

## Roadmap

We are committed to expanding the capabilities of this application with the following planned features:

- **Advanced Numbering Options**: More sophisticated numbering schemes, including prefix, suffix, and step options.
- **Multi-language Support**: Providing localized versions of the application.
- **Rollback Functionality**: Allowing users to revert changes if needed.
- **User Interface Enhancements**: Improving the overall user experience with a more intuitive and polished interface.

## Contribution

We welcome contributions to this project. If you would like to contribute, please feel free to fork the repository and submit a pull request. For any issues or feature requests, please open an issue in the GitHub repository.

## Contact

For any questions, suggestions, or feedback, please contact us through the repository's GitHub issues page.
