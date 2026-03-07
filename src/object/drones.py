# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  drones.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/05 15:11:21 by roandrie        #+#    #+#               #
#  Updated: 2026/03/07 16:53:40 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.utils.ui import Colors


class Drone():
    def __init__(self, id: int) -> None:
        self.id = f"D{id}"
        self.current_location = None

    def update_location(self, zone: str) -> None:
        self.current_location = zone

    def get_location(self) -> str:
        return self.current_location

    def __repr__(self) -> str:
        return self.id

    def get_drone_information(self) -> str:
        # Variable to short strings.
        LB = f"{Colors.LIGHT_BLUE}{Colors.BOLD}"
        EB = f"{Colors.END}{Colors.LIGHT_BLUE}"

        drone_info = f"{LB}\n=======Informations======\n\n{Colors.END}"
        drone_info += f"{LB}Drone ID:{EB} {self.id}\n{Colors.END}"
        drone_info += (f"{LB}Drone location:{EB} {self.current_location}"
                       f"{Colors.END}")

        return drone_info
