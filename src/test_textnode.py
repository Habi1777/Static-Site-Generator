import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from other_func import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq_same_with_default_link(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_same_with_link(self):
        node = TextNode("This", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_not_same_TextType(self):
        node = TextNode("Words", TextType.CODE, "https://www.boot.dev")
        node2 = TextNode("Words", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_not_same_Link(self):
        node = TextNode("Names", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Names", TextType.LINK, "https://www.boots.dev")
        self.assertNotEqual(node, node2)

    def test_eq_not_same_text(self):
        node = TextNode("This", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Is it", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_text_to_html_func(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_func_1(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_text_to_html_func_2(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_text_to_html_func_3(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {'href': 'https://www.boot.dev'})

class TestOtherFunc(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])
    
        

if __name__ == "__main__":
    unittest.main()