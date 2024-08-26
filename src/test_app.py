import unittest

from app import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        cases = [
            {
                "input": "# Hello World",
                "expected": "Hello World"
            },
            {
                "input": "# Hello World\n\n## Subtitle",
                "expected": "Hello World"
            },
            {
                "input": "## Subtitle\n\n# Hello World",
                "expected": "Hello World"
            },
            {
                "input": "## Subtitle\n\n# Hello World\n\n## Subtitle",
                "expected": "Hello World"
            },
            {
                "input": "## Subtitle\n\n# Subtitle\n\n## Subtitle\n\n# Hello World",
                "expected": "Subtitle"
            },
        ]

        for case in cases:
            self.assertEqual(extract_title(case["input"]), case["expected"])

    def test_extract_title_raise_error(self):
        cases = [
            "",
            "## Subtitle",
            "## Subtitle\n\n### Subtitle",
        ]

        for case in cases:
            with self.assertRaises(ValueError):
                extract_title(case)