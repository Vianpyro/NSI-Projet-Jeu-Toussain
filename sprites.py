#!/usr/bin/env python
# -*- coding: utf8 -*-
import pygame as pg
from settings import *
from xml.dom import minidom
from os import path

if __name__ == "__main__":
    quit()
 
vec = pg.math.Vector2                                       # Création d'une variable de type "vecteur en deux dimensions"
doc = minidom.parse(path.join('images', 'spritesheet.xml')) # Création d'une "instance" de mon fichier xml
items = doc.getElementsByTagName('SubTexture')              # Création d'un objet contenant les informations du fichier xml
images = {}
for i in range(len(items)):
    images[items[i].attributes['name'].value.split('.')[0]] = {
        'name': items[i].attributes['name'].value,
        'x': int(items[i].attributes['x'].value),
        'y': int(items[i].attributes['y'].value),
        'width': int(items[i].attributes['width'].value),
        'height': int(items[i].attributes['height'].value)
    }

class Spritesheet:                                  # Création de la classe Spritesheet qui charge ce(s) dernier(s)
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()        # Sauvegarde du nom du spritesheet

    def get_sub_image(self, x, y, width, height):                   # Découpage d'une image dans le spritesheet
        image = pg.Surface((width, height))                         # Définition de l'apparence de cette image
        image.blit(self.spritesheet, (0, 0), (x, y, width, height)) # Rendement de l'image
        return image


class Player(pg.sprite.Sprite):                     # Création de la classe joueur "enfant" de "sprite"
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        pg.sprite.Sprite.__init__(self)                     # Initialisation de la classe superieur "sprite"
        self.game = game                                    # Sauvegarde du jeu aquel "appartient" le joueur
        self.load_images()
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.image = self.idle_frame
        self.rect = self.image.get_rect()                   # Sauvegarde de la surface occupée par mon objet
        self.rect.center = (WIDTH / 2, HEIGHT / 2)          # Centrage du joueur dans la fenêtre
        self.position = vec(WIDTH / 2, HEIGHT / 2)          # Centrage de la position du joueur dans la fenêtre
        self.velocity = vec(0, 0)                           # Définition de la vélocité du joueur a 0x 0y
        self.acceleration = vec(0, 0)                       # Définition de l'accélération du joueur a 0x 0y

    def animate(self):
        now = pg.time.get_ticks()
        if self.velocity.x != 0: self.walking = True
        else: self.walking = False

        if self.velocity.y < 0: self.jumping = True
        else: self.jumping = False

        if not self.walking and not self.jumping:
            self.image = self.idle_frame


        if self.walking:
            if self.jumping:
                if self.velocity.x < 0:
                    self.image = self.jumping_left_frame
                else:
                    self.image = self.jumping_right_frame
            else:
                if now - self.last_update > 180:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walking_left_frames)

                    if self.velocity.x < 0:
                        self.image = self.walking_left_frames[self.current_frame]
                    else:
                        self.image = self.walking_right_frames[self.current_frame]

                    self.rect = self.image.get_rect()

    def load_images(self):
        self.idle_frame = pg.transform.scale(
            self.game.spritesheet.get_sub_image(            # Définition de l'apparence de mon objet (joueur)
                images['front']['x'],
                images['front']['y'],
                images['front']['width'],
                images['front']['height']
            ), (PLAYER_WIDTH, PLAYER_HEIGHT)
        )

        self.jumping_right_frame = pg.transform.scale(
            self.game.spritesheet.get_sub_image(
                images['jump_right']['x'],
                images['jump_right']['y'],
                images['jump_right']['width'],
                images['jump_right']['height']
            ), (PLAYER_WIDTH, PLAYER_HEIGHT)
        )

        self.jumping_left_frame = pg.transform.scale(
            self.game.spritesheet.get_sub_image(
                images['jump_left']['x'],
                images['jump_left']['y'],
                images['jump_left']['width'],
                images['jump_left']['height']
            ), (PLAYER_WIDTH, PLAYER_HEIGHT)
        )

        self.walking_right_frames = [
            pg.transform.scale(
                self.game.spritesheet.get_sub_image(
                    images[f'walk_right_{i + 1}']['x'],
                    images[f'walk_right_{i + 1}']['y'],
                    images[f'walk_right_{i + 1}']['width'],
                    images[f'walk_right_{i + 1}']['height']
                ), (PLAYER_WIDTH, PLAYER_HEIGHT)
            )
            for i in range(2)
        ]

        self.walking_left_frames = [
            pg.transform.scale(
                self.game.spritesheet.get_sub_image(
                    images[f'walk_left_{i + 1}']['x'],
                    images[f'walk_left_{i + 1}']['y'],
                    images[f'walk_left_{i + 1}']['width'],
                    images[f'walk_left_{i + 1}']['height']
                ), (PLAYER_WIDTH, PLAYER_HEIGHT)
            )
            for i in range(2)
        ]

        # Supression du "font" noir
        self.idle_frame.set_colorkey(BLACK)
        self.jumping_right_frame.set_colorkey(BLACK)
        self.jumping_left_frame.set_colorkey(BLACK)
        for a in self.walking_left_frames: a.set_colorkey(BLACK)
        for b in self.walking_right_frames: b.set_colorkey(BLACK)

    def update(self):
        self.animate()
        self.acceleration = vec(0, GRAVITY)                              # A chaque update (frame) on remet l'acceleration laterale a 0 et on ajoute la gravite
        if self.position.y >= HEIGHT + PLATFORM_HEIGHT:                  # Test pour voir si le joueur est tombé des platformes
            self.game.playing = False                                    # Arrêt de la partie
            try: self.game.death_sound.play()
            except: pass

        hits = pg.sprite.spritecollide(self, self.game.platforms, False) # Vérification que le joueur est bien sur une platforme
        keys = pg.key.get_pressed()                                      # Sauvegarde de touches enfoncées par le joueur dans une liste (type set)

        if hits and self.velocity.y > 0:
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
        if abs(self.velocity.x) < 0.1: self.velocity.x = 0

        # On fait en sorte que le joueur reste toujours dans la fenêtre de jeu
        if self.position.x < 0:
            self.position.x = WIDTH

        self.rect.midbottom = self.position         # Affichage du joueur à sa position


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, first_platform=False):
        self._layer = PLATFORM_LAYER
        pg.sprite.Sprite.__init__(self)                     # Initialisation de la classe superieur "sprite"
        self.game = game
        self.width = width                                  # Sauvegarde de la largeur de la platforme
        self.first_platform = first_platform
        self.image = self.game.spritesheet.get_sub_image(   # Définition de l'apparence de mon objet (Platform)
            0, 58, 195, 45
        )
        self.image = pg.transform.scale(    
            self.image, (width, height)
        )
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()                   # Sauvegarde de la surface occupée par mon objet
        self.rect.x = x                                     # Définition de l'abcisse de l'objet
        self.rect.y = y                                     # Définition de l'ordonnée de l'objet

    def update(self):
        if self.rect.right < 0:                             # Si la platforme sort du cadre on la supprime
            if not self.first_platform:
                self.game.score += PLATFORM_MAX_WIDTH - self.width
            self.kill()

class Cloud(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = PLATFORM_LAYER
        pg.sprite.Sprite.__init__(self)                     # Initialisation de la classe superieur "sprite"
        self.game = game
        self.width = width                                  # Sauvegarde de la largeur de la platforme
        self.image = self.game.spritesheet.get_sub_image(   # Définition de l'apparence de mon objet (Platform)
            0, 58, 195, 45
        )
        self.image = pg.transform.scale(    
            self.image, (width, height)
        )
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()                   # Sauvegarde de la surface occupée par mon objet
        self.rect.x = x                                     # Définition de l'abcisse de l'objet
        self.rect.y = y                                     # Définition de l'ordonnée de l'objet

    def update(self):
        if self.rect.right < 0 or self.rect.bottom > HEIGHT:
            self.kill()
