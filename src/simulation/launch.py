# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  launch.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/06 07:50:25 by roandrie        #+#    #+#               #
#  Updated: 2026/03/06 11:42:10 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import re

from typing import Dict

from src.utils.ui import Colors
from src.maps_parser.parser import MapModel
from src.object.drones import Drone
from src.object.zone import Zone


class Simulation():
    def __init__(self, map_config: MapModel) -> None:
        # Init Raw
        self.cfg = map_config
        self.raw_nb_drones = map_config.nb_drones
        self.raw_start_hub = map_config.start_hub
        self.raw_end_hub = map_config.end_hub
        self.raw_hubs = map_config.hub
        self.raw_connections = map_config.connection

        # Init Object
        self.drones: Dict[int, Drone] = {}
        self.zones: Dict[str, Zone] = {}
        self._create_drones()
        self._create_zone()

        for k, zone in self.zones.items():
            print(zone.get_zone_information())

        self.turns = 0

    def simulate(self) -> None:
        print("=== Starting Simulation ===")

    def get_map_information(self) -> str:
        # Variable to short strings.
        LB = f"{Colors.LIGHT_BLUE}{Colors.BOLD}"
        EB = f"{Colors.END}{Colors.LIGHT_BLUE}"

        map_info = f"{LB}\n=======Informations======\n\n{Colors.END}"
        map_info += (f"{LB}Number of drones:{EB} {self.raw_nb_drones}"
                     f"\n\n{Colors.END}")
        map_info += f"{LB}Start hub:{EB} {self.raw_start_hub}\n{Colors.END}"
        map_info += f"{LB}End hub:{EB} {self.raw_end_hub}\n\n{Colors.END}"
        map_info += f"{LB}List of hubs:\n{Colors.END}"
        for hub in self.raw_hubs:
            map_info += f"{Colors.LIGHT_BLUE}- {hub}\n"
        map_info += f"{LB}\nList of connections:\n{Colors.END}"
        for connection in self.raw_connections:
            map_info += f"{Colors.LIGHT_BLUE}- {connection}\n"
        map_info += f"{Colors.END}"
        return map_info

    def _print_log(self, drone_id: Drone, zone: Zone) -> str:
        return f"{drone_id}-{zone}"

    def _create_drones(self) -> None:
        for i in range(self.raw_nb_drones):
            self.drones[i] = Drone(i)

    def _create_zone(self) -> None:
        value = re.findall(r"\[[^\]]*\]|\S+", self.raw_start_hub)
        self._add_to_zone(value)
        value = re.findall(r"\[[^\]]*\]|\S+", self.raw_end_hub)
        self._add_to_zone(value)
        for hubs in self.raw_hubs:
            value = re.findall(r"\[[^\]]*\]|\S+", hubs)
            self._add_to_zone(value)

    def _add_to_zone(self, value: str | int) -> Zone:
        if len(value) == 4:
            self.zones[value[0]] = Zone(value[0], value[1], value[2], value[3])
        else:
            self.zones[value[0]] = Zone(value[0], value[1], value[2], None)
