#An HTMLNode without a tag will just render as raw text
#An HTMLNode without a value will be assumed to have children
#An HTMLNode without children will be assumed to have a value
#An HTMLNode without props simply won't have any attributes
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        html_props = [" "]
        for key in self.props:
            html_prop = f"{key}={self.props[key]}"
            html_props.append(html_prop)
        return " ".join(html_props)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, children={self.children}, props={self.props})"

