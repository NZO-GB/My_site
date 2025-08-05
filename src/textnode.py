from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "just text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        text_true = self.text == other.text
        type_true = self.text_type == other.text_type
        url_true = self.url == other.url
        return text_true and type_true and url_true
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case text_node.text_type.TEXT:
            return LeafNode(None, text_node.text)
        case text_node.text_type.BOLD:
            return LeafNode("b", text_node.text)
        case text_node.text_type.ITALIC:
            return LeafNode("i", text_node.text)
        case text_node.text_type.CODE:
            return LeafNode("code", text_node.text)
        case text_node.text_type.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case text_node.text_type.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt":text_node.text})
        case _:
            raise Exception("No known type")
