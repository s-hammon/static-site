from typing import Any, Dict, List, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        self.tag: str = tag or ""
        self.value: str = value or ""
        self.children: List["HTMLNode"] = children or []
        self.props: Dict[str, str] = props or {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])


class ParentNode(HTMLNode):
    def __init__(
        self,
        children: List[HTMLNode],
        tag: Optional[str] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == "":
            raise ValueError("ParentNode must have a tag")
        if len(self.children) == 0:
            raise ValueError("ParentNode must have children")

        html_string = (
            f"<{self.tag}>"
            if len(self.props) == 0
            else f"<{self.tag} {self.props_to_html()}>"
        )
        for children in self.children:
            html_string += children.to_html()

        return f"{html_string}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(
        self,
        value: str,
        tag: Optional[str] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        super().__init__(tag, value, None, props)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value}, {self.tag}, {self.props})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, LeafNode):
            return (
                self.value == other.value
                and self.tag == other.tag
                and self.props == other.props
            )
        return False

    def to_html(self) -> str:
        if self.value == "" and self.tag != "img":
            raise ValueError("LeafNode must have a value")
        if self.tag == "":
            return self.value

        if len(self.props) == 0:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
