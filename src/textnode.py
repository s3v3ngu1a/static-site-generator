from enum import Enum

class TextType(Enum):
    TEXT_PLAIN = "TEXT_PLAIN"
    TEXT_BOLD = "TEXT_BOLD"
    TEXT_ITALIC = "TEXT_ITALIC"
    TEXT_CODE = "TEXT_CODE"
    TEXT_URL = "TEXT_URL"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, another):
        eq_text = self.text == another.text
        eq_type = self.text_type == another.text_type
        eq_url = self.url == another.url
        return eq_text and eq_type and eq_url
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
