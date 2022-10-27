import platform
import subprocess
from typing import Any, Union


CANCEL_OPTION='Cancel'
EXIT_OPTION='Exit'


def pick(prompt: str="Pick an option:", options: Union[dict, list]=None, recommended_option: str=None, additional_option: str=CANCEL_OPTION) -> Any:
    # transform options list to dict (we allow options to be passed in for comfort but only want to handle dicts in code)
    if isinstance(options, list):
        options = {option: option for option in options}
    # prepend recommended tag to recommended option
    recommended_tag = "[RECOMMENDED]"
    if recommended_option and options[recommended_option] and not options[recommended_option].startswith(recommended_tag):
        options[recommended_option] = f"{recommended_tag} {options[recommended_option]}"
    # add additional option
    if additional_option:
        options[additional_option] = additional_option
    print(prompt)
    index_key_dict = {index + 1: key for index, key in enumerate(options)}
    for index, key in index_key_dict.items():
        print(f"{index}. {options[key]}")
    msg = "Choice: " if not recommended_option else f"Choice (press ENTER to use {recommended_tag}): "
    print(msg, end='', flush=True)
    char = getch()
    print(char + '\n')
    # if user pressed enter and a recommended option was set, use it
    if char == '\r' and recommended_option:
        return recommended_option
    try:
        option = int(char)
        value = index_key_dict[option]
        if value == CANCEL_OPTION:
            raise InteractiveCancel()
        if value == EXIT_OPTION:
            raise InteractiveExit()
        return index_key_dict[option]
    except (ValueError, KeyError):
        msg = "Please input a valid number from the given list"
        msg += f", or press ENTER to use to use the {recommended_tag} option." if recommended_option else "."
        print(f"{msg}\n")
        return pick(prompt=prompt, options=options, recommended_option=recommended_option, additional_option=None)


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


CLEAR_WINDOWS = "cls"
CLEAR_MACOS_LINUX = "clear"
CLEAR = CLEAR_WINDOWS if platform.system() == 'Windows' else CLEAR_MACOS_LINUX


def clear() -> None:
    subprocess.run(CLEAR, shell=True)


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
