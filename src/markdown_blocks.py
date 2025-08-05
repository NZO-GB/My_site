import re

from enum import Enum
from textnode import TextNode, TextType
from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):

    PARAGRAPH = "normal paragraph"
    HEADING = "a heading"
    CODE = "some code"
    QUOTE = "a quote"
    UNORDERED_LIST = "a list with no order"
    ORDERED_LIST = "a list with order"

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    final_list = []
    for block in block_list:
        block = block.strip()
        if block != "":
            final_list.append(block)
    return final_list

def block_to_blocktype(block):
    if re.search(r"^#{1,6} .*", block):
        return BlockType.HEADING
    
    if re.search(r"(^```)", block) and re.search(r"(```$)", block):
        return BlockType.CODE
    
    if re.search(r"^>", block):
        for line in block.split("\n"):
            if not re.search(r"^>", line):
                break
        else: return BlockType.QUOTE
        
    
    if re.search(r"^- ", block):
        for line in block.split("\n"):
            if not re.search(r"^- ", line):
                break
        else: return BlockType.UNORDERED_LIST
    
    if re.search(r"^1. ", block):
        for i, line in enumerate(block.split("\n"), 1):
            if not re.search(f"^{i}. ", line):
                break
        else: return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def code_block_parenter(block):
    block = block.strip("```").lstrip("\n")
    child = TextNode(block, TextType.TEXT)
    html_child = text_node_to_html_node(child)
    parent_code = ParentNode("code", [html_child])
    grandparent_pre = ParentNode("pre", [parent_code])
    return grandparent_pre

def paragraph_block_parenter(block, tag):
    childs = text_to_textnodes(block)
    childs = map(text_node_to_html_node, childs)
    return ParentNode(tag, childs)

def quote_block_parenter(block):
    block = block.split("\n")
    new_block = []
    for line in block:
        new_block.append(line.lstrip("> "))
    new_block = " ".join(new_block)
    childs = text_to_textnodes(new_block)
    childs = map(text_node_to_html_node, childs)
    return ParentNode("blockquote", childs)

def list_block_parenter(block, list_tag, stripper):
    childs = []
    listed = block.split("\n")
    for line in listed:
        line = line[stripper:]
        childs_childs = text_to_textnodes(line)
        childs_childs = map(text_node_to_html_node, childs_childs)
        childs.append(ParentNode("li", childs_childs))
    return ParentNode(list_tag, childs)

def head_block_parenter(block):
    hashes = re.findall(r"^#{1,6}", block)
    num_hashes = len(hashes[0])
    block = block[num_hashes+1:]
    tag = "h" + str(num_hashes)
    childs = text_to_textnodes(block)
    childs = map(text_node_to_html_node, childs)
    return ParentNode(tag, childs)

def paragraph_block_parenter(block):
    block = block.split("\n")
    block = " ".join(block)
    childs = text_to_textnodes(block)
    childs = map(text_node_to_html_node, childs)
    return ParentNode("p", childs)


def blocktype_helper(block):
    block_type = block_to_blocktype(block)
    match block_type:
        case BlockType.QUOTE:
            return quote_block_parenter(block)
        case BlockType.UNORDERED_LIST:
            return list_block_parenter(block, "ul", 2)
        case BlockType.ORDERED_LIST:
            return list_block_parenter(block, "ol", 3)
        case BlockType.CODE:
            return code_block_parenter(block)
        case BlockType.HEADING:
            return head_block_parenter(block)
        case BlockType.PARAGRAPH:
            return paragraph_block_parenter(block)

def markdown_to_html_node(markdown):
    blocked = markdown_to_blocks(markdown)
    block_list = []
    for block in blocked:
        block_list.append(blocktype_helper(block))
    return ParentNode("div", block_list)