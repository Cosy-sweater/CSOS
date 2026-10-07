if __name__ == "__main__":
    from main import ConsoleHandler


def _ls(c: "ConsoleHandler", args: list[str]):
    """Функция вывода директорий и файлов"""
    c.output(*c.file_system.get_tree(), sep="\n")


def _cd(c: "ConsoleHandler", args: list[str]):
    """Функция для изменения рабочей директории"""
    if args:
        t = c.file_system.goto(args[0])
        if t:
            c.output(t)
    else:
        c.output("cd requires an argument")


def _exit(c: "ConsoleHandler", args: list[str]):
    """Функция завершения работы"""
    if args:
        c.output("This command does not take any arguments")
    c.is_running = False


commands = {
    "ls": _ls,
    "cd": _cd,
    "exit": _exit,
}
