import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT_BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT_ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_missing_url(self):
        node = TextNode("This is a url node", TextType.TEXT_URL,
        "https://awesomesite.com")
        self.assertTrue(node.url is not None)

    def test_not_url_not_url_type(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        self.assertTrue((node.url is None) and (node.text_type != TextType.TEXT_URL))

if __name__ == "__main__":
    unittest.main()
