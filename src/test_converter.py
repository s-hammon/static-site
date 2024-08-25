import unittest

from converter import split_nodes_delimiter
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