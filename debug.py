import sys
sys.path.append('src')
from textnode import TextNode, TextType
from markdown_parser import split_nodes_delimiter

# Test the empty delimited text case
node = TextNode("Empty `` delimiter", TextType.TEXT)
result = split_nodes_delimiter([node], "`", TextType.CODE)
print(f"Number of nodes: {len(result)}")
for i, n in enumerate(result):
    print(f"Node {i}: text=\"{n.text}\", type={n.text_type}")

print("\nAnalyzing the split:")
text = "Empty `` delimiter"
parts = text.split("`")
print(f"Parts after split: {parts}")
print(f"Number of parts: {len(parts)}")
for i, part in enumerate(parts):
    print(f"Part {i}: \"{part}\" (empty: {part == ''})")
