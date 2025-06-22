import unittest
import os
from chat_processor import parse_whatsapp_chat, preprocess_data

class TestChatProcessor(unittest.TestCase):

    def setUp(self):
        self.test_chat_content_standard = """\
[01/01/2023, 10:00:00] Alice: Hello Bob! How are you?
[01/01/2023, 10:00:05] Bob: Hi Alice, I'm good.
This is a multi-line message.
[01/01/2023, 10:00:10] Alice: Great to hear.
System message: User joined the group.
[02/02/2024, 11:05:30 AM] Charles: Test with AM/PM format.
03/03/2024, 12:30 - Diana: Another format test.
"""
        self.test_file_path = "test_chat_temp.txt"
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            f.write(self.test_chat_content_standard)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_parse_whatsapp_chat_standard(self):
        messages = parse_whatsapp_chat(self.test_file_path)

        expected_messages = [
            "Hello Bob! How are you?", # Alice
            "Hi Alice, I'm good. This is a multi-line message.", # Bob
            "Great to hear. System message: User joined the group.", # Alice, with system message appended
            "Test with AM/PM format.", # Charles
            "Another format test." # Diana
        ]

        self.assertEqual(len(messages), len(expected_messages),
                         f"Number of parsed messages did not match expected. Got: {len(messages)}, Expected: {len(expected_messages)}")

        for i, expected_msg in enumerate(expected_messages):
            self.assertEqual(messages[i], expected_msg,
                             f"Message at index {i} did not match. Got: '{messages[i]}', Expected: '{expected_msg}'")

    def test_parse_whatsapp_chat_empty_file(self):
        empty_file = "empty_test_chat.txt"
        with open(empty_file, "w", encoding="utf-8") as f:
            pass
        messages = parse_whatsapp_chat(empty_file)
        self.assertEqual(len(messages), 0)
        os.remove(empty_file)

    def test_parse_whatsapp_chat_only_system_messages(self):
        content = "[01/01/2023, 10:00:00] Messages and calls are end-to-end encrypted.\n" \
                  "You created this group."
        sys_file = "sys_test_chat.txt"
        with open(sys_file, "w", encoding="utf-8") as f:
            f.write(content)
        messages = parse_whatsapp_chat(sys_file)
        self.assertEqual(len(messages), 0) # Expecting system messages to be ignored if no sender.
        os.remove(sys_file)

    def test_preprocess_data(self):
        test_messages = ["Hello", "How are you?", "I am fine."]
        processed_text = preprocess_data(test_messages)
        self.assertEqual(processed_text, "Hello\nHow are you?\nI am fine.")

    def test_preprocess_data_empty(self):
        test_messages = []
        processed_text = preprocess_data(test_messages)
        self.assertEqual(processed_text, "")

if __name__ == '__main__':
    unittest.main()
