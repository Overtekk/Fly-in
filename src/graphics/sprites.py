# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  sprites.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/16 14:34:19 by roandrie        #+#    #+#               #
#  Updated: 2026/03/19 09:24:50 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, Dict, List, Tuple

import math
import arcade
from arcade.types import PathOrTexture

from src.object.drones import Drone
from src.object.zone import Zone
from src.utils.ui import Colors
from src.graphics.graphics_settings import SpriteSetting


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
    def __init__(self, image_path: PathOrTexture, scale: float,
                 drone_data: Drone, id: int,
                 drone_sprites_anim: List[arcade.Texture]) -> None:
        super().__init__(image_path, scale)

        self.drone_data = drone_data

        self.id = id
        self.location = self.drone_data.get_location()
        self.finish = drone_data.finish

        self.target_x = 0.0
        self.target_y = 0.0
        self.speed = SpriteSetting.DRONE_SPEED
        self.is_moving = False

        self.cur_textures = 0
        self.time_counter = 0
        self.idle_texture = arcade.load_texture(image_path)
        self.finish_texture = drone_sprites_anim[2]
        self.move_textures = drone_sprites_anim

    def on_update(self, delta_time: float) -> None:
        if not self.is_moving:
            return

        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y

        distance = math.hypot(dx, dy)

        movement_in_pixels = self.speed * delta_time

        if distance <= movement_in_pixels:
            self.center_x = self.target_x
            self.center_y = self.target_y
            self.is_moving = False
            self.location = self.drone_data.get_location()

            if not self.finish:
                self.finish = self.drone_data.finish

        else:
            angle = math.atan2(dy, dx)

            velocity_x = math.cos(angle) * (self.speed * delta_time)
            velocity_y = math.sin(angle) * (self.speed * delta_time)

            self.center_x += velocity_x
            self.center_y += velocity_y

    def update_animation(self, delta_time: float,
                         *args: Tuple, **kwargs: Dict[str, Any]):
        if not self.is_moving:
            if self.drone_data.finish:
                self.texture = self.finish_texture
                self.cur_textures = 3
                return

            elif not self.cur_textures == 0:
                self.texture = self.idle_texture
                self.cur_textures = 0

        self.cur_textures = (self.cur_textures + 1) % 2

        self.time_counter += 1
        if self.time_counter > 7 * SpriteSetting.ANIM_SPEED:
            self.texture = self.move_textures[self.cur_textures]
