# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/16 14:08:32 by roandrie        #+#    #+#               #
#  Updated: 2026/03/20 11:18:25 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING, Dict, List

import arcade
import os

from src.graphics.graphics_settings import (WindowSettings, SpritePath,
                                            SpriteSetting)
from src.object.drones import Drone
from src.object.zone import Zone
from src.object.utils.type import ZoneType
from src.graphics.sprites import ZoneSprite, DroneSprite, TurnText


if TYPE_CHECKING:
    from src.simulation.manager import Manager

class Renderer(arcade.Window):
    def __init__(self, zones_dict: Dict[str, Zone], manager: 'Manager',
                 drones_dict: Dict[int, Drone],
                 connection_map: Dict[str, List[str]]) -> None:
        super().__init__(width=WindowSettings.WIDTH, antialiasing=True,
                         height=WindowSettings.HEIGHT, fullscreen=False,
                         title=WindowSettings.NAME, resizable=True,
                         center_window=True)

        self.zones_dict = zones_dict
        self.drones_dict = drones_dict
        self.connection_map = connection_map
        self.manager = manager

        self._init_variables()
        self._init_arcade_components()
        self._init_texts()
        self._load_sprites()
        self._calculate_line_to_draw()

    def simulate(self) -> None:
        if self.started:
            while not self.pause:
                for drone_sprite in self.drone_sprites_list:
                    if drone_sprite.is_moving:
                        continue

                self.manager.simulate_one_turn()
                self._update_drone_sprite()


    def on_update(self, delta_time: float) -> None:
        for drone_sprite in self.drone_sprites_list:
            was_moving = drone_sprite.is_moving
            drone_sprite.on_update(delta_time)
            drone_sprite.update_animation(delta_time, None, None)

            if was_moving and not drone_sprite.is_moving:
                for zone_sprite in self.zone_sprites_list:
                    if zone_sprite.zone_data.name == drone_sprite.location:
                        zone_sprite.update_drone_count()

    def on_draw(self) -> None:
        self.clear()

        # Static camera (no affected by the zoom)
        self.static_camera.use()
        arcade.draw_texture_rect(self.background, arcade.LBWH(
            0, 0, WindowSettings.WIDTH, WindowSettings.HEIGHT))

        if self.started:
            self.starting_text_ui.draw()

        if self.turn_text.turn != self.manager.turns:
            self.turn_text.update_turn()
        self.turn_text.draw_ui()

        # Main camera (affected by the zoon)
        self.camera.use()

        for (start_x, start_y), (end_x, end_y) in self.line_to_draw:
            arcade.draw_line(start_x, start_y, end_x, end_y,
                             arcade.color.WHITE, 1.5)

        self.zone_sprites_list.draw()
        for sprite in self.zone_sprites_list:
            sprite.draw_ui()

        self.drone_sprites_list.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
        elif symbol == arcade.key.SPACE:
            self.started = False
            self.manager.simulate_one_turn()
            self._update_drone_sprite()

    def on_mouse_scroll(self, x: int, y: int,
                        scroll_x: int, scroll_y: int) -> None:
        self.camera_zoom *= 0.9 if scroll_y < 0 else 1.1

        self.camera_zoom = max(0.1, min(2.0, self.camera_zoom))
        self.camera.zoom = self.camera_zoom

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int,
                      buttons: int, modifiers: int) -> None:
        # Allow camera movement
        if buttons == arcade.MOUSE_BUTTON_RIGHT:
            curr_x, curr_y = self.camera.position
            update_x = curr_x - (dx * self.camera_zoom)
            update_y = curr_y - (dy * self.camera_zoom)

            self.camera.position = (update_x, update_y)

    def on_mouse_press(self, x: int, y: int,
                       button: int, modifiers: int) -> None:
        # Reset camera position
        if button == arcade.MOUSE_BUTTON_MIDDLE:
            self.camera.position = (self.default_camera_x,
                                    self.default_camera_y)

    def _init_variables(self) -> None:
        self.zone_sprites_list = arcade.SpriteList()
        self.drone_sprites_list = arcade.SpriteList()
        self.zone_coords = {}
        self.line_to_draw = []
        self.draw_lines = set()
        self.pause = False

    def _init_arcade_components(self) -> None:
        self.camera = arcade.camera.Camera2D()
        self.static_camera = arcade.camera.Camera2D()
        self.camera_zoom = 1.0

        self.default_camera_x, self.default_camera_y = self.camera.position

    def _init_texts(self) -> None:
        # Text : start simulation
        self.started = True
        self.starting_text_ui = arcade.Text(
            text="Press SPACE to start", anchor_x="center", anchor_y="bottom",
            x=(WindowSettings.WIDTH / 2), y=(20 / 2),
            font_size=22, color=arcade.color.WHITE_SMOKE, font_name="arial"
        )

        # Text : number of turns
        self.turn_text = TurnText(self.manager)

    def _load_sprites(self) -> None:
        if not os.path.exists("src/graphics/sprites/"):
            raise OSError("PATH 'src/graphics/sprites/' does snot exist.")

        try:
            # Calcule the offset to center all sprites
            x_coords = [zone.x for zone in self.zones_dict.values()]
            y_coords = [zone.y for zone in self.zones_dict.values()]

            min_x, max_x = min(x_coords), max(x_coords)
            min_y, max_y = min(y_coords), max(y_coords)

            center_logical_x = (min_x + max_x) / 2
            center_logical_y = (min_y + max_y) / 2

            # Change the offset based on the actual map
            SpriteSetting.OFFSET_X = ((WindowSettings.WIDTH / 2)
                                      - (center_logical_x
                                         * SpriteSetting.SPACING))
            SpriteSetting.OFFSET_Y = ((WindowSettings.HEIGHT / 2)
                                      - (center_logical_y
                                         * SpriteSetting.SPACING))

            # Load background
            self.background = arcade.load_texture(SpritePath.BACKGROUND)

            # Create sprites for zones
            for zone in self.zones_dict.values():
                if zone.is_start:
                    zone_sprite = ZoneSprite(SpritePath.START_HUB,
                                             SpriteSetting.ZONE_SCALE, zone,
                                             self.manager)
                elif zone.is_end:
                    zone_sprite = ZoneSprite(SpritePath.END_HUB,
                                             SpriteSetting.ZONE_SCALE, zone,
                                             self.manager)
                else:
                    match zone.metadata_zone_type:
                        case ZoneType.NORMAL:
                            zone_sprite = ZoneSprite(SpritePath.DEFAULT_ZONE,
                                                    SpriteSetting.ZONE_SCALE,
                                                    zone, self.manager)
                        case ZoneType.BLOCKED:
                            zone_sprite = ZoneSprite(SpritePath.ZONE_BLOCKED,
                                                    SpriteSetting.ZONE_SCALE,
                                                    zone, self.manager)
                        case ZoneType.RESTRICTED:
                            zone_sprite = ZoneSprite(
                                SpritePath.ZONE_RESTRICTED,
                                SpriteSetting.ZONE_SCALE, zone, self.manager)
                        case ZoneType.PRIORITY:
                            zone_sprite = ZoneSprite(SpritePath.ZONE_PRIORITY,
                                                    SpriteSetting.ZONE_SCALE,
                                                    zone, self.manager)

                zone_sprite.center_x = ((zone.x * SpriteSetting.SPACING)
                                        + SpriteSetting.OFFSET_X)
                zone_sprite.center_y = ((zone.y * SpriteSetting.SPACING)
                                        + SpriteSetting.OFFSET_Y)
                zone_sprite.label_name_text.x = zone_sprite.center_x
                zone_sprite.label_name_text.y = zone_sprite.center_y - 30
                zone_sprite.label_count_text.x = zone_sprite.center_x + 20
                zone_sprite.label_count_text.y = zone_sprite.center_y + 30

                if self.manager.args.debug:
                    zone_sprite.label_weight_text.x = zone_sprite.center_x
                    zone_sprite.label_weight_text.y = zone_sprite.center_y + 30

                self.zone_sprites_list.append(zone_sprite)
                zone_sprite.update_drone_count()

                self.zone_coords[zone.name] = (zone_sprite.center_x,
                                               zone_sprite.center_y)

            # Create sprites for drones

            drone_sprites_anim = [
                arcade.load_texture(SpritePath.DRONE_ANIM1),
                arcade.load_texture(SpritePath.DRONE_ANIM2),
                arcade.load_texture(SpritePath.DRONE_FINISH)
            ]

            for (id, drone) in self.drones_dict.items():
                drone_sprite = DroneSprite(SpritePath.DRONE,
                                           SpriteSetting.DRONE_SCALE,
                                           drone, id, drone_sprites_anim)
                drone_location = drone.get_location()
                drone_x = self.zones_dict[drone_location].x
                drone_y = self.zones_dict[drone_location].y

                drone_sprite.center_x = ((drone_x * SpriteSetting.SPACING)
                                         + SpriteSetting.OFFSET_X)
                drone_sprite.center_y = ((drone_y * SpriteSetting.SPACING)
                                         + SpriteSetting.OFFSET_Y)
                self.drone_sprites_list.append(drone_sprite)

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Sprite not found in PATH {e}")

    def _calculate_line_to_draw(self) -> None:
        for zone_a, neighbors in self.connection_map.items():
            for zone_b in neighbors:
                connection_draw = tuple(sorted([zone_a, zone_b]))

                if connection_draw not in self.draw_lines:
                    coords_a = self.zone_coords[zone_a]
                    coords_b = self.zone_coords[zone_b]

                    self.line_to_draw.append((coords_a, coords_b))
                    self.draw_lines.add(connection_draw)

    def _update_drone_sprite(self) -> None:
        for drone_sprite in self.drone_sprites_list:
            drone_obj = self.drones_dict[drone_sprite.id]

            new_location = drone_obj.get_location()
            if new_location != drone_sprite.location:

                for zone_sprite in self.zone_sprites_list:
                    if zone_sprite.zone_data.name == drone_sprite.location:
                        zone_sprite.update_drone_count()

                if "-" in new_location:
                    next_zone = new_location.split("-")
                    new_loc_x, new_loc_y = self.zone_coords[next_zone[1]]
                    loc_x = new_loc_x - 50
                    loc_y = new_loc_y
                    print(f"{new_loc_x} {new_loc_y}")
                    print(f"{loc_x} {loc_y}")
                else:
                    loc_x, loc_y = self.zone_coords[new_location]

                drone_sprite.target_x = loc_x
                drone_sprite.target_y = loc_y
                drone_sprite.is_moving = True
