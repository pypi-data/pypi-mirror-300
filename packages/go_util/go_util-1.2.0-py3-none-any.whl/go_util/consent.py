# src/go_util/consent.py
# (c) Aiden McCormack, 2024. All rights reserved.

import os
import json
import importlib.resources
import click
from .bookmarks import BOOKMARKS_DIR

CONSENT_FILE = os.path.join(BOOKMARKS_DIR, "config.json")
EULA_LINK = "https://thundering-reaper-359.notion.site/END-USER-LICENSE-AGREEMENT-EULA-117f980b9b568038b74bedf1bac8dd88"

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

def prompt_user_consent(eula_link=EULA_LINK, consent_file=CONSENT_FILE):
    """Prompts the user for EULA consent."""
    # Read and display the license
    print("Notice to End User: use of this software and its source code are subject to the terms")
    print("of the following End User License Agreement (EULA):")
    print()
    print(f"{eula_link}\n")
    print("By continuing, you affirm that you have read the EULA in full and agree to use this")
    print("program and its source code in accordance with the terms and conditions outlined as such.")

    consent_prompt = "\nDo you accept the terms of the EULA?"
    if click.confirm(consent_prompt, default=False):
        # Record consent
        config = {'agreed_to_eula': True}
        with open(consent_file, 'w', encoding='utf-8') as f:
            json.dump(config, f)
        return True
    else:
        print("You must agree to the EULA to use this software.")
        return False
