import os
import shutil
from textnode import TextNode, TextType


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


def main():
    # Copy static files to public directory
    static_path = "static"
    public_path = "public"
    
    if os.path.exists(static_path):
        copy_static_to_public(static_path, public_path)
        print("Static files copied successfully!")
    else:
        print(f"Static directory '{static_path}' not found")


if __name__ == "__main__":
    main()
