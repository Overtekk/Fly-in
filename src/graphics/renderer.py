# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 22:18:37 by roandrie        #+#    #+#               #
#  Updated: 2026/03/07 23:08:30 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pygame

from typing import Dict

from src.object.zone import Zone

class Renderer():
    def __init__(self, zones: Dict[str, Zone]) -> None:
        self.zones = zones

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True

    def run_renderer(self) -> None:
        while self.running:

            # Quit the program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
