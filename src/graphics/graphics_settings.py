# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  graphics_settings.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/10 20:01:40 by roandrie        #+#    #+#               #
#  Updated: 2026/03/13 11:34:00 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pygame import font

PATH = "src/graphics/sprites/"


class ScreenSettings:
    FPS = 60
    WIDTH = 1280
    HEIGHT = 720
    NAME = "Fly-in"
    OFFSET = 100


class FontSettings:
    SIZE = 20

    font.init()
    try:
        FONT = font.Font(f"{PATH}whitrabt.ttf", SIZE, True)
    except Exception:
        FONT = font.SysFont("dejavuserif", SIZE, True)
