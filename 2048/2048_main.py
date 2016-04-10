import pygame
from pygame.locals import *


SCREENSIZE = (600, 600)
BLOCKS = 5

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Test")
screen.fill((255, 255, 255))

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
	for i in range(BLOCKS):
		for j in range(BLOCKS):
			pygame.draw.rect(screen, (100, 100, 100), (i*(SCREENSIZE[0]//BLOCKS) + 10, j*(SCREENSIZE[1]//BLOCKS) + 10,
								   (SCREENSIZE[0]//BLOCKS) - 20, (SCREENSIZE[1]//BLOCKS) - 20))
	# pygame.draw.rect(screen, (100, 100, 100), (distance from the left side, distance from the top side,
	# 						height, width))
	pygame.display.update()