# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ui.py                                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/24 16:56:39 by roandrie        #+#    #+#               #
#  Updated: 2026/03/19 14:26:57 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import time

from enum import Enum
from typing import Set

from src.utils.x11_colors import X11_NAMES


class Display():
    @staticmethod
    def error(message: str) -> None:
        """Print an error message to stderr.

        Arguments:
            message (str): message to print.
        """
        prefix = f"{Colors.BOLD}{Colors.RED}Error: {Colors.END}"
        content = f"{Colors.RED}{message}{Colors.END}"
        print(prefix + content, file=sys.stderr)

    @staticmethod
    def loading(wait_time: float) -> None:
        animation = "|/-\\"
        index = 0

        while wait_time >= 0:
            print(animation[index % len(animation)], end="\r")
            index += 1
            time.sleep(0.1)
            wait_time -= 1


class Colors(str, Enum):
    """
    Enumeration of ANSI color codes for terminal text coloring.
    """

    WHITE = "\033[37m"
    RED = "\033[31m"
    BLACK = "\033[30m"
    GREEN = "\033[32m"
    BROWN = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    DARK_GRAY = "\033[30m"
    LIGHT_GRAY = "\033[37m"
    LIGHT_RED = "\033[31m"
    LIGHT_GREEN = "\033[32m"
    LIGHT_BLUE = "\033[34m"
    LIGHT_PURPLE = "\033[35m"
    LIGHT_CYAN = "\033[36m"
    LIGHT_WHITE = "\033[37m"

    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    END = "\033[0m"
    CLEARLINE = "\033[F\033[K"

    @staticmethod
    def get_rgb_code(color_name: str) -> str:
        """
        Transform a CSS color name (ex: 'lime') in ANSI TrueColor. If a color
        does not exist, return white.

        Args:
            color_name (str): name of the color

        Returns:
            str: ANSI color sequence
        """
        name = color_name.lower()
        if name not in X11_NAMES:
            return Colors.WHITE.value

        hex_code = X11_NAMES[name].lstrip('#')

        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)

        return f"\033[38;2;{r};{g};{b}m"

    def get_rgb_color(color_name: str) -> Set[int]:
        """
        Transform a CSS color name (ex: 'lime') in rgb code. If a color
        does not exist, return white.

        Args:
            color_name (str): name of the color

        Returns:
            set: set of rgb code
        """
        name = color_name.lower()
        if name not in X11_NAMES:
            return (255, 255, 255)

        hex_code = X11_NAMES[name].lstrip('#')

        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)

        return (int(r), int(g), int(b))

    def __str__(self) -> str:
        """
        Returns the ANSI escape sequence.

        Returns:
            str: The raw ANSI color code.
        """
        return self.value
