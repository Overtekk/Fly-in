# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  graphics_settings.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/10 20:01:40 by roandrie        #+#    #+#               #
#  Updated: 2026/03/16 15:58:27 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

PATH = "src/graphics/sprites/"


class WindowSettings():
    WIDTH = 1280
    HEIGHT = 720
    NAME = "Fly-in"


class SpritePath():
    BACKGROUND = f"{PATH}background.png"
    DRONE = f"{PATH}drone.png"
    START_HUB = f"{PATH}start_hub.png"
    END_HUB = f"{PATH}end_hub.png"
    DEFAULT_ZONE = f"{PATH}default_zone.png"
    ZONE_BLOCKED = f"{PATH}zone_blocked.png"
    ZONE_PRIORITY = f"{PATH}zone_priority.png"
    ZONE_RESTRICTED = f"{PATH}zone_restricted.png"


class SpriteSetting():
    ZONE_SCALE = 0.7
    DRONE_SCALE = 0.6
    SPACING = 50
    OFFSET_X = 100
    OFFSET_Y = 100
