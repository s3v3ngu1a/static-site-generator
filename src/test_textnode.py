import unittest
from textnode import TextNode
from textnode import TextType
from textnode import text_node_to_html_node
from textnode import split_nodes_delimiter

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

    def test_node_text_creation(self):
        node = TextNode("This is a text node", TextType.TEXT_PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_code_creation(self):
        node = TextNode("This is a code node", TextType.TEXT_CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_text_url_creation(self):
        node = TextNode("Click me!", TextType.TEXT_URL, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")

    def test_text_image_creation(self):
        node = TextNode("", TextType.TEXT_IMAGE, "https://supersecurecdn.com/img/1", "monkey face")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold**", TextType.TEXT_PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.TEXT_BOLD)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT_BOLD)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is `code`", TextType.TEXT_PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.TEXT_CODE)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT_CODE)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is _italics_", TextType.TEXT_PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.TEXT_ITALIC)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "italics")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT_ITALIC)

if __name__ == "__main__":
    unittest.main()
