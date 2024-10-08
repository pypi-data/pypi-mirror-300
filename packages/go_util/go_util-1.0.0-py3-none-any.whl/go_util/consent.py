# src/go_util/consent.py
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
import json
import importlib.resources
import click
from .bookmarks import BOOKMARKS_DIR

CONSENT_FILE = os.path.join(BOOKMARKS_DIR, "config.json")
EULA_LINK = "https://www.gnu.org/licenses/agpl-3.0.html#license-text"
REPO_LINK = "https://github.com/aiden2244/go-util"

def check_user_consent(consent_file=CONSENT_FILE):
    """Checks if the user has agreed to the license."""
    if not os.path.exists(consent_file):
        return False
    try:
        with open(consent_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('agreed_to_eula', False)
    except json.JSONDecodeError:
        return False

def prompt_user_consent(eula_link=EULA_LINK, consent_file=CONSENT_FILE, repo_link=REPO_LINK):
    """Prompts the user for EULA consent."""
    # Read and display the license
    print("Notice to End User: use of this software and its source code are subject to the terms")
    print("of the GNU AFFERO GENERAL PUBLIC LICENSE - v3.0 or later:\n")
    print(f"{eula_link}\n\n")
   
    print("In accordance with the terms of the APGL, the source code of this project can be found")
    print("at the following repository:\n")
    print(f"{repo_link}\n\n")

    print("By continuing, you affirm that you have read the agreement in full and agree to use this")
    print("program and its source code in accordance with the terms and conditions outlined as such.\n")


    consent_prompt = "Do you accept the terms of the EULA?"
    if click.confirm(consent_prompt, default=False):
        # Record consent
        config = {'agreed_to_eula': True}
        with open(consent_file, 'w', encoding='utf-8') as f:
            json.dump(config, f)
        return True
    else:
        print("You must agree to the EULA to use this software.")
        return False
