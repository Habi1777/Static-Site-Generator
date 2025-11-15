import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_def_none(self):
        node = HTMLNode()
        node2 = "tag=None value=None children=None props=None"
        self.assertEqual(str(node), node2)

    def test_repr_with_vals(self):
        node = HTMLNode("h1", "Title Card", ["Node Object"], {"key": "val"})
        node2 = "tag=h1 value=Title Card children=['Node Object'] props={'key': 'val'}"
        self.assertEqual(str(node), node2)

    def test_props_to_html_1(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        string = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), string)

    def test_props_to_html_2(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        string = 'href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), string)

    def test_props_to_html_3(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank", "src": "src/pictur.jpg"})
        string = 'href="https://www.google.com" target="_blank" src="src/pictur.jpg"'
        self.assertEqual(node.props_to_html(), string)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_p_3(self):
        node = LeafNode("h1", "Title")
        self.assertEqual(node.to_html(), "<h1>Title</h1>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_greatgrandchildren(self):
        greatgrandchild_node = LeafNode("p", "greatgrandchild")
        grandchild_node = ParentNode("b", [greatgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><p>greatgrandchild</p></b></span></div>",
        )
    
    def test_to_html_with_4_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("b", "many nodes")
        parent_node = ParentNode("div", [child_node, child_node2, child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>many nodes</b><span>child</span><b>many nodes</b></div>")

    def test_to_html_with_2_leaf_children_1_parent_child_with_gran(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("p", "many nodes")
        child_node3 = ParentNode("div", [grandchild_node])
        parent_node = ParentNode("div", [child_node, child_node3, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><div><b>grandchild</b></div><p>many nodes</p></div>")

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, child_node)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    '''
    this test was temp for use in testing for exceptions, as i am getting more familiar with unittest vs pytest
    def test_exc(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    '''