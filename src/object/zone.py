# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  zone.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/06 13:43:53 by roandrie        #+#    #+#               #
#  Updated: 2026/03/07 21:03:18 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List

from src.utils.ui import Colors
from src.object.utils.type import ZoneType
from src.object.drones import Drone


class Zone():
    def __init__(self, name: str, x: int, y: int,
                 metadatata: str | None, connection: List[str]) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.connection = connection
        raw_metadatata = metadatata
        # Default value
        self.metadatata_color = "white"
        self.metadata_zone_type = ZoneType.NORMAL
        self.metadata_max_drones = 1
        if raw_metadatata is not None:
            self._write_metadata(raw_metadatata)

        self.drones_on_it: List[Drone] = []

    def is_occuped(self) -> bool:
        if len(self.drones_on_it) <= self.metadata_max_drones:
            return True
        return False

    def get_next_zone(self) -> List[str]:
        return self.connection

    def add_drone(self, drone_id: Drone) -> None:
        self.drones_on_it.append(drone_id)

    def remove_drone(self, drone_id: Drone) -> None:
        self.drones_on_it.remove(drone_id)

    def get_zone_information(self) -> str:
        # Variable to short strings.
        LB = f"{Colors.LIGHT_BLUE}{Colors.BOLD}"
        EB = f"{Colors.END}{Colors.LIGHT_BLUE}"

        zone_info = f"{LB}\n=======Informations======\n\n{Colors.END}"
        zone_info += f"{LB}Zone name:{EB} {self.name}\n{Colors.END}"
        zone_info += f"{LB}Coordinates:{EB} x={self.x} y={self.y}{Colors.END}"
        zone_info += f"\n{LB}metadatata:\n{Colors.END}"
        zone_info += (f"{LB}- Color: {Colors.END}{Colors.LIGHT_BLUE}"
                      f"{self.metadatata_color}\n")
        zone_info += (f"{LB}- Zone Type: {Colors.END}{Colors.LIGHT_BLUE}"
                      f"{self.metadata_zone_type}\n")
        zone_info += (f"{LB}- Max Drones: {Colors.END}{Colors.LIGHT_BLUE}"
                      f"{self.metadata_max_drones}\n\n")
        zone_info += f"{LB}Connection to:{EB} {self.connection}\n{Colors.END}"
        zone_info += f"{LB}Drones on zone:{EB} {self.drones_on_it}{Colors.END}"

        return zone_info

    def _write_metadata(self, raw_metadata: str) -> None:
        """
        Method to split and separate metadas from a complete string to better
        maipulate all datas later on.
        """
        cleaned_metadata = raw_metadata.strip("[").strip("]")
        splitted_metadata = cleaned_metadata.split()

        for data in splitted_metadata:
            key, value = data.split("=")
            match key:
                case "color":
                    self.metadatata_color = value
                case "zone":
                    match value:
                        case "normal":
                            self.metadata_zone_type = ZoneType.NORMAL
                        case "blocked":
                            self.metadata_zone_type = ZoneType.BLOCKED
                        case "priority":
                            self.metadata_zone_type = ZoneType.PRIORITY
                        case "restricted":
                            self.metadata_zone_type = ZoneType.RESTRICTED
                        case _:
                            continue
                case "max_drones":
                    self.metadata_max_drones = int(value)
                case _:
                    continue
