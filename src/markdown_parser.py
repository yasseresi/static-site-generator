from textnode import TextNode, TextType
import re


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
        temp_nodes = []
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Even indices are regular text (outside delimiters)
                if part != "":  # Only add non-empty text nodes
                    temp_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd indices are delimited text (inside delimiters)
                if part != "":  # Only add non-empty delimited nodes
                    temp_nodes.append(TextNode(part, text_type))
                # If delimited content is empty, we skip it (effectively removes the empty delimiter)
        
        # Merge adjacent TEXT nodes (this handles empty delimiter cases)
        if not temp_nodes:
            continue
            
        merged_nodes = [temp_nodes[0]]
        for node in temp_nodes[1:]:
            if (node.text_type == TextType.TEXT and 
                merged_nodes[-1].text_type == TextType.TEXT):
                # Merge with previous TEXT node
                merged_nodes[-1] = TextNode(
                    merged_nodes[-1].text + node.text, 
                    TextType.TEXT
                )
            else:
                merged_nodes.append(node)
        
        new_nodes.extend(merged_nodes)
    
    return new_nodes


def extract_markdown_images(text):
    """
    Extract markdown images from text.
    
    Args:
        text: String containing markdown text
        
    Returns:
        List of tuples containing (alt_text, url) for each image found
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract markdown links from text.
    
    Args:
        text: String containing markdown text
        
    Returns:
        List of tuples containing (anchor_text, url) for each link found
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
