import os, platform
from .term_colors import *

class RGB:
    reset = "\033[0m"
    def print(r, g, b):
        return "\033[38;2;{};{};{}m".format(r, g, b)


class HEX:
    reset = "\033[0m"

    @staticmethod
    def print(hex_value):
        r, g, b = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"


class Clear:
    def sys():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')


class Color:
    def palette():
        for i in range(8):
            print(f"\033[48;5;{i}m   \033[0m", end="")
        print ("")
        for i in range(8, 16):
            print(f"\033[48;5;{i}m   \033[0m", end="")
        print("")
