# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  sprites.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 23:22:54 by roandrie        #+#    #+#               #
#  Updated: 2026/03/16 09:53:11 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pygame
import math

from typing import Dict, Tuple, TYPE_CHECKING

from src.utils.ui import Colors
from src.object.zone import Zone
from src.object.drones import Drone
from src.object.utils.type import ZoneType
from src.graphics.graphics_settings import FontSettings, ScreenSettings

if TYPE_CHECKING:
    from src.simulation.manager import Manager

PATH = "src/graphics/sprites/"


class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.Surface, x: int, y: int, zone: Zone,
                 font_size: int) -> None:
        super().__init__()

        try:
            self.font = pygame.font.Font(f"{PATH}whitrabt.ttf", font_size,
                                         True)
        except Exception:
            self.font = pygame.font.SysFont("dejavuserif", font_size, True)

        self.zone = zone
        self.drone_count = len(zone.drones_on_it)
        self.previous_drone_count = -1

        name = zone.name
        if len(zone.name) > 10:
            name = zone.name[:10]
            name += "..."

        text = self.font.render(name, True,
                                (Colors.get_rgb_color(zone.metadata_color)))

        total_width = self._get_surface_width(sprite, text)
        total_height = self._get_surface_height(sprite, text)

        combined_surface = self._get_combined_surface(total_width,
                                                      total_height)

        combined_surface.blit(sprite,
                              ((total_width - sprite.get_width()) / 2, 0))
        combined_surface.blit(text, ((total_width - text.get_width()) / 2,
                                     sprite.get_height() + 5))

        self.image = combined_surface
        self.base_image = combined_surface.copy()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self) -> None:
        if self.drone_count != self.previous_drone_count:
            self.image = self.base_image.copy()

            if self.zone.metadata_zone_type == ZoneType.BLOCKED:
                pass
            elif self.zone.is_start or self.zone.is_end:
                text = self.font.render(f"{str(self.drone_count)}", True,
                                        Colors.get_rgb_color("tomato"))
                self.image.blit(text,
                                (self.image.get_width() - text.get_width() - 5,
                                 0))
            else:
                text = self.font.render(f"{str(self.drone_count)}/"
                                        f"{self.zone.metadata_max_drones}",
                                        True,
                                        (Colors.get_rgb_color("fuchsia")))
                self.image.blit(text,
                                (self.image.get_width() - text.get_width(), 0))

            self.previous_drone_count = self.drone_count

    def _add_visual_drone(self) -> None:
        self.drone_count += 1

    def _remove_visual_drone(self) -> None:
        if self.drone_count > 0:
            self.drone_count -= 1

    def _get_surface_width(self, sprite: pygame.Surface,
                           text: pygame.Surface) -> int:
        return max(sprite.get_width(), text.get_width())

    def _get_surface_height(self, sprite: pygame.Surface,
                            text: pygame.Surface) -> int:
        return sprite.get_height() + text.get_height() + 5

    def _get_combined_surface(self, total_width: int,
                              total_height: int) -> pygame.Surface:
        return pygame.Surface((total_width, total_height), pygame.SRCALPHA)


class DroneSprite(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.Surface, drone: Drone,
                 zone_coords: Dict[str, Tuple[int, int]],
                 zone_sprites_dict: Dict[str, Sprite]) -> None:
        super().__init__()

        self.logical_drone = drone
        self.zone_coords = zone_coords
        self.zone_sprites_dict = zone_sprites_dict
        self.speed = 4
        self.moving = False

        self.location = self.logical_drone.get_location()
        position = self.zone_coords[self.location]

        self.target_x = position[0]
        self.target_y = position[1]

        self.image = sprite
        self.rect = self.image.get_rect(center=(position))

    def update(self) -> None:
        if self.location != self.logical_drone.get_location():
            old_loc = self.location
            new_loc = self.logical_drone.get_location()
            new_pos = self.zone_coords[new_loc]

            self.target_x = new_pos[0]
            self.target_y = new_pos[1]
            self.location = new_loc

            self.zone_sprites_dict[old_loc]._remove_visual_drone()
            self.moving = True

        dx = self.target_x - self.rect.centerx
        dy = self.target_y - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > self.speed:
            vecteur_x = (dx / distance) * self.speed
            vecteur_y = (dy / distance) * self.speed

            self.rect.centerx += vecteur_x
            self.rect.centery += vecteur_y

        elif distance <= self.speed and self.moving:
            self.rect.centerx = self.target_x
            self.rect.centery = self.target_y

            self.zone_sprites_dict[self.location]._add_visual_drone()
            self.moving = False


class SpriteText(pygame.sprite.Sprite):
    def __init__(self, manager: 'Manager') -> None:
        super().__init__()

        self.manager = manager
        self.turn = self.manager.turns
        self.previous_turn = -1
        text_turn = FontSettings.FONT.render(f"TURN {str(self.turn)}", True,
                                             (Colors.get_rgb_color("navy")))

        self.image = text_turn
        self.rect = self.image.get_rect(center=(ScreenSettings.WIDTH / 2, 15))

    def update(self) -> None:
        if self.previous_turn != self.manager.turns:
            new_text_turn = FontSettings.FONT.render(
                f"TURN {str(self.manager.turns)}", True,
                (Colors.get_rgb_color("navy")))
            self.image = new_text_turn
            self.rect = self.image.get_rect(
                center=(ScreenSettings.WIDTH / 2, 15))

            self.previous_turn = self.manager.turns
