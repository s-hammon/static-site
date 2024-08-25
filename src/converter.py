import re
from typing import List

from textnode import TextNode
from nodetypes import TextType


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = node.text.split(delimiter)
        if len(split_nodes) == 1:
            raise ValueError("Invalid Markdown syntax")
        if len(split_nodes) != 3:
            new_nodes.append(node)
            continue

        for i, split_node in enumerate(split_nodes):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node, node.text_type.value))
            else:
                new_nodes.append(TextNode(split_node, text_type))

    return new_nodes

def extract_markdown_images(text: str) -> List[tuple]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)

def extract_markdown_links(text: str) -> List[tuple]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)