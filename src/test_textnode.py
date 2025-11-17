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

    def test_split_nodes_delimiter_1(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        node2 = TextNode("This is another node with a **bold**", TextType.TEXT)
        node3 = TextNode("This is a node with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT), TextNode("This is another node with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode("This is a node with no delimiters", TextType.TEXT)])

    def test_split_nodes_delimiter_2(self):
        node = TextNode("This is bold text", TextType.BOLD)
        node2 = TextNode("This is text text*", TextType.TEXT)
        node3 = TextNode("This is code text", TextType.CODE)
        new_nodes = split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is bold text", TextType.BOLD), TextNode("This is text text*", TextType.TEXT), TextNode("This is code text", TextType.CODE)])

    def test_split_nodes_delimiter_3(self):
        node = TextNode("This is bold text", TextType.BOLD)
        node2 = TextNode("This is _italic text_", TextType.TEXT)
        node3 = TextNode("This is code text", TextType.CODE)
        new_nodes = split_nodes_delimiter([node, node2, node3], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is bold text", TextType.BOLD), TextNode("This is ", TextType.TEXT), TextNode("italic text", TextType.ITALIC), TextNode("This is code text", TextType.CODE)])

if __name__ == "__main__":
    unittest.main()