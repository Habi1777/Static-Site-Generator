from textnode import *

def main():
    object1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #object2 = TextNode("This is some anchor text", TextType.IMAGE, "https://www.boot.dev")
    print(object1)

if __name__ == "__main__":
    main()