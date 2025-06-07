import os
import shutil
from textnode import TextNode, TextType
from markdown_blocks import markdown_to_html_node, extract_title


def copy_static_to_public(src_path, dest_path):
    """
    Recursively copy all contents from source directory to destination directory.
    First deletes all contents of destination directory to ensure clean copy.
    
    Args:
        src_path: Source directory path
        dest_path: Destination directory path
    """
    # Delete destination directory if it exists
    if os.path.exists(dest_path):
        print(f"Deleting existing directory: {dest_path}")
        shutil.rmtree(dest_path)
    
    # Create destination directory
    print(f"Creating directory: {dest_path}")
    os.mkdir(dest_path)
    
    # Copy contents recursively
    _copy_directory_contents(src_path, dest_path)


def _copy_directory_contents(src_path, dest_path):
    """
    Helper function to recursively copy directory contents.
    
    Args:
        src_path: Source directory path
        dest_path: Destination directory path
    """
    # List all items in source directory
    for item in os.listdir(src_path):
        src_item_path = os.path.join(src_path, item)
        dest_item_path = os.path.join(dest_path, item)
        
        if os.path.isfile(src_item_path):
            # Copy file
            print(f"Copying file: {src_item_path} -> {dest_item_path}")
            shutil.copy(src_item_path, dest_item_path)
        else:
            # Create subdirectory and copy recursively
            print(f"Creating directory: {dest_item_path}")
            os.mkdir(dest_item_path)
            _copy_directory_contents(src_item_path, dest_item_path)


def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from markdown content using a template.
    
    Args:
        from_path: Path to the markdown file
        template_path: Path to the HTML template file
        dest_path: Path where the generated HTML should be written
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML to the destination file
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages for all markdown files in the content directory.
    
    Args:
        dir_path_content: Path to the content directory
        template_path: Path to the HTML template file  
        dest_dir_path: Path to the destination directory
    """
    # Walk through all files and directories in content directory
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(item_path) and item.endswith('.md'):
            # Generate HTML page for markdown file
            if item == 'index.md':
                # For index files, use the directory name as the output
                dest_file = os.path.join(dest_dir_path, 'index.html')
            else:
                # For other markdown files, replace .md with .html
                dest_file = os.path.join(dest_dir_path, item.replace('.md', '.html'))
            
            generate_page(item_path, template_path, dest_file)
            
        elif os.path.isdir(item_path):
            # Create corresponding directory in destination and recurse
            dest_subdir = os.path.join(dest_dir_path, item)
            if not os.path.exists(dest_subdir):
                os.makedirs(dest_subdir)
            
            generate_pages_recursive(item_path, template_path, dest_subdir)


def main():
    # Delete anything in the public directory and copy static files
    static_path = "static"
    public_path = "public"
    
    if os.path.exists(static_path):
        copy_static_to_public(static_path, public_path)
        print("Static files copied successfully!")
    else:
        print(f"Static directory '{static_path}' not found")
    
    # Generate all pages recursively
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html", 
        dest_dir_path="public"
    )
    print("All pages generated successfully!")


if __name__ == "__main__":
    main()
