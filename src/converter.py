import re
from typing import Callable, List

from textnode import TextNode
from nodetypes import TextType


def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "~~", TextType.STRIKE)
    nodes = split_nodes_embed(nodes, extract_markdown_images, "![{}]({})", TextType.IMAGE)
    nodes = split_nodes_embed(nodes, extract_markdown_links, "[{}]({})", TextType.LINK)
    return nodes 

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Invalid Markdown syntax")

        delimited = extract_delimited(node.text, delimiter)
        if len(delimited) == 0:
            new_nodes.append(node)
            continue 
            
        text = node.text
        for delim in delimited:
            delim_md = f"{delimiter}{delim}{delimiter}"
            predicate = text.split(delim_md)[0]
            if predicate:
                new_nodes.append(TextNode(predicate, node.text_type.value))
                text = text.replace(predicate, "")
            
            new_nodes.append(TextNode(delim, text_type))
            text = text.replace(delim_md, "", 1)

        if text:
            new_nodes.append(TextNode(text, node.text_type.value))

    return new_nodes

def split_nodes_embed(old_nodes: List[TextNode], extract_func: Callable[[str], List[tuple]], md_format: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        embeds = extract_func(node.text)
        if len(embeds) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for embed in embeds:
            embed_md = md_format.format(embed[0], embed[1])
            predicate = text.split(embed_md)[0]
            if predicate:
                new_nodes.append(TextNode(predicate, node.text_type.value))
                text = text.replace(predicate, "")
            
            new_nodes.append(TextNode(embed[0], text_type, embed[1]))
            text = text.replace(embed_md, "")

    return new_nodes

def extract_markdown_images(text: str) -> List[tuple]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)

def extract_markdown_links(text: str) -> List[tuple]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def extract_delimited(text: str, delimiter: str) -> List[str]:
    match delimiter:
        case "**":
            return re.findall(r"\*\*(.*?)\*\*", text)
        case "*":
            return re.findall(r"(?<!\*)\*([^*]+)\*(?!\*)", text)
        case "`":
            return re.findall(r"`([^`]+)`", text)
        case "~~":
            return re.findall(r"~~(.*?)~~", text)
        case _:
            raise ValueError("Invalid delimiter")