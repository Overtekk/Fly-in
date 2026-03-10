# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 22:18:37 by roandrie        #+#    #+#               #
#  Updated: 2026/03/10 22:23:42 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pygame

from typing import Dict

from src.object.zone import Zone
from src.object.utils.type import ZoneType
from src.utils.errors import SpriteError
from src.graphics.sprites import Sprite
from src.graphics.graphics_settings import ScreenSettings


class Renderer():
    def __init__(self, zones: Dict[str, Zone]) -> None:
        self.zones = zones

        # pygame setup
        pygame.init()
        self.fpsClock = pygame.time.Clock()

        # Load the icon
        try:
            icon = pygame.image.load("src/graphics/sprites/icon.png")
            pygame.display.set_icon(icon)
        except Exception:
            pass

        # Set up the window
        self.screen = pygame.display.set_mode((ScreenSettings.WIDTH,
                                              ScreenSettings.HEIGHT),
                                              pygame.RESIZABLE)
        pygame.display.set_caption(ScreenSettings.NAME)

        # Load sprites
        self.assets = {}
        self._load_sprite()
        self.all_sprites = pygame.sprite.Group()
        self._init_zone_sprites()

        self.running = True

    def run_renderer(self) -> None:
        while self.running:

            # Quit the program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

            self.fpsClock.tick(ScreenSettings.FPS)

        pygame.quit()

    def _load_sprite(self) -> None:
        PATH = "src/graphics/sprites/"

        try:
            self.assets["spawn"] = (pygame.image.load(f"{PATH}spawn.png")
                                    .convert_alpha())
            self.assets["end"] = (pygame.image.load(f"{PATH}end.png")
                                  .convert_alpha())
            self.assets["hub"] = (pygame.image.load(f"{PATH}hub.png")
                                  .convert_alpha())
            self.assets["zone_blocked"] = (pygame.image.load(
                                           f"{PATH}zone_blocked.png")
                                           .convert_alpha())
            self.assets["zone_priority"] = (pygame.image.load(
                                            f"{PATH}zone_priority.png")
                                            .convert_alpha())
            self.assets["zone_restricted"] = (pygame.image.load(
                                              f"{PATH}zone_restricted.png")
                                              .convert_alpha())
            self.assets["drone"] = (pygame.image.load(f"{PATH}drone.png")
                                    .convert_alpha())
        except Exception:
            raise SpriteError("Error while loading sprite. Cancel rendering.")

    def _init_zone_sprites(self) -> None:
        # If there is no zones
        if not self.zones:
            return

        # List of all coordinates to find all boundaries coords
        x_coords_list = [zone.x for zone in self.zones.values()]
        y_coords_list = [zone.y for zone in self.zones.values()]
        min_x, max_x = min(x_coords_list), max(x_coords_list)
        min_y, max_y = min(y_coords_list), max(y_coords_list)
        map_width_units = max(max_x - min_x, 1)

        main_y = next(zone.y for zone in self.zones.values() if zone.is_start)

        max_offset_y = max(main_y - min_y, max_y - main_y)

        PADDING = 60  # Empty space to leave on the screen edges
        BASE_SIZE = 64  # Normal size of the images
        MARGIN = 10  # Small gap to prevent images from touching

        # Space usable in the window
        available_x_space = ScreenSettings.WIDTH - (2 * PADDING)
        half_available_y_space = (ScreenSettings.HEIGHT / 2) - PADDING

        # Calculate zoom for each sprites
        step_x = available_x_space / map_width_units

        if max_offset_y > 0:
            step_y = half_available_y_space / max_offset_y
        else:
            step_y = float("inf")

        # Final result
        final_step = min(step_x, step_y)
        # Final sprite size
        sprite_size = max(int(min(final_step - MARGIN, BASE_SIZE)), 12)

        scaled_assets = {}
        for name, image_surface in self.assets.items():
            new_image = (pygame.transform.smoothscale
                         (image_surface, (sprite_size, sprite_size)))
            scaled_assets[name] = new_image

        graph_pixel_width = map_width_units * final_step
        offset_x = ((ScreenSettings.WIDTH - graph_pixel_width)
                    / 2 - (min_x * final_step))
        offset_y = ScreenSettings.HEIGHT / 2 - (main_y * final_step)

        for zone in self.zones.values():
            pixel_x = int(offset_x + zone.x * final_step)
            pixel_y = int(offset_y + zone.y * final_step)

            if zone.is_start:
                image = scaled_assets["spawn"]
            elif zone.is_end:
                image = scaled_assets["end"]
            else:
                if zone.metadata_zone_type == ZoneType.BLOCKED:
                    image = scaled_assets["zone_blocked"]
                elif zone.metadata_zone_type == ZoneType.PRIORITY:
                    image = scaled_assets["zone_priority"]
                elif zone.metadata_zone_type == ZoneType.RESTRICTED:
                    image = scaled_assets["zone_restricted"]
                else:
                    image = scaled_assets["hub"]

            self.all_sprites.add(Sprite(image, pixel_x, pixel_y))
