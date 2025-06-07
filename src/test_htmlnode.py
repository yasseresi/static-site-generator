import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("p", "Hello world")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        props = {"href": "https://www.google.com"}
        node = HTMLNode("a", "Click me", None, props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "Click me", None, props)
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_multiple_props_different_order(self):
        props = {
            "class": "btn btn-primary",
            "id": "submit-btn",
            "disabled": "true"
        }
        node = HTMLNode("button", "Submit", None, props)
        result = node.props_to_html()
        # Check that all props are present (order might vary in Python < 3.7)
        self.assertIn('class="btn btn-primary"', result)
        self.assertIn('id="submit-btn"', result)
        self.assertIn('disabled="true"', result)
        # Check that it starts with a space and has the right number of spaces
        self.assertTrue(result.startswith(' '))
        self.assertEqual(result.count('="'), 3)

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello world")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        props = {"href": "https://www.google.com"}
        node = HTMLNode("a", "Click me", None, props)
        expected = "HTMLNode(a, Click me, children: None, {'href': 'https://www.google.com'})"
        self.assertEqual(repr(node), expected)

    def test_repr_with_children(self):
        child = HTMLNode("span", "child text")
        node = HTMLNode("p", None, [child])
        result = repr(node)
        self.assertIn("HTMLNode(p, None, children: [", result)
        self.assertIn("HTMLNode(span, child text, children: None, None)", result)


if __name__ == "__main__":
    unittest.main()
