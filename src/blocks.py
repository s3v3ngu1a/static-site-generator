from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

# This will not work because should be done on a list maybe
def block_to_block_type(md_block):
    if md_block.startswith("#"):
        for line in md_block.split('\n'):
            if not line.startswith('#'):
                return BlockType.PARAGRAPH
        return BlockType.HEADING
    elif md_block.startswith("```\n") and md_block.endswith("```\n"):
        return BlockType.CODE
    elif md_block.strip().startswith(">"):
        for line in md_block.split("\n"):
            if not line.startswith(">") and len(line) > 1:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif md_block.startswith("- "):
        for line in md_block.split("\n"):
            if not line.startswith("- ") and len(line) > 1:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif md_block[0].isdigit() and md_block[1:3] == ". ":
        for i, line in enumerate(md_block.split("\n"), start=1):
            if not line.startswith(f"{i}. ") and len(line) > 1:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

