# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    zone.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: roandrie <roandrie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/06 08:39:51 by roandrie          #+#    #+#              #
#    Updated: 2026/03/06 11:44:49 by roandrie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from src.utils.ui import Colors
from src.object.utils.type import ZoneType


class Zone():
    def __init__(self, name: str, x: int, y: int, metadata: str) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.metadata = metadata
        self.metadata_color = Colors.WHITE
        self.metada_zone_type = ZoneType.NORMAL
        self.metada_max_drones = 1

        if self.metadata is not None:
            self.metadata = self.metadata.strip("[").strip("]")
            self.metadata = sorted(self.metadata.split())

            self.metada_color = self.metadata[0]
            self.metada_zone_type = self.metadata[1]
            self.metada_max_drones = self.metadata[2]

    def is_occuped(self) -> bool:
        if self.metadata is None:
            pass

    def get_zone_information(self) -> str:
        # Variable to short strings.
        LB = f"{Colors.LIGHT_BLUE}{Colors.BOLD}"
        EB = f"{Colors.END}{Colors.LIGHT_BLUE}"

        zone_info = f"{LB}\n=======Informations======\n\n{Colors.END}"
        zone_info += f"{LB}Zone name:{EB} {self.name}{Colors.END}"
        zone_info += f"{LB}Coordinates:{EB} x={self.x} y={self.y}{Colors.END}"
        zone_info += f"{LB}Metadata:\n{Colors.END}"
        zone_info += f"{Colors.LIGHT_BLUE}- {self.metada_color}"
        zone_info += f"- {self.metada_zone_type}"
        zone_info += f"- {self.metada_max_drones}"

        return zone_info
