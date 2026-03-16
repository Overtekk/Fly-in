# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  type.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/06 11:40:10 by roandrie        #+#    #+#               #
#  Updated: 2026/03/16 08:00:43 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum


class ZoneType(str, Enum):
    """
    Defines the zone type for a zone.

    Normal = Standard zone with 1 turn movement cost.
    Blocked = Inaccessible zone.
    Restricted = Movement to this zone costs 2 turns.
    Priority = 1 turn movement cost but must be prioritized in pathfinding.
    """
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    def __str__(self) -> str:
        """Return the string value of the type of zone."""
        return self.value
