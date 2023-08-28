import colorama, numpy
import sys, msvcrt
from PIL import Image

class display():
	"""class display():
	a class for cli graphics
	"""
	shapes:list = []
	texts:list = []
	_texts:list = texts.copy()
	def __init__(self, width=10, height=10, border_width=1, border_color="white", clear_color="black"):
		self.border_width, self.border_color = border_width, border_color
		self.width, self.height = width, height
		self.pixels = numpy.array([[border_color for y in range(height+border_width*2)] for x in range(width+border_width*2)], dtype='<U7')
		self.pixels[border_width:-border_width, border_width:-border_width] = clear_color
		self._pixels = self.pixels.copy()
		self.clear_color = clear_color
		colorama.init(autoreset=True)
		self.back_to_top()
	def back_to_top(self):
		print(colorama.Cursor.POS(0, 0), end="")
	def get_pixels(self):
		return self.pixels[
			self.border_width:-self.border_width,
			self.border_width:-self.border_width
		]
	def set_pixels(self, data):
		assert len(data) == self.width, f"pixel array width {len(data)} unmatching screen width {self.width}"
		assert len(data[0]) == self.height, f"pixel array height {len(data[0])}(that of first row) unmatching screen height {self.height}"
		self.pixels[
			self.border_width:-self.border_width,
			self.border_width:-self.border_width
		] = data
	def set(self, x, y, val):
		"""def set(self, x, y, val):
		set a pixel with a 1-BASED index
		"""
		assert 0 < x <= self.width and 0 < y <= self.height, f"position {(x, y)} x out of screen coords (0, 0) to {(self.width, self.height)}"
		self.pixels[x-1+self.border_width][y-1+self.border_width] = val
	dot = pixel = set
	def get(self, x, y):
		"""def get(self, x, y):
		get a pixel (using a 1-BASED index)
		"""
		assert 0 < x <= self.width and 0 < y <= self.height, f"position {(x, y)} x out of screen coords (0, 0) to {(self.width, self.height)}"
		return self.pixels[x-1+self.border_width][y-1+self.border_width]
	def clear(self, color=None):
		self.pixels[self.border_width:-self.border_width,self.border_width:-self.border_width] = color or self.clear_color
	def draw_shapes(self):
		[shape.draw(self) for shape in self.shapes]
	def draw_text(self):
		[text.draw(self) for text in self.texts]
	def rect(self, x, y, width, height, color="white"):
		for _x in range(width):
			for _y in range(height):
				if x+_x <= self.width and y+_y <= self.height:
					self.set(x+_x, y+_y, color)
	def get_mouse_pos(self):
		return pyautogui.position()
	def line(self, x0, y0, x1, y1, color, width=1):
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
	def mp_text(self, font, message, column=0, row=32, color="white"):
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
	def _draw_to_cli(self):
		for ix, x in enumerate(self.pixels):
			for iy, y in enumerate(x):
				if self._pixels[ix][iy] != y:
					print(colorama.Cursor.POS(ix, iy)+self.get_obj(y)+" ")


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
