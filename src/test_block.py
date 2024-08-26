import unittest

from block import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode

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
            got = markdown_to_blocks(case["params"])
            for g, w in zip(got, case["want"]):
                self.assertEqual(g, w, f"\n\tcase: {case['name']}")
        

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        cases = [
            {
                "name": "test heading block",
                "params": "# This is a heading",
                "want": "heading"
            },
            {
                "name": "test heading6 block",
                "params": "###### This is a heading",
                "want": "heading"
            },
            {
                "name": "test paragraph block, starts with seven # characters",
                "params": "####### This is a paragraph",
                "want": "paragraph"
            },
            {
                "name": "test paragraph block, starts with a # without a space",
                "params": "#This is a paragraph",
                "want": "paragraph"
            },
            {
                "name": "test code block",
                "params": "```this is a code block```",
                "want": "code"
            },
            {
                "name": "test code block, contains ` characters",
                "params": "```this is a code block with ` characters```",
                "want": "code"
            },
            {
                "name": "test paragraph block, starts with ```",
                "params": "```This is a paragraph",
                "want": "paragraph"
            },
            {
                "name": "test single line quote block",
                "params": "> This is a quote",
                "want": "quote"
            },
            {
                "name": "test 3 line quote block",
                "params": "> This is a quote\n> with multiple\n> lines",
                "want": "quote"
            },
            {
                "name": "test paragraph block, starts with > without a space",
                "params": ">This is a paragraph",
                "want": "paragraph"
            },
            {
                "name": "test paragraph block, second line starts without a >",
                "params": "> This is a paragraph\nBecause this line does not start with a '>' character",
                "want": "paragraph"
            },
            {
                "name": "test unordered list, using *",
                "params": "* This is a list item\n* This is another list item",
                "want": "unordered_list"
            },
            {
                "name": "test unordered list, using -",
                "params": "- This is a list item\n- This is another list item",
                "want": "unordered_list"
            },
            {
                "name": "test unordered list, using both * and -",
                "params": "* This is a list item\n- This is another list item",
                "want": "unordered_list"
            },
            {
                "name": "test paragraph block, starts with * without a space",
                "params": "*This is a paragraph",
                "want": "paragraph"
            },
            {
                "name": "test paragraph block, second line starts without a *",
                "params": "* This is a paragraph\nBecause this line does not start with a '*' character",
                "want": "paragraph"
            },
            {
                "name": "test paragraph block, 1st & 3rd line starts with - ",
                "params": "- This is a paragraph\nThis is not a list item\n- This is another list item",
                "want": "paragraph"
            },
            {
                "name": "test ordered list, three items",
                "params": "1. This is a list item\n2. This is another list item\n3. This is a third list item",
                "want": "ordered_list"
            },
            {
                "name": "test paragraph, three lines, out of order",
                "params": "1. This is a list item\n3. This is a third list item\n2. This is another list item",
                "want": "paragraph"
            },
            {
                "name": "test paragraph, three lines, missing prefix",
                "params": "1. This is a list item\nThis is a third list item\n2. This is another list item",
                "want": "paragraph"
            },
        ]

        for case in cases:
            got = block_to_block_type(case["params"])
            self.assertEqual(got, case["want"], f"case: {case['name']}")


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node_simple(self):
        cases = [
            {
                "param": "# This is a heading",
                "want": "<div><h1>This is a heading</h1></div>",
            },
            {
                "param": "###### This is a heading",
                "want": "<div><h6>This is a heading</h6></div>",
            },
            {
                "param": "# This is a **bolded** heading",
                "want": "<div><h1>This is a <b>bolded</b> heading</h1></div>",
            },
            {
                "param": "####### This is actually a *paragraph*",
                "want": "<div><p>####### This is actually a <i>paragraph</i></p></div>",
            },
            {
                "param": "### This is a heading\n\nAnd this is a *paragraph*",
                "want": "<div><h3>This is a heading</h3><p>And this is a <i>paragraph</i></p></div>",
            },
            {
                "param": "```fmt.Println('This is a code block')```",
                "want": "<div><pre><code>fmt.Println('This is a code block')</code></pre></div>",
            },
            {
                "param": "This is a paragraph `which contains` a code block",
                "want": "<div><p>This is a paragraph <code>which contains</code> a code block</p></div>",
            },
            {
                "param": "> The thing that hath been, it is that which shall be;\n> and that which is done is that which shall be done:\n> and there is no new thing under the sun",
                "want": "<div><blockquote>The thing that hath been, it is that which shall be;\nand that which is done is that which shall be done:\nand there is no new thing under the sun</blockquote></div>",
            },
            {
                "param": "> Quoth the Raven:\n> Nevermore.\n\n--An excerpt from *The Raven* by Edgar Allan Poe",
                "want": "<div><blockquote>Quoth the Raven:\nNevermore.</blockquote><p>--An excerpt from <i>The Raven</i> by Edgar Allan Poe</p></div>",
            },
            {
                "param": "* This is a list item\n* This is another list item",
                "want": "<div><ul><li>This is a list item</li><li>This is another list item</li></ul></div>",
            },
            {
                "param": "- This is a list item\n- This is another list item",
                "want": "<div><ul><li>This is a list item</li><li>This is another list item</li></ul></div>",
            },
            {
                "param": "1. This is a list item\n2. This is another list item",
                "want": "<div><ol><li>This is a list item</li><li>This is another list item</li></ol></div>",
            },
        ]

        for case in cases:
            got =  markdown_to_html_node(case["param"])
            print(got.to_html())
            self.assertEqual(got.to_html(), case["want"])

    def test_markdown_to_html_node_from_file(self):
        cases = [
            {
                "filename": "sample",
            }
        ]

        for case in cases:
            with open(f"src/examples/{case['filename']}.md") as f:
                markdown = f.read()

            with open(f"src/examples/{case['filename']}.html") as f:
                want = f.read()

            got = markdown_to_html_node(markdown)
            self.assertEqual(got.to_html(), want)