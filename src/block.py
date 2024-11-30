import re
from typing import List, Tuple

from src.converter import text_to_textnodes
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = [convert_block_to_html_node(block) for block in blocks]

    return ParentNode(nodes, "div")


def convert_block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)

    match block_type:
        case "heading":
            tag, value = header_markdown_to_html(block)
            return ParentNode(
                [text_node_to_html_node(node) for node in text_to_textnodes(value)], tag
            )
        case "code":
            content = block.replace("```", "")
            return ParentNode([LeafNode(content, "code")], "pre")
        case "quote":
            content = block.replace("> ", "")
            return ParentNode(
                [text_node_to_html_node(node) for node in text_to_textnodes(content)],
                "blockquote",
            )
        case "unordered_list":
            lines = [line[2:] for line in block.splitlines()]
            return ParentNode(
                [
                    ParentNode(
                        [
                            text_node_to_html_node(node)
                            for node in text_to_textnodes(line)
                        ],
                        "li",
                    )
                    for line in lines
                ],
                "ul",
            )
        case "ordered_list":
            lines = [re.sub(r"^\d+\.\s*", "", line) for line in block.splitlines()]
            return ParentNode(
                [
                    ParentNode(
                        [
                            text_node_to_html_node(node)
                            for node in text_to_textnodes(line)
                        ],
                        "li",
                    )
                    for line in lines
                ],
                "ol",
            )
        case "paragraph":
            return ParentNode(
                [text_node_to_html_node(node) for node in text_to_textnodes(block)], "p"
            )
        case _:
            return ParentNode(
                [text_node_to_html_node(node) for node in text_to_textnodes(block)], "p"
            )


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


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
    # Returns the tag and value of the header
    # If no match is found, it returns h1 and the original markdown
    match = re.match(r"^(#{1,6}) (.*)", markdown)

    if match:
        depth = len(match.group(1))
        if depth <= 6:
            return f"h{depth}", match.group(2)

    return "h1", markdown
