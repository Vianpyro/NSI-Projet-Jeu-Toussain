from settings import *
import sys
import pygame as pg
from os import environ

class Game:
    def __init__(self):
        pg.init()
        environ["SDL_VIDEO_CENTERED"] = '1'
        pg.display.set_caption(GAME_TITLE)
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.run()

    def run(self):
        self.playing = True

    def exit(self):
        self.playing = False
        pg.quit()
        sys.exit()

game = Game()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            game.exit()