# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  custom_errors.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/24 17:42:28 by roandrie        #+#    #+#               #
#  Updated: 2026/02/25 17:58:35 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

class ArgumentError(Exception):
    """
    Invalid Argument provided by the user.
    """
    pass


class MapError(Exception):
    """
    No maps found, error validating map.
    """
    pass
