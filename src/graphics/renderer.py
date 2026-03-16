# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/16 14:08:32 by roandrie        #+#    #+#               #
#  Updated: 2026/03/16 15:57:13 by roandrie        ###   ########.fr        #
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
from src.graphics.sprites import ZoneSprite, DroneSprite

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
        self._load_sprites()

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        self.clear()

        self.all_sprites_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

    def _init_variables(self) -> None:
        self.all_sprites_list = arcade.SpriteList()

    def _load_sprites(self) -> None:
        if not os.path.exists("src/graphics/sprites/"):
            raise OSError("PATH 'src/graphics/sprites/' does snot exist.")

        try:
            # Create sprites for zones
            for (name, zone) in self.zones_dict.items():
                if zone.is_start:
                    zone_sprite = ZoneSprite(SpritePath.START_HUB,
                                             SpriteSetting.ZONE_SCALE)
                elif zone.is_end:
                    zone_sprite = ZoneSprite(SpritePath.END_HUB,
                                             SpriteSetting.ZONE_SCALE)
                else:
                    match zone.metadata_zone_type:
                        case ZoneType.NORMAL:
                            zone_sprite = ZoneSprite(SpritePath.DEFAULT_ZONE,
                                                    SpriteSetting.ZONE_SCALE)
                        case ZoneType.BLOCKED:
                            zone_sprite = ZoneSprite(SpritePath.ZONE_BLOCKED,
                                                    SpriteSetting.ZONE_SCALE)
                        case ZoneType.RESTRICTED:
                            zone_sprite = ZoneSprite(
                                SpritePath.ZONE_RESTRICTED,
                                SpriteSetting.ZONE_SCALE)
                        case ZoneType.PRIORITY:
                            zone_sprite = ZoneSprite(SpritePath.ZONE_PRIORITY,
                                                    SpriteSetting.ZONE_SCALE)
                        case _:
                            pass

                zone_sprite.center_x = ((zone.x * SpriteSetting.SPACING)
                                        + SpriteSetting.OFFSET_X)
                zone_sprite.center_y = ((zone.y * SpriteSetting.SPACING)
                                        + SpriteSetting.OFFSET_Y)
                self.all_sprites_list.append(zone_sprite)

            # Create sprites for drones

            for drone in self.drones_dict.values():
                drone_sprite = DroneSprite(SpritePath.DRONE,
                                           SpriteSetting.DRONE_SCALE)
                drone_location = drone.get_location()
                drone_x = self.zones_dict[drone_location].x
                drone_y = self.zones_dict[drone_location].y

                drone_sprite.center_x = ((drone_x * SpriteSetting.SPACING)
                                         + SpriteSetting.OFFSET_X)
                drone_sprite.center_y = ((drone_y * SpriteSetting.SPACING)
                                         + SpriteSetting.OFFSET_X)

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Sprite not found in PATH {e}")
