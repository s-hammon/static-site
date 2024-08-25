import unittest

from converter import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
) 
from textnode import TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        cases = [
            {
                "name": "test text node with bold word",
                "params": {
                    "old_nodes": [TextNode("This is text with a **bold** word", "text")],
                    "delimiter": "**",
                    "text_type": "bold",
                },
                "want": [
                    TextNode("This is text with a ", "text"),
                    TextNode("bold", "bold"),
                    TextNode(" word", "text")
                ]
            },
            {
                "name": "test bold node",
                "params": {
                    "old_nodes": [TextNode("**bold only**", "bold")],
                    "delimiter": "**",
                    "text_type": "bold",
                },
                "want": [
                    TextNode("**bold only**", "bold")
                ]
            },
            {
                "name": "test two text nodes with italicized and bold word, work only italicized",
                "params": {
                    "old_nodes": [
                        TextNode("This is text with a **bold** word", "text"),
                        TextNode("This is text with an *italicized* word", "text"),
                    ],
                    "delimiter": "*",
                    "text_type": "italic",
                },
                "want": [
                    TextNode("This is text with a **bold** word", "text"),
                    TextNode("This is text with an ", "text"),
                    TextNode("italicized", "italic"),
                    TextNode(" word", "text")
                ]
            },
        ]

        for case in cases:
            print(f"Test case: {case['name']}")
            got = split_nodes_delimiter(**case["params"])
            for g, w in zip(got, case["want"]):
                self.assertEqual(g, w)

    def test_split_nodes_delimiter_raise_error(self):
        print("Test case: test invalid markdown syntax (bold)")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode("This is text with a bold word", "text")], "**", "bold")


class TestExtractMarkdownImagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images_and_links(self):
        cases = [
            {
                "name": "test extract markdown images",
                "func": extract_markdown_images,
                "params": "![alt text](https://www.boot.dev)",
                "want": [("alt text", "https://www.boot.dev")]
            },
            {
                "name": "test extract markdown images with multiple images",
                "func": extract_markdown_images,
                "params": "![alt text](https://www.boot.dev) ![alt text](https://www.boot.dev)",
                "want": [("alt text", "https://www.boot.dev"), ("alt text", "https://www.boot.dev")]
            },
            {
                "name": "test extract markdown images with multiple images and different alt text",
                "func": extract_markdown_images,
                "params": "![alt text](https://www.boot.dev) ![another alt text](https://www.boot.dev)",
                "want": [("alt text", "https://www.boot.dev"), ("another alt text", "https://www.boot.dev")]
            },
            {
                "name": "test extract markdown images with an image and a link, only return image",
                "func": extract_markdown_images,
                "params": "![alt text](https://www.boot.dev) ![another alt text](https://www.boot.dev)",
                "params": "![alt text](https://www.boot.dev) [link text](https://www.boot.dev)",
                "want": [("alt text", "https://www.boot.dev")]
            },
            {
                "name": "test extract markdown links",
                "func": extract_markdown_links,
                "params": "[link text](https://www.boot.dev)",
                "want": [("link text", "https://www.boot.dev")]
            },
            {
                "name": "test extract markdown links with multiple links",
                "func": extract_markdown_links,
                "params": "[link text](https://www.boot.dev) [link text](https://www.boot.dev)",
                "want": [("link text", "https://www.boot.dev"), ("link text", "https://www.boot.dev")]
            },
            {
                "name": "test extract markdown links with multiple links and different link text",
                "func": extract_markdown_links,
                "params": "[link text](https://www.boot.dev) [another link text](https://www.boot.dev)",
                "want": [("link text", "https://www.boot.dev"), ("another link text", "https://www.boot.dev")]
            },
            {
                "name": "test extract markdown links with an image and a link, only return link",
                "func": extract_markdown_links,
                "params": "![alt text](https://www.boot.dev) [link text](https://www.boot.dev)",
                "want": [("link text", "https://www.boot.dev")]
            },
        ]

        for case in cases:
            print(f"Test case: {case['name']}")
            got = case["func"](case["params"])
            self.assertEqual(got, case["want"])