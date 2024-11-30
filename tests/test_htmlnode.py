import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "This is a div node")
        self.assertEqual(repr(node), "HTMLNode(div, This is a div node, [], {})") 
    
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
            {
                "params": {
                    "tag": "b",
                    "value": "Bolded text"
                },
                "expected": '<b>Bolded text</b>'
            },
        ]

        for case in cases:
            node = LeafNode(**case["params"])
            self.assertEqual(node.to_html(), case["expected"])
        
    def test_to_html_raises_value_error(self):
        node = LeafNode(value=None, tag="p")
        with self.assertRaises(ValueError):
            node.to_html()
        

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        cases = [
            {
                "params": {
                    "tag": "p",
                    "children": [
                        LeafNode("Bolded text", "b"),
                        LeafNode("Normal text", None),
                        LeafNode("italicized text", "i"),
                        LeafNode("Normal text", None)
                    ]
                },
                "expected": '<p><b>Bolded text</b>Normal text<i>italicized text</i>Normal text</p>'
            },
            {
                "params": {
                    "tag": "div",
                    "children": [
                        LeafNode("This is a div node", "p"),
                        ParentNode(
                            [
                                LeafNode("This is a child div node", "p"),
                                LeafNode("This is another child div node", "p")
                            ], 
                            "div"
                        )
                    ]
                },
                "expected": '<div><p>This is a div node</p><div><p>This is a child div node</p><p>This is another child div node</p></div></div>'
            },
            {
                "params": {
                    "tag": "a",
                    "children": [
                        LeafNode("This is a link", None)
                    ],
                    "props": {"href": "https://www.boot.dev"}
                },
                "expected": '<a href="https://www.boot.dev">This is a link</a>'
            },
            {
                "params": {
                    "tag": "div",
                    "children": [
                        LeafNode("This is a link", "a", {"href": "https://www.boot.dev"}), 
                    ],
                    "props": {"class": "container"}
                },
                "expected": '<div class="container"><a href="https://www.boot.dev">This is a link</a></div>'
            },
        ]

        for case in cases:
            node = ParentNode(**case["params"])
            self.assertEqual(node.to_html(), case["expected"])
        
    def test_to_html_raises_value_error(self):
        cases = [
            {
                "tag": "div",
                "children": None
            },
            {
                "tag": "div",
                "children": []
            },
            {
                "tag": None,
                "children": [LeafNode("This is a div node", "p")]
            },
            {
                "tag": "div",
                "children": [ParentNode([], "div")]
            },
            {
                "tag": "div",
                "children": [ParentNode([LeafNode("This is a child div node", "p")], None)]
            },
        ]

        for case in cases:
            node = ParentNode(**case)
            with self.assertRaises(ValueError):
                node.to_html()