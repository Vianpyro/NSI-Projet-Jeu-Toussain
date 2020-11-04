#!/usr/bin/env python
# -*- coding: utf8 -*-
if __name__ == "__main__":
    quit()

# Fichiers (Images libres de droit)
SAVE_NAME = 'hscore'
SPRITESHEET = 'spritesheet.png'

# Paramètres d'affichage
FPS = 60
WIDTH = 720
HEIGHT = 480
GAME_TITLE = "Cloud Jumper"
FONT_NAME = "calibri"
BACKGROUD_COLOR = (0, 200, 255)

# Définition de couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)

# Paramètres du jeu
GRAVITY = 0.5
PLATFORM_HEIGHT = 30
PLATFORM_MAX_WIDTH = PLATFORM_HEIGHT * 3
PLATFORMS = 15

# Paramètres du joueur
PLAYER_JUMP = 25
PLAYER_HEIGHT = 50
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.10
