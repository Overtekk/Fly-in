# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  icon_sprite.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 08:30:37 by roandrie        #+#    #+#               #
#  Updated: 2026/03/27 09:26:09 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from arcade.types import PathOrTexture
from src.graphics.graphics_settings import FontSettings


class Icon(arcade.Sprite):
    def __init__(self, image_path: PathOrTexture, scale: float,
                 legend: str) -> None:
        super().__init__(image_path, scale)

        self.label_legend = arcade.Text(
            text=legend, x=0, y=0, anchor_x="left", anchor_y="center",
            color=arcade.color.WHITE_SMOKE, font_size=12,
            font_name=FontSettings.PIXELOGIST_NAME
        )

    def draw_text(self) -> None:
        self.label_legend.draw()
