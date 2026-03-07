# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  manager.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/06 07:50:25 by roandrie        #+#    #+#               #
#  Updated: 2026/03/07 21:02:27 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import re

from typing import Dict, List

from src.utils.ui import Colors
from src.maps_parser.parser import MapModel
from src.object.drones import Drone
from src.object.zone import Zone


class Manager():
    def __init__(self, map_config: MapModel,
                 connection_map: Dict[str, List[str]]) -> None:
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
        self.start_name = None
        self.end_name = None
        self._create_drones()
        self._create_zone(connection_map)

        self.turns = 0

    def simulate(self) -> None:
        print("=== Starting Simulation ===")
        self._add_drones_to_spawn()
        self._debug_get_data()
        for drone in self.drones.values():
            loc = drone.get_location()
            next_zones = self.zones[loc].get_next_zone
            print(next_zones)

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
        for i in range(1, self.raw_nb_drones + 1):
            self.drones[i] = Drone(i)

    def _create_zone(self, connection_map: Dict[str, List[str]]) -> None:
        value = re.findall(r"\[[^\]]*\]|\S+", self.raw_start_hub)
        self.start_name = value[0]
        self._add_to_zone(value, connection_map[value[0]])
        value = re.findall(r"\[[^\]]*\]|\S+", self.raw_end_hub)
        self.end_name = value[0]
        self._add_to_zone(value, connection_map[value[0]])
        for hubs in self.raw_hubs:
            value = re.findall(r"\[[^\]]*\]|\S+", hubs)
            self._add_to_zone(value, connection_map[value[0]])

    def _add_to_zone(self, value: List[str], connection: List[str]) -> None:
        if len(value) == 4:
            self.zones[value[0]] = Zone(value[0], int(value[1]), int(value[2]),
                                        value[3], connection)
        else:
            self.zones[value[0]] = Zone(value[0], int(value[1]), int(value[2]),
                                        None, connection)

    def _add_drones_to_spawn(self) -> None:
        for drone in self.drones.values():
            self.zones[self.start_name].add_drone(drone)
            drone.update_location(self.start_name)

    def _debug_get_data(self) -> None:
        for zone in self.zones.values():
            print(zone.get_zone_information())
        for drone in self.drones.values():
            print(drone.get_drone_information())
