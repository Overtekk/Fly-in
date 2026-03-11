# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  sprites.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 23:22:54 by roandrie        #+#    #+#               #
#  Updated: 2026/03/11 16:17:15 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pygame

from src.utils.ui import Colors
from src.object.zone import Zone
from src.object.utils.type import ZoneType
from src.graphics.graphics_settings import FontSettings

PATH = "src/graphics/sprites/"


class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.Surface, x: int, y: int, zone: Zone,
                 font_size: int) -> None:
        super().__init__()

        try:
            font = pygame.font.Font(f"{PATH}whitrabt.ttf", font_size, True)
        except Exception:
            font = pygame.font.SysFont("dejavuserif", font_size, True)

        self.zone = zone
        self.previous_drone_count = -1

        name = zone.name
        if len(zone.name) > 10:
            name = zone.name[:10]
            name += "..."

        text = font.render(name, True, (Colors.get_rgb_color(zone.metadata_color)))

        total_width = self._get_surface_width(sprite, text)
        total_height = self._get_surface_height(sprite, text)

        combined_surface = self._get_combined_surface(total_width, total_height)

        combined_surface.blit(sprite, ((total_width - sprite.get_width()) / 2, 0))
        combined_surface.blit(text, ((total_width - text.get_width()) / 2, sprite.get_height() + 5))

        self.image = combined_surface
        self.base_image = combined_surface.copy()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self) -> None:
        try:
            font = pygame.font.Font(f"{PATH}whitrabt.ttf", FontSettings.SIZE, True)
        except Exception:
            font = pygame.font.SysFont("dejavuserif", FontSettings.SIZE, True)

        nb_drones = len(self.zone.drones_on_it)
        if nb_drones != self.previous_drone_count:
            self.image = self.base_image.copy()

            if self.zone.metadata_zone_type == ZoneType.BLOCKED:
                pass
            elif self.zone.is_start or self.zone.is_end:
                text = font.render(f"{str(nb_drones)}", True, (Colors.get_rgb_color("tomato")))
                self.image.blit(text, (self.image.get_width() - text.get_width() - 5, 0))
            else:
                text = font.render(f"{str(nb_drones)}/{self.zone.metadata_max_drones}", True, (Colors.get_rgb_color("fuchsia")))
                self.image.blit(text, (self.image.get_width() - text.get_width(), 0))

            self.previous_drone_count = nb_drones

    def _get_surface_width(self, sprite: pygame.Surface, text: pygame.Surface) -> int:
        return max(sprite.get_width(), text.get_width())

    def _get_surface_height(self, sprite: pygame.Surface, text: pygame.Surface) -> int:
        return sprite.get_height() + text.get_height() + 5

    def _get_combined_surface(self, total_width: int, total_height: int) -> pygame.Surface:
        return pygame.Surface((total_width, total_height), pygame.SRCALPHA)
