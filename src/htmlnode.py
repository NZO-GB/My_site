
class HTMLNode:
    def __init__(self, tag = None, value = None,
                 children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        list = []
        for pair in self.props.items():
            list.append(f'{pair[0]}="{pair[1]}"')
        return " ".join(list)
    
    def __repr__(self):
        return f"{self.tag = } {self.value = } {self.children = } {self.props = }"

class LeafNode(HTMLNode):
    def __init__(self, tag, value,
                props = None):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError("Valueless")
        if not self.tag:
            return self.value
        html_string = f"<{self.tag}"
        if self.props:
            html_string += (" " + self.props_to_html())
        html_string += ">"
        html_string += f"{self.value}"
        html_string += f"</{self.tag}>"
        return html_string
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children,
                props = None):
        super().__init__(tag, children, props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if not self.children:
            raise ValueError("Childless")
        if not self.tag:
            return ValueError("Tagless")
        parent_string = ""
        try:
            for child in self.children:
                parent_string += child.to_html()
        except:
            print(f"{child = }")
        parent_string = f"<{self.tag}>{parent_string}</{self.tag}>"
        return parent_string