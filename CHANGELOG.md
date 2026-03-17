# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-17

### Added
- Safe bulk rename for files across one or more folders while preserving each file's original directory.
- Number and Excel-style letter sequences with automatic padding and preserved file extensions.
- Undo for the last successful batch rename with partial-restore reporting.
- Manual file ordering controls including move up, move down, move to top, move to bottom, and reverse order.
- CZ and EN UI texts, built-in logging, and a simple log viewer.
- Drag-and-drop file import from Windows Explorer with automated regression coverage.

### Changed
- Refined the desktop UI layout so key controls remain stable across Czech and English labels.
- Reduced rename success flow noise by relying on the refreshed list and log output instead of a separate success dialog.

### Fixed
- Prevented rename targets from escaping their original directories when files with the same basename are selected from different folders.
- Blocked collisions with external existing files before starting a batch rename.
- Added a graceful TkDND fallback so the app and UI tests keep working when tkinterdnd2 is installed but the tkdnd command is unavailable.