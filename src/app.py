import os

from src.block import (
    block_to_block_type,
    header_markdown_to_html,
    markdown_to_blocks,
    markdown_to_html_node,
)


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == "heading":
            header = header_markdown_to_html(block)
            if header[0] == "h1":
                return header[1]

    raise ValueError("No title found in markdown")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}") # pragma: no cover

    markdown = load_file(from_path)
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = load_file(template_path)
    content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    save_file(dest_path, content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dir_path_public: str
) -> None: # pragma: no cover
    check_path(dir_path_public) 
    for file in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, file)
        public_path = os.path.join(dir_path_public, file.replace(".md", ".html"))

        if os.path.isdir(content_path):
            generate_pages_recursive(
                content_path, template_path, os.path.join(dir_path_public, file)
            )
        else:
            generate_page(content_path, template_path, public_path)


def check_path(path: str) -> None: # pragma: no cover
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Directory {path} created")


def load_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def save_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def run(): # pragma: no cover
    try:
        generate_pages_recursive("content", "template.html", "public")
    except Exception as e:
        print(f"Error: {e}")
