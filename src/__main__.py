# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/23 18:28:19 by roandrie        #+#    #+#               #
#  Updated: 2026/03/19 14:30:50 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import argparse

from pathlib import Path

from src.utils.ui import Display
from src.utils.errors import ArgumentError, MapError
from src.utils.module_checker import module_checker
from src.simulation.manager import Manager


def main() -> int:
    try:
        try:
            module_checker()
        except ModuleNotFoundError as e:
            Display.error(f"{e}")
            return 2

        from src.maps_parser.parser import Maps, MapModel
        from src.maps_parser.menu import print_menu

        parser = argparse.ArgumentParser(
            prog="Fly-in",
            description=("Design an efficient drone routing system that "
                         "navigates multiple drones through connected zones "
                         "while minimizing simulation turns and handling "
                         "movement constraints.")
        )

        parser.add_argument(
            "filepath",
            nargs="?",
            default=None,
            help=("Launch the main program script. You can specify a map to "
                  "use instead of having the whole menu. (Maps are stored in "
                  "the folder 'maps')")
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Launch the program with the debug mode, used to test things."
        )

        args = parser.parse_args()

        if args.filepath is not None:
            map = MapModel.is_map_valid(Path(args.filepath))
        else:
            map_model = Maps()
            map = print_menu(map_model)
            if not isinstance(map, MapModel):
                return 0

            Display.loading(1 * 10)
            print("\n")

        # Launch main simulation
        my_manager = Manager(map, map.connection_map, args)
        my_manager.simulate()

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
