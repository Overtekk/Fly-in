# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  sprites.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/16 14:34:19 by roandrie        #+#    #+#               #
#  Updated: 2026/03/26 14:56:12 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
"""
Graphical sprites and UI components for the Arcade simulation.

This module defines the visual representations of the core simulation
entities (zones and drones) as well as the interactive graphical user
interface (UI) elements used to control and monitor the simulation state.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

import random
import math
import arcade
from arcade.types import PathOrTexture

from src.object.drones import Drone
from src.object.zone import Zone
from src.utils.ui import Colors
from src.graphics.graphics_settings import (SpriteSetting, WindowAction,
                                            FontSettings, WindowSettings)


if TYPE_CHECKING:
    from src.simulation.manager import Manager


class ZoneSprite(arcade.Sprite):
    """
    Visual representation of a simulation zone.

    This sprite handles the display of a physical hub/node on the map,
    including its name, the number of drones currently occupying it,
    and its pathfinding weight (in debug mode).
    """

    def __init__(self, image_path: PathOrTexture,
                 scale: float, zone_data: Zone, manager: 'Manager') -> None:
        """
        Initializes a visual representation of a simulation zone.

        Sets up the sprite image, scales it, and prepares the text labels for
        displaying the zone's name, current drone count, and pathfinding weight.

        Args:
            image_path (PathOrTexture): The path to the zone's sprite asset.
            scale (float): The scaling factor for the sprite.
            zone_data (Zone): The logical Zone object containing backend data.
            manager (Manager): The core simulation manager.
        """
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
            text=self.zone_name, x=0, y=0, anchor_x="center", anchor_y="top",
            color=Colors.get_rgb_color(self.zone_data.metadata_color),
            font_name=FontSettings.PIXELOGIST_NAME, font_size=10
            )

        # Write drones count
        self.label_count_text = arcade.Text(
            text="", x=0, y=0, anchor_x="left", anchor_y="baseline",
            color=arcade.color.FLORAL_WHITE,
            font_name=FontSettings.PIXELOGIST_NAME, font_size=13
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

    def update_drone_count(self, visual_count: int) -> None:
        """
        Updates the textual display of the drone count on the zone.

        Formats the text differently depending on whether the zone is a start
        hub, end hub, or a regular zone with a maximum capacity.

        Args:
            visual_count (int): The current number of drones occupying the zone.
        """
        if self.zone_data.is_start:
            text_drone = f"{visual_count}"
        elif self.zone_data.is_end:
            text_drone = f"{visual_count}"
        else:
            text_drone = f"{visual_count}/{self.max_drones}"

        self.label_count_text.text = text_drone

    def draw_ui(self) -> None:
        """
        Renders the UI overlays for the zone sprite.

        Draws the zone's name, current capacity count, and debug information
        (pathfinding weight) directly above or below the sprite.
        """
        # text_width = self.label_name_text.content_width
        # text_height = self.label_name_text.content_height
        # text_x = self.label_name_text.x
        # text_y = self.label_name_text.y

        # arcade.draw.draw_lbwh_rectangle_filled(
        #     text_x - (text_width / 2) - 1, text_y - text_height - 2.5,
        #     text_width + 3, text_height + 0.6,
        #     (0, 0, 0, 190)
        #     )

        self.label_name_text.draw()
        self.label_count_text.draw()

        if self.manager.args.debug:
            self.label_weight_text.draw()


class DroneSprite(arcade.Sprite):
    """
    Visual representation of a drone.

    This sprite manages its own movement interpolation between zones
    and idle animations (swarming effect) when stationary.
    """

    def __init__(self, image_path: PathOrTexture, scale: float,
                 drone_data: Drone, id: int,
                 drone_sprites_anim: List[arcade.Texture]) -> None:
        """
        Initializes a visual representation of a drone.

        Sets up the sprite, its animation frames, and initializes state
        tracking variables for movement and idle swarming (oscillation).

        Args:
            image_path (PathOrTexture): The path to the drone's default sprite.
            scale (float): The scaling factor for the sprite.
            drone_data (Drone): The logical Drone object containing backend
                                data.
            id (int): The unique identifier of the drone.
            drone_sprites_anim (List[arcade.Texture]): A list of textures for
                                                       movement animation.
        """
        super().__init__(image_path, scale)

        self.drone_data = drone_data
        self.id = id
        self.location = self.drone_data.get_location()
        self.finish = drone_data.finish

        self.target_x = 0.0
        self.target_y = 0.0
        self.is_moving = False
        self.active_connection = ""

        self.cur_textures = 0
        self.time_counter = 0.0
        self.idle_texture = self.texture
        self.finish_texture = drone_sprites_anim[2]
        self.move_textures = drone_sprites_anim

    def on_update(self, delta_time: float) -> None:
        """
        Handles the movement and positional logic of the drone.

        If the drone is moving, it calculates the velocity vector towards its
        target and updates its coordinates.

        Args:
            delta_time (float): Time interval since the last frame.
        """
        if not self.is_moving:
            return

        if self.departure_timer > 0.0:
            self.departure_timer -= delta_time
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
        """
        Cycles through the drone's textures to create an animation.

        Switches textures based on the elapsed time if the drone is moving.
        Resets to the idle or finished texture when stationary.

        Args:
            delta_time (float): Time interval since the last frame.
                                Defaults to 1/60.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
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
    """
    Interactive UI control window.

    A draggable, self-contained UI element that displays the simulation
    progress, speed controls, and handles interaction hitboxes.
    """

    def __init__(self, image_path: PathOrTexture,
                 scale: float, manager: 'Manager'):
        """
        Initializes the interactive UI control window.

        Sets up the window's sprite, initializes the progress bar ratio,
        prepares all textual elements, and defines the local coordinates for
        clickable hitboxes.

        Args:
            image_path (PathOrTexture): The path to the window's sprite asset.
            scale (float): The scaling factor for the sprite.
            manager (Manager): The core simulation manager to access simulation
                               state.
        """
        super().__init__(image_path, scale)

        self.manager = manager
        self.end_name = self.manager.end_name
        self.is_imploding = False
        self.is_ejected = False
        self.ratio = 0.0

        self.buttons_data: Dict[str, Any] = {
            WindowAction.CLOSE: {
                "anchor": "TOP_RIGHT",
                "offset": (-11, 0),
                "size": (10, 10)
            },
            WindowAction.COPY: {
                "anchor": "TOP_RIGHT",
                "offset": (-23, 0),
                "size": (10, 10)
            },
            WindowAction.REMOVE: {
                "anchor": "TOP_RIGHT",
                "offset": (-36, 0),
                "size": (10, 10)
            },
            WindowAction.MOVE: {
                "anchor": "TOP_LEFT",
                "offset": (0, 0),
                "size": (162, 11.5)
            },
            WindowAction.SPEED_MINUS: {
                "anchor": "BOTTOM_LEFT",
                "offset": (0, 20),
                "size": (20, 15)
            },
            WindowAction.SPEED_PLUS: {
                "anchor": "BOTTOM_LEFT",
                "offset": (79, 20),
                "size": (20, 15)
            },
            WindowAction.TOGGLE_PAUSE: {
                "anchor": "BOTTOM_RIGHT",
                "offset": (-94, 25),
                "size": (90, 22)
            },
        }

        self.speed_text = arcade.Text(
            text=f"{str(SpriteSetting.DRONE_SPEED)}%", x=0, y=0,
            anchor_x="center", color=(0, 0, 0, 255), font_size=19,
            font_name=FontSettings.PIXELOGIST_NAME,
        )
        self.speed_plus = arcade.Text(
            text="+", x=0, y=0, anchor_x="left",
            color=(0, 0, 0, 255), font_size=30,
            font_name=FontSettings.PIXELOGIST_NAME,
        )
        self.speed_minus = arcade.Text(
            text="-", x=0, y=0, anchor_x="center",
            color=(0, 0, 0, 255), font_size=30,
            font_name=FontSettings.PIXELOGIST_NAME,
        )
        self.turn_text = arcade.Text(
            text=f"TURN {int(self.manager.turns)}", x=0, y=0,
            anchor_x="center", color=(0, 0, 0, 255), font_size=24,
            font_name=FontSettings.PIXELOGIST_NAME
        )
        self.pause_text = arcade.Text(
            text="PAUSE", x=0, y=0, anchor_x="center", color=(0, 0, 0, 255),
            font_size=24, font_name=FontSettings.PIXELOGIST_NAME
        )
        self.resume_text = arcade.Text(
            text="RESUME", x=0, y=0, anchor_x="center", color=(0, 0, 0, 255),
            font_size=24, font_name=FontSettings.PIXELOGIST_NAME
        )
        self.big_pause_text = arcade.Text(
            text="PAUSE", x=0, y=0, anchor_x="center",
            color=arcade.color.WHITE_SMOKE, font_size=40,
            font_name=FontSettings.PIXELMANIA_NAME
        )

    def get_ui_action(self, mouse_x: float, mouse_y: float) -> Optional[str]:
        """
        Determines which UI button was clicked based on mouse coordinates.

        Args:
            mouse_x (float): The X-coordinate of the mouse click.
            mouse_y (float): The Y-coordinate of the mouse click.

        Returns:
            Optional[str]: The action string corresponding to the clicked
                           button, or None if no button was clicked.
        """
        for action, data in self.buttons_data.items():
            hitbox = self._calculate_hitbox(data)

            # Check if mouse is in the box
            if hitbox["left"] <= mouse_x <= hitbox["right"]:
                if hitbox["bottom"] <= mouse_y <= hitbox["top"]:
                    return action
        return None

    def draw_ui(self, state_pause: bool) -> None:
        """
        Renders the UI window, its progress bar, and textual elements.

        Skips rendering if the window is currently playing a destruction
        animation. Draws the dynamic progress bar based on the calculated
        completion ratio.

        Args:
            state_pause (bool): The current pause state of the simulation to
                                toggle text.
        """
        if self.is_imploding or self.is_ejected:
            return

        arcade.draw.draw_lbwh_rectangle_filled(
            left=self.left + 5, bottom=self.bottom + 6,
            width=145, height=30, color=(192, 192, 192, 255)
            )

        arcade.draw.draw_lbwh_rectangle_filled(
            left=self.right - 29, bottom=self.bottom + 5,
            width=12, height=29, color=(192, 192, 192, 255)
            )

        if self.ratio > 0:
            arcade.draw.draw_lbwh_rectangle_filled(
                left=self.left + 6, bottom=self.top - 120,
                width=289 * self.ratio, height=29,
                color=arcade.color.BUD_GREEN
            )

        arcade.draw.draw_lbwh_rectangle_outline(
            left=self.left + 5, bottom=self.top - 120,
            width=290, height=29, color=(160, 159, 158, 255), border_width=4
            )

        arcade.draw.draw_lbwh_rectangle_outline(
            left=self.left + 5, bottom=self.top - 120,
            width=289, height=28.9, color=(29, 31, 33, 255), border_width=1
            )

        self.speed_text.draw()
        self.speed_plus.draw()
        self.speed_minus.draw()
        self.turn_text.draw()
        if not state_pause:
            self.pause_text.draw()
        else:
            self.resume_text.draw()
            self.big_pause_text.draw()

    def update_ui_position(self) -> None:
        """
        Recalculates and updates the positions of all internal textual
        elements.

        Ensures that text labels stay anchored correctly to the window sprite
        when the user drags it across the screen.
        """
        self.speed_text.x = self.center_x - 73
        self.speed_text.y = self.top - 170

        self.speed_minus.x = self.center_x - 135
        self.speed_minus.y = self.top - 172

        self.speed_plus.x = self.center_x - 30
        self.speed_plus.y = self.top - 172

        self.turn_text.x = self.center_x
        self.turn_text.y = self.top - 58

        self.pause_text.x = self.right - 73
        self.pause_text.y = self.bottom + 9

        self.resume_text.x = self.right - 73
        self.resume_text.y = self.bottom + 9

        self.big_pause_text.x = WindowSettings.WIDTH / 2
        self.big_pause_text.y = WindowSettings.HEIGHT / 2

    def update_info(self, action: str) -> None:
        """
        Updates the values displayed on the dynamic text elements.

        Args:
            action (str): The specific information to update
                          (e.g., speed or turn count).
        """
        if (action == WindowAction.SPEED_PLUS or
                action == WindowAction.SPEED_MINUS):
            self.speed_text.text = f"{str(SpriteSetting.DRONE_SPEED)}%"

        elif action == WindowAction.TURN:
            self.turn_text.text = f"TURN {int(self.manager.turns)}"

    def debug_draw_hitboxes(self) -> None:
        """
        Draws red outlines around all defined UI hitboxes for debugging
        purposes.
        """
        for data in self.buttons_data.values():
            hitbox = self._calculate_hitbox(data)

            arcade.draw_lrbt_rectangle_outline(
                hitbox["left"], hitbox["right"], hitbox["bottom"],
                hitbox["top"], arcade.color.RED, 2
            )

    def _calculate_hitbox(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculates the absolute screen coordinates for a UI element's hitbox.

        Resolves the bounding box based on the specified anchor point on the
        main sprite, the defined pixel offset, and the element's size.

        Args:
            data (Dict[str, Any]): A dictionary containing the anchor, offset,
                                  and size.

        Returns:
            Dict[str, float]: A dictionary containing the absolute 'left',
                              'right', 'top', and 'bottom' coordinates of the
                              hitbox.
        """
        if data["anchor"] == "TOP_RIGHT":
            ref_x = self.right
            ref_y = self.top

        elif data["anchor"] == "TOP_LEFT":
            ref_x = self.left
            ref_y = self.top

        elif data["anchor"] == "BOTTOM_LEFT":
            ref_x = self.left
            ref_y = self.bottom

        elif data["anchor"] == "BOTTOM_RIGHT":
            ref_x = self.right
            ref_y = self.bottom

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

    def on_update(self, delta_time: float) -> None:
        """
        Updates the UI logic and handles destruction animations at each frame.

        Calculates the simulation completion ratio based on drones at the end
        hub. Applies mathematical transformations to scale down (implosion) or
        shake (ejection) the window before destroying it entirely.

        Args:
            delta_time (float): Time interval since the last frame.
        """
        if self.end_name:
            nb_drones = self.manager.raw_nb_drones
            drone_finished = self.manager.zones[self.end_name].drones_on_it
            self.ratio = len(drone_finished) / nb_drones

        if not self.is_imploding and not self.is_ejected:
            return

        if self.is_imploding:
            new_scale_x, new_scale_y = self.scale

            new_scale_x -= 5 * delta_time
            new_scale_y -= 5 * delta_time

            self.scale = (new_scale_x, new_scale_y)

            if self.scale <= (0.05, 0.05):
                self.kill()

        elif self.is_ejected:
            self.center_x += random.randint(-10, 10)
            self.center_y += random.randint(-10, 10)

            new_scale_x, new_scale_y = self.scale

            new_scale_x -= 1 * delta_time
            new_scale_y -= 1 * delta_time

            self.scale = (new_scale_x, new_scale_y)

            if self.scale <= (0.05, 0.05):
                self.kill()
