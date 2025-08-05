import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node3 = TextNode("Test", TextType.LINK, None)
        node4 = TextNode("Test", TextType.LINK, None)
        self.assertEqual(node3, node4)

    def test_type_diff(self):
        node5 = TextNode("Test", TextType.BOLD, None)
        node6 = TextNode("Test", TextType.LINK, None)
        self.assertNotEqual(node5, node6)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_img(self):
        node = TextNode("alt text", TextType.IMAGE, "www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(),
                          '<img src="www.image.com" alt="alt text"></img>')
