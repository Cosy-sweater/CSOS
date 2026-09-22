import typing

from vfs_components import *


class ConsoleHandler:
    def __init__(self) -> None:
        self.current_user = "user"
        self.current_path = "/"

        self.file_system = FileSystem()
        self.interpreter = Interpreter(self)

        self.is_running = True

    def output(self, *arg: str, sep: str = " ") -> None:
        print(*arg, sep=sep)

    def _get_prefix(self) -> str:
        return f'{self.current_user}:[{self.file_system.current_path}]#'

    def read_input(self) -> None:
        print(self._get_prefix(), end="")
        command = input().split()
        self.interpreter.handle_command(*command)

    def run(self) -> None:
        while self.is_running:
            self.read_input()


class Interpreter:
    def __init__(self, console: ConsoleHandler) -> None:
        self.console: ConsoleHandler = console

    def handle_command(self, *args: str) -> str:
        if args[0] == "ls":
            self.console.output("ls")
            # self.console.output(*self.console.file_system.get_tree(), sep="\n")
        elif args[0] == "cd":
            self.console.output("cd")
            # self.console.file_system.goto(args[1])
        elif args[0] == "exit":
            self.console.is_running = False
        return "None"


class FileSystem:
    default_tree = Dir("/", [
        Dir("users", [
            Dir("admin", [
                File("test.txt"),
                File("test2.txt")
            ]),
            Dir("user1", [
                File("test_user.txt")
            ])
        ]),
        Dir("bin")
    ])

    def __init__(self, name: str = "DefaultVFS"):
        self.name = name
        self.tree = self.default_tree

        self.current_dir = self.tree
        self.current_path = "/"

    def get_tree(self, start_dir: Dir = None):
        def scan_dir(dir: Dir, depth=-1):
            res = ["---" * depth + " " + dir.name + "/"]
            for i in dir.children:
                if type(i) is File:
                    res.append("---" * (depth + 1) + " " + i.name)
                else:
                    res += scan_dir(i, depth + 1)
            # else:
            #     res.append("-" * (depth + 1) * 2)
            return res

        if start_dir is None:
            start_dir = self.tree

        return scan_dir(start_dir)

    def goto(self, path: str):
        old_dir = self.current_dir
        old_path = self.current_path

        if path.startswith("/"):
            self.current_dir = self.tree
            self.current_path = "/"
            path = path[1:]

        path = path.split("/")
        for dir in path:
            if new_dir := self.current_dir.get_child(dir):
                self.current_dir = new_dir
                self.current_path += self.current_dir.name + "/"
            else:
                self.current_dir = old_dir
                self.current_path = old_path
                return f"Directory not found: {dir}"




if __name__ == "__main__":
    app = ConsoleHandler()
    app.run()
