# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  errors.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/24 17:42:28 by roandrie        #+#    #+#               #
#  Updated: 2026/03/10 18:09:22 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from src.utils.ui import Colors


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


class ArgumentError(Exception):
    """
    Invalid Argument provided by the user.
    """
    pass


class MapError(Exception):
    """
    No maps found, error validating map.
    """
    pass

class SpriteError(Exception):
    """
    Sprite not found, or error while loading sprite.
    """
    pass
