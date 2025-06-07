#!/usr/bin/env python3
"""Simple test verification script"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from textnode import TextNode, TextType
from markdown_parser import split_nodes_delimiter

def test_empty_delimited_text():
    """Test the empty delimited text case"""
    print("=== Testing empty delimited text ===")
    
    node = TextNode("Empty `` delimiter", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    print(f"Input: 'Empty `` delimiter'")
    print(f"Result: {len(new_nodes)} nodes")
    for i, n in enumerate(new_nodes):
        print(f"  Node {i}: '{n.text}' ({n.text_type.name})")
    
    # Expected: 1 node with "Empty  delimiter"
    expected_text = "Empty  delimiter"
    if len(new_nodes) == 1 and new_nodes[0].text == expected_text:
        print("✅ PASS")
        return True
    else:
        print(f"❌ FAIL - Expected 1 node with '{expected_text}'")
        return False

def test_normal_delimiter():
    """Test normal delimiter case for comparison"""
    print("\n=== Testing normal delimiter ===")
    
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    print(f"Input: 'This is text with a `code block` word'")
    print(f"Result: {len(new_nodes)} nodes")
    for i, n in enumerate(new_nodes):
        print(f"  Node {i}: '{n.text}' ({n.text_type.name})")

if __name__ == "__main__":
    success = test_empty_delimited_text()
    test_normal_delimiter()
    
    if success:
        print("\n🎉 Test passed!")
    else:
        print("\n💥 Test failed!")
        sys.exit(1)
