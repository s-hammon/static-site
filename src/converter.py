import re
from typing import List

from textnode import TextNode
from nodetypes import TextType


def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes 

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Invalid Markdown syntax")

        # split_nodes = node.text.split(delimiter)
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

        # if len(split_nodes) != 3:
        #     new_nodes.append(node)
        #     continue

        # for i, split_node in enumerate(split_nodes):
        #     if split_node == "":
        #         continue
        #     if i % 2 == 0:
        #         new_nodes.append(TextNode(split_node, node.text_type.value))
        #     else:
        #         new_nodes.append(TextNode(split_node, text_type))

    return new_nodes

def split_nodes_image(old_nodes: List[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        for image in images:
            image_md = f"![{image[0]}]({image[1]})"
            predicate = text.split(image_md)[0]
            if predicate:
                new_nodes.append(TextNode(predicate, node.text_type.value))
                text = text.replace(predicate, "")
            
            new_nodes.append(TextNode(image[0], "image", image[1]))
            text = text.replace(image_md, "")

    return new_nodes

def split_nodes_link(old_nodes: List[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        for link in links:
            link_md = f"[{link[0]}]({link[1]})"
            predicate = text.split(link_md)[0]
            if predicate:
                new_nodes.append(TextNode(predicate, node.text_type.value))
                text = text.replace(predicate, "")
            
            new_nodes.append(TextNode(link[0], "link", link[1]))
            text = text.replace(link_md, "")

    return new_nodes

def extract_markdown_images(text: str) -> List[tuple]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)

def extract_markdown_links(text: str) -> List[tuple]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def extract_bold(text: str) -> List[str]:
    return re.findall(r"\*\*(.*?)\*\*", text)

def extract_italic(text: str) -> List[str]:
    # must be exactly one * on each side
    return re.findall(r"(?<!\*)\*([^*]+)\*(?!\*)", text)

def extract_code(text: str) -> List[str]:
    return re.findall(r"`([^`]+)`", text)

def extract_delimited(text: str, delimiter: str) -> List[str]:
    match delimiter:
        case "**":
            return re.findall(r"\*\*(.*?)\*\*", text)
        case "*":
            return re.findall(r"(?<!\*)\*([^*]+)\*(?!\*)", text)
        case "`":
            return re.findall(r"`([^`]+)`", text)
        case _:
            raise ValueError("Invalid delimiter")