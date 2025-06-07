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


def split_nodes_image(old_nodes):
    """
    Split text nodes based on markdown image syntax and convert them to IMAGE nodes.
    
    Args:
        old_nodes: List of TextNode objects
        
    Returns:
        List of TextNode objects with images converted to IMAGE type
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all images from the text
        images = extract_markdown_images(old_node.text)
        
        # If no images found, add the original node
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Process the text by splitting on each image
        current_text = old_node.text
        
        for alt_text, url in images:
            # Split the text around this image
            image_markdown = f"![{alt_text}]({url})"
            sections = current_text.split(image_markdown, 1)
            
            if len(sections) != 2:
                # This shouldn't happen if extract_markdown_images is working correctly
                continue
            
            before_text, after_text = sections
            
            # Add the text before the image (if not empty)
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Continue processing with the text after this image
            current_text = after_text
        
        # Add any remaining text after the last image (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split text nodes based on markdown link syntax and convert them to LINK nodes.
    
    Args:
        old_nodes: List of TextNode objects
        
    Returns:
        List of TextNode objects with links converted to LINK type
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all links from the text
        links = extract_markdown_links(old_node.text)
        
        # If no links found, add the original node
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Process the text by splitting on each link
        current_text = old_node.text
        
        for anchor_text, url in links:
            # Split the text around this link
            link_markdown = f"[{anchor_text}]({url})"
            sections = current_text.split(link_markdown, 1)
            
            if len(sections) != 2:
                # This shouldn't happen if extract_markdown_links is working correctly
                continue
            
            before_text, after_text = sections
            
            # Add the text before the link (if not empty)
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Continue processing with the text after this link
            current_text = after_text
        
        # Add any remaining text after the last link (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes
