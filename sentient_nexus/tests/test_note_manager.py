import os
import shutil
import unittest
import tempfile
import unittest.mock # Import the mock library

# Assuming tests are run from the project root (sentient_nexus directory)
# or that the sentient_nexus package is in PYTHONPATH.
# This allows `from sentient_nexus.app.core.note_manager import add_note` to work.
# If sentient_nexus/ is the current working directory when running tests,
# then Python might not see 'sentient_nexus' as a package directly for the import string in patch.
# A common way to run tests is `python -m unittest discover -s tests` from project root,
# or `python -m unittest tests.test_note_manager`
# This makes `sentient_nexus` available as a top-level package if an __init__.py is in the root,
# or if the directory containing `sentient_nexus` is in PYTHONPATH.

# For the patch string to work reliably ("sentient_nexus.app.core.note_manager.DATA_DIR"),
# the tests should be run in a way that `sentient_nexus` is recognized as a package.
# Let's add an __init__.py to the project root to help with this if tests are run from parent of project_root.
# However, the plan was to put tests in `sentient_nexus/tests/`.

# Let's assume sentient_nexus is the project root and also the top-level package name.
# We need to ensure imports work correctly.
# `from app.core.note_manager import add_note` might be more robust if tests are run
# from `sentient_nexus` directory and `PYTHONPATH` includes `sentient_nexus`.

# Let's adjust imports for clarity assuming `sentient_nexus` is the project root
# and tests are run from there.
# `sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))`
# would add `sentient_nexus` to the path if tests are in `sentient_nexus/tests/`.

# Try direct import from app - this requires `sentient_nexus` to be in PYTHONPATH
# or for tests to be run as module `python -m unittest sentient_nexus.tests.test_note_manager`
from sentient_nexus.app.core.note_manager import add_note


# The target for patching should be where the object is looked up.
# `add_note` in `sentient_nexus.app.core.note_manager` uses `DATA_DIR` from its own module.
MODULE_UNDER_TEST = "sentient_nexus.app.core.note_manager"
DATA_DIR_PATCH_TARGET = f"{MODULE_UNDER_TEST}.DATA_DIR"

class TestNoteManager(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = tempfile.mkdtemp()
        # Patch DATA_DIR within the note_manager module
        self.patcher = unittest.mock.patch(DATA_DIR_PATCH_TARGET, self.test_data_dir)
        self.mocked_data_dir_value = self.patcher.start()
        # Ensure the original DATA_DIR is restored even if add_note is re-imported or module reloaded by test runner
        self.addCleanup(self.patcher.stop)


    def tearDown(self):
        # self.patcher.stop() # Handled by addCleanup
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_data_dir)

    def test_add_note_creates_file_with_content(self):
        """Test that add_note creates a file with the specified content."""
        note_content = "This is a test note."
        filename = "test_note_content.txt"

        expected_filepath = os.path.join(self.test_data_dir, filename)

        returned_filepath = add_note(note_content, filename=filename)

        self.assertEqual(returned_filepath, expected_filepath)
        self.assertTrue(os.path.exists(expected_filepath))

        with open(expected_filepath, "r", encoding="utf-8") as f:
            content_in_file = f.read()
        self.assertEqual(content_in_file, note_content)

    def test_add_note_generates_filename(self):
        """Test that add_note generates a filename if none is provided."""
        note_content = "Another test note for generated filename."

        returned_filepath = add_note(note_content)

        self.assertTrue(os.path.exists(returned_filepath))
        self.assertTrue(os.path.basename(returned_filepath).startswith("note_"))
        self.assertTrue(os.path.basename(returned_filepath).endswith(".txt"))

        with open(returned_filepath, "r", encoding="utf-8") as f:
            content_in_file = f.read()
        self.assertEqual(content_in_file, note_content)
        # Check if it's in our mocked test_data_dir
        self.assertEqual(os.path.dirname(returned_filepath), self.mocked_data_dir_value) # Use the patched value for comparison

    def test_add_note_creates_data_dir_if_not_exists(self):
        """
        Test that add_note creates the data directory if it doesn't exist.
        """
        # Remove the test_data_dir *after* patching it and *before* calling add_note
        # to ensure add_note recreates it.
        # The self.mocked_data_dir_value holds the path to the temp dir.
        if os.path.exists(self.mocked_data_dir_value):
            shutil.rmtree(self.mocked_data_dir_value)

        # Sanity check it's gone
        self.assertFalse(os.path.exists(self.mocked_data_dir_value))

        note_content = "Testing directory creation."
        filename = "dir_creation_test.txt"
        # The expected path is now based on self.mocked_data_dir_value, which is what DATA_DIR is patched to
        expected_filepath = os.path.join(self.mocked_data_dir_value, filename)

        returned_filepath = add_note(note_content, filename=filename)

        self.assertEqual(returned_filepath, expected_filepath)
        self.assertTrue(os.path.exists(expected_filepath)) # This implies dir was created by add_note

if __name__ == "__main__":
    # This allows running the test file directly like:
    # python -m unittest sentient_nexus.tests.test_note_manager
    # ( vanuit de parent directory van sentient_nexus )
    # OR from the project root (sentient_nexus directory):
    # python -m unittest tests.test_note_manager
    # The latter requires `tests` to be a package or discoverable.
    # `python -m unittest discover -s tests` (from project root) is standard.
    unittest.main()
