import os
import datetime

# Relative to this file (note_manager.py), to reach sentient_nexus/data/
# This assumes main.py (or any script importing this) is run from the project root.
# A more robust solution might involve passing the base path or using __file__.
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

def add_note(content: str, filename: str = None) -> str:
    """
    Saves content to a text file in the DATA_DIR.

    Args:
        content: The string content of the note.
        filename: Optional. The desired filename. If None, a timestamp-based
                  filename will be generated.

    Returns:
        The path to the saved note file.

    Raises:
        IOError: If there's an issue creating the directory or writing the file.
    """
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
        except OSError as e:
            raise IOError(f"Could not create data directory: {DATA_DIR}") from e

    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"note_{timestamp}.txt"

    filepath = os.path.join(DATA_DIR, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Could not write to file: {filepath}") from e

    return filepath
