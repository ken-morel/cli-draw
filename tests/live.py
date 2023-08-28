from json import dumps
from random import randrange
from cli_draw import display
W, H = 140, 40
BW = 1
FPS = 1
screen = display(W, H, border_width=BW, border_color="blue")
board = [["white" if y else "black" for y in numpy.random.randint(0, 2, H)] for x in range(W)]
# p = [
# 	(3, 3),(4, 3),
# 	(3, 4),(4, 4),
# 	(3, 5),(4, 5),

# 	(30, 3),
# 	(30, 4),
# 	(30, 5),

# 	(40, 4),(41, 4),
# ]
# for pi in p:
# 	screen.set(*pi, "white")

# i = 0
while True:
	# print(len(screen.pixels), "------", len(screen.pixels[0]))
	# time.sleep(0.1)
	screen.pixels[BW:-BW, BW:-BW] = board
	screen._update()
	board = screen.pixels.copy()[BW:-BW, BW:-BW]
	# print(i:=i+1)
	for x in range(W):
		for y in range(H):
			c = [
				screen.get(x-1, y),#left
				screen.get(x, y-1),#top
				screen.get(x+1, y),#right
				screen.get(x, y+1),#bottom

				screen.get(x-1, y-1),#left-top
				screen.get(x-1, y+1),#left-bottom
				screen.get(x+1, y-1),#right-top
				screen.get(x+1, y+1),#right-bottom
			]
			c = c.count("white")
			# print("_"*c+("|||||" if c == 8 else ""))
			MIN = 1
			MAX= 3
			if screen.get(x, y) == "white":
				if c > MAX:
					board[x][y] =  "black"
				elif c < MIN:
					board[x][y] =  "black"

			elif screen.get(x, y) == "black":
				if c >= MIN and c <= MAX:
					board[x][y] =  "white"



