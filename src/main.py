import os
from textnode import *
from other_func import clear_and_paste_public_dir, generate_page, generate_pages_recursive

src_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(src_dir)
#this code above will give us the absolute path to the root project folder, we use it on main.py to get its path, then use dirname on the src_dir path to go back one folder to the project folder

def main():
    clear_and_paste_public_dir()
    #generate_page("content/index.md", "template.html", "public/index.html")
    content_folder = os.path.join(project_root, "content")
    template_file = os.path.join(project_root, "template.html")
    destination_folder = os.path.join(project_root, "public")
    generate_pages_recursive(content_folder, template_file, destination_folder)

if __name__ == "__main__":
    main()