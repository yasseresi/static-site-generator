from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes based on a delimiter and convert the delimited text to a specific type.
    
    Args:
        old_nodes: List of TextNode objects
        delimiter: String delimiter to split on (e.g., "`", "**", "_")
        text_type: TextType to assign to the text between delimiters
        
    Returns:
        List of TextNode objects with delimited text converted to the specified type
        
    Raises:
        ValueError: If a closing delimiter is not found
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        parts = old_node.text.split(delimiter)
        
        # If there's an odd number of parts, we have unmatched delimiters
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, {delimiter} delimiter not closed")
        
        # Process the parts
        for i, part in enumerate(parts):
            if part == "":
                # Skip empty parts (happens when delimiter is at start/end)
                continue
                
            if i % 2 == 0:
                # Even indices are regular text (outside delimiters)
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd indices are delimited text (inside delimiters)
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes
