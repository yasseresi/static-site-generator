import unittest

from htmlnode import ParentNode, LeafNode


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

    def test_to_html_multiple_children(self):
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "italic text")
        child4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child1, child2, child3, child4])
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        expected = '<div class="container" id="main"><span>child</span></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_nested_parents(self):
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode("i", "Italic")
        parent1 = ParentNode("span", [leaf1])
        parent2 = ParentNode("div", [leaf2])
        parent_root = ParentNode("p", [parent1, parent2])
        expected = "<p><span><b>Bold</b></span><div><i>Italic</i></div></p>"
        self.assertEqual(parent_root.to_html(), expected)

    def test_to_html_complex_nesting(self):
        # Create a complex nested structure
        bold_text = LeafNode("b", "Bold")
        italic_text = LeafNode("i", "Italic")
        normal_text = LeafNode(None, " and some normal text")
        
        inner_span = ParentNode("span", [bold_text, italic_text])
        paragraph = ParentNode("p", [inner_span, normal_text])
        article = ParentNode("article", [paragraph])
        
        expected = "<article><p><span><b>Bold</b><i>Italic</i></span> and some normal text</p></article>"
        self.assertEqual(article.to_html(), expected)

    def test_constructor_no_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [child_node])
        self.assertIn("ParentNode must have a tag", str(context.exception))

    def test_constructor_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)
        self.assertIn("ParentNode must have children", str(context.exception))

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        parent_node.tag = None  # Manually set to None to test the method
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("ParentNode must have a tag", str(context.exception))

    def test_to_html_no_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        parent_node.children = None  # Manually set to None to test the method
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("ParentNode must have children", str(context.exception))

    def test_to_html_empty_children_list(self):
        # Test with empty list (should work, just produce empty content)
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "test"})
        result = repr(parent_node)
        # Should inherit the HTMLNode repr
        self.assertIn("HTMLNode(div, None, children:", result)
        self.assertIn("'class': 'test'", result)


if __name__ == "__main__":
    unittest.main()
