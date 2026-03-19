# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pathfinding.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 22:15:21 by roandrie        #+#    #+#               #
#  Updated: 2026/03/19 15:05:30 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

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
        goal_node = self._create_node(
            position=goal,
            cost=0
            )

        open_list = [(goal_node["cost"], goal)]  # Priority queue
        open_dict = {goal: goal_node}            # Quickly node lookup
        closed_set = set()                       # Explorer for nodes

        while open_list:
            # Get zone with lowest value
            _, current_pos = heapq.heappop(open_list)
            if current_pos in closed_set:
                continue

            current_node = open_dict[current_pos]

            # End the loop if the position is the end
            # if current_pos == start_node:
            #     return self._reconstruct_path(current_node)

            # Mark the position as visited
            closed_set.add(current_pos)
            self._calculte_weight(
                current_pos,
                open_dict[current_pos]["cost"]
                )

            # Explore neighbors
            for (neighbor, cost) in self._get_valid_neighbors(
                    current_pos).items():
                # Skip if already explored
                if neighbor in closed_set:
                    continue

                neighbor_cost = (current_node["cost"] + cost)

                # Create or update neighbor
                if neighbor not in open_dict:
                    node = self._create_node(
                        position=neighbor,
                        cost=neighbor_cost,
                        parent=current_node)

                    heapq.heappush(open_list, (node["cost"], neighbor))
                    open_dict[neighbor] = node

                # Better path to the neighbor
                elif neighbor_cost < open_dict[neighbor]["cost"]:
                    node = open_dict[neighbor]
                    node["cost"] = neighbor_cost
                    node["parent"] = current_node
                    heapq.heappush(open_list, (node["cost"], neighbor))

        return []

    def _create_node(self, position: str, cost: float = float('inf'),
                     parent: Dict = None) -> Dict[str, str | float | Dict]:
        return {
            "position": position,
            "cost": cost,
            "parent": parent
        }

    def _get_valid_neighbors(self, position: str) -> Dict[str, int]:
        valid_neighbors = {}

        for neighbor in self.connect_map[position]:

            match self.zones[neighbor].metadata_zone_type:
                case ZoneType.BLOCKED:
                    pass
                case ZoneType.RESTRICTED:
                    valid_neighbors[neighbor] = 2
                case ZoneType.PRIORITY:
                    valid_neighbors[neighbor] = 0.99
                case ZoneType.NORMAL:
                    valid_neighbors[neighbor] = 1

        return valid_neighbors

    def _calculte_weight(self, position: str, cost: int) -> None:
        self.zones[position].weight = cost

    # def _reconstruct_path(self, goal_node: Dict) -> List[str]:
    #     path = []
    #     current = goal_node

    #     while current is not None:
    #         path.append(current["position"])
    #         current = current["parent"]

    #     return path[::-1]
