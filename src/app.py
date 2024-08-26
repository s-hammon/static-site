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

def run():
    try:
        generate_page("content/index.md", "template.html", "public/index.html")
    except Exception as e:
        print(f"Error: {e}")