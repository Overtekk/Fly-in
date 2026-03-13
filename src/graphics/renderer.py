# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 22:18:37 by roandrie        #+#    #+#               #
#  Updated: 2026/03/13 11:40:49 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from typing import Dict, List, Tuple, TYPE_CHECKING

from src.object.drones import Drone
from src.object.zone import Zone
from src.object.utils.type import ZoneType
from src.utils.errors import SpriteError
from src.graphics.sprites import Sprite, DroneSprite, SpriteText
from src.graphics.graphics_settings import ScreenSettings

if TYPE_CHECKING:
    from src.simulation.manager import Manager

PATH = "src/graphics/sprites/"


class Renderer():
    def __init__(self, zones: Dict[str, Zone], drones: Dict[int, Drone],
                 connection_map: Dict[str, List[str]],
                 manager: 'Manager') -> None:
        self.zones = zones
        self.drones = drones
        self.connection_map = connection_map
        self.manager = manager

        # pygame setup
        pygame.init()
        pygame.font.init()
        self.fpsClock = pygame.time.Clock()

        # Load the icon
        try:
            icon = pygame.image.load("src/graphics/sprites/icon.png")
            pygame.display.set_icon(icon)
        except Exception:
            pass

        # Set up the window
        self.screen = pygame.display.set_mode((ScreenSettings.WIDTH,
                                              ScreenSettings.HEIGHT))
        pygame.display.set_caption(ScreenSettings.NAME)

        # Load sprites
        self.assets = {}
        self._load_sprite()
        self.all_sprites = pygame.sprite.Group()
        self.drones_sprites = pygame.sprite.Group()
        self.text_sprite = pygame.sprite.Group()
        self.zone_coords: Dict[str, Tuple[int, int]] = {}
        self.zone_sprites_dict: Dict[str, Sprite] = {}

        self._init_zone_sprites()
        self._init_drone_sprites()
        self._init_text_sprites()

        # Calculate lines for each connections to draw
        self.lines_to_draw = []
        self._calculate_line_to_draw()

        self.running = True
        self.last_update_time = pygame.time.get_ticks()

    def run_renderer(self) -> None:
        while self.running:
            current_time = pygame.time.get_ticks()

            if current_time - self.last_update_time > 2000 and self.manager.turns == 0:
                self.manager._debug_simulate_one_step()
                self.manager.turns += 1
                self.last_update_time = current_time

            # Quit the program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.screen.blit(self.background, (0, 0))

            self.text_sprite.update()
            self.text_sprite.draw(self.screen)

            for start_pos, end_pos in self.lines_to_draw:
                pygame.draw.line(self.screen, (255, 255, 255), start_pos, end_pos, 3)

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            self.drones_sprites.update()
            self.drones_sprites.draw(self.screen)

            pygame.display.flip()

            self.fpsClock.tick(ScreenSettings.FPS)

        pygame.quit()

    def _load_sprite(self) -> None:
        try:
            background_image = (pygame.image.load(f"{PATH}background.jpg").
                                convert())
            self.background = pygame.transform.smoothscale(background_image,
                                (ScreenSettings.WIDTH, ScreenSettings.HEIGHT))

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

        # Final sprite size
        sprite_size = max(int(min(min(step_x, step_y) - MARGIN, BASE_SIZE)),
                          12)
        # Font size based on sprite size
        font_size = max(int(sprite_size * 0.16), 1)

        scaled_assets = {}
        for name, image_surface in self.assets.items():
            new_image = (pygame.transform.smoothscale
                         (image_surface, (sprite_size, sprite_size)))
            scaled_assets[name] = new_image

        graph_pixel_width = map_width_units * step_x
        offset_x = ((ScreenSettings.WIDTH - graph_pixel_width)
                    / 2 - (min_x * step_x))
        offset_y = ScreenSettings.HEIGHT / 2 - (main_y * step_y)

        for zone in self.zones.values():
            pixel_x = int(offset_x + zone.x * step_x)
            pixel_y = int(offset_y + zone.y * step_y)

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

            zone_sprite = Sprite(image, pixel_x, pixel_y, zone, font_size)
            self.all_sprites.add(zone_sprite)
            self.zone_coords[zone.name] = (pixel_x, pixel_y)
            self.zone_sprites_dict[zone.name] = zone_sprite

    def _init_drone_sprites(self) -> None:
        if not self.drones:
            return

        image = self.assets["drone"]
        for drone in self.drones.values():
            self.drones_sprites.add(DroneSprite(image, drone, self.zone_coords, self.zone_sprites_dict))

    def _init_text_sprites(self) -> None:
        self.text_sprite.add(SpriteText(self.manager))

    def _calculate_line_to_draw(self) -> None:
        draw_lines = set()

        for zone_a, neighbors in self.connection_map.items():
            for zone_b in neighbors:
                connection_draw = tuple(sorted([zone_a, zone_b]))

                if connection_draw not in draw_lines:
                    coords_a = self.zone_coords[zone_a]
                    coords_b = self.zone_coords[zone_b]

                    self.lines_to_draw.append((coords_a, coords_b))
                    draw_lines.add(connection_draw)
