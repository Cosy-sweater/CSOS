import xml.etree.ElementTree as ET

from vfs_components import File, Dir


def _load_file_contents(root_dir: Dir, contents: ET.Element) -> None:
    content_path = contents.attrib["path"].split("/")

    if content_path[0] == "":
        raise Exception(
            "VFS reading error: file-contents path is empty"
        )

    current = root_dir

    for path_part in content_path[:-1]:
        current = current.get_child(path_part)

        if current is None or type(current) is not Dir:
            raise Exception(
                "VFS reading error: incorrect file-contents "
                f"path {'/'.join(content_path)}"
            )

    file = current.get_child(content_path[-1])

    if file is None or type(file) is not File:
        raise Exception(
            "VFS reading error: file-contents file "
            f"not found {'/'.join(content_path)}"
        )

    file.contents = contents.text or ""


def load_vfs(path: str) -> tuple[str, Dir]:
    """Функция чтения, загрузки и обработки XML файла,
      содержащего виртуальную файловую систему"""

    def parse_element(element: ET.Element) -> Dir | File:
        if element.tag == "Dir":
            return Dir(
                element.attrib["name"],
                [parse_element(child) for child in element],
            )

        if element.tag == "File":
            return File(element.attrib["name"])

        raise Exception(
            f"VFS reading errpr: incorrect tree tag {element.tag}"
        )

    try:
        with open(path, "rb") as f:
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

    root_dir = Dir(
        "~",
        [parse_element(child) for child in file_tree],
    )

    for contents in root.findall("file-contents"):
        _load_file_contents(root_dir, contents)

    return vfs_name, root_dir


def save_vfs(local_path: str):
    pass


def create_vfs(local_path: str):
    pass


if __name__ == "__main__":
    load_vfs("test")
