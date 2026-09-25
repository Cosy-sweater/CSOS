import xml.etree.ElementTree as ET

from vfs_components import *


def load_vfs(path: str) -> Dir:
    def parse_element(element: ET.Element) -> Dir | File:
        if element.tag == "Dir":
            return Dir(
                element.attrib["name"],
                [parse_element(child) for child in element],
            )

        if element.tag == "File":
            return File(element.attrib["name"])

        raise Exception(f"VFS reading errpr: incorrect tree tag {element.tag}")

    try:
        with open(path, 'rb') as f:
            raw = f.read()
    except FileNotFoundError:
        raise Exception("VFS reading error: no VFS found at given path")

    root = ET.fromstring(raw)
    file_tree = root.find("file-tree")
    vfs_name = root.find("vfs-name").text

    if file_tree is None:
        raise Exception("VFS reading error: file tree not found")

    if vfs_name is None:
        raise Exception("VFS reading error: unnamed vfs")

    # building tree
    root_dir = Dir("/", [parse_element(child) for child in file_tree])

    # reading file contents
    for contents in root.findall("file-contents"):
        path = contents.attrib["path"].split("/")

        if path[0] == "":
            raise Exception("VFS reading error: file-contents path is empty")

        current = root_dir

        for path_part in path[:-1]:
            current = current.get_child(path_part)

            if current is None or type(current) is not Dir:
                raise Exception(f"VFS reading error: incorrect file-contents path {''.join(path)}")

        file = current.get_child(path[-1])
        if file is None or type(file) is not File:
            raise Exception(f"VFS reading error: file-contents file not found {''.join(path)}")

        file.contents = contents.text or ""

    return vfs_name, root_dir


def save_vfs(local_path: str):
    pass


def create_vfs(local_path: str):
    pass


if __name__ == "__main__":
    load_vfs("test")
