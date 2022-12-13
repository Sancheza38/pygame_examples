# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022

@author: richa
"""
import os
import random
from typing import List
from typing import Tuple

import pygame
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile
pygame.init()

# pylint: disable=no-member
LIGHT_CYAN = (85, 255, 255)
LIGHT_MAGENTA = (255, 85, 255)
current_player = LIGHT_CYAN
next_player = LIGHT_MAGENTA

_FONT_PATH = os.path.join("code","hexagonal_tiles","ModernDOS8x8.ttf")
font = pygame.font.Font(_FONT_PATH, 31)
player = font.render("Player 1", False, (0, 170, 170))
nextPlayer = font.render("Player 2", False, (170, 0, 170))



def create_hexagon(position, radius=34.64, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, colour=(255, 255, 255))


def get_random_colour(min_=254, max_=255) -> Tuple[int, ...]:
    """Returns a random RGB colour with each component between min_ and max_"""
    return tuple(random.choices(list(range(min_, max_)), k=3))


def init_hexagons(num_x=17, num_y=14, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    #(159,150)
    leftmost_hexagon = create_hexagon(position=(115,108), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 4 if x % 2 == 1 or flat_top else 2
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for i in range(num_x):
            x, y = hexagon.position  # type: ignore
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    return hexagons


def render(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill(current_player)
    screen.blit(player,(4,5))

    for hexagon in hexagons:
        hexagon.render(screen)
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))
    pygame.display.flip()

def render_mouse_down(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill(current_player)
    screen.blit(player,(4,5))

    for hexagon in hexagons:
        hexagon.render(screen)
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))

    # draw borders around colliding hexagons and neighbours
    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in colliding_hexagons:
        hexagon.render_highlight(screen, border_colour=(255, 255, 255))
    pygame.display.flip()

def changePlayer():
    global current_player, next_player, textsurface, player, nextPlayer
    current_player, next_player, player, nextPlayer = next_player, current_player, nextPlayer, player


def main():
    """Main function"""
    pygame.init()
    mouse_down = False
    screen = pygame.display.set_mode((1280, 960))
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=False)
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                changePlayer()
        for hexagon in hexagons:
            hexagon.update()

        if mouse_down == True:
            render_mouse_down(screen, hexagons)
        else:
            render(screen, hexagons)

        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()
