import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_create_empty_node(self):
        html_node = HTMLNode()
        self.assertIsInstance(html_node, HTMLNode)

    def test_empty_props(self):
        html_child = HTMLNode(tag="p", props={"style": "{font-size: 12px}"})
        html_node = HTMLNode(tag="div", children=[html_child], props=None)
        self.assertIsNone(html_node.props)
        
    def test_representation(self):
        html_node = HTMLNode(tag="div", children=None, props=None)
        self.assertEqual(html_node.__repr__(), "HTMLNode(tag=div, value=None, children=None, props=None)")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_url(self):
        node = LeafNode("a", "Click me, i'm secure!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me, i\'m secure!</a>')

if __name__ == "__main__":
    unittest.main()
