#!/usr/bin/env python
# -*- coding: utf8 -*-
from settings import *
from sprites import *
from random import randint
from os import environ, path
import sys


if __name__ != "__main__":
    quit()

# Tentative de chargement de la librairie Pygame, retourne un message d'erreur dans le cas contraire
try: import pygame as pg
except: input("Unable to load the Pygame library, please check that it is properly installed on this computer...")

class Game:
    def __init__(self):
        """
        Initialisation de la fenêtre du jeu:
        """
        pg.init()                                               # Initialisation de Pygame
        pg.mixer.init()                                         # Initialisation du son de Pygame
        environ["SDL_VIDEO_CENTERED"] = '1'                     # Centrage de la fenêtre
        pg.display.set_caption(GAME_TITLE)                      # Titrage de la fenêtre
        self.window = pg.display.set_mode((WIDTH, HEIGHT))      # Affichage de la fenêtre
        self.clock = pg.time.Clock()                            # Définition du chronomètre (pour suivre la fluidité du jeu)
        self.font_name = pg.font.match_font(FONT_NAME)          # Paramêtrage du font (style d'écriture)
        self.load_data()                                        # Chargement des données
        self.running = True                                     # Comprend que le jeu est lancé

    def new(self):
        """
        Création d'une nouvelle partie
        """
        self.all_sprites = pg.sprite.Group()                    # Création d'un groupe contenant toutes les instances d'entitées
        self.platforms = pg.sprite.Group()                      # Création d'un groupe contenant toutes les platformes
        self.clouds = pg.sprite.Group()                         # Création d'un groupe contenant tous les nuages
        self.player = Player(self)                              # Création du joueur
        p1 = Platform(self, 0, HEIGHT - 25, WIDTH, 25)          # Création de la platforme initiale
        self.all_sprites.add(self.player)                       # Ajout du joueur dans le groupe d'objets
        self.all_sprites.add(p1)                                # Ajout de la platforme initale dans le groupe d'entitées
        self.platforms.add(p1)                                  # Ajout de la platforme initale dans le groupe de platformes
        self.score = -WIDTH                                     # Création du compteur de points (initialisé a -WIDTH : la première platforme)
        pg.mixer.music.load(path.join(
            self.snd_directory, 'HAPPY_VICTORY! By HeatleyBros.ogg'
        ))
        self.run()                                              # Lancement de la partie

    def run(self):
        """
        Execution des differentes fonctions nécessaires au fonctionnement du jeu
        C'est ici qu'est située la boucle principale de la partie !
        """
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)                                # Limite l'affichage d'ips (fps) selon les réglages
            self.events()                                       # Écoute les evenements
            self.update()                                       # Met a jour les données du jeu
            self.draw()                                         # Affiche les données du jeu
        pg.mixer.music.fadeout(100)
    
    def update(self):
        """
        Met a jour tout ce qui est affiché (mouvement, apparence etc...)
        """
        self.all_sprites.update()                                           # Met a jour les instances d'objets
        
        # Apparition de nuages en font d'ecran
        while len(self.clouds) <= 3:
            c = Cloud(
                self,
                randint(WIDTH, WIDTH * 2),
                randint(0, int(HEIGHT // 3)),
                randint(PLATFORM_HEIGHT * 5, PLATFORM_HEIGHT * 7),
                randint(PLATFORM_HEIGHT * 3, PLATFORM_HEIGHT * 5)
            )

            pg.sprite.spritecollide(c, self.clouds, True)                   # On supprime le(s) nuage(s) touché(s) par le nouveau nuage
            self.clouds.add(c)
            self.all_sprites.add(c)

        if self.player.position.x >= (2 * WIDTH) / 3:                       # Test si le joueur est a 2/3 de l'écran
            player_velocity = max(                                          # Sauvegarde du maximum entre la valeur absolue de la vélocité du joueur et "2"...
                abs(self.player.velocity.x), 2                              # ...pour bouger la camera quand le joueur passe par la gauche de l'écran
            )
            self.player.position.x -= player_velocity                       # Ajoute cette valeur a la "camera" pour avancer fluidement 
            for p in self.platforms:                                        # Déplacement fluide des plateformes
                p.rect.x -= int(player_velocity)
            for c in self.clouds:
                c.rect.x -= int(player_velocity / 2)                        # Déplacement "fluide" des nuages
        

        # Apparition de nouvelles plateformes
        while len(self.platforms) <= 10:
            p = Platform(
                self,                                                       # Création d'une nouvelle plateforme
                randint(WIDTH, WIDTH * 2),                                  # Coordonée sur l'axe des abscisses
                randint(                                                    # Coordonée sur l'axe des ordonnées
                    min(
                        int(self.player.position.y + PLATFORM_HEIGHT),
                        HEIGHT - PLATFORM_HEIGHT
                    ),
                    max(
                        int(self.player.position.y - PLATFORM_HEIGHT),
                        HEIGHT - PLATFORM_HEIGHT
                    )
                ),
                randint(                                                    
                    PLATFORM_HEIGHT * 2, PLATFORM_HEIGHT * 3),              # Longeur maximum de la platforme
                PLATFORM_HEIGHT                                             # Largeur de la platforme
            )

            self.platforms.add(p)                                           # Ajout de la nouvelle platforme dans le groupe de plateformes
            self.all_sprites.add(p)                                         # Ajout de la nouvelle platforme dans le groupe d'entitées

    def events(self):
        """
        Écoute des actions du joueur
        """
        for event in pg.event.get():                            # Écoute les evenements du joueur
            if event.type == pg.QUIT or (                       # Écoute si le joueur clique sur la croix "rouge" pour fermer le jeu
                event.type == pg.KEYDOWN and
                event.key == pg.K_ESCAPE                        # Écoute si le joueur presse "escape" pour fermer le jeu
                ):                           
                if self.playing:                                
                    self.playing = False                        # Arrête la partie si elle est en cours
                self.running = False                            # Arrête le jeu

    def draw(self):
        """
        Affichage de ce qui est a afficher
        """
        self.window.fill(BACKGROUD_COLOR)                       # Remplie tout l'écran de noir pour repartir d'une image de base
        self.all_sprites.draw(self.window)                      # "Dessine" tout ce qui doit être affiché
        self.draw_text(                                         # Affichage du score
            f"Score : {max(self.score, 0)}",
            PLATFORM_HEIGHT, BLACK,
            WIDTH / 2, PLATFORM_HEIGHT * 2
        )
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

    def show_start_screen(self):
        """
        Fonction affichant l'écran de départ du jeu
        """
        self.window.fill(BACKGROUD_COLOR)                               # Remplissage de la fenêtre en noir
        self.draw_text(GAME_TITLE, 64, WHITE, WIDTH / 2, HEIGHT / 4)    # Affichage du titre du jeu
        self.draw_text(
            "Utilisez les fleches pour bouger !", 32, WHITE, 
            WIDTH / 2, HEIGHT / 2
        )
        self.draw_text(
            "Traversez le bord gauche de l'ecran pour aller a droite.",
            32, WHITE, WIDTH / 2, (HEIGHT / 2) + 32
        )
        self.draw_text(
            f"Highscore : {self.highscore}", 32, WHITE, WIDTH / 2, 
            (HEIGHT / 4) + 64
        )
        self.draw_text(
            "Appuyez sur n'importe quelle touche pour jouer...", 32, 
            WHITE, WIDTH / 2, (HEIGHT / 4) * 3
        )
        pg.display.flip()                                               # Flip pour afficher ce qui est a afficher
        pg.mixer.music.load(path.join(
            self.snd_directory, 'Mii.ogg'
        ))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(loops=-1)
        self.wait_for_key()                                             # Attente qu'une touche soit pressée pour finir la fonction
        pg.mixer.music.fadeout(100)

    def show_game_over_screen(self):
        self.window.fill(BACKGROUD_COLOR)
        self.draw_text("GAME OVER", 64, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(
            f"Score : {max(self.score, 0)}", 32, WHITE, WIDTH / 2, 
            HEIGHT / 2
        )
        self.draw_text(
            f"Appuyez sur n'importe quelle touche pour rejouer...",
            32, WHITE, WIDTH / 2, (HEIGHT / 4) * 3
        )

        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text(
                f"Nouvel highscore : {self.score} !", 32, YELLOW, 
                WIDTH / 2, (HEIGHT / 2) + 64
            )
            with open(SAVE_NAME, 'w') as f:
                f.write(str(self.highscore))
        else:
            self.draw_text(
                f"Highscore : {self.highscore}", 32, YELLOW, 
                WIDTH / 2, (HEIGHT / 2) + 64
            )

        pg.display.flip()                                               # Flip pour afficher ce qui est a afficher
        pg.mixer.music.load(path.join(
            self.snd_directory, 'Mii.ogg'
        ))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(loops=-1)
        # Attente qu'une touche soit pressée pour finir la fonction
        self.wait_for_key()
        pg.mixer.music.fadeout(100)

    def wait_for_key(self):                                             # Définition de la fonction d'attente qu'une touche soit pressée
        while True:
            self.clock.tick(5)                                          # Rafraichissement ralenti (5 images/s)
            for event in pg.event.get():
                if event.type == pg.QUIT or (                           # Fermeture de la fenêtre si le joueur ne veut pas jouer
                event.type == pg.KEYDOWN and
                event.key == pg.K_ESCAPE
                ):
                    self.running = False
                    return
                if event.type == pg.KEYDOWN:                            # Fin de l'attente quand le joueur appuie sur une touche (sauf esc)
                    return

    def load_data(self):                                        # Chargement des données
        self.directory = path.dirname(__file__)                 # Sauvegarde du répertoir du jeu
        img_directory = path.join(                              # Entrée dans le dossier de ressources
            self.directory, 'images'
        )
        self.snd_directory = path.join(
            self.directory, 'sounds'
        )
        self.jump_sound = pg.mixer.Sound(path.join(
            self.snd_directory, 'jump.ogg'
        ))
        self.death_sound = pg.mixer.Sound(path.join(
            self.snd_directory, 'death.ogg'
        ))

        # Chargement de l'highscore
        try:
            with open(SAVE_NAME, 'r') as f:                     # On essaye d'ouvrir le fichier de l'highscore
                try: self.highscore = int(f.read())             # On prend l'highscore
                except: self.highscore = 0                      # Ou on prend 0
        except: self.highscore = 0                              # Si le fichier est introuvable on prend 0

        self.spritesheet = Spritesheet(path.join(               # Chargement du spritesheet du joueur
            img_directory, SPRITESHEET
        ))



game = Game()                                                   # Création de l'instance game
game.show_start_screen()                                        # Affichage de l'écran de départ

while game.running:
    game.new()                                                  # Création et execution du jeu
    if game.running: game.show_game_over_screen()               # Affichage de l'écran de fin

pg.quit()                                                       # Fermeture de la fenêtre
quit()                                                          # Fermeture du programme
