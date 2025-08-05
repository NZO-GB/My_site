import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_list = node.text.split(delimiter)
        in_block = False
        for textblock in split_list:
            if not in_block and textblock != "":
                new_nodes.append(TextNode(textblock, TextType.TEXT))
            if in_block:
                new_nodes.append(TextNode(textblock, text_type))
            in_block = not in_block
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    return split_splitter(old_nodes, "image")

def split_nodes_link(old_nodes):
    return split_splitter(old_nodes, "link")

def split_splitter(old_nodes, decider):
    new_nodes = []
    extractor_map = {
        "image": extract_markdown_images,
        "link": extract_markdown_links
    }
    format_map = {
        "image": lambda text, link: f"![{text}]({link})",
        "link": lambda text, link: f"[{text}]({link})"
    }
    type_map = {
        "image": TextType.IMAGE,
        "link": TextType.LINK
    }

    extractor = extractor_map[decider]
    formatter = format_map[decider]
    node_type = type_map[decider]

    for node in old_nodes:
        textlink_pairs = extractor(node.text)
        if len(textlink_pairs) == 0:
            new_nodes.append(node)
            continue

        for text, link in textlink_pairs:
            textlink_formatted = formatter(text, link)

            subnodes = node.text.split(textlink_formatted)
            if subnodes[0]:
                new_nodes.append(TextNode(subnodes[0], TextType.TEXT))

            new_nodes.append(TextNode(text, node_type, link))

            if len(subnodes) > 1:
                node.text = subnodes[1]
            else:
                continue

        if node.text != "":
            new_nodes.append(TextNode(node.text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    old_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    old_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
    old_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
    old_nodes = split_nodes_image(old_nodes)
    old_nodes = split_nodes_link(old_nodes)
    return old_nodes