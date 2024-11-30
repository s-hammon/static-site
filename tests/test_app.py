import os
import unittest

from src.app import extract_title, generate_page, check_path


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        cases = [
            {"input": "# Hello World", "expected": "Hello World"},
            {"input": "# Hello World\n\n## Subtitle", "expected": "Hello World"},
            {"input": "## Subtitle\n\n# Hello World", "expected": "Hello World"},
            {
                "input": "## Subtitle\n\n# Hello World\n\n## Subtitle",
                "expected": "Hello World",
            },
            {
                "input": "## Subtitle\n\n# Subtitle\n\n## Subtitle\n\n# Hello World",
                "expected": "Subtitle",
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


class TestGeneratePage(unittest.TestCase):
    def test_generate_page(self):
        params = {
            "from_path": "tests/test_data/test.md",
            "template_path": "template.html",
            "dest_path": "tests/test_data/test.html",
        }

        check_path("tests/test_data")
        try:
            os.remove(params["dest_path"])
        except FileNotFoundError:
            pass

        generate_page(**params)

        self.assertTrue(os.path.exists(params["dest_path"]))