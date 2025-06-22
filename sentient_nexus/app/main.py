# Main application file for Sentient Nexus
import os
import click
from app.core.note_manager import add_note, DATA_DIR

@click.group()
def cli():
    """Sentient Nexus: A CLI for your Second Brain."""
    pass

@cli.command("add")
@click.option("--filename", "-f", help="Optional filename for the note.")
@click.argument("content", required=True)
def add_note_command(content: str, filename: str | None):
    """Adds a new note."""
    try:
        note_path = add_note(content, filename)
        click.echo(f"Note saved to: {note_path}")
    except IOError as e:
        click.echo(f"Error: {e}", err=True)

@cli.command("list")
def list_notes_command():
    """Lists all existing notes."""
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        click.echo("No notes found.")
        return

    click.echo("Your notes:")
    for note_file in sorted(os.listdir(DATA_DIR)):
        if note_file.endswith(".txt"): # Basic filtering
            click.echo(f"- {note_file}")

if __name__ == "__main__":
    cli()
