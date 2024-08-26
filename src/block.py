import re
from typing import List, Tuple

from converter import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case "heading":
                tag, value = header_markdown_to_html(block)
                children = []
                for node in text_to_textnodes(value):
                    children.append(text_node_to_html_node(node))
                
                nodes.append(ParentNode(children, tag))

            case "code":
                child = LeafNode(block.replace("```", ""), "code")
                nodes.append(ParentNode([child], "pre"))

            case "quote":
                children = []
                for node in text_to_textnodes(block.replace("> ", "")):
                    children.append(text_node_to_html_node(node))
                nodes.append(ParentNode(children, "blockquote"))

            case "unordered_list":
                lines = [ line[2:] for line in block.splitlines()]
                children = []
                for line in lines:
                    grandchildren = []
                    for node in text_to_textnodes(line):
                        grandchildren.append(text_node_to_html_node(node))
                    children.append(ParentNode(grandchildren, "li"))

                nodes.append(ParentNode(children, "ul"))

            case "ordered_list":
                lines = [ re.sub(r"^\d+\.\s*", "", line) for line in block.splitlines() ]
                children = []
                for line in lines:
                    grandchildren = []
                    for node in text_to_textnodes(line):
                        grandchildren.append(text_node_to_html_node(node))
                    children.append(ParentNode(grandchildren, "li"))
        
                nodes.append(ParentNode(children, "ol"))

            case "paragraph":
                children = []
                for node in text_to_textnodes(block):
                    children.append(text_node_to_html_node(node))

                nodes.append(ParentNode(children, "p")) 

    return ParentNode(nodes, "div") 

def markdown_to_blocks(markdown: str) -> List[str]:
    blocks =  markdown.split("\n\n") 
    return [ block.strip() for block in blocks if block.strip()]

def block_to_block_type(block: str) -> str:
    if re.match(r"^(#{1,6}) (.*)", block):
        return "heading"
    if re.match(r"^```[\s\S]*?```", block):
        return "code"
    if re.match(r"^(> .*\n?)+$", block):
        return "quote"
    if re.match(r"^([*|-] .*\n?)+$", block):
        return "unordered_list"
    if check_ordered_list(block.splitlines()):
        return "ordered_list"
    return "paragraph"

def check_ordered_list(lines: List[str]) -> bool:
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            return False
    return True

def header_markdown_to_html(markdown: str) -> Tuple[str, str]:
    match = re.match(r"^(#{1,6}) (.*)", markdown)

    depth = len(match.group(1))
    if match and depth <= 6:
        return f"h{depth}", match.group(2)

    return None
