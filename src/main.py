import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./public"  # Default for local development/bootdev
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"


def main():
    basepath = default_basepath
    output_dir = dir_path_public
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--github":
            output_dir = "./docs"
            basepath = "/"
        elif sys.argv[1].startswith("--output="):
            output_dir = sys.argv[1].split("=")[1]
        else:
            basepath = sys.argv[1]

    print("Deleting public directory...")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, output_dir)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, output_dir, basepath)


main()
