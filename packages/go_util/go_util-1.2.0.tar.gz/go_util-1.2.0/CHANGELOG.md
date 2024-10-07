## 1.2.0 (2024-10-06)

### Fix

- **consent.py**: removed LICENSE file reading logic from consent.py

### Refactor

- **consent**: used click library to handle user input instead of builtin input function
- **consent.py**: prompt_user_consent function now takes an 'eula_link' argument instead of a 'license_file' argument
- **consent.py**: added a link to EULA hosted on Notion

## 1.1.8 (2024-09-29)

### Fix

- **consent**: tried to patch the file path error one more time
- **consent.py**: fixed path displaying licence

## 1.1.4-a0 (2024-09-28)

### Fix

- **consent.py**: addressed bug where consent.py could not find license

## 1.1.3-a0 (2024-09-27)

### Fix

- **consent.py**: fixed bug preventing consent.py from properly locating LICENSE fille

## 1.1.1 (2024-09-27)

### Fix

- **bookmarks.py**: fixed compiler errors in bookmarks

## 1.1.0 (2024-09-27)

### Feat

- **cli**: added 'clean' and 'reset' subcommands
- **bookmarks.py**: added reset() and clean() functions to remove the project directory and bookmarks file respectively

### Refactor

- **dev-branch**: merged fix/cz-versioning-bug into dev

## 1.0.0 (2024-09-27)

### BREAKING CHANGE

- this is supposed to be a breaking change

### Feat

- **breaking.txt**: added breaking.txt to simulate a breaking change and modified pyproject to version 1.0.0

## 0.2.0 (2024-09-27)

### BREAKING CHANGE

- This changes both the UX of the program (using subcommands instead of flags) and how the commands are internally processed (managed by click instead of using string comparison directly)

### Feat

- **cli**: added 'to' command to preserve primary program functionality

### Refactor

- **src/go_util/cli.py**: refactored to use click for cli

## 0.2.0-a0 (2024-09-23)

### Feat

- configured build and dev environment to be managed by poetry

### Refactor

- **src/tests**: moved /tests dir to project root

## 0.1.1-a0 (2024-09-22)

### Refactor

- refactored source code to be in /src directory
- **pyenv**: removed 'pyenv' directory from project
- **pyproject.toml,-setup.py**: migrated functionality of setup.py to pyproject.toml

## 0.1.0 (2024-09-22)

### Feat

- **go-util**: added features from dev

## 0.0.2 (2024-09-22)

### Refactor

- added a changelog file in main branch to be managed by commitizen
