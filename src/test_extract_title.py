import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title_get_the_title(self):
        content = """
        # This is sample title
        """
        title = extract_title(content)
        self.assertEqual(title, "This is sample title")

    def test_extract_title_raise_error(self):
        content = ""
        self.assertRaises(ValueError, extract_title, content)
