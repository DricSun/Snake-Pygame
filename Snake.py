import sys
from random import randrange

import pygame as pg

vec = pg.math.Vector2


class Snake:
    def __init__(self, game): #Initialisation propriété serpent
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 15, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.range = self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size
        self.rect.center = self.get_random_position()
        self.direction = vec(0, 0)
        self.step_delay = 100 # milliseconds
        self.time = 0
        self.length = 1
        self.segments = []
        self.directions = {pg.K_z: 1, pg.K_s: 1, pg.K_q: 1, pg.K_d: 1}

    def control(self, event): # Commande
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_z and self.directions[pg.K_z]: # Commande haut
                self.direction = vec(0, -self.size)
                self.directions = {pg.K_z: 1, pg.K_s: 0, pg.K_q: 1, pg.K_d: 1}

            if event.key == pg.K_s and self.directions[pg.K_s]: #Commande Bas
                self.direction = vec(0, self.size)
                self.directions = {pg.K_z: 0, pg.K_s: 1, pg.K_q: 1, pg.K_d: 1}

            if event.key == pg.K_q and self.directions[pg.K_q]: #Commande Gauche
                self.direction = vec(-self.size, 0)
                self.directions = {pg.K_z: 1, pg.K_s: 1, pg.K_q: 1, pg.K_d: 0}

            if event.key == pg.K_d and self.directions[pg.K_d]: # Commande Droite
                self.direction = vec(self.size, 0)
                self.directions = {pg.K_z: 1, pg.K_s: 1, pg.K_q: 0, pg.K_d: 1}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_random_position(self):
        return [randrange(*self.range), randrange(*self.range)]

    def check_borders(self): # Sortie D'ecran
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()

    def check_food(self): # Position de la food
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.length += 1

    def check_selfeating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            self.game.new_game()

    def check_width_snake(self): # Verification de la longeur du snake
        if len(self.segments) > 25:
            self.game.new_game()

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self): # Déclaration des fonctionnalités
        self.check_selfeating()
        self.check_borders()
        self.check_food()
        self.move()
        self.check_width_snake()

    def draw(self):
        [pg.draw.rect(self.game.screen, 'white', segment) for segment in self.segments]