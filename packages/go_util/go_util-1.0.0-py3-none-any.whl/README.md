## OVERVIEW

`go-util` is a cross-platform CLI bookmark manager. It allows users to create aliases for URLs, which can be accessed quickly from the terminal using the `go` command. The utility also supports adding new links, removing links, and managing stored bookmarks through various commands.

## INSTALLATION

### Prerequisites
1. **Python:** This software is built in Python and thus requires Python 3.9 or greater to run. To install Python on your system, please refer to the official downloads page: https://www.python.org/downloads/

2. **pipx:** As `go-util` is a standalone CLI app, it is best to install via pipx to isolate it from the rest of your system. To install pipx, first ensure Python is installed then refer to the official documentation: https://github.com/pypa/pipx

### Installing on your system
To install `go-util`, follow these steps:

1. **Install via pipx (RECOMMENDED)**:
   Installing via pipx ensures that the application is both available globally and contained within its own isolated environment. 
   
   To install, open your terminal and run the following command:

   ```bash
   pipx install go-util
   ```
    This will install the `go-util` utility, making it available globally on your system.


2. **Install via pip (ADVANCED)**:
    If you would prefer to install `go-util` in a virtual environment (or, at your own risk, in your Python distribution's global environment), go-util is also available via pip:

    ```bash
    pip install go-util
    ```

    Note that while this option exists, it is generally advisable to not install CLI applications globally, thus installing via pipx is **highly** recommended.

## USAGE

The `go-util` CLI has the following commands and options:

### General Usage:

```bash
go [OPTIONS] COMMAND [ARGS]...
```

- `--help`: Show the help message for any command.

### Available Commands:

#### 1. `go add`
   **Adds a new alias with a corresponding URL.**

   Usage:

   ```bash
   go add [ALIAS] [LINK]
   ```

   Example:

   ```bash
   go add wiki https://en.wikipedia.org/wiki/Main_Page
   ```

#### 2. `go to`
   **Opens a saved alias in the default web browser.**

   Usage:

   ```bash
   go to [ALIAS]
   ```

   Example:

   ```bash
   go to wiki
   ```

#### 3. `go list`
   **Lists all saved aliases and their corresponding URLs.**

   Usage:

   ```bash
   go list
   ```

#### 4. `go remove`
   **Removes an existing alias.**

   Usage:

   ```bash
   go remove [ALIAS]
   ```

   Example:

   ```bash
   go remove wiki
   ```

#### 5. `go clean`
   **Deletes all saved bookmarks.**

   Usage:

   ```bash
   go clean
   ```

#### 6. `go reset`
   **Removes all program-generated data (e.g., on uninstall).**

   Usage:

   ```bash
   go reset
   ```

### Example Workflow:

1. **Adding a bookmark**:
   ```bash
   go add google https://www.google.com
   ```

2. **Opening a saved bookmark**:
   ```bash
   go to google
   ```

3. **Listing all saved bookmarks**:
   ```bash
   go list
   ```

4. **Removing a bookmark**:
   ```bash
   go remove google
   ```

5. **Resetting the program**:
   ```bash
   go reset
   ```

## Attributions

The development of `go-util` relies on several open-source libraries and tools, which have been essential in building and testing the project.

For a full list of runtime and development dependencies, including their licenses, please refer to the [DEPENDENCIES.md](DEPENDENCIES.md) file. You can also find the full text of each license in the [licenses/](licenses/) directory.

I extend my thanks to the authors and contributors of these projects for their work.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You can find the full text of the license in the [LICENSE.txt](LICENSE.txt) file or at the [GNU AGPL v3](https://www.gnu.org/licenses/agpl-3.0.html).

### Contributions

By contributing to this project, you agree that your contributions will be licensed under the AGPL v3, in line with the project's license.

### Third-Party Licenses

This project includes dependencies that are released under their respective open-source licenses (e.g., MIT, BSD). You can find more details in the [DEPENDENCIES.md](DEPENDENCIES.md) file or the `licenses/` directory.

### Disclaimer

This software is provided "as is", without any warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

### Copyright Notice

Copyright (c) Aiden McCormack, 2024. All Rights Reserved.


