# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  sprites.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/07 23:22:54 by roandrie        #+#    #+#               #
#  Updated: 2026/03/07 23:31:36 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pygame

PATH = "src/graphics/sprite/"

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, color: str):
        super().__init__()

        self.image = pygame.image.load(f"{PATH}spawn.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
