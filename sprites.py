import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):                     # Création de la classe joueur "enfant" de "sprite"
    def __init__(self):
        pg.sprite.Sprite.__init__(self)             # Initialisation de la classe superieur "sprite"
        self.image = pg.Surface((50, 50))           # Définition de la surface de mon objet (joueur)
        self.image.fill(YELLOW)                     # Coloriage de la surface définie
        self.rect = self.image.get_rect()           # Sauvegarde de la surface occupée par mon objet
        self.vel_x = 0                              # Définition de la velocité x
        self.vel_y = 0                              # Définition de la velocité y
        self.rect.center = (WIDTH / 2, HEIGHT / 2)  # Centrage du joueur dans la fenêtre

    def update(self):
        self.vel_x = 0                              # A chaque update (frame) on remet la velocité a 0
        keys = pg.key.get_pressed()                 # Sauvegarde de touches enfoncées par le joueur dans une liste (type set)
        if keys[pg.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
        if keys[pg.K_RIGHT]:
            self.vel_x = PLAYER_SPEED
            
        self.rect.x += self.vel_x                   # Mouvement de l'objet sur l'axe des abscisses
        self.rect.y += self.vel_y                   # Mouvement de l'objet sur l'axe des ordonnées
