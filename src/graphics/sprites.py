# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  sprites.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/16 14:34:19 by roandrie        #+#    #+#               #
#  Updated: 2026/03/18 11:26:21 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
from arcade.types import PathOrTexture

from src.object.zone import Zone
from src.utils.ui import Colors


class ZoneSprite(arcade.Sprite):
    def __init__(self, image_path: PathOrTexture,
                 scale: float, zone_data: Zone) -> None:
        super().__init__(image_path, scale)

        self.zone_data = zone_data

        zone_name = self.zone_data.name
        if len(self.zone_data.name) > 12:
            zone_name = self.zone_data.name[:12]
            zone_name += "..."

        self.label_name_text = arcade.Text(
            text=zone_name, bold=True, italic=True,
            x=0, y=0, anchor_x="center", anchor_y="top",
            color=Colors.get_rgb_color(self.zone_data.metadata_color),
            font_name="arial", font_size=8
            )

        nb_drones = len(self.zone_data.drones_on_it)
        max_drones = self.zone_data.metadata_max_drones
        if self.zone_data.is_start:
            text_drone = f"{nb_drones}"
        elif self.zone_data.is_end:
            text_drone = f"{nb_drones}"
        else:
            text_drone = f"{nb_drones}/{max_drones}"

        self.label_count_text = arcade.Text(
            text=text_drone, bold=True, italic=False,
            x=0, y=0, anchor_x="left", anchor_y="baseline",
            color=arcade.color.FLORAL_WHITE,
            font_name="arial", font_size=8
        )


class DroneSprite(arcade.Sprite):
    pass
