# src/go_util/cli.py
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


import click
from go_util.bookmarks import (
    ensure_bookmarks_file,
    add_alias,
    remove_alias,
    list_aliases,
    open_alias,
    clean_bookmarks,
    reset_go_util,
)
from go_util.consent import check_user_consent, prompt_user_consent

@click.group()
def cli():
    """CLI for managing bookmarks with go."""
    ensure_bookmarks_file()

    # Check for user consent
    if not check_user_consent():
        consent = prompt_user_consent()
        if not consent:
            raise click.Abort()

@cli.command()
@click.argument('alias')
def to(alias):
    """Opens a saved alias."""
    open_alias(alias)

@cli.command()
@click.argument('alias')
@click.argument('link')
def add(alias, link):
    """Adds a new alias with a corresponding URL."""
    add_alias(alias, link)

@cli.command()
@click.argument('alias')
def remove(alias):
    """Removes an existing alias."""
    remove_alias(alias)

@cli.command()
def list():
    """Lists all saved aliases and their corresponding URLs."""
    list_aliases()

@cli.command()
def clean():
    """Removes the bookmarks.txt file if user chooses."""
    warning = (
        "WARNING: this action will permanently erase all existing bookmarks.\n\n"
        "Do you wish to proceed ('y' to continue, 'n' or ENTER to abort)?"
    )
    if click.confirm(warning, default=False):
        try:
            clean_bookmarks()
            click.echo("Successfully removed all bookmarks.")
        except FileNotFoundError:
            click.echo("No bookmarks file found to delete.")
        except Exception as e:
            click.echo(f"An error occurred: {e}")
    else:
        print("Process aborted.")

@cli.command()
@click.argument('called_on_uninstall', required=False, default=False)
def reset(called_on_uninstall):
    """Removes all program-generated data if user chooses or on uninstall."""

    def perform_reset():
        try:
            click.echo("Removing program-generated data...")
            go_util_dir = reset_go_util()
            click.echo(f"Successfully removed {go_util_dir}")
        except FileNotFoundError:
            click.echo("Error: The directory does not exist.")
        except Exception as e:
            click.echo(f"An unexpected error occurred: {str(e)}")

    if called_on_uninstall:
        perform_reset()
        return

    warning = (
        "WARNING: this action will permanently erase all program-generated data.\n"
        "Proceeding will require you re-accept the terms and conditions as detailed\n"
        "in the EULA should you resume use of this program in the future.\n\n"
        "Do you wish to proceed? ('y' to continue, 'n' or ENTER to abort)"
    )
    if click.confirm(warning, default=False):
        perform_reset()
    else:
        print("Process aborted.")
    


if __name__ == "__main__":
    cli()
