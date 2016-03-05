import SimpleGUICS2Pygame.simpleguics2pygame as game
import random

cards = [0, 1, 2, 3, 4, 5, 6, 7] + [0, 1, 2, 3, 4, 5, 6, 7]
turns = 0
unsee = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
seen = []
exposed = []


def new_game():
	global state, turns, unsee, seen, exposed
	turns = 0
	unsee = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
	seen = []
	exposed = []
	state = 0
	random.shuffle(cards)
	l.set_text("Turns = %s" % turns)


def mouseclick(pos):
	global state, exposed, turns
	n = pos[0] // 50
	if state == 0:
		exposed.append(n)
		turns = 1
		state = 1
	elif state == 1:
		if unsee[n] == unsee.index(exposed[0]):
			turns -= 1
		turns += 1
		exposed.append(n)
		state = 2
	else:
		if exposed[0] == exposed[1]:
			if unsee[n] != exposed[0]:
				turns += 1
			exposed.pop(1)
			exposed.append(n)
		elif cards[exposed[0]] == cards[exposed[1]]:
			seen.append(exposed[0])
			seen.append(exposed[1])
			exposed = [n]
			state = 1
			turns += 1
		elif unsee[n] not in exposed:
			exposed = [n]
			turns += 1
			state = 1
		else:
			pass


def draw(canvas):
	a = 0
	l.set_text("Turns = %s" % turns)
	for num in cards:
		canvas.draw_text(str(num), [5 + 50 * a, 78], 80, "White")
		a += 1
	for n in unsee:
		if n not in seen and n not in exposed:
			canvas.draw_polygon([[50 * n, 0], [50 * (n + 1), 0], [50 * (n + 1), 100], [50 * n, 100]], 2,
					    line_color="Red", fill_color="Red")
		canvas.draw_line([50 * (n + 1), 0], [50 * (n + 1), 100], line_width=5, line_color="Black")


frame = game.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game, 200)
l = frame.add_label("Turns = %s" % turns)

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

new_game()
frame.start()