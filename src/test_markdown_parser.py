import unittest

from textnode import TextNode, TextType
from markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_bold_delimiter(self):
        node = TextNode("This is text with **bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_italic_delimiter(self):
        node = TextNode("This is text with _italic_ words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" words", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_multiple_delimiters(self):
        node = TextNode("Code `here` and `there` end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Code ", TextType.TEXT),
            TextNode("here", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("there", TextType.CODE),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_delimiter_at_end(self):
        node = TextNode("End with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_no_delimiter(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, expected[0].text)
        self.assertEqual(new_nodes[0].text_type, expected[0].text_type)

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Plain text with `code`", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        # First node should be split
        self.assertEqual(new_nodes[0].text, "Plain text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        
        # Other nodes should remain unchanged
        self.assertEqual(new_nodes[2].text, "Already bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "Already italic")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)

    def test_unmatched_delimiter_raises_error(self):
        node = TextNode("This has `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("Invalid markdown", str(context.exception))
        self.assertIn("delimiter not closed", str(context.exception))

    def test_empty_delimited_text(self):
        node = TextNode("Empty `` delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # Empty delimited text should be skipped
        expected = [TextNode("Empty  delimiter", TextType.TEXT)]
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Empty  delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_only_delimited_text(self):
        node = TextNode("`only code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("only code", TextType.CODE)]
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "only code")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("First `code` block", TextType.TEXT),
            TextNode("Second `code` block", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 6)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_complex_delimiters(self):
        # Test with ** delimiter for bold
        node = TextNode("This **is** really **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" really ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        text = "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_with_links(self):
        text = "This has ![image](https://example.com/image.png) and [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/image.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_text(self):
        text = "This is text with a link [](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_ignores_images(self):
        text = "This has ![image](https://example.com/image.png) and [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_complex_text(self):
        text = "Check out [my GitHub](https://github.com/user) and [my website](https://example.com/path?param=value)"
        matches = extract_markdown_links(text)
        expected = [("my GitHub", "https://github.com/user"), ("my website", "https://example.com/path?param=value")]
        self.assertListEqual(expected, matches)

    def test_extract_mixed_images_and_links(self):
        text = "Here's an ![cool image](https://example.com/image.jpg) and a [cool link](https://example.com)"
        
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        self.assertListEqual([("cool image", "https://example.com/image.jpg")], image_matches)
        self.assertListEqual([("cool link", "https://example.com")], link_matches)

    def test_extract_nested_brackets_in_text(self):
        # Test that the regex handles simple cases without nested brackets in alt text
        text = "This [has] some ![image description](https://example.com/img.png) text"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image description", "https://example.com/img.png")], matches)

    def test_extract_special_characters_in_alt_text(self):
        text = "Here's an ![image with \"quotes\" & symbols](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image with \"quotes\" & symbols", "https://example.com/img.png")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertEqual(len(new_nodes), 4)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_single_image(self):
        node = TextNode(
            "This has an ![image](https://example.com/img.png) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This has an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/img.png) at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_image_at_end(self):
        node = TextNode(
            "Text ending with ![image](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_only_image(self):
        node = TextNode(
            "![only image](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("only image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, expected[0].text)
        self.assertEqual(new_nodes[0].text_type, expected[0].text_type)
        self.assertEqual(new_nodes[0].url, expected[0].url)

    def test_split_no_images(self):
        node = TextNode("This text has no images at all", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("This text has no images at all", TextType.TEXT)]
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, expected[0].text)
        self.assertEqual(new_nodes[0].text_type, expected[0].text_type)
        self.assertEqual(new_nodes[0].url, expected[0].url)

    def test_split_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Text with ![image](https://example.com/img.png)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_image(nodes)
        
        # First node should be split
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/img.png")
        
        # Other nodes should remain unchanged
        self.assertEqual(new_nodes[2].text, "Already bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "Already italic")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)

    def test_split_images_empty_alt_text(self):
        node = TextNode(
            "Image with ![](https://example.com/img.png) empty alt",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Image with ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" empty alt", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_multiple_nodes_input(self):
        nodes = [
            TextNode("First ![image1](https://example.com/1.png) node", TextType.TEXT),
            TextNode("Second ![image2](https://example.com/2.png) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://example.com/1.png"),
            TextNode(" node", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/2.png"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 6)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(len(new_nodes), 4)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_single_link(self):
        node = TextNode(
            "This has a [link](https://example.com) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_link_at_start(self):
        node = TextNode(
            "[link](https://example.com) at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_link_at_end(self):
        node = TextNode(
            "Text ending with [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_only_link(self):
        node = TextNode(
            "[only link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("only link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, expected[0].text)
        self.assertEqual(new_nodes[0].text_type, expected[0].text_type)
        self.assertEqual(new_nodes[0].url, expected[0].url)

    def test_split_no_links(self):
        node = TextNode("This text has no links at all", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This text has no links at all", TextType.TEXT)]
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, expected[0].text)
        self.assertEqual(new_nodes[0].text_type, expected[0].text_type)
        self.assertEqual(new_nodes[0].url, expected[0].url)

    def test_split_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Text with [link](https://example.com)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_link(nodes)
        
        # First node should be split
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")
        
        # Other nodes should remain unchanged
        self.assertEqual(new_nodes[2].text, "Already bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "Already italic")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)

    def test_split_links_empty_text(self):
        node = TextNode(
            "Link with [](https://example.com) empty text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Link with ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://example.com"),
            TextNode(" empty text", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_links_ignores_images(self):
        node = TextNode(
            "This has ![image](https://example.com/img.png) and [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Should only split the link, not the image
        expected = [
            TextNode("This has ![image](https://example.com/img.png) and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_multiple_nodes_input(self):
        nodes = [
            TextNode("First [link1](https://example.com/1) node", TextType.TEXT),
            TextNode("Second [link2](https://example.com/2) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(" node", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 6)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)

    def test_split_mixed_with_images_and_links(self):
        # Test that links are extracted but images are left as text
        node = TextNode(
            "Here's an ![image](https://example.com/img.png) and a [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here's an ![image](https://example.com/img.png) and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)
            self.assertEqual(new_nodes[i].url, expected_node.url)
