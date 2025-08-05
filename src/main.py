
from generating import copy_from_to_dir, generate_pages_recursive

def main():
    copy_from_to_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()