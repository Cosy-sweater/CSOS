from vfs_components import File, Dir


class ConsoleHandler:
    """Основной класс, используемый для запуска и исполнения программы"""
    def __init__(self) -> None:
        self.current_user = "user"
        self.current_path = "/"

        self.file_system = FileSystem()
        self.interpreter = Interpreter(self)

        self.is_running = True

    def output(self, *arg: str, sep: str = " ") -> None:
        """Метод вывода в консоль для использования программой"""
        print(*arg, sep=sep)

    def _get_prefix(self) -> str:
        """Метод, возвращающий префикс перед приглашением к вводу"""
        return f'{self.current_user}:[{self.file_system.current_path}]#'

    def read_input(self) -> None:
        """Метод для первичной обработки ввода пользователя и
                  автоматического ввода стартового скрипта"""
        print(self._get_prefix(), end="")
        command = input().split()
        self.interpreter.handle_command(*command)

    def run(self) -> None:
        """Метод запуска программы. Выполняет переданный в
                  метод код автоматически"""
        while self.is_running:
            self.read_input()


class Interpreter:
    """Класс для обработки и исполнения команд пользователя"""
    def __init__(self, console: ConsoleHandler) -> None:
        self.console: ConsoleHandler = console

    def handle_command(self, *args: str) -> str:
        """Метод исполнения строки, содержащей команду"""
        if args[0] == "ls":
            self.console.output("ls")
        elif args[0] == "cd":
            self.console.output("cd")
        elif args[0] == "exit":
            self.console.is_running = False
        return "None"


class FileSystem:
    """Класс, реализующий и хранящий виртуальную файловую систему,
          а также методы работы с ней"""
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
        """Возвращает строковое представление дерева файловой системы"""
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
        """Метод для изменения рабочей директории"""
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
