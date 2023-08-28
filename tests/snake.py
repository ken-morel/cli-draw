from random import randrange
from cli_draw import display
W, H = 100, 50

screen = display(W, H, border_width=1, border_color="cyan")
screen.clear_color = "black"
UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4
D = DOWN
FPS = 5
@screen.on_key("z")
def up(key):
	global D, UP
	D = UP

@screen.on_key("s")
def down(key):
	global D, DOWN
	D = DOWN

@screen.on_key("q")
def left(key):
	global D, LEFT
	D = LEFT

@screen.on_key("d")
def right(key):
	global D, RIGHT
	D = RIGHT
L = 3
snake = [(5, 5), (5, 6), (5, 7)]
food = (20, 20)
while True:
	a, b = snake[-1]
	if D == UP:
		snake.append((a, b-1))
	elif D == DOWN:
		snake.append((a, b+1))
	elif D == LEFT:
		snake.append((a-1, b))
	elif D == RIGHT:
		snake.append((a+1, b))
	x, y = snake[-1]
	snake = snake[-3:]


	if ((x, y) in snake[:-1]) or not((0<x<W) and (0<y<H)):
		screen.clear("red")
		screen._update()
		break

	if (x, y) == food:
		L+=1
		while food in snake:
			food = (randrange(5, 45), randrange(5, 45))

	screen.clear()
	for p in snake:
		screen.pixel(*p, "green")

	screen.pixel(*food, "blue")

	screen._update()

	time.sleep(1/FPS)


