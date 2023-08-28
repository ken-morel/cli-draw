direction = "r"
PAD_WIDTH = 10
BALL_HEIGHT = 2
W, H = 150, 30
FPS = 5
screen = display(W, H, border_width=1, border_color="blue")

pad1 = draw.rect(screen, 1, 2, PAD_WIDTH, 2, "red")
pad2 = draw.rect(screen, 1, H-1, PAD_WIDTH, 2, "red")

ball = draw.rect(screen, 2, 20, 3, BALL_HEIGHT, "green", sx=1, sy=1)

@screen.on_key("l")
def left(key):
	global pad1, pad2
	pad1.x = pad2.x = pad1.x-1

@screen.on_key("r")
def right(key):
	global pad1, pad2
	pad1.x = pad2.x = pad1.x+1

i = 0
c = 0
while True:
	i+=1
	try:
		if ball.x == W or ball.x == 1:
			ball.sx = -ball.sx

		if ball.y <= pad1.y+2 or ball.y >= pad2.y-2:
			if (pad1.x <= ball.x) and (ball.x <= pad1.x+pad1.width):
				ball.sy = -ball.sy
		"""if pos := (pad1.hovered() or pad1.hovered()):
			x = pos[0] - PAD_WIDTH//2
			if x>0:
				pad1.sx = pad2.sx = 1
			else:
				pad1.sx = pad2.sx = -1
		else:
			pad1.sx = pad2.sx = 0"""
		if ball.y<=pad1.y or ball.y >= pad2.y:
			screen.clear("red")
			screen._update()
			input()
			break

		screen.update()
		time.sleep(1/FPS)
	except KeyboardInterrupt:
		return
