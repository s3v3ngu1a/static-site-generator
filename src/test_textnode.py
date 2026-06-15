import unittest
from textnode import TextNode
from textnode import TextType
from textnode import text_node_to_html_node
from textnode import split_nodes_delimiter
from textnode import extract_markdown_images
from textnode import split_nodes_link
from textnode import split_nodes_image
from textnode import text_to_textnodes

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
                )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT_PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT_PLAIN),
                TextNode("image", TextType.TEXT_IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT_PLAIN),
                TextNode(
                    "second image", TextType.TEXT_IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):

        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT_PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT_PLAIN),
                TextNode("to boot dev", TextType.TEXT_URL, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT_PLAIN),
                TextNode(
                    "to youtube", TextType.TEXT_URL, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
                )

    def test_text_to_text_nodes_sucess(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
			[
				TextNode("This is ", TextType.TEXT_PLAIN),
				TextNode("text", TextType.TEXT_BOLD),
				TextNode(" with an ", TextType.TEXT_PLAIN),
				TextNode("italic", TextType.TEXT_ITALIC),
				TextNode(" word and a ", TextType.TEXT_PLAIN),
				TextNode("code block", TextType.TEXT_CODE),
				TextNode(" and an ", TextType.TEXT_PLAIN),
				TextNode("obi wan image", TextType.TEXT_IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode(" and a ", TextType.TEXT_PLAIN),
				TextNode("link", TextType.TEXT_URL, "https://boot.dev"),
			],
                new_nodes
                )

if __name__ == "__main__":
    unittest.main()
