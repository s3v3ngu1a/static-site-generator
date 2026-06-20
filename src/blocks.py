from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

def block_to_block_type(md_block):
    lines = md_block.split("\n")
    is_heading = md_block.startswith("#") or  \
            md_block.startswith("##") or \
            md_block.startswith("###") or \
            md_block.startswith("####") or \
            md_block.startswith("#####") or \
            md_block.startswith("######")

    is_code = md_block.startswith("```\n") and (md_block.endswith("```") or md_block.endswith("```\n"))
    is_quote = md_block.strip().startswith("> ")
    is_unordered = md_block.startswith("- ")

    if is_heading:
        for line in lines:
            if not is_heading:
                return BlockType.PARAGRAPH
        return BlockType.HEADING
    elif is_code:
        return BlockType.CODE
    elif is_quote:
        for line in lines:
            if not is_quote and len(line) > 1:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif is_unordered:
        for line in lines:
            if not is_unordered and len(line) > 1:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif md_block[0].isdigit() and md_block[1:3] == ". ":
        for i, line in enumerate(lines, start=1):
            if not line.startswith(f"{i}. ") and len(line) > 1:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

