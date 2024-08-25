import unittest

from converter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
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
    
    def test_split_nodes_image_and_link(self):
        rick_roll = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        obi_wan = "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        cases = [
            {
                "name": "test single node, one image",
                "func": split_nodes_image,
                "params": [
                    TextNode(
                        f"This is text with a {rick_roll} image",
                        "text"
                    )
                ],
                "want": [
                    TextNode("This is text with a ", "text"),
                    TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" image", "text")
                ]
            },
            {
                "name": "test single node, two images",
                "func": split_nodes_image,
                "params": [
                    TextNode(
                        f"This is text with a {rick_roll} and {obi_wan}", 
                        "text"
                    )
                ],
                "want": [
                    TextNode("This is text with a ", "text"),
                    TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" and ", "text"),
                    TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg")
                ]
            },
            {
                "name": "test single node, one image at start",
                "func": split_nodes_image,
                "params": [TextNode(f"{rick_roll} is an ancient meme", "text")],
                "want": [
                    TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" is an ancient meme", "text")
                ]
            },
            {
                "name": "test two nodes, one image one text",
                "func": split_nodes_image,
                "params": [
                    TextNode("This is normal text", "text"),
                    TextNode(f"This is text with a {rick_roll} image", "text")
                ],
                "want": [
                    TextNode("This is normal text", "text"),
                    TextNode("This is text with a ", "text"),
                    TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" image", "text")
                ]
            },
            {
                "name": "test single node, one link",
                "func": split_nodes_link,
                "params": [
                    TextNode(
                        "This is text with a link [to boot dev](https://www.boot.dev)",
                        "text"
                    )
                ],
                "want": [
                    TextNode("This is text with a link ", "text"),
                    TextNode("to boot dev", "link", "https://www.boot.dev")
                ]
            },
            {
                "name": "test two nodes, one two links and one text",
                "func": split_nodes_link,
                "params": [
                    TextNode("This is normal text", "text"),
                    TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")
                ],
                "want": [
                    TextNode("This is normal text", "text"),
                    TextNode("This is text with a link ", "text"),
                    TextNode("to boot dev", "link", "https://www.boot.dev"),
                    TextNode(" and ", "text"),
                    TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")
                ]
            },
        ]

        for case in cases:
            print(f"Test case: {case['name']}")
            got = case["func"](case["params"])
            for g, w in zip(got, case["want"]):
                self.assertEqual(g, w)