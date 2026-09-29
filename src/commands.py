import typing

from vfs_components import *

if __name__ == "__main__":
    from main import ConsoleHandler


def _ls(c: "ConsoleHandler", tokens: dict[str, str]):
    if tokens.get("args"):
        start_dir = c.file_system.get_dir(tokens["args"][0])
    else:
        start_dir = c.file_system.tree

    slashes = "-p" in tokens.keys()

    def scan_dir(dir: Dir, depth=-1):
        res = ["---" * depth + " " * (depth > 0) + dir.name + ("/" if slashes else "")]
        for i in dir.children:
            if type(i) is File:
                res.append("---" * (depth + 1) + " " * (depth > 0) + i.name)
            else:
                res += scan_dir(i, depth + 1)
        return res

    if "-R" in tokens.keys():
        c.output(*scan_dir(start_dir)[1:], sep="\n")
    else:
        # c.output(start_dir.name + ("/" if slashes else ""))
        for i in start_dir.children:
            c.output(i.name + ("/" if type(i) is Dir and slashes else ""))


def _cd(c: "ConsoleHandler", tokens):
    if tokens["args"]:
        t = c.file_system.goto(tokens["args"][0])
        if t:
            c.output(t)
    else:
        c.output("cd requires an argument")


def _exit(c: "ConsoleHandler", args: list[str]):
    if args:
        c.output("This command does not take any arguments")
    c.is_running = False


commands = {
    "ls": _ls,
    "cd": _cd,
    "exit": _exit,
}
