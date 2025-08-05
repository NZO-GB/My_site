import unittest
from generating import extract_title

class TestTitle(unittest.TestCase):

    def test_basic(self):
        md = """
###### Wrong

#### Another wrong

# YES

not a # heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
"""
        title = extract_title(md)
        self.assertEqual("YES", title)