# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  drones.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/05 15:11:21 by roandrie        #+#    #+#               #
#  Updated: 2026/03/19 09:12:59 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING

from src.utils.ui import Colors

if TYPE_CHECKING:
    from src.object.zone import Zone


class Drone():
    def __init__(self, id: int) -> None:
        self.id = f"D{id}"
        self.current_location = None

        self.finish = False

    def update_location(self, zone: 'Zone') -> None:
        self.current_location = zone.name

        if zone.is_end:
            self.finish = True

    def get_location(self) -> str:
        return self.current_location

    def __repr__(self) -> str:
        """Return the ID of the Drone instead of it's memory adress.

        Returns:
            str: ID of the drone.
        """
        return f"Drone(id={self.id})"

    def get_drone_information(self) -> str:
        # Variable to short strings.
        LB = f"{Colors.LIGHT_BLUE}{Colors.BOLD}"
        EB = f"{Colors.END}{Colors.LIGHT_BLUE}"

        drone_info = f"{LB}\n=======Informations======\n\n{Colors.END}"
        drone_info += f"{LB}Drone ID:{EB} {self.id}\n{Colors.END}"
        drone_info += (f"{LB}Drone location:{EB} {self.current_location}"
                       f"{Colors.END}")

        return drone_info
