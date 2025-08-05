import os, shutil, re

from markdown_blocks import markdown_to_html_node

def copy_from_to_dir(source, destination):

    if not os.path.exists(source):
        raise Exception("source doesn't exist")

    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    to_copy = os.listdir(source)

    for element in to_copy:
        abspath_to_copy_element = os.path.join(source, element)
        abspath_to_paste_element = os.path.join(destination, element)
        if not os.path.isfile(abspath_to_copy_element):
             copy_from_to_dir(abspath_to_copy_element, abspath_to_paste_element)
        else:
            shutil.copy(abspath_to_copy_element, abspath_to_paste_element)

    if os.listdir(source) == os.listdir(destination):
        print("Pasted succesfully")

def extract_title(markdown):
    markdown = markdown.split("\n")
    title_search = []
    for line in markdown:
        if re.search(r"^# (.*)", line):
            title_search.append(line[2:])
    
    if len(title_search) > 1:
        print(f"{title_search = }")
        raise Exception("More than one title")
    title = title_search[0].strip()
    return title

def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_file = f.read(10000)
    with open(template_path) as f: 
        template_file = f.read(10000)
    from_html = markdown_to_html_node(from_file).to_html()
    title = extract_title(from_file)
    dest_file = template_file.replace(r"{{ Title }}", title).replace(r"{{ Content }}", from_html)
    with open(dest_path, "w") as f:
        f.write(dest_file)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    print(f"Recursive IN {dir_path_content} to {dest_dir_path} using {template_path}")

    to_copy = os.listdir(dir_path_content)

    for element in to_copy:
        element_path = os.path.join(dir_path_content, element)
        dest_element_path = os.path.join(dest_dir_path, element)
        if element.endswith(".md"): 
            print(f"MARKDOWN {element}")
            dest_element_path = dest_element_path.replace(".md", ".html")
            generate_page(element_path, template_path, dest_element_path)
        elif not os.path.isfile(element_path):
            print(f"DIRECTORY {element}")
            os.mkdir(dest_element_path)
            generate_pages_recursive(element_path, template_path, dest_element_path)