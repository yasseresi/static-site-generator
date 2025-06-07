#!/usr/bin/env python3
import sys
import os
sys.path.append('src')

from textnode import TextNode, TextType
from markdown_parser import split_nodes_delimiter

def test_empty_delimiter():
    print("Testing empty delimiter case...")
    text = "Empty `` delimiter"
    print(f"Original text: '{text}'")
    
    # Show how split works
    parts = text.split("`")
    print(f"Split parts: {parts}")
    print(f"Number of parts: {len(parts)}")
    
    # Test our function
    node = TextNode(text, TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    
    print(f"Result: {len(result)} nodes")
    for i, n in enumerate(result):
        print(f"  Node {i}: '{n.text}' ({n.text_type})")
    
    # What the test expects
    print(f"Expected: 1 node with text 'Empty  delimiter'")

if __name__ == "__main__":
    test_empty_delimiter()
