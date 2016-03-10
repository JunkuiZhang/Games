import pygame
import random
from pygame.locals import *
import numpy
import time


class Worldgrid:

	def __init__(self, length=800, population=50, width=20):
		self.length = length
		self.population = population
		self.screen_size = (1600, length + 200)
		self.width = width
		self.po = int(self.length / self.width + 2)

	def generate_grid(self, entity):
		pygame.init()
		screen = pygame.display.set_mode(self.screen_size)
		pygame.display.set_caption("Sociaty")
		po = self.po
		grid_matrix = numpy.zeros((po, po))
		for i in range(po):
			if i == 0 or i == po - 1:
				continue
			for j in range(po):
				if j == 0 or j == po - 1:
					continue
				v = random.gauss(mu=60, sigma=30)
				if v <= 0:
						v = 0
				elif v >= 100:
						v = 100
				else:
					pass
				grid_matrix[i, j] = v

		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					exit()
			pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1000, 1000))
			pygame.draw.rect(screen, (225, 225, 225), (0, 0, 1000, 1000), 1)
			for n in range(po - 2):
				pos_1 = n * self.width
				pos_2 = n * self.width
				pygame.draw.line(screen, (20, 20, 20), (0, pos_1), (1000, pos_2), 1)
				pygame.draw.line(screen, (20, 20, 20), (pos_1, 0), (pos_2, 1000), 1)
			# for i in range(po-2):
			# 	for j in range(po-2):
			# 		pygame.draw.rect(screen, (grid_matrix[i+1, j+1], grid_matrix[i+1, j+1],
			# 					  grid_matrix[i+1, j+1]),
			# 				 (j*self.width + 1, i*self.width + 1, (j+1)*self.width - 1, (i+1)*self.width - 1))
			entity.draw_entities(screen, self.width)
			# time.sleep(1)
			entity.entities_move(grid_matrix)
			entity.draw_entities(screen, self.width)
			# time.sleep(1)
			pygame.display.update()
			alive = 0
			rich = 0
			life_time = 0
			poores = 10000000000000000000000000000000
			for en in entity.entity_list:
				alive += en["state"]
				rich = max([rich, en["welfare"]])
				life_time = max([life_time, en["life_length"]])
				if en["state"] == 1:
					poores = min([en["welfare"], poores])
			print("Alive now: %s" % alive)
			print("Richest: %s" % rich)
			print("Poorest: %s" % poores)
			print("World time is %s" % life_time)
			print("World threshold %s" % entity.threshold)
			print("=="*20)
			if alive == 0:
				print("Game over.")
				break


class Entity:

	def __init__(self, total_num, po, threshold=30):
		self.population = total_num
		self.po = po
		self.threshold = threshold
		self.entity_list = list()
		for n in range(total_num):
			self.entity_list.append({
				"id": n,
				"state": 1,
				"welfare": 0,
				"life_length": 0,
				"position": [0, 0]
			})
		self.position_matrix = self.get_position_matrix()

	def get_position_matrix(self):
		m = numpy.zeros((self.po, self.po))
		for en in self.entity_list:
			row_num = random.choice(range(self.po-2))
			col_num = random.choice(range(self.po-2))
			while True:
				if m[row_num + 1, col_num + 1] == 0:
					m[row_num + 1, col_num + 1] = 1
					en["position"] = [row_num+1, col_num + 1]
					break
				else:
					row_num = random.choice(range(self.po - 2))
					col_num = random.choice(range(self.po - 2))
			print(en["position"], "===", type(en["position"]))
		return m

	def draw_entities(self, screen, width):
		# for en in self.entity_list:
		# 	if en["state"] == 0:
		# 		continue
		# 	i = en["position"][0]
		# 	j = en["position"][1]
		# 	pygame.draw.rect(screen, (225, 225, 225),
		# 			 (j*width+1, i*width+1, (j+1)*width-1, (i+1)*width-1))
		for i in range(self.po):
				for j in range(self.po):
					if self.position_matrix[i, j] == 1:
						pygame.draw.rect(screen, (225, 225, 225),
								 (j*width+1, i*width+1, (j+1)*width-1, (i+1)*width-1))
					else:
						# pass
						pygame.draw.rect(screen, (0, 0, 0),
								 (j*width+1, i*width+1, (j+1)*width-1, (i+1)*width-1))

	def entities_move(self, grid_matrix):
		world_time = 1
		for en in self.entity_list:
			if en["state"] == 0:
				continue
			i = en["position"][0]
			j = en["position"][1]
			right_value = grid_matrix[i, j+1]
			down_value = grid_matrix[i+1, j]
			up_value = grid_matrix[i-1, j]
			left_value = grid_matrix[i, j-1]
			if right_value >= max([down_value, up_value, left_value]) and self.position_matrix[i, j+1] != 1:
				self.position_matrix[i, j+1] = 1
				self.position_matrix[i, j] = 0
				en["position"] = [i, j + 1]
			elif down_value >= max([right_value, up_value, left_value]) and self.position_matrix[i, j+1] != 1:
				self.position_matrix[i+1, j] = 1
				self.position_matrix[i, j] = 0
				en["position"] = [i + 1, j]
			elif up_value >= max([down_value, right_value, left_value]) and self.position_matrix[i, j+1] != 1:
				self.position_matrix[i-1, j] = 1
				self.position_matrix[i, j] = 0
				en["position"] = [i - 1, j]
			elif left_value >= max([down_value, up_value, right_value]) and self.position_matrix[i, j+1] != 1:
				self.position_matrix[i, j-1] = 1
				self.position_matrix[i, j] = 0
				en["position"] = [i, j - 1]
			else:
				pass
			en["welfare"] = en["welfare"] + grid_matrix[en["position"][0], en["position"][1]] - self.threshold
			en["life_length"] += world_time
			if en["welfare"] < 0:
				en["state"] = 0
				self.position_matrix[en["position"][0], en["position"][1]] = 0
		if self.threshold < 90:
			self.threshold += 1
		world_time += 1


if __name__ == '__main__':
	w = Worldgrid()
	e = Entity(w.population, w.po)
	w.generate_grid(e)