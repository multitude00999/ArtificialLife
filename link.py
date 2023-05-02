class LINK:
	def __init__(self, linkName, parent, dim, relPos):
		self.linkName = linkName
		self.globalPos = [0,0,0]
		self.relPos = relPos
		self.dim = dim
		self.color = "Blue"
		self.rgba = "0 0 1.0 1"
		self.mass = 1.0
		self.parent = parent
		self.occupied_face = []
		self.isDangling = True


	def setDim(self, l, w, h):
		self.dim = [l, w, h]

	def setGlobalPos(self, x, y, z):
		self.globalPos = [x,y,z]

	def setColor(self, color, rgba):
		self.color = color
		self.rgba = rgba
