import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))           # Définition de la surface de mon objet (joueur)
        self.image.fill(YELLOW)                     # Coloriage de la surface définie
        self.rect = self.image.get_rect()           # Sauvegarde de la surface occupée par mon objet
        self.vec_x = 0                              # Définition du vecteur directeur x
        self.vec_y = 0                              # Définition du vecteur directeur y

    def update(self):
        self.vec_x = 0                              # A chaque update (frame) on remet le vecteur a 0
        keys = pg.key.get_pressed()                # Sauvegarde de touches enfoncées par le joueur dans une liste (type set)
        if keys[pg.K_LEFT]:
            self.vec_x = -PLAYER_SPEED
        if keys[pg.K_RIGHT]:
            self.vec_x = PLAYER_SPEED
            
        self.rect.x += self.vec_x                   # Mouvement de l'objet sur l'axe des abscisses
        self.rect.y += self.vec_y                   # Mouvement de l'objet sur l'axe des ordonnées
