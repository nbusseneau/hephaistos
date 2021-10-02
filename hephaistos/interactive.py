import platform
import subprocess
from typing import Any, Union


CANCEL_OPTION='Cancel'
EXIT_OPTION='Exit'


def pick(prompt: str="Pick an option:", options: Union[dict, list]=None, add_option: str=CANCEL_OPTION, *args, **kwargs) -> Any:
    if not options and kwargs:
        options = kwargs
    if add_option:
        if isinstance(options, dict):
            options[add_option] = add_option
        elif add_option not in options:
            options.append(add_option)
    print(prompt)
    index_key_dict = {index + 1: key for index, key in enumerate(options)}
    for index, key in index_key_dict.items():
        print(f"{index}. {options[key]}") if isinstance(options, dict) else print(f"{index}. {key}")
    print("Choice: ", end='', flush=True)
    char = getch()
    print(char + '\n')
    try:
        option = int(char)
        value = index_key_dict[option]
        if value == CANCEL_OPTION:
            raise InteractiveCancel()
        if value == EXIT_OPTION:
            raise InteractiveExit()
        return index_key_dict[option]
    except (ValueError, KeyError):
        print("Please input a valid number from the given list.")
        return pick(prompt, options, False)


class InteractiveCancel(RuntimeError): ...
class InteractiveExit(RuntimeError): ...


def input_number(prompt: str=None) -> int:
    data = input(prompt)
    try:
        int(data)
        return data
    except ValueError:
        print("Invalid value -- please enter a number.")
        return input_number(prompt)


def any_key(prompt: str="Press any key to continue...") -> None:
    print(prompt, end='', flush=True)
    getch()


def clear() -> None:
    subprocess.run("cls" if platform.system() == 'Windows' else "clear", shell=True)


# Source: https://code.activestate.com/recipes/134892/
# Modifications:
# - Removed unused import in Unix __init__
# - Added filters for arrow keys (224 on Windows, 27/91 on Unix) to avoid multiple keypresses
# - Added .decode() to Windows getch() with default 'a' char return to simplify handling
class _Getch:
    """Gets a single character from standard input. Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self): ...
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return self.__call__() if ord(ch) in [27, 91] else ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        ch = msvcrt.getch()
        if ord(ch) == 224:
            return self.__call__()
        try:
            return ch.decode()
        except UnicodeDecodeError:
            return 'a'


getch = _Getch()
