# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pathfinding.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 22:15:21 by roandrie        #+#    #+#               #
#  Updated: 2026/03/07 22:25:38 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Dict

from src.object.zone import Zone


class PathFinding():
    def __init__(self, start: str, end: str,
                 connect_map: Dict[str, Zone]) -> None:
        self.start = start
        self.end = end
        self.connect_map = connect_map
