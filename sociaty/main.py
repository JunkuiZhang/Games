import pygame
import random
from pygame.locals import *
import sys


class Worldgrid:

	def __init__(self, length=1000, population=800):
		self.length = length
		self.population = population
		self.screen_size = (1200, 1000)

	def generate_grid(self):
		pygame.init()
		screen = pygame.display.set_mode(self.screen_size)
		pygame.display.set_caption("Sociaty")
		indice1 = range(100)
		indice2 = range(100)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					exit()
			pygame.draw.rect(screen, (225, 225, 225), (0, 0, 1000, 1000), 1)
			for n in range(100):
				pos_1 = n * 10
				pos_2 = n * 10
				pygame.draw.line(screen, (20, 20, 20), (0, pos_1), (1000, pos_2), 1)
				pygame.draw.line(screen, (20, 20, 20), (pos_1, 0), (pos_2, 1000), 1)
			for
			random.gauss(60, 10)
			pygame.display.update()


if __name__ == '__main__':
	w = Worldgrid()
	w.generate_grid()