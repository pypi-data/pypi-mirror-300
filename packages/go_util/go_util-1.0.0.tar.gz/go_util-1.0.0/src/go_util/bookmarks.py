# src/go_util/bookmarks.py
# (c) Aiden McCormack, 2024. All rights reserved.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import shutil
import webbrowser
from appdirs import user_data_dir

APP_NAME = "go_util"
APP_AUTHOR = "AidenMcCormack"

BOOKMARKS_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
BOOKMARKS_FILE = os.path.join(BOOKMARKS_DIR, "bookmarks.txt")

def ensure_bookmarks_file():
    """Ensures the bookmarks directory and file exist."""
    if not os.path.exists(BOOKMARKS_DIR):
        os.makedirs(BOOKMARKS_DIR)
    if not os.path.exists(BOOKMARKS_FILE):
        open(BOOKMARKS_FILE, 'a', encoding='utf-8').close()  

def add_alias(alias, link):
    """Adds a new alias and link to bookmarks.txt."""
    alias = alias.lower()  
    with open(BOOKMARKS_FILE, 'a', encoding='utf-8', newline='') as bookmarks:  
        bookmarks.write(f"{alias} {link}\n")
    print(f"Added bookmark: {alias} -> {link}")

def remove_alias(alias):
    """Removes an alias and its associated URL from bookmarks.txt."""
    alias = alias.lower()  
    temp_file = os.path.join(BOOKMARKS_DIR, "temp.txt")
    found = False  
    with open(BOOKMARKS_FILE, 'r', encoding='utf-8', newline='') as bookmarks, \
         open(temp_file, 'w', encoding='utf-8') as temp:
        for line in bookmarks:
            current_alias, _ = line.strip().split(maxsplit=1)
            if current_alias.lower() != alias:
                temp.write(line)
            else:
                found = True
    if found:
        os.replace(temp_file, BOOKMARKS_FILE)
        print(f"Removed link associated with alias '{alias}'")
    else:
        os.remove(temp_file)
        print(f"No alias '{alias}' found.")

def list_aliases():
    """Lists all saved aliases and their URLs."""
    print("\n=============== SAVED LINKS ===============\n")
    with open(BOOKMARKS_FILE, 'r', encoding='utf-8', newline='') as bookmarks:  
        for line in bookmarks:
            print(line.strip())
    print("\n===========================================\n")

def open_alias(alias):
    """Opens the URL associated with the alias in the default web browser."""
    alias = alias.lower()  
    with open(BOOKMARKS_FILE, 'r', encoding='utf-8', newline='') as bookmarks:  
        for line in bookmarks:
            current_alias, url = line.strip().split(maxsplit=1)
            if current_alias.lower() == alias:
                webbrowser.open(url)  
                return
    print(f"No match found for alias '{alias}'.")

def clean_bookmarks(bookmarks_file=BOOKMARKS_FILE):
    """Removes the file containing the bookmarks"""
    if not os.path.exists(bookmarks_file):
        raise FileNotFoundError(f"ERROR cleaning: {bookmarks_file} does not exist")
    os.remove(bookmarks_file)

def reset_go_util(bookmarks_dir=BOOKMARKS_DIR):
    """Removes the entire directory containing generated files."""
    if not os.path.exists(bookmarks_dir):
        raise FileNotFoundError(f"ERROR resetting: {bookmarks_dir} does not exist")
    
    shutil.rmtree(bookmarks_dir)
    return bookmarks_dir

    