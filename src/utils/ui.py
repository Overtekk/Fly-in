# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ui.py                                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/24 16:56:39 by roandrie        #+#    #+#               #
#  Updated: 2026/03/02 15:48:41 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from enum import Enum

from src.utils.css3_colors import CSS3_NAMES


class Display():
    @staticmethod
    def error(message: str) -> None:
        """Print an error message to stderr.

        Arguments:
            message (str): message to print.
        """
        prefix = f"{COLORS.BOLD}{COLORS.RED}Error: {COLORS.END}"
        content = f"{COLORS.RED}{message}{COLORS.END}"
        print(prefix + content, file=sys.stderr)


class COLORS(str, Enum):
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
        if name not in CSS3_NAMES:
            return COLORS.WHITE.value

        hex_code = CSS3_NAMES[name].lstrip('#')

        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)

        return f"\033[38;2;{r};{g};{b}m"

    def __str__(self) -> str:
        """
        Returns the ANSI escape sequence.

        Returns:
            str: The raw ANSI color code.
        """
        return self.value
