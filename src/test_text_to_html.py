import unittest

from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node
from htmlnode import LeafNode


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.to_html(), "<i>This is italic text</i>")

    def test_code(self):
        node = TextNode("print('hello world')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello world')")
        self.assertEqual(html_node.to_html(), "<code>print('hello world')</code>")

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "An image"})
        expected_html = '<img src="https://example.com/image.jpg" alt="An image"></img>'
        self.assertEqual(html_node.to_html(), expected_html)

    def test_link_no_url(self):
        node = TextNode("Click me!", TextType.LINK, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Link TextNode must have a URL", str(context.exception))

    def test_image_no_url(self):
        node = TextNode("An image", TextType.IMAGE, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Image TextNode must have a URL", str(context.exception))

    def test_unsupported_text_type(self):
        # Create a TextNode with an invalid text_type by manually setting it
        node = TextNode("Some text", TextType.TEXT)
        node.text_type = "invalid_type"  # This would not normally be possible
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Unsupported TextType", str(context.exception))

    def test_all_types_return_leaf_node(self):
        # Test that all valid types return LeafNode instances
        test_cases = [
            TextNode("text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode("image", TextType.IMAGE, "http://example.com/img.jpg"),
        ]
        
        for text_node in test_cases:
            html_node = text_node_to_html_node(text_node)
            self.assertIsInstance(html_node, LeafNode)

    def test_link_empty_text(self):
        node = TextNode("", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com"></a>')

    def test_image_special_characters_alt(self):
        node = TextNode("Image with \"quotes\" & symbols", TextType.IMAGE, "https://example.com/img.jpg")
        html_node = text_node_to_html_node(node)
        expected_html = '<img src="https://example.com/img.jpg" alt="Image with "quotes" & symbols"></img>'
        self.assertEqual(html_node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
