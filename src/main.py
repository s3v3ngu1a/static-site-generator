import os
import shutil
from textnode import TextNode

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


def main():
    public_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "public"))
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "static"))
    copy_files(static_path, public_path)

if __name__ == "__main__":
    main()
