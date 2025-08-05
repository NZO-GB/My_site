import unittest

from inline_markdown import split_nodes_image, split_nodes_link
from textnode import TextType, TextNode

class TestSplitImage(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "No image :(",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("No image :(", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_images_adv(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        noted = TextNode(
            "[linktext](www.link1.com)[linktext](www.link1.com)[linker](www.linker.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([noted])
        self.assertListEqual(
             [
                TextNode("linktext", TextType.LINK, "www.link1.com"),
                TextNode("linktext", TextType.LINK, "www.link1.com"),
                TextNode("linker", TextType.LINK, "www.linker.com")
             ],
             new_nodes
        )