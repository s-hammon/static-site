import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "This is a div node")
        self.assertEqual(repr(node), "HTMLNode(div, This is a div node, None, None)") 
    
    def test_props_to_html(self):
        cases = [
            {
                "params": {
                    "tag": "a",
                    "value": "This is a link",
                    "children": None,
                    "props": {"href": "https://www.boot.dev"}
                },
                "expected": 'href="https://www.boot.dev"'
            },
            {
                "params": {
                    "tag": "input",
                    "value": None,
                    "children": None,
                    "props": {"type": "text", "name": "username"}
                },
                "expected": 'type="text" name="username"'
            },
            {
                "params": {
                    "tag": "img",
                    "value": None,
                    "children": None,
                    "props": {"src": "https://www.boot.dev", "alt": "Boot"}
                },
                "expected": 'src="https://www.boot.dev" alt="Boot"'
            },
            {
                "params": {
                    "tag": "a",
                    "value": "This is a link with a target",
                    "children": None,
                    "props": {"href": "https://www.boot.dev", "target": "_blank"}
                },
                "expected": 'href="https://www.boot.dev" target="_blank"'
            }
        ]

        for case in cases:
            node = HTMLNode(**case["params"])
            self.assertEqual(node.props_to_html(), case["expected"])


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        cases = [
            {
                "params": {
                    "tag": "a",
                    "value": "This is a link",
                    "props": {"href": "https://www.boot.dev"}
                },
                "expected": '<a href="https://www.boot.dev">This is a link</a>'
            },
            {
                "params": {
                    "tag": "a",
                    "value": "This is a link with a target",
                    "props": {"href": "https://www.boot.dev", "target": "_blank"}
                },
                "expected": '<a href="https://www.boot.dev" target="_blank">This is a link with a target</a>'
            },
        ]

        for case in cases:
            node = LeafNode(**case["params"])
            self.assertEqual(node.to_html(), case["expected"])
        
    def test_to_html_raises_value_error(self):
        node = LeafNode(value=None, tag="p")
        with self.assertRaises(ValueError):
            node.to_html()
        