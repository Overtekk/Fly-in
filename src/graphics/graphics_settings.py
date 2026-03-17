# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  graphics_settings.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/10 20:01:40 by roandrie        #+#    #+#               #
#  Updated: 2026/03/17 19:21:55 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

PATH = "src/graphics/sprites/default/"


class WindowSettings():
    WIDTH = 1280
    HEIGHT = 720
    NAME = "Fly-in"


class SpritePath():
    BACKGROUND = f"{PATH}background.png"
    DRONE = f"{PATH}drone.png"
    DRONE1 = f"{PATH}drone1.png"
    DRONE2 = f"{PATH}drone2.png"
    DRONE_FINISH = f"{PATH}drone_finish.png"
    START_HUB = f"{PATH}start_hub.png"
    END_HUB = f"{PATH}end_hub.png"
    DEFAULT_ZONE = f"{PATH}default_zone.png"
    ZONE_BLOCKED = f"{PATH}zone_blocked.png"
    ZONE_PRIORITY = f"{PATH}zone_priority.png"
    ZONE_RESTRICTED = f"{PATH}zone_restricted.png"


class SpriteSetting():
    ZONE_SCALE = 0.9
    DRONE_SCALE = 0.6
    SPACING = 120
    OFFSET_X = 100
    OFFSET_Y = 100
