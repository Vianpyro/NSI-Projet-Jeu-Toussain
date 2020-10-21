from settings import *
import pygame as pg
vec = pg.math.Vector2                               # Création d'une variable de type "vecteur en deux dimensions"

class Player(pg.sprite.Sprite):                     # Création de la classe joueur "enfant" de "sprite"
    def __init__(self):
        pg.sprite.Sprite.__init__(self)             # Initialisation de la classe superieur "sprite"
        self.image = pg.Surface((50, 50))           # Définition de la surface de mon objet (joueur)
        self.image.fill(RED)                        # Coloriage de la surface définie
        self.rect = self.image.get_rect()           # Sauvegarde de la surface occupée par mon objet
        self.rect.center = (WIDTH / 2, HEIGHT / 2)  # Centrage du joueur dans la fenêtre
        self.position = vec(WIDTH / 2, HEIGHT / 2)  # Centrage de la position du joueur dans la fenêtre
        self.velocity = vec(0, 0)                   # Définition de la vélocité du joueur a 0x 0y
        self.acceleration = vec(0, 0)               # Définition de l'accélération du joueur a 0x 0y

    def update(self):
        self.acceleration = vec(0, GRAVITY)         # A chaque update (frame) on remet l'acceleration laterale a 0 et on ajoute la gravite
        keys = pg.key.get_pressed()                 # Sauvegarde de touches enfoncées par le joueur dans une liste (type set)
        if keys[pg.K_LEFT]:
            self.acceleration.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acceleration.x = PLAYER_ACCELERATION
            
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION    # Application de la friction au mouvement lateral ; plus on va vite plus on est freiné
        self.velocity += self.acceleration                          # Mouvement de l'objet selon son accélération
        self.position += self.velocity + 0.5 * self.acceleration    # Déplacement de l'objet selon l'équation du mouvement

        # On fait en sorte que le joueur reste toujours dans la fenêtre de jeu
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH

        self.rect.midbottom = self.position         # Affichage du joueur à sa position


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)             # Initialisation de la classe superieur "sprite"
        self.image = pg.Surface((width, height))    # Définition de la surface de mon objet (Platform)
        self.image.fill(WHITE)                      # Coloriage de la surface définie
        self.rect = self.image.get_rect()           # Sauvegarde de la surface occupée par mon objet
        self.rect.x = x                             # Définition de l'abcisse de l'objet
        self.rect.y = y                             # Définition de l'ordonnée de l'objet
