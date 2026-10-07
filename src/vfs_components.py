import typing


class Dir:
    """Часть виртуальной файловой системы, симулирующий директорию"""
    def __init__(self, name: str, children: typing.Iterable = ()):
        self.name = name
        self.children: list[Dir | File] = list(children)

    def get_child(self, name):
        """Метод поиска файла или директории внутри текущего объекта"""
        for i in self.children:
            if i.name == name:
                return i

        return None


class File:
    """Часть виртуальной файловой системы, симулирующая файл с содержимым"""
    def __init__(self, name: str, contents: bytes = b""):
        self.name = name
        self.contents: bytes = contents
