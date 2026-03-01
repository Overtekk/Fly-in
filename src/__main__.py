# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/23 18:28:19 by roandrie        #+#    #+#               #
#  Updated: 2026/03/01 18:16:21 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from pathlib import Path

from src.utils.ui import Display
from src.utils.custom_errors import ArgumentError, MapError
from src.utils.module_checker import module_checker


def main() -> int:
    try:
        try:
            module_checker()
        except ModuleNotFoundError as e:
            Display.error(f"{e}")
            return 2

        from src.maps_parser.parser import Maps, MapModel
        from src.maps_parser.menu import print_menu

        if len(sys.argv) > 2:
            raise ArgumentError("Too many arguments. Use 'make run' or 'uv run"
                                " python run.py [map.txt]'")

        elif len(sys.argv) == 2:
            map = MapModel.is_map_valid(Path(sys.argv[1]))

        else:
            maps = Maps()
            print_menu(maps)

    except (ArgumentError, MapError) as e:
        Display.error(f"{e}")
        return 1

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print("")
        Display.error("\nProgram interrupted by user.")
        sys.exit(130)

    # except Exception as e:
    #     Display.error(f"{e}")
    #     sys.exit(1)
