# WhatsApp Chatbot Trainer

This application allows you to upload your WhatsApp chat history (exported as a `.txt` file) and fine-tune a GPT-2 model based on that chat. You can then interact with this personalized chatbot.

## Project Structure

```
.
├── app.py                # Main Flask application
├── chat_processor.py     # Module for parsing and preprocessing WhatsApp chat files
├── model_trainer.py      # Module for fine-tuning the GPT-2 model
├── requirements.txt      # Python dependencies
├── templates/
│   ├── upload.html       # HTML for the file upload page
│   └── chat.html         # HTML for the chatbot interaction page
├── tests/
│   ├── test_chat_processor.py # Unit tests for chat_processor.py
│   └── test_app.py            # Integration tests for the Flask app (currently facing environment issues)
├── uploads/              # Directory where uploaded chat files are stored (created automatically)
└── models/               # Directory where fine-tuned models are stored (created automatically)
```

## Setup and Installation

**Note:** Due to potentially large dependencies (PyTorch, Transformers), ensure you have sufficient disk space. If you encounter space issues, especially with CUDA versions of PyTorch, you might need to install CPU-only versions.

1.  **Clone the repository (if applicable) or ensure all project files are in a directory.**

2.  **Create a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    The `requirements.txt` is configured to use a CPU-only version of PyTorch to save space. If you have a GPU and sufficient space, you can change `torch --index-url https://download.pytorch.org/whl/cpu` to just `torch` in `requirements.txt` before installing.
    ```bash
    pip install -r requirements.txt
    ```
    If you still face disk space issues, the environment might be too constrained for these libraries.

## How to Run

1.  **Ensure all dependencies are installed.**
2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
3.  **Open your web browser and go to:** `http://127.0.0.1:5000/`

## Usage

1.  **Upload Chat File:**
    *   On the main page, you'll see an upload form.
    *   Click "Choose File" and select your WhatsApp chat history file (must be a `.txt` file).
        *   To export your WhatsApp chat: Open the chat -> Tap on the three dots (menu) -> More -> Export chat -> Without media.
    *   Click "Upload".

2.  **Model Training:**
    *   After uploading, the application will:
        *   Parse the chat file.
        *   Fine-tune a GPT-2 model using the chat data. This may take some time, especially on a CPU. The model will be saved in the `models/<chat_filename_without_extension>/` directory.
        *   If a model for that chat file already exists, training will be skipped.
    *   You will be redirected to the chat interface page.

3.  **Chat with your Bot:**
    *   On the chat page, type your message in the input box and press Enter or click "Send".
    *   The chatbot, powered by the fine-tuned model, will respond based on the personality and context learned from your chat history.
    *   Conversation history is maintained for the current session with that model.

## Running Tests

Unit tests for the chat processor can be run using:
```bash
python -m unittest tests/test_chat_processor.py
```
Integration tests for the Flask application (`tests/test_app.py`) are available but may require a robust environment with all dependencies (including PyTorch/Transformers) correctly installed. Due to sandbox limitations during development, these might not pass in very constrained environments.
```bash
python -m unittest tests/test_app.py
```

## Important Notes & Limitations

*   **Model Quality:** The quality of the chatbot heavily depends on the size and variety of your chat history, as well as the fine-tuning process (e.g., number of epochs, hyperparameters in `model_trainer.py`). The current setup uses minimal training (1 epoch) for demonstration purposes. For better results, increase epochs and consider hyperparameter tuning.
*   **Training Time:** Fine-tuning LLMs can be time-consuming, especially without a GPU. The application currently performs training synchronously after file upload, which might lead to a long wait time in the browser. For production use, training should be handled as an asynchronous background task.
*   **Context Management:** The chatbot's ability to maintain long conversations and complex context is limited by the base model's architecture (GPT-2) and the current simple context handling (last few messages).
*   **Resource Intensive:** LLMs are resource-intensive. Running the training and even inference can consume significant CPU/GPU and RAM.
*   **Error Handling:** The application has basic error handling. More robust error management would be needed for a production system.
*   **Security:** Uploaded chat files are stored on the server. Ensure appropriate security measures if deploying this application. Model names are derived from filenames; ensure filenames don't contain sensitive information if this is a concern.

## Potential Future Improvements

*   Asynchronous model training (e.g., using Celery, RQ).
*   More sophisticated prompt engineering for better chatbot personality and control.
*   Advanced context management techniques.
*   Allowing users to select different base models or specify training parameters.
*   User authentication and management of multiple trained models.
*   Better UI/UX, including loading indicators and real-time chat updates.
*   Option to delete uploaded data and trained models.
