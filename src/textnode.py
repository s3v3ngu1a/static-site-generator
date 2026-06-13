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
        eq_alt = self.alt == another.alt
        return eq_text and eq_type and eq_url and eq_alt
    def __repr__(self):
        return f"TextNode(text=\"{self.text}\", text_type={self.text_type.value}, url={self.url}, alt={self.alt})"

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

def split_nodes_delimiter(old_nodes: list[TextNode],
                          delimiter: str,
                          text_type: TextType) -> list[TextNode]:
    parsed_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT_PLAIN:
            content = node.text
            splitter = content.split(delimiter)
            if len(splitter) % 2 == 0:
                raise ValueError(f"Unmatched delimiter: {content}")

            for idx, split in enumerate(splitter):
                if len(split) == 0:
                    continue
                if idx % 2 != 0:
                    new_node = TextNode(text=split, text_type=text_type)
                else:
                    new_node = TextNode(text=split, text_type=TextType.TEXT_PLAIN)
                parsed_nodes.append(new_node)
        else:
            parsed_nodes.append(node)
    return parsed_nodes

def main():
    node = TextNode("This is **text** with a **bold block** **word**", TextType.TEXT_PLAIN)
    new_nodes = split_nodes_delimiter([node], "**", TextType.TEXT_BOLD)
    print(new_nodes)

if __name__ == '__main__':
    main()
