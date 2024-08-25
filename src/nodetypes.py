from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKE = "link"
    IMAGE = "image"
    BLOCKQUOTE = "blockquote"