"""
@author: Junkui Zhang
"""
import pygame
import random
from pygame.locals import *
import numpy
import os
import csv
import time

# None for not saving files
FILE_NAME = ""

LENGTH = 800
ENTITIES = 500
WIDTH = 20

# -1 for no field upper bound
FIELD_UPPER_BOUND = -1
FIELD_LOWER_BOUND = 10

MU = 100
SIGMA = 60

THRESHOLD_LOWER_BOUND = 50
THRESHOLD_GROW = 1
# -1 for no threshold upper bound
THRESHOLD_UPPER_BOUND = -1


class Worldgrid:

	def __init__(self, length=LENGTH, population=ENTITIES, width=WIDTH):
		self.length = length
		self.population = population
		self.screen_size = (1600, length + 200)
		self.width = width
		self.po = int(self.length / self.width + 2)

	def generate_world_grid(self):
		grid_length = self.po
		grid_matrix = numpy.zeros((grid_length, grid_length))
		center_index = grid_length // 2
		center_semidiameter = grid_length // 10
		medium_semidiameter = grid_length // 4

		def check_values(value):
			if value < FIELD_LOWER_BOUND:
				value = FIELD_LOWER_BOUND
			if FIELD_UPPER_BOUND != -1:
				if value > FIELD_UPPER_BOUND:
					value = FIELD_UPPER_BOUND
			return value

		for i in range(grid_length):
			if i == 0 or i == grid_length - 1:
				continue
			for j in range(grid_length):
				if j == 0 or j == grid_length - 1:
					continue
				if abs(i - center_index) <= center_semidiameter and abs(j - center_index) <= center_semidiameter:
					v = random.gauss(mu=MU + 300, sigma=SIGMA//3)
					v = check_values(v)
					grid_matrix[i, j] = v
				elif abs(i - center_index) <= medium_semidiameter and abs(j - center_index) <= medium_semidiameter:
					v = random.gauss(mu=MU + 150, sigma=SIGMA//2)
					v = check_values(v)
					grid_matrix[i, j] = v
				else:
					v = random.gauss(mu=MU, sigma=SIGMA)
					v = check_values(v)
					grid_matrix[i, j] = v
		return grid_matrix

	def draw_grid(self):
		grid_matrix = self.generate_world_grid()
		pygame.init()
		screen = pygame.display.set_mode(self.screen_size)
		pygame.display.set_caption("Test")
		grid_length = self.po
		width = self.width
		while True:
			for i in range(grid_length - 2):
				for j in range(grid_length - 2):
					font = pygame.font.SysFont(None, 12)
					num = font.render(str(grid_matrix[i+1, j+1]), 1, (225, 225, 225))
					screen.blit(num, (j*width + width//2, i*width + width//2))
			pygame.display.update()
			time.sleep(60)

	def run(self, entity):
		pygame.init()
		screen = pygame.display.set_mode(self.screen_size)
		pygame.display.set_caption("Society")
		grid_matrix = self.generate_world_grid()
		po = self.po

		if FILE_NAME != "":
			save_data = True
			if not os.path.exists("./Data"):
					os.mkdir("./Data")
			f_name0 = FILE_NAME + "0.csv"
			f_name1 = FILE_NAME + "1.csv"
			f0 = open("./Data/%s" % f_name0, "w", newline="")
			f1 = open("./Data/%s" % f_name1, "w", newline="")
			w0 = csv.writer(f0)
			w1 = csv.writer(f1)
			w0.writerow(["Time", "Alive_num", "Richest", "Poorest", "Gini", "Threshold"])
			w1.writerow(["Time", "ID", "Status", "Field_product", "Welfare", "Threshold"])
		else:
			save_data = False

		def get_gini(ent):
			incomes = list()
			for en in ent:
				if en["state"] == 1:
					# incomes.append(en["welfare"])
					incomes.append(grid_matrix[en["position"][0], en["position"][1]])
				else:
					pass
			if len(incomes) == 0:
				return 0
			average_income = sum(incomes) / len(incomes)
			summation = 0
			for income1 in incomes:
				for income2 in incomes:
					summation += abs(income1 - income2)
			summ = summation / (len(incomes)**2)
			res = summ / (2 * average_income)
			return res

		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					exit()
			pygame.draw.rect(screen, (225, 225, 225), (0, 0, 1002, 1002), 2)
			for n in range(po - 2):
				pos_1 = n * self.width
				pos_2 = n * self.width
				pygame.draw.line(screen, (20, 20, 20), (0, pos_1), (1000, pos_2), 1)
				pygame.draw.line(screen, (20, 20, 20), (pos_1, 0), (pos_2, 1000), 1)
			entity.draw_entities(screen, self.width)
			entity.entities_move(grid_matrix)
			entity.draw_entities(screen, self.width)
			pygame.display.update()

			alive = 0
			rich = 0
			life_time = 0
			poor = 1000000
			rich_i = 0
			rich_j = 0
			for en in entity.entity_list:
				alive += en["state"]
				if en["welfare"] > rich:
					rich = en["welfare"]
					rich_i = en["position"][0]
					rich_j = en["position"][1]
				life_time = max([life_time, en["life_length"]])
				if en["state"] == 1:
					poor = min([en["welfare"], poor])
				if save_data:
					w1.writerow([life_time, en["id"], en["state"], grid_matrix[en["position"][0], en["position"][1]],
						     en["welfare"], entity.threshold])
			print("Alive now: %s" % alive)
			print("Richest: %s" % rich)
			if poor == 1000000:
				poor = 0
			print("Poorest: %s" % poor)
			print("World time is %s" % life_time)
			print("World threshold %s" % entity.threshold)
			product = grid_matrix[rich_i, rich_j]
			print("The richest's field product %s" % product)
			gini = get_gini(entity.entity_list)
			print("The Gini index is %s" % gini)
			print("=="*20)
			if save_data:
				w0.writerow([life_time, alive, rich, poor, gini, entity.threshold])
			if alive == 0:
				print("Game over.")
				if save_data:
					f0.close()
					f1.close()
				break


class Entity:

	def __init__(self, total_num, po, threshold=THRESHOLD_LOWER_BOUND):
		self.population = total_num
		self.po = po
		self.threshold = threshold
		self.entity_list = list()
		if total_num >= (po - 2) ** 2:
			print("You have inefficient grid.")
			raise ValueError
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
			while True:
				row_num = random.choice(range(self.po-2))
				col_num = random.choice(range(self.po-2))
				if m[row_num + 1, col_num + 1] == 0:
					m[row_num + 1, col_num + 1] = 1
					en["position"] = [row_num+1, col_num + 1]
					break
				else:
					pass
		return m

	def draw_entities(self, screen, width):
		for i in range(self.po):
				for j in range(self.po):
					if self.position_matrix[i, j] == 1:
						pygame.draw.rect(screen, (225, 225, 225),
								 (j*width+1, i*width+1, (j+1)*width-1, (i+1)*width-1))
					else:
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
			mid_value = grid_matrix[i, j]
			if right_value > max([down_value, up_value, left_value, mid_value]) and self.position_matrix[i, j+1] != 1:
				self.position_matrix[i, j+1] = 1
				self.position_matrix[i, j] = 0
				en["position"] = [i, j + 1]
			elif down_value > max([right_value, up_value, left_value, mid_value]) and self.position_matrix[i+1, j] != 1:
				self.position_matrix[i+1, j] = 1
				self.position_matrix[i, j] = 0
				en["position"] = [i + 1, j]
			elif up_value > max([down_value, right_value, left_value, mid_value]) and self.position_matrix[i-1, j] != 1:
				self.position_matrix[i-1, j] = 1
				self.position_matrix[i, j] = 0
				en["position"] = [i - 1, j]
			elif left_value > max([down_value, up_value, right_value, mid_value]) and self.position_matrix[i, j-1] != 1:
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
		if THRESHOLD_UPPER_BOUND == -1:
			self.threshold += THRESHOLD_GROW
		elif self.threshold < THRESHOLD_UPPER_BOUND:
			self.threshold += THRESHOLD_GROW
		world_time += 1


if __name__ == '__main__':
	w = Worldgrid()
	e = Entity(w.population, w.po)
	w.run(e)
	# w.draw_grid()