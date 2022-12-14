import pygame as pg
class Unit:
    num: int
    x: int
    y: int
    player: int
    link: int
    color: int
    alive: bool
    radius: float
    king: bool
    def __init__(self, num, center, player, link, color, alive, radius, king):
        self.num = num
        self.center = center
        self.player = player
        self.link = link
        self.color = color
        self.alive = alive
        self.radius = radius
        self.king = king

    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        x,y = self.center
        pg.draw.circle(screen, self.color, (x+1.1,y+1), self.radius)