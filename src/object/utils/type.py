# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  type.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/06 11:40:10 by roandrie        #+#    #+#               #
#  Updated: 2026/03/06 12:41:57 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum


class ZoneType(str, Enum):
    """
    Defines the zone type for a zone.
    """
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    def __str__(self) -> str:
        """Return the string value of the type of zone."""
        return self.value
