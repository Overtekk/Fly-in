# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    zone.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: roandrie <roandrie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/06 08:39:51 by roandrie          #+#    #+#              #
#    Updated: 2026/03/06 09:50:20 by roandrie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


class Zone():
    def __init__(self, name: str, x: int, y: int, metadata: str) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.metadata = metadata
