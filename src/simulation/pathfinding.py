# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pathfinding.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 22:15:21 by roandrie        #+#    #+#               #
#  Updated: 2026/03/13 14:36:56 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Dict, List

from src.object.zone import Zone
from src.object.utils.type import ZoneType


class PathFinding():
    def __init__(self, start: str, end: str,
                 connect_map: Dict[str, List[str]],
                 zones: Dict[str, Zone]) -> None:
        self.start = start
        self.end = end
        self.connect_map = connect_map
        self.zones = zones

    def find_shortest_path(self) -> List[str]:
        open

    # def find_shortest_path(self) -> List[str]:
    #     cost = 0
    #     queue = [[self.start]]
    #     visited = [self.start]

    #     while queue:
    #         curr_list = queue.pop(0)
    #         curr_node = curr_list[-1]

    #         if curr_node == self.end:
    #             print(f"{curr_list} {cost}")
    #             break

    #         node = self.connect_map[curr_node]
    #         for zone in node:
    #             if self.zones[zone].metadata_zone_type == ZoneType.BLOCKED:
    #                 pass

    #             # elif self.zones[self.zones].metadata_zone_type == ZoneType.PRIORITY:
    #             #     pass

    #             elif zone not in visited:
    #                 if self.zones[zone].metadata_zone_type == ZoneType.RESTRICTED:
    #                     cost += 2
    #                 else:
    #                     cost += 1
    #                 visited.append(zone)
    #                 copy = curr_list.copy()
    #                 copy.append(zone)
    #                 queue.append(copy)
