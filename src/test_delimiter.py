import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestDelimiter(unittest.TestCase):
    def test_basic(self):
        old_nodes = [TextNode("this is *a* test", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        test = [
    TextNode("this is ", TextType.TEXT),
    TextNode("a", TextType.BOLD),
    TextNode(" test", TextType.TEXT),
]
        self.assertEqual(new_nodes, test)

    def test_confusing(self):
        old_nodes = [
            TextNode("this is *a* test", TextType.TEXT),
            TextNode("this is already bold", TextType.BOLD),
            TextNode("*yeah* this *yeah* that", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        test = [
            TextNode("this is ", TextType.TEXT),
            TextNode("a", TextType.BOLD),
            TextNode(" test", TextType.TEXT),
            TextNode("this is already bold", TextType.BOLD),
            TextNode("yeah", TextType.BOLD),
            TextNode(" this ", TextType.TEXT),
            TextNode("yeah", TextType.BOLD),
            TextNode(" that", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, test)