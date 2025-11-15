from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = None
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        if not isinstance(other, TextNode):
            return False 
        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception(f"Invalid Text Type for {text_node} of {text_node.text_type}")
    
    match text_node.text_type:
        case TextType.LINK:
            return LeafNode(TextType.LINK.value, text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(TextType.IMAGE.value, "", {"src": text_node.url, "alt": text_node.text})
        case _:
            return LeafNode(text_node.text_type.value, text_node.text)