# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  sprites.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/16 14:34:19 by roandrie        #+#    #+#               #
#  Updated: 2026/03/24 21:33:46 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING, Any, Dict, List, Optional

import math
import arcade
from arcade.types import PathOrTexture

from src.object.drones import Drone
from src.object.zone import Zone
from src.utils.ui import Colors
from src.graphics.graphics_settings import (SpriteSetting, WindowAction)


if TYPE_CHECKING:
    from src.simulation.manager import Manager


class ZoneSprite(arcade.Sprite):
    def __init__(self, image_path: PathOrTexture,
                 scale: float, zone_data: Zone, manager: 'Manager') -> None:
        super().__init__(image_path, scale)

        self.zone_data = zone_data
        self.max_drones = self.zone_data.metadata_max_drones
        self.manager = manager

        # Override zone name if it's too long
        self.zone_name = self.zone_data.name
        if len(self.zone_data.name) > 12:
            self.zone_name = self.zone_data.name[:12]
            self.zone_name += "..."

        # Write zone name
        self.label_name_text = arcade.Text(
            text=self.zone_name, bold=True, italic=True,
            x=0, y=0, anchor_x="center", anchor_y="top",
            color=Colors.get_rgb_color(self.zone_data.metadata_color),
            font_name="arial", font_size=10
            )

        # Write drones count
        self.label_count_text = arcade.Text(
            text="", bold=True, italic=False,
            x=0, y=0, anchor_x="left", anchor_y="baseline",
            color=arcade.color.FLORAL_WHITE,
            font_name="arial", font_size=13
        )

        # Write zone weight (for debug mode)
        if self.manager.args.debug:
            weight = str(self.zone_data.weight)

            if len(weight) > 8:
                weight = weight[:8]

            self.label_weight_text = arcade.Text(
                text=f"{weight}", bold=True, italic=False,
                x=0, y=0, anchor_x="center", anchor_y="center",
                color=arcade.color.WHITE_SMOKE,
                font_name="arial", font_size=18
            )

    def update_drone_count(self) -> None:
        nb_drones = len(self.zone_data.drones_on_it)

        if self.zone_data.is_start:
            text_drone = f"{nb_drones}"
        elif self.zone_data.is_end:
            text_drone = f"{nb_drones}"
        else:
            text_drone = f"{nb_drones}/{self.max_drones}"

        self.label_count_text.text = text_drone

    def draw_ui(self) -> None:

        text_width = self.label_name_text.content_width
        text_height = self.label_name_text.content_height
        text_x = self.label_name_text.x
        text_y = self.label_name_text.y

        arcade.draw.draw_lbwh_rectangle_filled(
            text_x - (text_width / 2) - 1, text_y - text_height - 2.5,
            text_width + 3, text_height + 0.6,
            (0, 0, 0, 190)
            )

        self.label_name_text.draw()
        self.label_count_text.draw()

        if self.manager.args.debug:
            self.label_weight_text.draw()


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
        self.is_moving = False

        self.cur_textures = 0
        self.time_counter = 0.0
        self.idle_texture = self.texture
        self.finish_texture = drone_sprites_anim[2]
        self.move_textures = drone_sprites_anim

    def on_update(self, delta_time: float) -> None:
        if not self.is_moving:
            return

        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y

        distance = math.hypot(dx, dy)

        movement_in_pixels = SpriteSetting.DRONE_SPEED * delta_time

        if distance <= movement_in_pixels:
            self.center_x = self.target_x
            self.center_y = self.target_y
            self.is_moving = False
            self.location = self.drone_data.get_location()

            if not self.finish:
                self.finish = self.drone_data.finish

        else:
            angle = math.atan2(dy, dx)

            velocity_x = math.cos(angle) * (SpriteSetting.DRONE_SPEED
                                            * delta_time)
            velocity_y = math.sin(angle) * (SpriteSetting.DRONE_SPEED
                                            * delta_time)

            self.center_x += velocity_x
            self.center_y += velocity_y

    def update_animation(self, delta_time: float = 1 / 60,
                         *args: Any, **kwargs: Any) -> None:
        if not self.is_moving:
            if self.drone_data.finish:
                self.texture = self.finish_texture
            else:
                self.texture = self.idle_texture

            self.scale = SpriteSetting.DRONE_SCALE
            self.cur_textures = 0
            return

        self.time_counter += delta_time
        self.scale = SpriteSetting.DRONE_SCALE - 0.2

        if self.time_counter > (0.1 / SpriteSetting.ANIM_SPEED):
            self.cur_textures = (self.cur_textures + 1) % 2
            self.texture = self.move_textures[self.cur_textures]

            self.time_counter = 0.0


class WindowInfo(arcade.Sprite):
    def __init__(self, image_path: PathOrTexture,
                 scale: float, manager: 'Manager'):
        super().__init__(image_path, scale)

        self.manager = manager

        self.buttons_data = {
            WindowAction.CLOSE: {
                "anchor": "TOP_RIGHT",
                "offset": (-11, 0),
                "size": (10, 10)
            },
            WindowAction.MOVE: {
                "anchor": "TOP_LEFT",
                "offset": (0, 0),
                "size": (162, 11.5)
            }
        }

        speed = SpriteSetting.DRONE_SPEED
        self.speed_text0 = arcade.Text(
            text=f"{str(speed)}%", x=0, y=0, anchor_x="center",
            color=(56, 56, 56, 255), font_size=16, font_name="Aseprite",
            bold=True
        )
        self.speed_text = arcade.Text(
            text=f"{str(speed)}%", x=0, y=0, anchor_x="center",
            color=(0, 0, 0, 255), font_size=16, font_name="Aseprite",
            bold=True
        )

    def get_ui_action(self, mouse_x: float, mouse_y: float) -> Optional[str]:
        for action, data in self.buttons_data.items():
            hitbox = self._calculate_hitbox(data)

            # Check if mouse is in the box
            if hitbox["left"] <= mouse_x <= hitbox["right"]:
                if hitbox["bottom"] <= mouse_y <= hitbox["top"]:
                    return action

        return None

    def draw_ui(self) -> None:
        self.speed_text0.draw()
        self.speed_text.draw()

    def update_ui_position(self) -> None:
        self.speed_text0.x = self.center_x - 75
        self.speed_text0.y = self.top - 168
        self.speed_text.x = self.center_x - 76
        self.speed_text.y = self.top - 167

    def debug_draw_hitboxes(self) -> None:
        for data in self.buttons_data.values():
            hitbox = self._calculate_hitbox(data)

            arcade.draw_lrbt_rectangle_outline(
                hitbox["left"], hitbox["right"], hitbox["bottom"],
                hitbox["top"], arcade.color.RED, 2
            )

    def _calculate_hitbox(self, data: Dict[str, Any]) -> Dict[str, float]:
        if data["anchor"] == "TOP_RIGHT":
            ref_x = self.right
            ref_y = self.top

        elif data["anchor"] == "TOP_LEFT":
            ref_x = self.left
            ref_y = self.top

        else:  # Default value
            ref_x = self.left
            ref_y = self.bottom

        # Calculate boundaries
        button_left = ref_x + (data["offset"][0] * self.scale_x)
        button_right = button_left + (data["size"][0] * self.scale_x)

        button_top = ref_y + (data["offset"][1] * self.scale_y)
        button_bottom = button_top - (data["size"][1] * self.scale_y)

        return {
            "left": button_left,
            "right": button_right,
            "top": button_top,
            "bottom": button_bottom
        }
