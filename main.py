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
        self.font_name = pg.font.match_font(FONT_NAME)          # Paramêtrage du font (style d'écriture)
        self.running = True                                     # Comprend que le jeu est lancé

    def new(self):
        """
        Création d'une nouvelle partie
        """
        self.all_sprites = pg.sprite.Group()                    # Création d'un groupe contenant toutes les instances d'entitées
        self.platforms = pg.sprite.Group()                      # Création d'un groupe contenant toues les platformes
        self.player = Player(self)                              # Création du joueur
        p1 = Platform(0, HEIGHT - 25, WIDTH, 25)                # Création de la platforme initiale
        self.all_sprites.add(self.player)                       # Ajout du joueur dans le groupe d'objets
        self.all_sprites.add(p1)                                # Ajout de la platforme initale dans le groupe d'entitées
        self.platforms.add(p1)                                  # Ajout de la platforme initale dans le groupe de platformes
        self.score = -WIDTH                                     # Création du compteur de points (initialisé a -WIDTH : la première platforme)
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
            self.player.position.y = hits[0].rect.top                       # Remet de joueur au dessus de la platforme touchée
            self.player.velocity.y = 0                                      # Réinitialise l'effet de la gravité sur le joueur

        if self.player.position.y >= HEIGHT + PLATFORM_HEIGHT:              # Test pour voir si le joueur est tombé des platformes
            self.playing = False                                            # Arrêt de la partie

        if self.player.position.x >= (2 * WIDTH) / 3:                       # Test si le joueur est a 2/3 de l'écran
            player_velocity = abs(self.player.velocity.x)                   # Sauvegarde la valeur absolue de la vélocité du joueur
            self.player.position.x -= player_velocity                       # Ajoute cette valeur a la "camera" pour avancer fluidement 
            for p in self.platforms:                                        # Vérification de chaque plateforme
                p.rect.x -= int(player_velocity)                            # Déplacement fluide de la plateforme
                if p.rect.right <= 0:                                       # Si elle est en dehors du champ de vision on la supprime
                    self.score += p.width
                    p.kill()

        # Apparition de nouvelles plateformes
        while len(self.platforms) <= 10:
            p = Platform(                                                   # Création d'une nouvelle plateforme
                max(
                    self.player.position.x + 
                    WIDTH * (len(self.platforms) / 3),
                    WIDTH
                ),
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

            self.platforms.add(p)                                               # Ajout de la nouvelle platforme dans le groupe de plateformes
            self.all_sprites.add(p)                                             # Ajout de la nouvelle platforme dans le groupe d'entitées

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
        self.draw_text(                                         # Affichage du score
            f"Score : {max(self.score, 0)}",
            PLATFORM_HEIGHT, WHITE,
            WIDTH / 2, PLATFORM_HEIGHT * 2
        )
        self.all_sprites.draw(self.window)                      # "Dessine" tout ce qui doit être affiché
        pg.display.flip()                                       # Ne change que ce qui a "bougé" entre deux images (frames) pour les fps

    def draw_text(self, text, size, color, x, y):
        """
        Fonction permetant d'afficher du texte de manière simple
        """
        font = pg.font.Font(self.font_name, size)               # Définition de l'objet font
        text_surface = font.render(text, True, color)           # Vrai (True) pour l'anti-aliasing
        text_rect = text_surface.get_rect()                     # Détection de la surface occupée par le texte
        text_rect.midtop = (int(x), int(y))                     # Paramétrage de l'emplacement du texte
        self.window.blit(text_surface, text_rect)               # Affichage du texte

    def show_start_screen(self): pass

    def show_game_over_screen(self): pass

game = Game()                                                   # Création de l'instance game
game.show_start_screen()                                        # Affichage de l'écran de départ

while game.running:
    game.new()                                                  # Création et execution du jeu
    game.show_game_over_screen()                                # Affichage de l'écran de fin

pg.quit()                                                       # Fermeture de la fenêtre
