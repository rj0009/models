import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

def train_model(text_data, model_name="whatsapp_chatbot", output_dir="./models", model_base="gpt2"):
    """
    Fine-tunes a GPT-2 model on the provided text data.

    Args:
        text_data (str): A single string containing all the chat messages.
        model_name (str): Name for the output model directory.
        output_dir (str): Directory to save the trained model and tokenizer.
        model_base (str): The base GPT-2 model to fine-tune (e.g., "gpt2", "gpt2-medium").

    Returns:
        str: Path to the saved model.
    """
    # Create a temporary file for the dataset
    temp_train_file = f"{model_name}_train_data.txt"
    with open(temp_train_file, "w", encoding="utf-8") as f:
        f.write(text_data)

    # Load tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained(model_base)
    model = GPT2LMHeadModel.from_pretrained(model_base)

    # Special tokens (if not already present)
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer)) # Resize model embeddings

    # Create dataset and data collator
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=temp_train_file,
        block_size=128  # Adjust block size based on your data and memory
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # We are doing causal LM (next token prediction), not masked LM
    )

    # Define training arguments
    model_output_path = os.path.join(output_dir, model_name)
    training_args = TrainingArguments(
        output_dir=model_output_path,
        overwrite_output_dir=True,
        num_train_epochs=1, # Start with 1 epoch for quick testing, increase for better results
        per_device_train_batch_size=1, # Adjust based on GPU memory
        save_steps=10_000, # How often to save checkpoints
        save_total_limit=2, # Limit the number of checkpoints
        logging_steps=500, # How often to log training progress
        # Add learning_rate, weight_decay etc. as needed for fine-tuning
        # For smaller datasets or quicker runs, you might use fewer epochs and smaller batch sizes.
        # Consider adding gradient_accumulation_steps if per_device_train_batch_size is small.
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )

    # Start training
    print(f"Starting fine-tuning for model: {model_name} based on {model_base}")
    trainer.train()
    print("Training complete.")

    # Save the fine-tuned model and tokenizer
    trainer.save_model(model_output_path)
    tokenizer.save_pretrained(model_output_path)
    print(f"Model and tokenizer saved to {model_output_path}")

    # Clean up temporary training file
    os.remove(temp_train_file)

    return model_output_path

if __name__ == '__main__':
    # Example Usage (requires a GPU or will be very slow)
    # Create dummy data for testing
    dummy_text = """\
Person A: Hello, how are you?
Person B: I'm fine, thank you. How about you?
Person A: I'm doing well. Been working on a new project.
Person B: Oh really? What is it about?
Person A: It's a chatbot that learns from conversations.
Person B: That sounds fascinating!
Person A: It is! The goal is to make it sound very natural.
Person B: I'd love to try it out when it's ready.
Person A: Sure, I'll let you know.
Person B: Great, thanks!
"""
    # Ensure models directory exists
    if not os.path.exists("./models"):
        os.makedirs("./models")

    print("Starting dummy model training example...")
    # Note: This will download GPT-2 model files from Hugging Face if not cached.
    # This training is very minimal and just for demonstration.
    # Real training would require more data, epochs, and hyperparameter tuning.
    try:
        trained_model_path = train_model(
            dummy_text,
            model_name="dummy_chatbot_test",
            output_dir="./models/test_models",
            model_base="gpt2" # Using the smallest GPT-2 for faster example
        )
        print(f"Dummy model trained and saved to: {trained_model_path}")

        # Test loading the model (optional)
        # tokenizer = GPT2Tokenizer.from_pretrained(trained_model_path)
        # model = GPT2LMHeadModel.from_pretrained(trained_model_path)
        # print("Dummy model loaded successfully for verification.")

    except Exception as e:
        print(f"An error occurred during the dummy training: {e}")
        print("Please ensure you have PyTorch, Transformers, and internet access for model downloads.")
        print("If on a system without a GPU, training will be very slow. Consider reducing epochs or using a CPU-only setup for testing.")

    # To clean up the dummy model after testing:
    # import shutil
    # if os.path.exists("./models/test_models/dummy_chatbot_test"):
    #     shutil.rmtree("./models/test_models/dummy_chatbot_test")
    # if os.path.exists("dummy_chatbot_test_train_data.txt"):
    #      os.remove("dummy_chatbot_test_train_data.txt")
    # print("Cleaned up dummy model files.")
