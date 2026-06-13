from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT_PLAIN = "TEXT_PLAIN"
    TEXT_BOLD = "TEXT_BOLD"
    TEXT_ITALIC = "TEXT_ITALIC"
    TEXT_CODE = "TEXT_CODE"
    TEXT_URL = "TEXT_URL"
    TEXT_IMAGE = "TEXT_IMAGE"

class TextNode:
    def __init__(self, text, text_type, url=None, alt=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url
        self.alt = alt

    def __eq__(self, another):
        eq_text = self.text == another.text
        eq_type = self.text_type == another.text_type
        eq_url = self.url == another.url
        return eq_text and eq_type and eq_url
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT_PLAIN:
        return LeafNode(tag=None, value=text_node.text, props=None)
    elif text_node.text_type == TextType.TEXT_BOLD:
        return LeafNode(tag="b", value=text_node.text, props=None)
    elif text_node.text_type == TextType.TEXT_ITALIC:
        return LeafNode(tag="i", value=text_node.text, props=None)
    elif text_node.text_type == TextType.TEXT_CODE:
        return LeafNode(tag="code", value=text_node.text, props=None)
    elif text_node.text_type == TextType.TEXT_URL:
        return LeafNode(tag="a", value=text_node.text, props={"href": f"{text_node.url}"})
    elif text_node.text_type == TextType.TEXT_IMAGE:
        return LeafNode(tag="img", value="", props={"src": f"{text_node.url}", "alt": f"{text_node.alt}"})
    else:
        # This is weird why would be an objecti with a text type not defined at enum?
        raise ValueError("Unknown text_type")
