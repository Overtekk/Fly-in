# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  type.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/06 11:40:10 by roandrie        #+#    #+#               #
#  Updated: 2026/03/06 11:44:29 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
