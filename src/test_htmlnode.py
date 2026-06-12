import unittest
from htmlnode import HTMLNode

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
        self.assertEqual(html_node.__repr__(), "HTMLNode(tag=div, children=None, props=None)")

if __name__ == "__main__":
    unittest.main()
