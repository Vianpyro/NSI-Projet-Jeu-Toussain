from settings import *
from sprites import *
import pygame as pg
from random import randint
from os import environ
import sys

class Game:
    def __init__(self):
        """
        Initialisation de la fenêtre du jeu:
        """
        pg.init()                                               # Initialisation de Pygame
        environ["SDL_VIDEO_CENTERED"] = '1'                     # Centrage de la fenêtre
        pg.display.set_caption(GAME_TITLE)                      # Titrage de la fenêtre
        self.window = pg.display.set_mode((WIDTH, HEIGHT))      # Affichage de la fenêtre
        self.clock = pg.time.Clock()                            # Définition du chronomètre (pour suivre la fluidité du jeu)
        self.running = True                                     # Comprend que le jeu est lancé

    def new(self):
        """
        Création d'une nouvelle partie
        """
        self.all_sprites = pg.sprite.Group()                    # Création d'un groupe contenant toutes les instances d'objets
        self.platforms = pg.sprite.Group()
        self.player = Player(self)                              # Création du joueur
        p1 = Platform(0, HEIGHT - 25, WIDTH, 25)
        self.all_sprites.add(self.player)                       # Ajout du joueur dans le groupe d'objets
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        self.run()                                              # Lancement de la partie

    def run(self):
        """
        Execution des differentes fonctions nécessaires au fonctionnement du jeu
        C'est ici qu'est située la boucle principale de la partie !
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)                                # Limite l'affichage d'ips (fps) selon les réglages
            self.events()                                       # Écoute les evenements
            self.update()                                       # Met a jour les données du jeu
            self.draw()                                         # Affiche les données du jeu
    
    def update(self):
        """
        Met a jour tout ce qui est affiché (mouvement, apparence etc...)
        """
        self.all_sprites.update()                                           # Met a jour les instances d'objets
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)  # Detecte la collision entre le joueur et les plateformes (False = sans les supprimer)
        if hits:
            self.player.position.y = hits[0].rect.top
            self.player.velocity.y = 0

        if self.player.position.x >= (2 * WIDTH) / 3:                       # Test si le joueur est a 2/3 de l'écran
            player_velocity = abs(self.player.velocity.x)                   # Sauvegarde la valeur absolue de la vélocité du joueur
            self.player.position.x -= player_velocity                       # Ajoute cette valeur a la "camera" pour avancer fluidement 
            for p in self.platforms:                                        # Vérification de chaque plateforme
                p.rect.x -= int(player_velocity)                            # Déplacement fluide de la plateforme
                if p.rect.right <= 0:                                       # Si elle est en dehors du champ de vision on la supprime
                    p.kill()

        # Apparition de nouvelles plateformes
        while len(self.platforms) <= 10:
            p = Platform(                                                       # Création d'une nouvelle plateforme
                randint(WIDTH, WIDTH * 3),
                randint(
                    min(
                        int(self.player.position.y + PLATFORM_HEIGHT),
                        HEIGHT - PLATFORM_HEIGHT
                    ),
                    max(
                        int(self.player.position.y + PLATFORM_HEIGHT),
                        HEIGHT - PLATFORM_HEIGHT
                    )
                ),
                randint(
                    PLATFORM_HEIGHT * 2, 
                    PLATFORM_HEIGHT * 3
                ), PLATFORM_HEIGHT
            )

            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        """
        Écoute des actions du joueur
        """
        for event in pg.event.get():                            # Écoute les evenements du joueur
            if event.type == pg.QUIT:                           # Écoute si le joueur clique sur la croix "rouge" pour fermer le jeu
                if self.playing:                                
                    self.playing = False                        # Arrête la partie si elle est en cours
                self.running = False                            # Arrête le jeu

    def draw(self):
        """
        Affichage de ce qui est a afficher
        """
        self.window.fill(BLACK)                                 # Remplie tout l'écran de noir pour repartir d'une image de base
        self.all_sprites.draw(self.window)                      # "Dessine" tout ce qui doit être affiché
        pg.display.flip()                                       # Ne change que ce qui a "bougé" entre deux images (frames) pour les fps

    def show_start_screen(self): pass

    def show_go_screen(self): pass

game = Game()                                                   # Création de l'instance game
game.show_start_screen()                                        # Affichage de l'écran de départ

while game.running:
    game.new()                                                  # Création et execution du jeu
    game.show_go_screen()                                       # Affichage de l'écran de fin

pg.quit()                                                       # Fermeture de la fenêtre
