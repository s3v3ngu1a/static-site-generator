import re
from textnode import TextType
from textnode import TextNode
from textnode import markdown_to_blocks
from textnode import text_to_textnodes
from textnode import text_node_to_html_node
from blocks import BlockType
from blocks import block_to_block_type
from htmlnode import ParentNode

def _build_header(text):
    header_count = 0
    for i,c in enumerate(text):
        if c == "#":
            header_count += 1
        else:
            break
    header_raw = text.replace("#", "").strip()
    text_nodes = text_to_textnodes(header_raw)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    block_parent = ParentNode(tag=f"h{header_count}", children=html_nodes, props=None)
    return block_parent

def _build_quote(text):
    quote_raw = text.replace("> ", "").strip()
    text_nodes = text_to_textnodes(quote_raw)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    block_parent = ParentNode(tag="blockquote", children=html_nodes, props=None)
    return block_parent

def _build_list(text="", ordered=False):
    if text == "":
        return None
    list_lines = text.replace("- ","").split("\n")
    html_nodes = []
    for line in list_lines:
        text_nodes = text_to_textnodes(line)
        line_childs = []
        for text_node in text_nodes:
            inline_child = text_node_to_html_node(text_node)
            line_childs.append(inline_child)

        child_list_item = ParentNode(tag="li", children=line_childs, props=None)
        html_nodes.append(child_list_item)
    order_tag = "ul"
    if ordered:
        order_tag = "ol"
    block_parent = ParentNode(tag=order_tag, children=html_nodes, props=None)
    return block_parent

def _build_code(text):
    raw_code = text.replace("```", "")
    code_lines = raw_code.split("\n")
    # This removes the lines that contain a \n after removing the ```
    clean_lines = [line.strip() for line in code_lines if len(line) >= 1]
    code_formatted = "\n".join(clean_lines)

    text_nodes = [TextNode(text=code_line, text_type=TextType.TEXT_PLAIN) for code_line in clean_lines]
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    code_html = text_node_to_html_node(TextNode(text=rf"{code_formatted}", text_type=TextType.TEXT_PLAIN))
    block_code = ParentNode(tag="code", children=[code_html])
    block_parent = ParentNode(tag="pre", children=[block_code], props=None)
    return block_parent

def _build_paragraph(text):
    text_lines = text.split("\n")
    clean_lines = [line.strip() for line in text_lines]
    text_formatted = " ".join(clean_lines)
    text_nodes = text_to_textnodes(text_formatted)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    block_parent = ParentNode(tag="p", children=html_nodes, props=None)
    return block_parent

def text_to_children(text):
    markdown_block_type = block_to_block_type(text)
    if markdown_block_type == BlockType.HEADING:
        return _build_header(text)
    elif markdown_block_type == BlockType.CODE:
       return _build_code(text) 
    elif markdown_block_type == BlockType.QUOTE:
        return _build_quote(text)
    elif markdown_block_type == BlockType.UNORDERED_LIST:
        return _build_list(text=text, ordered=False)
    elif markdown_block_type == BlockType.ORDERED_LIST:
        return _build_list(text=text, ordered=True)
    elif markdown_block_type == BlockType.PARAGRAPH:
        return _build_paragraph(text)
    else:
        raise ValueError("unknown markdown_block_type")

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)

    children_blocks = []
    for markdown_block in markdown_blocks:
        html_node = text_to_children(markdown_block)
        children_blocks.append(html_node)
    block_parent = ParentNode(tag="div", children=children_blocks, props=None)
    return block_parent

def main():
    pass

if __name__ == '__main__':
    main()
