from typing import List

def markdown_to_blocks(markdown: str) -> List[str]:
    blocks =  markdown.split("\n\n") 
    return [ block.strip() for block in blocks if block.strip()]