#!/usr/bin/env python3
"""Simple verification of the current implementation"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from textnode import TextNode, TextType
    from markdown_parser import split_nodes_delimiter
    print("✅ Imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

try:
    # Test the problematic case
    node = TextNode("Empty `` delimiter", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    
    print(f"Input: 'Empty `` delimiter'")
    print(f"Result: {len(result)} nodes")
    for i, n in enumerate(result):
        print(f"  Node {i}: '{n.text}' ({n.text_type.name})")
    
    # Check expectation
    if len(result) == 1 and result[0].text == "Empty  delimiter" and result[0].text_type == TextType.TEXT:
        print("✅ Test PASSED")
    else:
        print("❌ Test FAILED")
        print(f"Expected: 1 node with text 'Empty  delimiter' and type TEXT")

except Exception as e:
    print(f"❌ Runtime error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
