# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  manager.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/06 07:50:25 by roandrie        #+#    #+#               #
#  Updated: 2026/03/18 12:01:13 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import re
import arcade

from typing import Dict, List

from src.utils.ui import Colors, Display
from src.maps_parser.parser import MapModel
from src.object.drones import Drone
from src.object.zone import Zone
from src.simulation.pathfinding import PathFinding
from src.graphics.renderer import Renderer


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
        self.connection_map = connection_map

        self.turns = 0

        # Init Object
        self.drones: Dict[int, Drone] = {}
        self.zones: Dict[str, Zone] = {}
        self.start_name = None
        self.end_name = None
        self._create_drones()
        self._create_zone(self.connection_map)

    def simulate(self) -> None:
        print("=== Starting Simulation ===")
        self._add_drones_to_spawn()
        #path = PathFinding(self.connection_map, self.zones)
        #tmp = path.find_path(self.start_name, self.end_name)
        #print(tmp)
        self._init_renderer()

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

    def _init_renderer(self) -> None:
        try:
            Renderer(self.zones, self, self.drones, self.connection_map)
            arcade.run()
        except (OSError, FileNotFoundError) as e:
            Display.error(e)
            arcade.exit()
            return 1
        # except Exception as e:
        #     Display.error(e)
        #     arcade.exit()
        #     return 1

    def _print_log(self, drone_id: Drone, zone: Zone) -> str:
        return f"{drone_id}-{zone}"

    def _create_drones(self) -> None:
        for i in range(1, self.raw_nb_drones + 1):
            self.drones[i] = Drone(i)

    def _create_zone(self, connection_map: Dict[str, List[str]]) -> None:
        # Start
        value = re.findall(r"\[[^\]]*\]|\S+", self.raw_start_hub)
        self.start_name = value[0]
        self._add_to_zone(value, connection_map.get(value[0], []), "start")

        # End
        value = re.findall(r"\[[^\]]*\]|\S+", self.raw_end_hub)
        self.end_name = value[0]
        self._add_to_zone(value, connection_map.get(value[0], []), "end")

        # Hubs
        for hubs in self.raw_hubs:
            value = re.findall(r"\[[^\]]*\]|\S+", hubs)
            self._add_to_zone(value, connection_map.get(value[0], []), "hub")

    def _add_to_zone(self, value: List[str], connection: List[str],
                     type: str) -> None:
        if type not in ["start", "end"]:
            type = None
        if len(value) == 4:
            self.zones[value[0]] = Zone(value[0], int(value[1]), int(value[2]),
                                        value[3], connection, type)
        else:
            self.zones[value[0]] = Zone(value[0], int(value[1]), int(value[2]),
                                        None, connection, type)

    def _add_drones_to_spawn(self) -> None:
        for drone in self.drones.values():
            self.zones[self.start_name].add_drone(drone)
            drone.update_location(self.start_name)

    def _debug_get_data(self) -> None:
        for zone in self.zones.values():
            print(zone.get_zone_information())
        for drone in self.drones.values():
            print(drone.get_drone_information())

    def _debug_simulate_one_step(self) -> None:
        pos = self.drones[1].get_location()
        next_zone = self.connection_map[pos][0]
        self.drones[1].update_location(next_zone)
        self.zones[pos].remove_drone(self.drones[1])
        self.zones[next_zone].add_drone(self.drones[1])
