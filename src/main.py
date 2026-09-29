import sys

from vfs_components import *
from commands import commands


class ConsoleHandler:
    def __init__(self, vfs_path: str = None, starting_script: str = None) -> None:
        try:
            self.file_system = FileSystem(vfs_path)
            self.is_running = True
            self.interpreter = Interpreter(self)
        except Exception as e:
            print(e)
            self.is_running = False
            return

    def output(self, *arg: str, sep: str = " ") -> None:
        print(*arg, sep=sep)

    def _get_prefix(self) -> str:
        return f'{self.file_system.name}:[{self.file_system.current_path}]#'

    def read_input(self, force_input_text: str = None) -> None:
        print(self._get_prefix(), end="")
        if force_input_text is None:
            command = input()
        else:
            command = force_input_text
            print(command)
        self.interpreter.handle_command(command)

    def run(self, script: typing.Iterable[str] = ()) -> None:
        script: list = list(script)

        while self.is_running:
            self.read_input(script.pop(0) if len(script) > 0 else None)


class Interpreter:
    def __init__(self, console: ConsoleHandler) -> None:
        self.console: ConsoleHandler = console

    def handle_command(self, raw: str) -> str:
        tokens = self._parse_input(raw)
        if cmd := commands.get(tokens["command"]):
            cmd(self.console, tokens)
        else:
            self.console.output("Unknown command: " + tokens["command"])

        return "None"

    def _parse_input(self, raw: str):
        tokens = []
        current = []
        in_quotes = False

        # Tokenize while respecting quoted strings.
        for char in raw:
            if char == '"':
                in_quotes = not in_quotes
                continue

            if char == " " and not in_quotes:
                if current:
                    tokens.append("".join(current))
                    current = []
            else:
                current.append(char)

        if current:
            tokens.append("".join(current))

        if not tokens:
            return {}

        result = {
            "command": tokens[0],
            "args": [],
        }

        for token in tokens[1:]:
            if token.startswith("-"):
                if "=" in token:
                    key, value = token.split("=", 1)
                    result[key] = value
                else:
                    result[token] = None
            else:
                result["args"].append(token)

        if not result["args"]:
            del result["args"]

        return result


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

    def __init__(self, vfs_path: str = None):
        self.name: str = None
        self.tree: Dir = None
        self.load_vfs(vfs_path)

        self.current_dir = self.tree
        self.current_path = "/"

    def goto(self, path: str) -> str | None:
        old_dir = self.current_dir
        old_path = self.current_path

        if path.startswith("/"):
            self.current_dir = self.tree
            self.current_path = "/"
            path = path[1:]

            if len(path) == 0:
                return None

        path = path.split("/")
        for dir in path:
            if new_dir := self.current_dir.get_child(dir):
                self.current_dir = new_dir
                self.current_path += self.current_dir.name + "/"
            else:
                self.current_dir = old_dir
                self.current_path = old_path
                return f"Directory not found: {dir}"

    def get_dir(self, path: str) -> Dir | None:
        search_dir = None
        if path.startswith("/"):
            search_dir = self.tree
            path = path[1:]

            if len(path) == 0:
                return search_dir

        path = path.split("/")
        for dir in path:
            if new_dir := self.current_dir.get_child(dir):
                search_dir = new_dir
            else:
                return None

        return search_dir

    def load_vfs(self, path: str) -> None:
        import vfs_handler

        if path is None:
            self.name = "Default Tree"
            self.tree = self.default_tree
        else:
            self.name, self.tree = vfs_handler.load_vfs(path)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        vfs_path = args[0]
        app = ConsoleHandler(vfs_path)
    else:
        app = ConsoleHandler()

    if len(args) > 1:
        try:
            with open(args[1], "r") as f:
                test_script = [i.strip() for i in f.readlines()]
        except FileNotFoundError as e:
            print(e)
            exit(1)

        app.run(test_script)
    else:
        app.run()
