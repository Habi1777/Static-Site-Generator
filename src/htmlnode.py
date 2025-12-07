

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("NotImplementedError")
    
    def props_to_html(self):
        if self.props is None:
            return ''
        
        html_string = ''
        for key in self.props:
            html_string += f'{key}="{self.props[key]}" '
        
        return html_string[:-1]
    
    def __repr__(self):
        return  f"tag={self.tag} value={self.value} children={self.children} props={self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value and self.tag != "img":
            raise ValueError(f"{self.tag}, {self.value}, {self.props} self.value for object is empty")
        if not self.tag:
            return f"{self.value}"
        if not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        
        prop_string = super().props_to_html()
        return f'<{self.tag} {prop_string}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("self.tag for object is empty")
        if not self.children:
            raise ValueError("self.children for object is empty")
        inner_html_string = ""
        for child in self.children:
            inner_html_string += child.to_html()

        if not self.props:
            return f'<{self.tag}>{inner_html_string}</{self.tag}>'
        prop_string = super().props_to_html()
        return f'<{self.tag} {prop_string}>{inner_html_string}</{self.tag}>'
    
    def __repr__(self):
            return f"ParentNode({self.tag}, children: {self.children}, {self.props})"