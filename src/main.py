import os
import sys
from textnode import *
from other_func import clear_and_paste_public_dir, generate_page, generate_pages_recursive

if len(sys.argv) > 1 and sys.argv[1]:
    basepath = sys.argv[1]
else:
    #src_dir = os.path.dirname(os.path.abspath(__file__))
    #basepath = os.path.dirname(src_dir)
    basepath = "/"
#originally built the system to create the path based on the folder but for github pages


src_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(src_dir)

#this code above will give us the absolute path to the root project folder, we use it on main.py to get its path, then use dirname on the src_dir path to go back one folder to the project folder

def main():
    clear_and_paste_public_dir(project_root)
    #generate_page("content/index.md", "template.html", "public/index.html")
    content_folder = os.path.join(project_root, "content")
    template_file = os.path.join(project_root, "template.html")
    destination_folder = os.path.join(project_root, "docs")
    #changed destination folder to the docs folder, as that is the folder that github pages uses
    generate_pages_recursive(content_folder, template_file, destination_folder, basepath)

if __name__ == "__main__":
    main()