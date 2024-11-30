from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    BLOCKQUOTE = "blockquote"
    STRIKE = "strike"
    SPOILER = "spoiler"
