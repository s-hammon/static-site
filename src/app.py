import os

from block import (
    block_to_block_type, 
    header_markdown_to_html, 
    markdown_to_blocks,
    markdown_to_html_node
)


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == "heading":
            if header_markdown_to_html(block)[0] == "h1":
                return header_markdown_to_html(block)[1]
    
    raise ValueError("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()


    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    with open(template_path, 'r') as f:
        template = f.read().replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(dest_path, 'w') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dir_path_public):
    for file in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, file)
        if os.path.isdir(path):
            generate_pages_recursive(path, template_path, os.path.join(dir_path_public, file))
        else:
            if not os.path.exists(dir_path_public):
                os.mkdir(dir_path_public)
            if file.endswith(".md"):
                generate_page(path, template_path, os.path.join(dir_path_public, file.replace(".md", ".html")))

def run():
    try:
        generate_pages_recursive("content", "template.html", "public")
    except Exception as e:
        print(f"Error: {e}")