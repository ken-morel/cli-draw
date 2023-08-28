WIDTH =  210
HEIGHT=  54
WIDTH = 200
HEIGHT = 75
import colorama, numpy, pyautogui
from pygame import draw, Surface, PixelArray
import time, asyncio, sys, msvcrt
from PIL import Image
"""  xe0H
xe0k      xe0M
     xe0P"""
class display(list):
	keys = {
		"up": "\xe03"

	}
	chrdown = "\u2584"
	kbhit = key_hitted = msvcrt.kbhit
	getch = waitkey = lambda self, w=msvcrt.getch: w().decode("ansi")
	key_events = {}
	def on_key(self, key):
		def set_e(func, self=self, key=key):
			if isinstance(key, str):
				self.key_events[key] = func
			else:
				for k in key:
					self.key_events[k] = func
			return func
		return set_e
	def key_event_update(self):
		ks = ""
		while self.kbhit():
			ks+=(self.waitkey())
			"""time.sleep(3)
			if key in self.key_events:
				self.key_events[key](key)"""
		print("key----", ks)
	def events(self):
		self.key_event_update()
	clearcolor = "black"
	shapes = []
	border_width = 0
	border_color= "white"
	_pixels = []
	rgb_cols = {
		(True, True, True): "WHITE",
		(True, True, False): "YELLOW",
		(True, False, True): "MAGENTA",
		(False, True, True): "CYAN",
		(True, False, False): "RED",
		(False, True, False): "GREEN",
		(False, False, True): "BLUE",
		(False, False, False): "BLACK",
	}
	def rgb_to_col(self, r, g, b):
		return getattr(colorama.Back, self.rgb_to_name(r, b, b))

	def rgb_to_name(self, r, g, b):
		return self.rgb_cols[(r>128, g>128, b>128)]

	def name_to_col(self, name):
		return getattr(colorama.Back, name.upper())
	def get_obj(self, col):
		if isinstance(col, str):
			return self.name_to_col(col)
		elif isinstance(col, tuple) or isinstance(col, list):
			return self.rgb_to_col(*col)
	def back_to_top(self):
		print(colorama.Cursor.POS(0, 0), end="")
	def draw_to_cli(self):
		for ix, x in enumerate(self.pixels):
			for iy, y in enumerate(x):
				if self._pixels[ix][iy] != y:
					print(colorama.Cursor.POS(ix, iy)+self.get_obj(y)+" ")
	def set(self, x, y, val):
		self.pixels[x-1+self.border_width][y-1+self.border_width] = val
	def get(self, x, y):
		try:
			return self.pixels[x-1+self.border_width][y-1+self.border_width]
		except IndexError:
			return False
	def clear(self, color=None):
		self.pixels[self.border_width:-self.border_width,self.border_width:-self.border_width] = color or self.clearcolor

	def __init__(self, width=WIDTH, height=HEIGHT, border_width=1, border_color="white"):
		self.border_width, self.border_color = border_width, border_color
		self.width, self.height = width, height
		self.pixels = numpy.array([["black" for y in range(height+border_width*2)] for x in range(width+border_width*2)], dtype='<U7')
		self._pixels = self.pixels.copy()
		colorama.init(autoreset=True)
		self.update_mouse()
		self.back_to_top()
		[print(" "*self.width) for x in range(self.height)]
	def update(self):
		self.back_to_top()
		self.clear()
		self.events()
		self.draw_shapes()
		self.draw_borders()
		self.draw_to_cli()
		self._pixels = self.pixels.copy()
	def _update(self):
		self.back_to_top()
		self.events()
		self.draw_shapes()
		self.draw_borders()
		self.draw_to_cli()
		self._pixels = self.pixels.copy()


	dot = set
	pixel = dot
	def draw_shapes(self):
		[shape.draw(self) for shape in self.shapes]
	def draw_borders(self):
		if self.border_width:
			self.pixels[:self.border_width,:] = self.pixels[-self.border_width:,:] = self.border_color
			self.pixels[:,:self.border_width] = self.pixels[:,-self.border_width:] = self.border_color
	def rect(self, x, y, width, height, color="white"):
		for _x in range(width):
			for _y in range(height):
				if x+_x <= self.width and y+_y <= self.height:
					self.set(x+_x, y+_y, color)
	chr_height = 12
	chr_width = 6
	def offset_x(self):
		return self.window.left
	def offset_y(self):
		return self.window.top+25
	def update_mouse(self):
		input("hit enter")
		self.window = pyautogui.getActiveWindow()
	def get_mouse_pos(self):
		return pyautogui.position()
	def get_hover_chr(self):
		mx, my = self.get_mouse_pos()
		ox, oy = self.offset_x(), self.offset_y()
		chr_w, chr_h = self.chr_width, self.chr_height

		posx, posy = mx-ox, my-oy

		return posx//chr_w, posy//chr_h
	def line(self, x0, y0, x1, y1, color, width=1):
		# Line drawing function.  Will draw a single pixel wide line starting at
		# x0, y0 and ending at x1, y1.
		vw = -width//2
		hw = width+vw
		del width
		steep = abs(y1 - y0) > abs(x1 - x0)
		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1
		if x0 > x1:
			x0, x1 = x1, x0
			y0, y1 = y1, y0
		dx = x1 - x0
		dy = abs(y1 - y0)
		err = dx // 2
		if y0 < y1:
			ystep = 1
		else:
			ystep = -1
		while x0 <= x1:
			if steep:
				for ci in range(vw, hw, 1):
					self.pixel(y0, x0+ci, color)
			else:
				for ci in range(vw, hw, 1):
					self.pixel(x0+ci, y0, color)
			err -= dy
			if err < 0:
				y0 += ystep
				err += dx
			x0 += 1
	"""def line(self, x0, y0, x1, y1, color, width=1):
		# Line drawing function.  Will draw a single pixel wide line starting at
		# x0, y0 and ending at x1, y1.
		steep = abs(y1 - y0) > abs(x1 - x0)
		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1
		if x0 > x1:
			x0, x1 = x1, x0
			y0, y1 = y1, y0
		dx = x1 - x0
		dy = abs(y1 - y0)
		err = dx // 2
		if y0 < y1:
			ystep = 1
		else:
			ystep = -1
		while x0 <= x1:
			if steep:
				self.pixel(y0, x0, color)
			else:
				self.pixel(x0, y0, color)
			err -= dy
			if err < 0:
				y0 += ystep
				err += dx
			x0 += 1"""

	def text(self, font, message, column=0, row=32, color="white"):
		'''
		Write `text` on `display` starting on `row` stating in `column` using
	`    font` in `color`

		Args:
			display: The display device to write on
			font: The pyfont module to use
			message: The message to write
			row: Row to start at, defaults to 32
			column: Column to start at, defaults to 0
			color: The color to write in
		'''
		from_x = to_x = pos_x = column
		from_y = to_y = pos_y = row

		for char in [ord(char) for char in message]:
			penup = True
			if 32 <= char <= 127:
				data = bytearray(font.get_ch(char))
				length = data[0]
				left = data[1] - 0x52
				right = data[2] - 0x52
				width = right - left

				for vect in range (3, len(data), 2):
					vector_x = data[vect] - 0x52
					vector_y = data[vect+1] - 0x52

					if vector_x == -50:
						penup = True
						continue

					if not vect or penup:
						from_x = pos_x + vector_x - left
						from_y = pos_y + vector_y
					else:
						to_x = pos_x + vector_x - left
						to_y = pos_y + vector_y

						self.line(from_x, from_y, to_x, to_y, color, width=5)

						from_x = to_x
						from_y = to_y
					penup = False

				pos_x += width
class draw():
	class rect():
		sx=0
		sy=0
		x = 0
		y = 0
		width = 0
		height = 0
		parent = None
		color = 'white'
		def __init__(self, parent, x=1, y=1, w=1, h=1, color="white", sx=0, sy=0):
			self.x, self.y, self.width, self.height = x, y, w, h
			self.sx, self.sy = sx, sy
			self.color = color
			self.parent = parent
			self.parent.shapes.append(self)
		def draw(self, screen=None):
			self.x+=self.sx
			self.y+=self.sy
			(screen or self.parent).rect(self.x, self.y, self.width, self.height, self.color)
		def hovered(self):
			chrpos = self.parent.get_hover_chr()
			pos = []
			[[pos.append((x, y)) for x in range(self.x, self.x+self.width)] for y in range(self.y, self.y+self.height)]
			# print("pos--"+str(chrpos)+" not in "+str(pos))
			# time.sleep(1)
			if chrpos in pos:
				return chrpos[0]-self.x+1, chrpos[1]-self.y+1
			else:
				return False
	class image():
		sx=0
		sy=0
		x = 0
		y = 0
		parent = None
		color = 'white'
		image = []
		def __init__(self, parent, src, x=1, y=1, sx=0, sy=0):
			self.x, self.y = x, y
			self.sx, self.sy = sx, sy
			self.parent = parent
			self.image = Image.open(src)
			self.parent.shapes.append(self)
		def draw(self, screen=None):
			self.x+=self.sx
			self.y+=self.sy

			for _x in range(self.image.width):
				for _y in range(self.image.height):
					self.parent.set(
						self.x+_x,
						self.y+_y,
						self.parent.rgb_to_name(
							*(
								self.image.getpixel((_x, _y))
							)
						)
					)
		def hovered(self):
			chrpos = self.parent.get_hover_chr()
			pos = []
			[[pos.append((x, y)) for x in range(self.x, self.x+self.width)] for y in range(self.y, self.y+self.height)]
			# print("pos--"+str(chrpos)+" not in "+str(pos))
			# time.sleep(1)
			if chrpos in pos:
				return chrpos[0]-self.x+1, chrpos[1]-self.y+1
			else:
				return False

	class pixmap():
		def __init__(self, parent, x, y, width, height, content=None, sx=0, sy=0, default="black"):
			self.parent = parent
			self.x, self.y, self.width, self.height = x, y, width, height
			self.sx, self.sy = sx, sy
			if content:
				self.data = numpy.array(content, dtype='<U7')
			else:
				self.data = numpy.array([[default for y in range(height)] for x in range(width)], dtype='<U7')
			parent.shapes.append(self)
		def draw(self, screen=None):
			self.x+=self.sx
			self.y+=self.sy
			for _x, ax in enumerate(self.data):
				for _y, pix in enumerate(ax):
					self.parent.set(
						self.x+_x,
						self.y+_y,
						pix
					)
		def hovered(self):
			chrpos = self.parent.get_hover_chr()
			pos = []
			[[pos.append((x, y)) for x in range(self.x, self.x+self.width)] for y in range(self.y, self.y+self.height)]
			# print("pos--"+str(chrpos)+" not in "+str(pos))
			# time.sleep(1)
			if chrpos in pos:
				return chrpos[0]-self.x+1, chrpos[1]-self.y+1
			else:
				return False
	class Hrange(pixmap):
		def __init__(self, parent, x, y, max=10, value=10, color="white", size=1, background="black"):
			super().__init__(parent, x, y, max, size, default=background)
			self.color, self.background = color, background
			self.value(value)
		def value(self, val=None):
			if val == None:
				return self._value
			else:
				self._value = val
				self.data[:][:] = self.background
				self.data[:val][:] = self.color
				return self._value



def tennis():
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
		nonlocal pad1, pad2
		pad1.x = pad2.x = pad1.x-1

	@screen.on_key("r")
	def right(key):
		nonlocal pad1, pad2
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

colors = ["red", "green", "blue", "white", "black", "yellow", "cyan", "magenta"]

def live():
	from json import dumps
	from random import randrange
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


def pixmap():
	W, H = 10, 10
	screen = display(W, H, border_width=1)
	m = draw.pixmap(screen, 0, 0, 10, 10)
	m.data[2][:] = "blue"
	screen.update()


def image():
	screen = display()
	if len(sys.argv) > 2:
		img = draw.image(screen, sys.argv[2])
	else:
		img = draw.image(screen, "scr.png")
	screen.update()
	input()
def range_test():
	W, H = 50, 50
	screen = display(W, H, border_width=1, border_color="magenta")
	rng = draw.Hrange(screen, 2, 2)
	for x in range(10):
		rng.value(x)
		screen.update()
		time.sleep(1)
def text_test():
	import pyfonts.astrol as font
	W, H = 150, 50
	screen = display(W, H, border_width=1, border_color="magenta")
	# for i, x in enumerate(range(97, 122+1)):
	# 	screen.text(
	# 		font,
	# 		chr(x)+" "+chr(x-32),
	# 		1,
	# 		25+(25*i),
	# 		"red"
	# 	)
	#screen.line(3, 3, 7, 7, "red", width=5)
	for i, x in enumerate(range(2)):
		screen.text(
			font,
			"a",
			1,
			(25*i),
			"red"
		)
	screen._update()

def snake():
	from random import randrange
	W, H = 100, 50

	screen = display(W, H, border_width=1, border_color="cyan")
	screen.clear_color = "black"
	UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4
	D = DOWN
	FPS = 5
	@screen.on_key("z")
	def up(key):
		nonlocal D, UP
		D = UP

	@screen.on_key("s")
	def down(key):
		nonlocal D, DOWN
		D = DOWN

	@screen.on_key("q")
	def left(key):
		nonlocal D, LEFT
		D = LEFT

	@screen.on_key("d")
	def right(key):
		nonlocal D, RIGHT
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



if __name__ == '__main__':
	if len(sys.argv)>1:
		name = sys.argv[1]
	else:
		name = input("""choose:
		-tennis
		-live
		-image
		-pixmap
		-range
		-text
		-snake
		->""")

	if name == "tennis":
		tennis()
	elif name == "live":
		live()
	elif name == "image":
		image()
	elif name == "pixmap":
		pixmap()
	elif name == "range":
		range_test()
	elif name == "text":
		text_test()
	elif name == "snake":
		snake()
