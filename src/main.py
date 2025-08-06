import sys, os, shutil
from generating import copy_from_to_dir, generate_pages_recursive

if len(sys.argv) <= 1:
        basepath = "/"
else: basepath = sys.argv[1] +"/"

dir_path_static = "static"
dir_path_docs = "docs"
dir_path_content = "content"
template_path = "template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    copy_from_to_dir(dir_path_static, dir_path_docs)
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)


if __name__ == "__main__":
    main()