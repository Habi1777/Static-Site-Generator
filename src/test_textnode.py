import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from other_func import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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
        self.assertListEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_1(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        node2 = TextNode("This is another node with a **bold**", TextType.TEXT)
        node3 = TextNode("This is a node with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT), TextNode("This is another node with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode("This is a node with no delimiters", TextType.TEXT)])

    def test_split_nodes_delimiter_2(self):
        node = TextNode("This is bold text", TextType.BOLD)
        node2 = TextNode("This is text text*", TextType.TEXT)
        node3 = TextNode("This is code text", TextType.CODE)
        new_nodes = split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode("This is bold text", TextType.BOLD), TextNode("This is text text*", TextType.TEXT), TextNode("This is code text", TextType.CODE)])

    def test_split_nodes_delimiter_3(self):
        node = TextNode("This is bold text", TextType.BOLD)
        node2 = TextNode("This is _italic text_", TextType.TEXT)
        node3 = TextNode("This is code text", TextType.CODE)
        new_nodes = split_nodes_delimiter([node, node2, node3], "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, [TextNode("This is bold text", TextType.BOLD), TextNode("This is ", TextType.TEXT), TextNode("italic text", TextType.ITALIC), TextNode("This is code text", TextType.CODE)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_1(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_1(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_2(self):
        matches = extract_markdown_links("This is text with a link [to boot dev]https://www.boot.dev)")
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ]        
        )

    def test_split_images_1(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ]        
        )

    def test_split_images_2_no_image(self):
        node = TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
                TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
            ]        
        )

    def test_split_images_3(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)This is text with an ", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with an ", TextType.TEXT)
            ]        
        )

    def test_split_images_4(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.BOLD)
            ]        
        )

    def test_split_images_5(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ]        
        )

    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode( "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ]
        )

    def test_split_links_1(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ]
        )

    def test_split_links_2_no_link(self):
        node = TextNode("This is text with a link [to boot dev(https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
                TextNode("This is text with a link [to boot dev(https://www.boot.dev)", TextType.TEXT)
            ]
        )

    def test_split_links_3(self):
        node = TextNode("[to boot dev](https://www.boot.dev)This is text with a link ", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is text with a link ", TextType.TEXT)
            ]
        )  

    def test_split_links_4(self):
        node = TextNode("[to boot dev](https://www.boot.dev)This is text with a link ", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
                TextNode("[to boot dev](https://www.boot.dev)This is text with a link ", TextType.BOLD)
            ]
        )

    def test_split_links_5(self):
        node = TextNode("[to boot dev](https://www.boot.dev)This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ]
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(text_to_textnodes(text), [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_to_textnodes_2(self):
        text = ""
        self.assertListEqual(text_to_textnodes(text), [
                TextNode("", TextType.TEXT)
            ]
        )

    def test_text_to_textnodes_3(self):
        text = "This is *text** with an _italic_ word ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(text_to_textnodes(text), [
                TextNode("This is *text** with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_text_to_textnodes_4(self):
        text = "This is a sentence with a bold word inbetween image object ![obi wan image]**bold**(https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(text_to_textnodes(text), [
                TextNode("This is a sentence with a bold word inbetween image object ![obi wan image]", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("(https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
            ]
        )

    def test_text_to_textnodes_5(self):
        text = "This is *text** with an _italic_ word but this is a `block of code that has some_symbols*`![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(text_to_textnodes(text), [
                TextNode("This is *text** with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word but this is a ", TextType.TEXT),
                TextNode("block of code that has some_symbols*", TextType.CODE),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )    

if __name__ == "__main__":
    unittest.main()