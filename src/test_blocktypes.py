import unittest

from markdown_blocks import block_to_blocktype, BlockType

class TestBlockTypes(unittest.TestCase):

    def test_block2block_basic(self):
        block = """
some cheese. 
and more cheese.
"""
        testblocktype = block_to_blocktype(block)
        self.assertEqual(testblocktype, BlockType.PARAGRAPH)

    def test_block2block_headings(self):
        block = """#### this is a heading.
It has parts.
"""
        testblocktype = block_to_blocktype(block)
        self.assertEqual(testblocktype, BlockType.HEADING)

    def test_block2block_code(self):
        block = """```code() function()
```
"""
        testblocktype = block_to_blocktype(block)
        self.assertEqual(testblocktype, BlockType.CODE)

    def test_block2block_quote(self):
        block = """>thing
> another thing
> cool
>the thing"""
        testblocktype = block_to_blocktype(block)
        self.assertEqual(testblocktype, BlockType.QUOTE)

    def test_block2block_unordered(self):
        block = """- thing
- cosa
- queso"""
        testblocktype = block_to_blocktype(block)
        self.assertEqual(testblocktype, BlockType.UNORDERED_LIST)

    def test_block2block_ordered(self):
        block= """1. wow
2. wew
3. waw"""
        testblocktype = block_to_blocktype(block)
        self.assertEqual(testblocktype, BlockType.ORDERED_LIST)

    def test_block2block_notquote(self):
        block = """>cosa
>cosa
laca"""
        testblocktype = block_to_blocktype(block)
        self.assertEqual(testblocktype, BlockType.PARAGRAPH)

    def test_block2block_notorder(self):
        block = """1. a
2. b
4. c"""
        testblocktype = block_to_blocktype(block)
        self.assertEqual(testblocktype, BlockType.PARAGRAPH)