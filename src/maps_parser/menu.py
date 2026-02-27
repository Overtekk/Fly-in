# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  menu.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/24 18:48:26 by roandrie        #+#    #+#               #
#  Updated: 2026/02/27 10:46:19 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import re
import os

from time import sleep

from src.utils.ui import COLORS
from src.maps_parser.parser import Maps


def print_menu(maps: Maps) -> str | int:
    WIDTH = 40
    order = ["easy", "medium", "hard", "other", "custom", "challenger"]

    available_categories = list(maps.maps_dict.keys())

    def custom_sort(name: str) -> int:
        """Utilitary function to sort maps categories based on a order.

        Args:
            name (str): the item to sort.

        Returns:
            int: index of the sorted item.
        """
        name_lower = name.lower()
        if name_lower in order:
            return order.index(name_lower)
        return len(order)

    available_categories.sort(key=custom_sort)

    category = {i: name for i, name in enumerate(available_categories, 1)}

    def get_title() -> str:
        """Get the project's title of the project.

        Returns:
            str: the title project.
        """
        return f"{COLORS.LIGHT_CYAN}{COLORS.BOLD}Fly-in{COLORS.END}"

    def get_subtitle() -> str:
        """Short string to explain to the user how to select map.

        Returns:
            str: the string with the explanation.
        """
        return f"{COLORS.BLUE}Choose your map using the numpad{COLORS.END}"

    def center(text: str, width: int) -> str:
        """Center a text based on a with.

        Args:
            text (str): the text to center.
            width (int): the width to calculate.

        Returns:
            str: string centered with spaces.
        """
        visible_text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        visible_len = len(visible_text)

        padding = ((width + 2) - visible_len) // 2

        return " " * padding + text

    def print_header() -> None:
        """
        Print the header of the project containing the title and the
        subtitle and clear the terminal screen.
        """
        os.system("clear")
        print("")
        print(f"{COLORS.LIGHT_WHITE}┏" + "━" * WIDTH + f"┓{COLORS.END}")
        print(center(get_title(), WIDTH))
        print("")
        print(center(get_subtitle(), WIDTH))
        print(f"{COLORS.LIGHT_WHITE}┗" + "━" * (WIDTH) + f"┛{COLORS.END}")
        print("")

    def print_error_input() -> None:
        """
        Print an error if the user input is incorrect and clear the line.
        """
        print(f"{COLORS.CLEARLINE}{COLORS.RED}❌ERROR{COLORS.END}",
              end="", flush=True)
        sleep(0.6)
        print("\r\033[K\033[A", end="")

    curr_category = None

    while True:
        user_input = None
        choice = None
        print_header()

        # Show category menu
        if curr_category is None:
            for i, name in category.items():
                print(f"{COLORS.BOLD}{COLORS.LIGHT_BLUE}{i}: {name.title()}"
                      f"{COLORS.END}")

            if maps.invalid_maps_dict:
                print(f"\n{COLORS.BOLD}{COLORS.LIGHT_BLUE}{len(category) + 1}"
                    f": Invalid maps{COLORS.END}")

            print(f"\n{COLORS.BOLD}{COLORS.LIGHT_WHITE}0: Leave{COLORS.END}")

            while True:
                user_input = input(f"\n{COLORS.ITALIC}Choice: {COLORS.END}")
                try:
                    choice = int(user_input)
                    if 0 <= choice <= len(category) + 1:
                        break
                    else:
                        raise ValueError

                except ValueError:
                    print_error_input()

            if choice == 0:
                print(f"{COLORS.GREEN}\n👋 Bye!{COLORS.END}")
                return 0
            if choice == len(category) + 1:
                curr_category = "invalid"
            else:
                curr_category = category[choice]

        # Show invalid maps
        elif curr_category == "invalid":
            maps_list = [map for list in maps.invalid_maps_dict.values()
                         for map in list]

            for i, (name, error) in enumerate(maps_list, 1):
                print(f"{COLORS.BOLD}{COLORS.LIGHT_BLUE}{i}: {COLORS.ITALIC}"
                      f"{name}{COLORS.END}")

            print(f"\n{COLORS.BOLD}{COLORS.LIGHT_WHITE}0: Back{COLORS.END}")

            while True:
                user_input = input(f"\n{COLORS.ITALIC}Choice: {COLORS.END}")
                try:
                    choice = int(user_input)
                    if 0 <= choice <= len(maps_list):
                        break
                    else:
                        raise ValueError

                except ValueError:
                    print_error_input()

            if choice == 0:
                curr_category = None
            else:
                selected_map = maps_list[choice - 1]
                print(f"\n{COLORS.RED}{COLORS.BOLD}Error in '{selected_map[0]}'"
                      f":\n{COLORS.ITALIC}{selected_map[1]}{COLORS.END}")
                input("\nPress Enter to continue...")
                curr_category = "invalid"

        # Show maps menu
        else:
            maps_list = maps.maps_dict[curr_category]
            maps_selection = {i: name for i, name in enumerate(maps_list, 1)}

            if len(maps_selection) == 0:
                print(f"{COLORS.BOLD}{COLORS.LIGHT_BLUE}No map in this folder."
                      f" Maybe an error?{COLORS.END}")
            else:
                for i, name in maps_selection.items():
                    print(f"{COLORS.BOLD}{COLORS.LIGHT_BLUE}{i}: "
                          f"{COLORS.ITALIC}{name}{COLORS.END}")

            print(f"\n{COLORS.BOLD}{COLORS.LIGHT_WHITE}0: Back{COLORS.END}")

            while True:
                user_input = input(f"\n{COLORS.ITALIC}Choice: {COLORS.END}")
                try:
                    choice = int(user_input)
                    if 0 <= choice <= len(maps_selection):
                        break
                    else:
                        raise ValueError

                except ValueError:
                    print_error_input()

            if choice == 0:
                curr_category = None
            else:
                print(f"\n{COLORS.YELLOW}Selected map: {COLORS.GREEN}"
                      f"{maps_selection[choice]}{COLORS.END}")
                return maps_selection[choice]

        print_header()
