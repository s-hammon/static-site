import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_neq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_repr_with_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, https://www.boot.dev)")
        

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node(self):
        cases = [
            {
                "params": TextNode("This is a raw text node", "text"),
                "expected": LeafNode("This is a raw text node", None)
            },
            {
                "params": TextNode("This is a bold text node", "bold"),
                "expected": LeafNode("This is a bold text node", "b")
            },
            {
                "params": TextNode("This is an italic text node", "italic"),
                "expected": LeafNode("This is an italic text node", "i")
            },
            {
                "params": TextNode("print('This is a code text node')", "code"),
                "expected": LeafNode("print('This is a code text node')", "code")
            },
            {
                "params": TextNode("This is a link text node", "link", "https://www.boot.dev"),
                "expected": LeafNode("This is a link text node", "a", {"href": "https://www.boot.dev"})
            },
            {
                "params": TextNode("This is an image text node", "image", "https://www.boot.dev"),
                "expected": LeafNode("", "img", {"src": "https://www.boot.dev", "alt": "This is an image text node"})
            }
        ]

        for case in cases:
            self.assertEqual(text_node_to_html_node(case["params"]), case["expected"])

    def test_text_node_to_html_node_throw_error(self):
        cases = [
            TextNode("> This is a text node", "blockquote"),
            # TextNode("This is a link text node", "link")
        ]

        for case in cases:
            with self.assertRaises(ValueError):
                text_node_to_html_node(case)

if __name__ == '__main__':
    unittest.main()