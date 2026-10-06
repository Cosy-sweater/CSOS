import typing


class Dir:
    def __init__(self, name: str, children: typing.Iterable = ()):
        self.name = name
        self.children: list[Dir | File] = list(children)

    def get_child(self, name):
        for i in self.children:
            if i.name == name:
                return i

        return None


class File:
    def __init__(self, name: str, contents: bytes = b""):
        self.name = name
        self.contents: bytes = contents
