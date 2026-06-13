import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_no_children_raise_value_error(self):
        parent_node = ParentNode("div", {"class": "heading-1"})
        self.assertRaises(ValueError, msg="children must be set")

    def test_value_not_set_raise_value_error(self):
        child_node = LeafNode("span", "child", {"width": "50%"})
        parent_node = ParentNode([child_node], {"class": "heading-1"})
        self.assertRaises(ValueError, msg="value must be set")

    def test_parent_props_correct_render(self):
        child_node = LeafNode("span", "child", {"width": "50%"})
        parent_node = ParentNode("div", [child_node], {"class": "heading-1"})
        self.assertEqual(
                parent_node.to_html(),
                "<div class=\"heading-1\"><span width=\"50%\">child</span></div>"
                )

if __name__ == "__main__":
    unittest.main()
