import sys
import pygame
from pygame.locals import *


def hello_world():
	pygame.init()
	pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Hello World!")

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()

if __name__ == '__main__':
	hello_world()