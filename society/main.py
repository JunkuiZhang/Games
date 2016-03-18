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
ENTITIES = 250
WIDTH = 20

# entity's behavior
# -1 for random assigning
ENTITY_ABILITY = -1
RANDOM_RANGE = [1, 6]

# -1 for no field upper bound
FIELD_UPPER_BOUND = -1
FIELD_LOWER_BOUND = 10

MU = 100
SIGMA = 50

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
		self.field_greatest_product = list()

	def generate_world_grid(self):
		grid_length = self.po
		grid_matrix = numpy.zeros((grid_length, grid_length))
		center_index = grid_length // 2
		center_semidiameter = grid_length // 24
		medium_semidiameter = grid_length // 8

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
					v = random.gauss(mu=10 * MU, sigma=SIGMA//3)
					v = check_values(v)
					grid_matrix[i, j] = v
					self.field_greatest_product.append(v)
				elif abs(i - center_index) <= medium_semidiameter and abs(j - center_index) <= medium_semidiameter:
					v = random.gauss(mu=4.5 * MU, sigma=SIGMA//2)
					v = check_values(v)
					grid_matrix[i, j] = v
					self.field_greatest_product.append(v)
				else:
					v = random.gauss(mu=MU, sigma=SIGMA)
					v = check_values(v)
					grid_matrix[i, j] = v
					self.field_greatest_product.append(v)
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
		max_product = max(self.field_greatest_product)

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
			w1.writerow(["Time", "ID", "Ability", "Status", "Field_product", "Welfare", "Threshold"])
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
			entity.draw_entities(screen, self.width, max_product, grid_matrix)

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
					w1.writerow([life_time, en["id"], en["ability"], en["state"], grid_matrix[en["position"][0], en["position"][1]],
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

			entity.entities_move(grid_matrix)
			pygame.display.update()

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
		if total_num > (po - 2) ** 2:
			print("You have insufficient grid.")
			raise ValueError
		for n in range(total_num):
			self.entity_list.append({
				"id": n,
				"state": 1,
				"ability": ENTITY_ABILITY,
				"welfare": 0,
				"life_length": 0,
				"position": [0, 0]
			})
		self.generate_entities_position()
		self.generate_entities_ability()

	def generate_entities_position(self):
		positions = list()
		positions.append([0, 0])
		for en in self.entity_list:
			row_num = random.choice(range(self.po-2))
			col_num = random.choice(range(self.po-2))
			while [row_num + 1, col_num + 1] in positions:
				row_num = random.choice(range(self.po-2))
				col_num = random.choice(range(self.po-2))
			positions.append([row_num + 1, col_num + 1])
			en["position"] = [row_num + 1, col_num + 1]

	def generate_entities_ability(self):
		if ENTITY_ABILITY != -1:
			pass
		else:
			half_value = RANDOM_RANGE[1] // 2
			for en in self.entity_list:
				index = random.gauss(0, 1)
				if index >= 1.97:
					# with a probability of 0.975
					# only 2.5% of the entities will fall in this class
					en["ability"] = RANDOM_RANGE[1]
				elif index >= 0.2:
					# with a probability of .58
					# that's saying 40% of the entities will fall in this class
					en["ability"] = random.choice(range(half_value + 1, RANDOM_RANGE[1], 1))
				else:
					# the rest 57.5% entities are normal
					en["ability"] = random.choice(range(RANDOM_RANGE[0], half_value + 1, 1))

	def draw_entities(self, screen, width, max_product, grid_matrix):
		positions = list()
		for en in self.entity_list:
			if en["state"] == 0:
				continue
			positions.append(en["position"])
		for i in range(self.po):
				for j in range(self.po):
					v = grid_matrix[i, j] * 255 // max_product
					pygame.draw.rect(screen, (v, v, v),
							 ((j-1)*width, (i-1)*width, j*width, i*width))
					if [i, j] in positions:
						pygame.draw.circle(screen, (234, 103, 83),
								   ((j-1)*width+width//2, (i-1)*width+width//2), width//3)

	def entities_move(self, grid_matrix):
		world_time = 1
		position_list = list()
		total_time = -1
		for en in self.entity_list:
			if en["state"] == 0:
				continue
			position_list.append(en["position"])
			if en["life_length"] > total_time:
				total_time = en["life_length"]
		for en in self.entity_list:
			if en["state"] == 0:
				continue
			i = en["position"][0]
			j = en["position"][1]

			movement_list = list()
			movement_list.append({
				"position": [i, j],
				"value": grid_matrix[i, j]
			})
			for row_num in range(i-en["ability"], i+en["ability"]+1, 1):
				if row_num == i:
					continue
				if row_num > self.po - 1 or row_num < 0:
					continue
				movement_list.append({
					"position": [row_num, j],
					"value": grid_matrix[row_num, j]
				})
			for col_num in range(j-en["ability"], j+en["ability"]+1, 1):
				if col_num == j:
					continue
				if col_num > self.po - 1 or col_num < 0:
					continue
				movement_list.append({
					"position": [i, col_num],
					"value": grid_matrix[i, col_num]
				})

			def find_max(ls):
				max_position = ls[0]["position"]
				max_value = ls[0]["value"]
				for l in ls:
					if l["value"] > max_value and l["position"] not in position_list:
						max_position = l["position"]
				position_list.append(max_position)
				position_list.pop(position_list.index(ls[0]["position"]))
				return max_position

			en["position"] = find_max(movement_list)
			en["welfare"] = en["welfare"] + grid_matrix[en["position"][0], en["position"][1]] - self.threshold
			en["life_length"] += world_time
			if en["welfare"] < 0:
				en["state"] = 0
		if THRESHOLD_UPPER_BOUND == -1:
			if total_time <= 550:
				self.threshold += THRESHOLD_GROW
			else:
				self.threshold += THRESHOLD_GROW * (((total_time - 550)**(1/2))//1)
		elif self.threshold < THRESHOLD_UPPER_BOUND:
			if total_time <= 550:
				self.threshold += THRESHOLD_GROW
			else:
				self.threshold += THRESHOLD_GROW * (((total_time - 550)**(1/2))//1)


if __name__ == '__main__':
	w = Worldgrid()
	e = Entity(w.population, w.po)
	w.run(e)
	# codes blow this line is used for testing
	# w.draw_grid()