class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError()
        
    def props_to_html(self) -> str:
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])


class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str=None, props: dict=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
