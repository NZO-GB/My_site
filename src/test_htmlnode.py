import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("tag", "value", "children", "props")
        base_string = str(node)
        test_string = f"self.tag = 'tag' self.value = 'value' self.children = 'children' self.props = 'props'"
        self.assertEqual(base_string, test_string)

    def test_props(self):
        props_dict = {'a': 1, 'b': 2}
        node = HTMLNode("tag", "value", "children", props_dict)
        base_string = node.props_to_html()
        test_string = 'a="1" b="2"'
        self.assertEqual(base_string, test_string)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_url(self):
        leaf_url = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        self.assertEqual(leaf_url, '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )