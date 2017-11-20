class Node(object):
	"""docstring for Node"""
	def __init__(self, key):
		super(Node, self).__init__()
		self.key = key
		self.right = None
		self.left = None
		self.color = None
		self.parent = None
			

class RedBlackTree(object):
	"""docstring for RedBlackTree"""
	def __init__(self, root):
		super(RedBlackTree, self).__init__()
		self.root = root

	def left_rotate(T, x):
		y = x.right	
		x.right = y.left  # Turn y's left subtree into x's right subtree
		if y.left is not None:
			y.left.parent = x
		y.parent = x.parent  # Link x's parent to y 
		if x.parent is None:
			T.root = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y
		y.left = x  # Put x on y's left
		x.parent = y

	def right_rotate(T, x):
		y = x.left 
		x.left = y.right  # Turn y's right subtree into x's left subtree
		if y.right is not None:
			y.right.parent = x
		y.parent = x.parent  # Link x's parent to y
		if x.parent is None:
			T.root = y
		elif x == x.parent.right:
			x.parent.right = y
		else:
			x.parent.left = y
		y.right = x # Put x on y's right
		x.parent = y

	def insert(T, z):
		y = None
		x = T.root
		while x is not None:
			y = x
			if z.key < x.key:
				x = x.left
			else: 
				x = x.right
		z.parent = y
		if y is None:
			T.root = z
		elif z.key < y.key: 
			y.left = z
		else:
			y.right = z
		z.left = None
		z.right = None
		z.color = "Red"
		self.insert_fixup(T, z)




		