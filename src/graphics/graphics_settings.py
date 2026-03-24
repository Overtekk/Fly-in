# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  graphics_settings.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/10 20:01:40 by roandrie        #+#    #+#               #
#  Updated: 2026/03/24 20:45:17 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

DEFAULT_PATH = "src/graphics/sprites/default/"


class WindowSettings():
    WIDTH = 1280
    HEIGHT = 720
    NAME = "Fly-in"


class SpritePath():
    BACKGROUND = f"{DEFAULT_PATH}background.png"
    WINDOW_INFO = f"{DEFAULT_PATH}window_info.png"
    DRONE = f"{DEFAULT_PATH}drone.png"
    DRONE_ANIM1 = f"{DEFAULT_PATH}drone1.png"
    DRONE_ANIM2 = f"{DEFAULT_PATH}drone2.png"
    DRONE_FINISH = f"{DEFAULT_PATH}drone_finish.png"
    START_HUB = f"{DEFAULT_PATH}start_hub.png"
    END_HUB = f"{DEFAULT_PATH}end_hub.png"
    DEFAULT_ZONE = f"{DEFAULT_PATH}default_zone.png"
    ZONE_BLOCKED = f"{DEFAULT_PATH}zone_blocked.png"
    ZONE_PRIORITY = f"{DEFAULT_PATH}zone_priority.png"
    ZONE_RESTRICTED = f"{DEFAULT_PATH}zone_restricted.png"


class FontPath():
    ASEPRITE = "src/graphics/sprites/font/AsepriteFont.ttf"


class SpriteSetting():
    ZONE_SCALE = 1
    DRONE_SCALE = 0.9
    SPACING = 120
    OFFSET_X = 100.0
    OFFSET_Y = 100.0
    DRONE_SPEED = 100.0
    ANIM_SPEED = 5


class WindowAction():
    CLOSE = "CLOSE"
    MOVE = "MOVE"
