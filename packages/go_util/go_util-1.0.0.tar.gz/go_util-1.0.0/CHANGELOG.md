## 1.0.0dev0 (2024-10-07)

### BREAKING CHANGE

- this is supposed to be a breaking change
- This changes both the UX of the program (using subcommands instead of flags) and how the commands are internally processed (managed by click instead of using string comparison directly)

### Feat

- **cli**: added 'clean' and 'reset' subcommands
- **bookmarks.py**: added reset() and clean() functions to remove the project directory and bookmarks file respectively
- **breaking.txt**: added breaking.txt to simulate a breaking change and modified pyproject to version 1.0.0
- **cli**: added 'to' command to preserve primary program functionality
- configured build and dev environment to be managed by poetry
- **go-util**: added features from dev

### Fix

- testing and publishing first stable release
- **consent.py**: removed LICENSE file reading logic from consent.py
- **consent**: tried to patch the file path error one more time
- **consent.py**: fixed path displaying licence
- **consent.py**: addressed bug where consent.py could not find license
- **consent.py**: fixed bug preventing consent.py from properly locating LICENSE fille
- **bookmarks.py**: fixed compiler errors in bookmarks

### Refactor

- consent was excluded from last commit
- **consent**: used click library to handle user input instead of builtin input function
- **consent.py**: prompt_user_consent function now takes an 'eula_link' argument instead of a 'license_file' argument
- **consent.py**: added a link to EULA hosted on Notion
- **dev-branch**: merged fix/cz-versioning-bug into dev
- **src/go_util/cli.py**: refactored to use click for cli
- **src/tests**: moved /tests dir to project root
- refactored source code to be in /src directory
- **pyenv**: removed 'pyenv' directory from project
- **pyproject.toml,-setup.py**: migrated functionality of setup.py to pyproject.toml
- added a changelog file in main branch to be managed by commitizen
