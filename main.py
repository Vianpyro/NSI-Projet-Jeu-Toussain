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
        self.load_hscore()                                      # Chargement (s'il existe) de l'highscore
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
        self.window.fill(BACKGROUD_COLOR)                                 # Remplie tout l'écran de noir pour repartir d'une image de base
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
        self.wait_for_key()                                             # Attente qu'une touche soit pressée pour finir la fonction

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
        self.wait_for_key()                                             # Attente qu'une touche soit pressée pour finir la fonction


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

    def load_hscore(self):                                      # Chargement de l'highscore
        try:
            with open(SAVE_NAME, 'r') as f:                      # On essaye d'ouvrir le fichier
                try: self.highscore = int(f.read())             # On prend l'highscore
                except: self.highscore = 0                      # Ou on prend 0
        except: self.highscore = 0                              # Si le fichier est introuvable on prend 0

game = Game()                                                   # Création de l'instance game
game.show_start_screen()                                        # Affichage de l'écran de départ

while game.running:
    game.new()                                                  # Création et execution du jeu
    if game.running: game.show_game_over_screen()               # Affichage de l'écran de fin

pg.quit()                                                       # Fermeture de la fenêtre
