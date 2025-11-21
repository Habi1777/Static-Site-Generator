from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''
    had to go back in scope and end up using the solution from the project outline, due to the outcome i would want would need more work and probably use of backslashes
    to be able to mark text to be taken as literal, the project recommends i do that at a later point, so i will go back to code that is more rigid for our use
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        delimiter_count = old_node.text.count(delimiter)
        if delimiter_count < 2:
            new_nodes.append(old_node)
            continue
        if delimiter_count % 2 != 0:
            delimiter_count -= 1
        #we adjust the delimiter count if it is odd, to be one less than so we only split on pairs, and not any left over 3rd delimiter that was meant to be text
        sections = old_node.text.split(delimiter, delimiter_count)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes
    '''
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    '''
    Initial working code written without splits, rewrote new version with splits
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        image_data_list = extract_markdown_images(old_node.text)
        if not image_data_list:
            new_nodes.append(old_node)
            continue
        image_index_list = []
        image_string_len_list = []
        for image in image_data_list:
            image_index_list.append(old_node.text.find(f"![{image[0]}]({image[1]})"))
            image_string_len_list.append(len(f"![{image[0]}]({image[1]})"))
        new_node_text = ""
        img_start, img_stop = None, None
        # create variable for inner loop skipping of img data
        for i in range(len(old_node.text)):
            if img_start is not None and img_stop is not None:
                if img_start <= i <= img_stop:
                    continue
            if i not in image_index_list:
                new_node_text += old_node.text[i]
            if i in image_index_list:
                if new_node_text != "":
                    new_nodes.append(TextNode(new_node_text, TextType.TEXT))
                    new_node_text = ""
                new_nodes.append(TextNode(image_data_list[0][0], TextType.IMAGE, image_data_list[0][1]))
                # skip over the text containing the image data, for the image data we just added to new_node list, need to set img start & stop variables 
                img_start = i
                img_stop = (i - 1) + image_string_len_list[0]
                # iterate over the image information lists, to move onto the next image datas since it has already been added to new_nodes list
                image_data_list = image_data_list[1:]
                image_index_list = image_index_list[1:]
                image_string_len_list = image_string_len_list[1:]
            if i == (len(old_node.text)-1):
               if new_node_text != "":
                    new_nodes.append(TextNode(new_node_text, TextType.TEXT))
    return new_nodes 
    '''
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        image_data_list = extract_markdown_images(old_node.text)
        if not image_data_list:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for image in image_data_list:
            split_text = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remaining_text = split_text[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    '''
    the first version we wrote of this code, we wrote without split method, in this second version we can try to use it
    by using it we would be splitting based on one img data at a time, using max split 1, this would cause a 2 len list everytime
    and we would place the img data text node inbetween those 2 other text nodes that would be created from the list
    even if the img starts at the beginning or end, split() ends up making an empty string on the other side of the img data
    example "how are you".split("how") = ["", " are you"] or "how are you".split("you") = ["how are ", ""]
    The part before "how" is empty (since "how" is at the start), so you get an empty string as the first element. The second element is the remainder (" are")
    '''
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        link_data_list = extract_markdown_links(old_node.text)
        if not link_data_list:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for link in link_data_list:
            split_text = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining_text = split_text[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
            

def text_to_textnodes(text):
    if text == "":
        return [TextNode(text, TextType.TEXT)]
    delimiters = [("**", TextType.BOLD), ("_", TextType.ITALIC), ("`", TextType.CODE)]
    initial_node = TextNode(text, TextType.TEXT)
    current_nodes = [initial_node]
    for delimiter in delimiters:
        current_nodes = split_nodes_delimiter(current_nodes, delimiter[0], delimiter[1])
    current_nodes = split_nodes_image(current_nodes)
    current_nodes = split_nodes_link(current_nodes)
    return current_nodes

