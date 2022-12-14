import sys
from random import randrange

import pygame as pg

from Food import Food

from Snake import Snake

vec = pg.math.Vector2



class Game:
    def __init__(self): #Initialisation propriété jeu
        pg.init()
        self.WINDOW_SIZE = 750
        self.TILE_SIZE = 50
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.new_game()

    def draw_grid(self): # Parametres de la grille
        [pg.draw.line(self.screen, [70] * 4, (x, 0), (x, self.WINDOW_SIZE))
         for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, [90] * 3, (0, y), (self.WINDOW_SIZE, y))
         for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

    def new_game(self): # Creation , instance du joueur(snake) et du food
        self.snake = Snake(self)
        self.food = Food(self)

    def update(self):
        self.snake.update()
        pg.display.flip()
        self.clock.tick(50)

    def draw(self):
        self.screen.fill('black')
        self.draw_grid()
        self.food.draw()
        self.snake.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # snake control
            self.snake.control(event)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()