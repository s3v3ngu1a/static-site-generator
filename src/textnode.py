import re
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

def extract_markdown_links(text):
    reg = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(reg, text)
    return matches

def extract_markdown_images(text):
    reg = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(reg, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    parsed_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT_PLAIN:
            parsed_nodes.append(node)
            continue
        full_text = None
        images_extraction_results = extract_markdown_images(node.text)
        if not images_extraction_results:
            parsed_nodes.append(node)
        else:
            full_text = node.text
            for alt_text, url in images_extraction_results:
                img_split = full_text.split(f"![{alt_text}]({url})", 1)
                trailing_text = img_split[0]
                if trailing_text:
                    node_text = TextNode(text=trailing_text, text_type=TextType.TEXT_PLAIN)
                    parsed_nodes.append(node_text)
                node_img = TextNode(text=alt_text, url=url, text_type=TextType.TEXT_IMAGE)
                full_text = img_split[1]
                parsed_nodes.append(node_img)
        if full_text:
            node_text = TextNode(text=full_text, text_type=TextType.TEXT_PLAIN)
            parsed_nodes.append(node_text)
    return parsed_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    parsed_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT_PLAIN:
            parsed_nodes.append(node)
            continue
        links_extraction_results = extract_markdown_links(node.text)
        full_text = None
        if not links_extraction_results:
            parsed_nodes.append(node)
        else:
            full_text = node.text
            for link_text, url in links_extraction_results:
                link_split = full_text.split(f"[{link_text}]({url})", 1)
                trailing_text = link_split[0]
                if trailing_text:
                    node_text = TextNode(text=trailing_text, text_type=TextType.TEXT_PLAIN)
                    parsed_nodes.append(node_text)
                node_link = TextNode(text=link_text, url=url, text_type=TextType.TEXT_URL)
                full_text = link_split[1]
                parsed_nodes.append(node_link)
        if full_text:
            node_text = TextNode(text=full_text, text_type=TextType.TEXT_PLAIN)
            parsed_nodes.append(node_text)
    return parsed_nodes

def text_to_textnodes(text):
    result_nodes = []
    root = [TextNode(text=text, text_type=TextType.TEXT_PLAIN)]
    bold_extraction_result = split_nodes_delimiter(root, '**', TextType.TEXT_BOLD)
    italic_extraction_result = split_nodes_delimiter(bold_extraction_result, '_', TextType.TEXT_ITALIC)
    code_extraction_result = split_nodes_delimiter(italic_extraction_result, '`', TextType.TEXT_CODE)
    link_extraction_result = split_nodes_link(code_extraction_result)
    image_extraction_result = split_nodes_image(link_extraction_result)
    result_nodes.extend(image_extraction_result)
    return result_nodes

def main():
    print("Hello World")

if __name__ == '__main__':
    main()
