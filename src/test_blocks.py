import unittest
from blocks import BlockType, block_to_block_type

class TestMdBlock(unittest.TestCase):
    def test_convert_to_code_type(self):
        block_code = "```\n#This is a python block\nprint(\"Hello World\")```\n"
        block_type = block_to_block_type(block_code)
        self.assertEqual(block_type, BlockType.CODE)

    def test_convert_to_quote_type(self):
        block_quote = ">Right now, if you're coming out of school—is the generalization of the age of people who happen to be\n>coming out of school, usually—it's a very valuable time where you\'re kind of in your prime in terms of\n>learning new stuff and adapting and having energy and inspiration and all this. Or at the last, you'll\n>probably match any later time in your life, whether those impulses decline or not—very good time right now. And sort of one of the worst things you can do is go work at some company that's kinda big and\n>bureaucratic and slow, at that age, because you're still learning and you wanna run the engine fast, you wanna learn things quickly because learning is like compound interest and the more you learn, the\n>more you'll learn from your later experience because you can handle it better or whatever.\n"
        block_type = block_to_block_type(block_quote)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_convert_to_unordered_list_type(self):
        block_unordered = "- This is a list item\n- This is a list item\n- This is a list item\n- This is a list item\n- This is a list item"
        block_type = block_to_block_type(block_unordered)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_convert_to_ordered_type(self):
        block_ordered = "1. one\n2. two\n3. three\n4. four\n5. five\n6. six"
        block_type = block_to_block_type(block_ordered)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)


