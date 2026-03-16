# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pathfinding.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 22:15:21 by roandrie        #+#    #+#               #
#  Updated: 2026/03/16 11:41:46 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import math
import heapq

from typing import Dict, List

from src.object.zone import Zone
from src.object.utils.type import ZoneType


class PathFinding():
    def __init__(self, connect_map: Dict[str, List[str]],
                 zones: Dict[str, Zone]) -> None:
        self.connect_map = connect_map
        self.zones = zones

    def find_path(self, start: str, goal: str) -> List[str]:
        start_node = self._create_node(start, 0,
                                       self._calculate_heuristic(start, goal))

        open_list = [(start_node["sum"], start)]  # Priority queue
        open_dict = {start: start_node}           # Quickly node lookup
        closed_set = set()                        # Explorer for nodes

        while open_list:
            # Get zone with lowest sum value
            _, current_pos = heapq.heappop(open_list)
            current_node = open_dict[current_pos]

            # End the loop if the position is the end
            if current_pos == goal:
                return self._reconstruct_path(current_node)

            # Mark the position as visited
            closed_set.add(current_pos)

            # Explore neighbors and cost
            for (neighbor, cost) in self._get_valid_neighbors(current_pos).items():
                # Skip if already explored
                if neighbor in closed_set:
                    continue

                zone_cost = cost
                neighbor_cost = (current_node["cost"] + zone_cost)

                if neighbor not in open_dict:
                    node = self._create_node(
                        neighbor, neighbor_cost,
                        self._calculate_heuristic(neighbor, goal),
                        current_node)
                    heapq.heappush(open_list, (node["sum"], neighbor))
                    open_dict[neighbor] = node

                elif neighbor_cost < open_dict[neighbor]["cost"]:
                    node = open_dict[neighbor]
                    neighbor["cost"] = node
                    neighbor["sum"] = neighbor_cost + neighbor["estimate_cost"]
                    neighbor["parent"] = current_node

        return []

    def _create_node(self, position: str, cost: float = float('inf'),
                     estimate_cost: float = 0.0,
                     parent: Dict = None) -> Dict[str, str | float | Dict]:
        return {
            "position": position,
            "cost": cost,
            "estimate_cost": estimate_cost,
            "sum": cost + estimate_cost,
            "parent": parent
        }

    def _calculate_heuristic(self, zone1: str, zone2: str) -> float:
        x1, y1 = self.zones[zone1].x, self.zones[zone1].y
        x2, y2 = self.zones[zone2].x, self.zones[zone2].y
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def _get_valid_neighbors(self, position: str) -> Dict[str, int]:
        valid_neighbors = {}

        for neighbor in self.connect_map[position]:
            if self.zones[neighbor].metadata_zone_type == ZoneType.BLOCKED:
                pass
            elif (self.zones[neighbor].metadata_zone_type ==
                  ZoneType.RESTRICTED):
                valid_neighbors[neighbor] = 2
            elif self.zones[neighbor].metadata_zone_type == ZoneType.PRIORITY:
                valid_neighbors[neighbor] = 1
            else:
                valid_neighbors[neighbor] = 1
        return valid_neighbors

    def _reconstruct_path(self, goal_node: Dict) -> List[str]:
        path = []
        current = goal_node

        while current is not None:
            path.append(current["position"])
            current = current["parent"]

        return path[::-1]
