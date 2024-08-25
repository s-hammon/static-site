import unittest

from block import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        cases = [
            {
                "name": "test 1 block with leading whitespace",
                "params": "   this is a paragraph wiht leading whitespace",
                "want": ["this is a paragraph wiht leading whitespace"]
            },
            {
                "name": "test 1 block with leading and trailing whitespace",
                "params": "   this is a paragraph wiht leading and trailing whitespace   ",
                "want": ["this is a paragraph wiht leading and trailing whitespace"]
            },
            {
                "name": "test 2 blocks, separated by 3 newlines",
                "params": "this is a paragraph\n\n\nthis is another paragraph",
                "want": ["this is a paragraph", "this is another paragraph"]
            },
            {
                "name": "test 2 blocks, separatedy by 4 newlines",
                "params": "this is a paragraph\n\n\n\nthis is another paragraph",
                "want": ["this is a paragraph", "this is another paragraph"]
            },
            {
                "name": "test 3 blocks",
                "params": "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item",
                "want": [
                    "# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                ]
            },
        ]

        for case in cases:
            print(f"Test case: {case['name']}")
            got = markdown_to_blocks(case["params"])
            for g, w in zip(got, case["want"]):
                self.assertEqual(g, w)