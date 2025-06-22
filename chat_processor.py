import re

def parse_whatsapp_chat(file_path):
    """
    Parses a WhatsApp chat export file.
    Assumes the standard WhatsApp export format:
    [DD/MM/YYYY, HH:MM:SS] Sender: Message
    or
    DD/MM/YYYY, HH:MM - Sender: Message (older format)
    """
    messages = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Regex to capture date, time, sender, and message
            # This regex tries to be robust to different WhatsApp export formats
            # It looks for a date-like pattern, then a time-like pattern, then a sender, then the message
            # It also handles system messages that don't have a sender.
            match = re.match(r'\[?(\d{1,2}/\d{1,2}/\d{2,4}),? (\d{1,2}:\d{2}(?::\d{2})?(?: [AP]M)?)\s*\]?\s*(?:-\s*)?([^:]+):\s*(.*)', line)
            if match:
                # date_str, time_str, sender, message_text = match.groups()
                # For now, we are only interested in the message text for training
                messages.append(match.group(4).strip())
            else:
                # Handle lines that might be continuations of previous messages or system messages
                # For simplicity, we'll append them to the last message if they don't match the sender pattern
                # Or if it's a system message (e.g., "You created this group"), we might want to filter it.
                # For now, if it doesn't have a 'Sender:' part, we'll consider it part of the previous message or ignore.
                # A more sophisticated approach would be needed for perfect parsing.
                if messages and not re.match(r'\[?\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2}', line): # not a new message start
                    if line.strip(): # Append if not empty
                        messages[-1] += " " + line.strip()
                # else:
                # Potentially log or handle system messages or unparsed lines
                # print(f"Skipping line: {line.strip()}")
    return messages

def preprocess_data(messages):
    """
    Basic preprocessing of messages.
    - Concatenate messages into a single text block for training.
    - Could add more steps like lowercasing, removing special characters, etc.
    """
    return "\n".join(messages)

if __name__ == '__main__':
    # Example usage:
    # Create a dummy chat file for testing
    dummy_chat_content = """\
[01/01/2023, 10:00:00] Alice: Hi Bob!
[01/01/2023, 10:00:05] Bob: Hey Alice, how are you?
[01/01/2023, 10:00:10] Alice: I'm good, thanks! Just working on this project.
It's quite interesting.
[01/01/2023, 10:00:15] Bob: Sounds cool! What's it about?
02/01/2023, 11:00 AM - Charles: Hey everyone!
[02/01/2023, 11:00:30 AM] Diana: Hi Charles
Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.
[03/01/2023, 12:00:00] Eve: Lunchtime! 🍕
"""
    dummy_file_path = "dummy_chat.txt"
    with open(dummy_file_path, "w", encoding="utf-8") as f:
        f.write(dummy_chat_content)

    parsed_messages = parse_whatsapp_chat(dummy_file_path)
    print("Parsed Messages:")
    for msg in parsed_messages:
        print(f"- {msg}")

    processed_text = preprocess_data(parsed_messages)
    print("\nProcessed Text for Training:")
    print(processed_text)

    # Clean up dummy file
    import os
    os.remove(dummy_file_path)
