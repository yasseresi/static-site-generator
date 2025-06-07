import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")

    def test_leaf_to_html_multiple_props(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = LeafNode("a", "Click me!", props)
        expected = '<a href="https://www.google.com" target="_blank">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_no_value_constructor(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_no_value_to_html(self):
        # This test shouldn't be possible with the constructor check,
        # but we'll test the to_html method directly
        node = LeafNode("p", "test")
        node.value = None  # Manually set to None to test the method
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_self_closing_tag(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image"></img>')

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello", {"class": "text"})
        result = repr(node)
        # Should inherit the HTMLNode repr
        self.assertIn("HTMLNode(p, Hello, children: None,", result)
        self.assertIn("'class': 'text'", result)


if __name__ == "__main__":
    unittest.main()
