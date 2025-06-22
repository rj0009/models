from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the chat file and train the model
            # This should ideally be an asynchronous task in a production app
            try:
                from chat_processor import parse_whatsapp_chat, preprocess_data
                from model_trainer import train_model

                parsed_messages = parse_whatsapp_chat(filepath)
                processed_text = preprocess_data(parsed_messages)

                model_name = filename.split('.')[0] # Use filename (without extension) as model_name
                # Define a subdirectory within 'models' for this specific chat
                model_output_base_dir = os.path.join('models', model_name)
                os.makedirs(model_output_base_dir, exist_ok=True)

                # The train_model function saves the model in a subfolder named model_name within output_dir
                # So, the actual path will be 'models/<filename_no_ext>/<filename_no_ext>'
                # For clarity, let's adjust `train_model` or how we call it.
                # Let's make `train_model` save directly into `model_output_base_dir`
                # and output_dir in train_model becomes the parent `models` dir, and `model_name` is the specific subfolder.

                # For simplicity, let's assume train_model saves into 'output_dir/model_name'
                # So, if output_dir is 'models', and model_name is 'chat1', it saves to 'models/chat1'

                # Check if model already exists to avoid retraining unless specified
                # This is a simple check; a more robust system would handle versions or force retraining.
                final_model_path = os.path.join('models', model_name) # This is where the model will be saved by train_model
                if not os.path.exists(os.path.join(final_model_path, "pytorch_model.bin")): # Check for a key model file
                    print(f"Training model: {model_name}")
                    train_model(processed_text, model_name=model_name, output_dir='models')
                else:
                    print(f"Model {model_name} already exists. Skipping training.")

                # Redirect to a chat page, passing the model name (which is derived from filename)
                return redirect(url_for('chat_page', model_name=model_name))
            except Exception as e:
                # Handle errors during processing or training
                print(f"Error processing file {filename}: {e}")
                # You might want to render an error page or flash a message
                return f"Error processing file: {e}", 500

    return render_template('upload.html')

# Keep track of loaded models and tokenizers to avoid reloading them on every request for the same model
loaded_models = {}

@app.route('/chat/<model_name>', methods=['GET', 'POST'])
def chat_page(model_name):
    from transformers import GPT2LMHeadModel, GPT2Tokenizer

    model_path = os.path.join('models', model_name)

    if model_name not in loaded_models:
        if not os.path.exists(model_path) or not os.path.exists(os.path.join(model_path, "pytorch_model.bin")):
            return "Model not found. Please upload and train the chat data first.", 404
        try:
            tokenizer = GPT2Tokenizer.from_pretrained(model_path)
            model = GPT2LMHeadModel.from_pretrained(model_path)
            model.eval() # Set to evaluation mode
            loaded_models[model_name] = {"model": model, "tokenizer": tokenizer, "history": []}
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            return f"Error loading model: {e}", 500

    chat_session = loaded_models[model_name]
    model = chat_session["model"]
    tokenizer = chat_session["tokenizer"]
    history = chat_session["history"] # List of strings

    if request.method == 'POST':
        user_input = request.form['user_input']
        history.append(f"User: {user_input}")

        # Simple context: join last few messages. More sophisticated context management is needed for long conversations.
        # The prompt should guide the model to act as the chatbot personality.
        # For now, we'll just use the recent history.
        # A better approach might be to format history like: "Person A: msg1\nPerson B: msg2\nPerson A: user_input\nPerson B:"

        # Construct prompt from history. Let's try to make it conversational.
        # We need to decide who the "bot" is. The training data implies the bot is one of the participants.
        # This part is tricky and needs a good prompting strategy.
        # For a basic version, let's just feed the recent conversation.

        # Max history tokens to consider to avoid overly long inputs to the model
        # This needs to be less than model's max input size (e.g., 1024 for GPT-2)
        # We'll take the last few interactions.
        context_messages = []
        temp_history = list(history) # Operate on a copy
        # A very naive way to build context - needs refinement
        # The training data is just a block of text. The model learns patterns.
        # When generating, we give it a prompt and it completes it.
        # We need to format the prompt so it knows it's its turn to speak.

        # Let's assume the training data was "Sender1: Hi\nSender2: Hello\nSender1: How are you?\nSender2: Good."
        # If user types "Hi", we want the model to respond as if it were the other person.
        # This requires knowing who the "user" is and who the "bot" should emulate.
        # This is a complex part of the "personality" aspect.
        # For now, let's just try a simple completion task based on the last input.

        prompt_text = "\n".join(history[-3:]) # Use last 3 exchanges as context

        inputs = tokenizer.encode(prompt_text + "\nAssistant:", return_tensors='pt', max_length=512, truncation=True)

        # Generate a response
        # Adjust max_length, num_beams, temperature, top_k, top_p for better responses
        # no_repeat_ngram_size can help reduce repetitive responses
        # pad_token_id is important if your prompt is shorter than max_length
        attention_mask = torch.ones(inputs.shape, dtype=torch.long, device=inputs.device) # Create attention mask

        outputs = model.generate(
            inputs,
            attention_mask=attention_mask,
            max_length=len(inputs[0]) + 60,  # Max length of generated text part
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id, # Use EOS token for padding during generation
            eos_token_id=tokenizer.eos_token_id,
            do_sample=True, # Enable sampling for more diverse outputs
            top_k=50,       # Consider only top_k tokens for sampling
            top_p=0.95,     # Nucleus sampling: cumulative probability cutoff
            temperature=0.8 # Controls randomness: lower is more deterministic
        )

        response_text = tokenizer.decode(outputs[0][inputs.shape[-1]:], skip_special_tokens=True).strip()

        # Naive split if model generates multiple lines or includes "User:" again
        response_text = response_text.split("\n")[0] # Take the first line of response

        history.append(f"Assistant: {response_text}")
        chat_session["history"] = history # Update history in loaded_models

        return render_template('chat.html', model_name=model_name, history=history)

    return render_template('chat.html', model_name=model_name, history=history)


if __name__ == '__main__':
    app.run(debug=True)
