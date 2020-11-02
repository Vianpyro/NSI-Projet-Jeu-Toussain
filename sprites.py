#!/usr/bin/env python
# -*- coding: utf8 -*-
import pygame as pg
from settings import *

if __name__ == "__main__":
    quit()
 
vec = pg.math.Vector2                               # Création d'une variable de type "vecteur en deux dimensions"

class Spritesheet:                                  # Création de la classe Spritesheet qui charge ce(s) dernier(s)
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()        # Sauvegarde du nom du spritesheet

    def get_sub_image(self, x, y, width, height):                   # Découpage d'une image dans le spritesheet
        image = pg.Surface((width, height))                         # Définition de l'apparence de cette image
        image.blit(self.spritesheet, (0, 0), (x, y, width, height)) # Rendement de l'image
        return image


class Player(pg.sprite.Sprite):                     # Création de la classe joueur "enfant" de "sprite"
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)                     # Initialisation de la classe superieur "sprite"
        self.game = game                                    # Sauvegarde du jeu aquel "appartient" le joueur
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.image = self.game.spritesheet.get_sub_image(   # Définition de l'apparence de mon objet (joueur)
            x=60, y=0, width=16, height=27
        )
        self.image = pg.transform.scale(                    # Agrandissement de l'image
            self.image, (40, 64)
        )
        self.image.set_colorkey(BLACK)                      # Supression du "font" noir
        self.rect = self.image.get_rect()                   # Sauvegarde de la surface occupée par mon objet
        self.rect.center = (WIDTH / 2, HEIGHT / 2)          # Centrage du joueur dans la fenêtre
        self.position = vec(WIDTH / 2, HEIGHT / 2)          # Centrage de la position du joueur dans la fenêtre
        self.velocity = vec(0, 0)                           # Définition de la vélocité du joueur a 0x 0y
        self.acceleration = vec(0, 0)                       # Définition de l'accélération du joueur a 0x 0y

    def update(self):
        self.acceleration = vec(0, GRAVITY)                              # A chaque update (frame) on remet l'acceleration laterale a 0 et on ajoute la gravite
        if self.position.y >= HEIGHT + PLATFORM_HEIGHT:                  # Test pour voir si le joueur est tombé des platformes
            self.game.playing = False                                    # Arrêt de la partie
            try: self.game.death_sound.play()
            except: pass

        hits = pg.sprite.spritecollide(self, self.game.platforms, False) # Vérification que le joueur est bien sur une platforme
        keys = pg.key.get_pressed()                                      # Sauvegarde de touches enfoncées par le joueur dans une liste (type set)

        if hits:
            self.position.y = hits[0].rect.top                       # Remet de joueur au dessus de la platforme touchée
            self.velocity.y = 0                                      # Réinitialise l'effet de la gravité sur le joueur
            if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
                self.velocity.y = -PLAYER_JUMP * (1 - GRAVITY)       # On saute si le joueur appuie sur une touche et est en contact avec une platforme
                try: self.game.jump_sound.play()
                except: pass

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acceleration.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acceleration.x = PLAYER_ACCELERATION
            
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION    # Application de la friction au mouvement lateral ; plus on va vite plus on est freiné
        self.velocity += self.acceleration                          # Mouvement de l'objet selon son accélération
        self.position += self.velocity + 0.5 * self.acceleration    # Déplacement de l'objet selon l'équation du mouvement

        # On fait en sorte que le joueur reste toujours dans la fenêtre de jeu
        if self.position.x < 0:
            self.position.x = WIDTH

        self.rect.midbottom = self.position         # Affichage du joueur à sa position


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        pg.sprite.Sprite.__init__(self)                     # Initialisation de la classe superieur "sprite"
        self.game = game
        self.width = width                                  # Sauvegarde de la largeur de la platforme
        self.image = self.game.spritesheet.get_sub_image(   # Définition de l'apparence de mon objet (Platform)
            0, 58, 195, 45
        )
        self.image = pg.transform.scale(                    # Agrandissement de l'image
            self.image, (width, height)
        )
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()                   # Sauvegarde de la surface occupée par mon objet
        self.rect.x = x                                     # Définition de l'abcisse de l'objet
        self.rect.y = y                                     # Définition de l'ordonnée de l'objet

    def update(self):
        if self.rect.right < 0:                                 # Si la platforme sort du cadre on la supprime
            if self.width != WIDTH:
                self.game.score += PLATFORM_MAX_WIDTH - self.width
            self.kill()

class Cloud(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        pg.sprite.Sprite.__init__(self)                     # Initialisation de la classe superieur "sprite"
        self.game = game
        self.width = width                                  # Sauvegarde de la largeur de la platforme
        self.image = self.game.spritesheet.get_sub_image(   # Définition de l'apparence de mon objet (Platform)
            0, 58, 195, 45
        )
        self.image = pg.transform.scale(                    # Agrandissement de l'image
            self.image, (width, height)
        )
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()                   # Sauvegarde de la surface occupée par mon objet
        self.rect.x = x                                     # Définition de l'abcisse de l'objet
        self.rect.y = y                                     # Définition de l'ordonnée de l'objet

    def update(self):
        if self.rect.right < 0 or self.rect.bottom > HEIGHT:
            self.kill()
