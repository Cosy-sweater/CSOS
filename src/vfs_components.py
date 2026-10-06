import typing


class Dir:
    """Класс виртуальной файловой системы, симулирующий директорию"""
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
    """Класс виртуальной файловой системы, симулирующий файл и его содержимое"""
    def __init__(self, name: str, contents: bytes = b""):
        self.name = name
        self.contents: bytes = contents
