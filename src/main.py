import sys
import os
import shutil
from mdtohtml import markdown_to_html_node

def _rec_copy_files(src, dst):
    if os.path.exists(src):
        for item in os.listdir(src):
            copy_src = os.path.join(src, item)
            copy_dst = os.path.join(dst, item)
            if os.path.isfile(copy_src):
                shutil.copy(copy_src, copy_dst) 
            elif os.path.isdir(copy_src):
                os.mkdir(copy_dst)
                _rec_copy_files(copy_src, copy_dst)

def copy_files(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    _rec_copy_files(src, dst)

def extract_title(markdown):
    stripped_content = markdown.strip()
    if len(stripped_content) > 1:
        title = stripped_content.split('\n')[0].strip()
        if not title.startswith("# "):
            raise ValueError("there is no header on this markdown text")
        return title.replace("# ", "").strip()
    raise ValueError("there is no markdown content")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f_in:
        content_markdown = f_in.read()

    with open(template_path) as f_in:
        content_template = f_in.read()

    html_content = markdown_to_html_node(content_markdown).to_html()
    page_title = extract_title(content_markdown)
    content_template = content_template.replace("{{ Title }}", page_title)
    content_template = content_template.replace("{{ Content }}", html_content)
    content_template = content_template.replace("href=\"/", f"href=\"{basepath}")
    content_template = content_template.replace("src=\"/", f"src=\"{basepath}")

    dst_base = os.path.dirname(dest_path)
    if not os.path.exists(dst_base):
        makedirs(dst_base, exist_ok=True)

    with open(dest_path, 'w') as f_out:
        f_out.write(content_template)

# TODO Implement many templates or dynamic templates
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dir_path_content):
        for item in os.listdir(dir_path_content):
            gen_src = os.path.join(dir_path_content, item)
            gen_dst = os.path.join(dest_dir_path, item)
            if os.path.isfile(gen_src):
                gen_dst = gen_dst.replace('.md', '.html')
                generate_page(gen_src, template_path, gen_dst, basepath) 
            elif os.path.isdir(gen_src):
                os.mkdir(gen_dst)
                generate_pages_recursive(gen_src, template_path, gen_dst, basepath)

def main():
    if len(sys.argv) < 2:
        basepath = "/"
    elif len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        print("usage: main.py <base path>")
        return -1

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    public_path = os.path.join(base_dir, "docs")
    static_path = os.path.join(base_dir, "static")
    copy_files(static_path, public_path)

    generate_pages_recursive(os.path.join(base_dir, "content"),
                             os.path.join(base_dir, "template.html"),
                             public_path,
                             basepath
                             )

if __name__ == "__main__":
    main()
