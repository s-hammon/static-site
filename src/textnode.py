from typing import Any, Optional

from src.htmlnode import LeafNode
from src.nodetypes import TextType


class TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None):
        self.text: str = text

        try:
            self.text_type: TextType = TextType(text_type)
        except ValueError:
            raise ValueError("Unsupported text type")

        self.url: str = url or ""

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TextNode):
            return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
            )
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    value = text_node.text
    text_type = text_node.text_type
    url = text_node.url
    match text_type.value:
        case "text":
            return LeafNode(value, None, None)
        case "bold":
            return LeafNode(value, "b", None)
        case "italic":
            return LeafNode(value, "i", None)
        case "code":
            return LeafNode(value, "code", None)
        case "link":
            return LeafNode(value, "a", {"href": url})
        case "image":
            return LeafNode("", "img", {"src": url, "alt": value})
        case "strike":
            return LeafNode(value, "s", None)
        case _:
            raise ValueError("Unsupported text type")
