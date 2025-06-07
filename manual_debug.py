#!/usr/bin/env python3
"""Manual test for debugging split_nodes_delimiter"""

# Manually implement the logic to debug
def debug_split(text, delimiter):
    print(f"Input: '{text}'")
    parts = text.split(delimiter)
    print(f"Split parts: {parts}")
    print(f"Parts count: {len(parts)}")
    
    # Check if odd number of parts
    if len(parts) % 2 == 0:
        print("ERROR: Even number of parts - unmatched delimiter")
        return None
    
    temp_nodes = []
    for i, part in enumerate(parts):
        print(f"Part {i}: '{part}' (index {'even' if i % 2 == 0 else 'odd'})")
        if i % 2 == 0:
            # Even indices are regular text
            if part != "":
                temp_nodes.append(("TEXT", part))
                print(f"  → Added TEXT node: '{part}'")
            else:
                print(f"  → Skipped empty TEXT part")
        else:
            # Odd indices are delimited text
            if part != "":
                temp_nodes.append(("CODE", part))
                print(f"  → Added CODE node: '{part}'")
            else:
                print(f"  → Skipped empty CODE part")
    
    print(f"Temp nodes: {temp_nodes}")
    
    # Merge adjacent TEXT nodes
    if not temp_nodes:
        print("No nodes to merge")
        return []
    
    merged_nodes = [temp_nodes[0]]
    for node in temp_nodes[1:]:
        if node[0] == "TEXT" and merged_nodes[-1][0] == "TEXT":
            # Merge with previous TEXT node
            old_text = merged_nodes[-1][1]
            new_text = old_text + node[1]
            merged_nodes[-1] = ("TEXT", new_text)
            print(f"  → Merged TEXT nodes: '{old_text}' + '{node[1]}' = '{new_text}'")
        else:
            merged_nodes.append(node)
            print(f"  → Added separate node: {node}")
    
    print(f"Final nodes: {merged_nodes}")
    return merged_nodes

if __name__ == "__main__":
    result = debug_split("Empty `` delimiter", "`")
    print(f"\nResult: {len(result) if result else 0} nodes")
    if result:
        for i, (node_type, text) in enumerate(result):
            print(f"  Node {i}: {node_type} '{text}'")
