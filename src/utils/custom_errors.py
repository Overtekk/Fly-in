# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  custom_errors.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/24 17:42:28 by roandrie        #+#    #+#               #
#  Updated: 2026/03/07 21:02:58 by roandrie        ###   ########.fr        #
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
