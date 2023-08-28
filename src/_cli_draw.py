

"""  xe0H
xe0k      xe0M
     xe0P"""
class display(list):
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






	def get_hover_chr(self):
		mx, my = self.get_mouse_pos()
		ox, oy = self.offset_x(), self.offset_y()
		chr_w, chr_h = self.chr_width, self.chr_height

		posx, posy = mx-ox, my-oy

		return posx//chr_w, posy//chr_h
	
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


class draw:
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