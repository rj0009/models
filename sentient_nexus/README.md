# Sentient Nexus

A personalized Second Brain application to enhance productivity, creativity, and long-term memory.
Project initiated to support a Singapore government professional driving AI initiatives.

## Current Functionality (MVP - Phase 1)

This initial version focuses on basic text-based note-taking via a Command Line Interface (CLI).

### Features

*   **Add Notes:** Save text content as notes. Notes are stored as `.txt` files in the `data/` directory.
*   **List Notes:** View all notes currently stored.

### Setup and Installation

1.  **Prerequisites:**
    *   Python 3.8+
    *   pip (Python package installer)

2.  **Clone the repository (if applicable) or download the files.**

3.  **Navigate to the project root directory (`sentient_nexus`).**
    ```bash
    cd path/to/sentient_nexus
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` currently includes `click` and `pytest`)*

### Usage

All commands are run from the `sentient_nexus` project root directory.

**1. Adding a new note:**

*   Provide content directly:
    ```bash
    python app/main.py add "This is my first note about AI governance."
    ```
*   Provide content and a custom filename:
    ```bash
    python app/main.py add --filename "my_thoughts.txt" "Some thoughts on policy."
    ```
    (or `python app/main.py add -f "my_thoughts.txt" "Some thoughts on policy."`)

    Notes will be saved in the `data/` directory. If no filename is provided, a timestamp-based filename will be generated (e.g., `note_YYYYMMDD_HHMMSS.txt`).

**2. Listing existing notes:**

```bash
python app/main.py list
```
This will display a list of `.txt` files found in the `data/` directory.

### Running Tests

To ensure the application is working correctly, you can run the automated tests.

1.  **Navigate to the directory *containing* the `sentient_nexus` project root.**
    ```bash
    cd path/to/parent_of_sentient_nexus
    ```
2.  **Run the tests:**
    ```bash
    python -m unittest discover -s sentient_nexus/tests
    ```
    You should see output indicating that all tests passed.

## Next Steps for "Quick Notes" Feature

*   **View Note Content:** Add a command to display the content of a specific note.
*   **Edit Notes:** Implement functionality to modify existing notes.
*   **Delete Notes:** Allow users to remove notes.
*   **More Robust Storage:** Consider alternatives to plain text files if metadata or more complex structures are needed soon (e.g., JSON, SQLite).
*   **Voice-to-Text:** Integrate voice input for note creation (requires external libraries/services).

## Future Vision (High-Level from Prompt)

This project aims to evolve into a comprehensive "Sentient Nexus" with features including:
*   Web Capture, EPUB & Document Ingestion
*   Visual Knowledge Graph & AI Chat Interface
*   Automated Tagging & Semantic Search
*   Task & Project Management Integration
*   Idea Generation & Incubation tools
*   Personalized Learning & Reflection Dashboards
*   Integrations with MS Office, Google Workspace, etc.
*   Strong focus on security and privacy.
