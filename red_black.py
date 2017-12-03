class Node(object):
    """Red-Black Tree Node
    - Similar to a binary tree node with color property"""
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None
        self.red = False
        self.p = None

    def __str__(self):
        msg = ("Key: {}\nRed: {}\nLeft: {}\nRight: {}\nParent: {}"
               .format(self.key, self.red, self.left.key, self.right.key, self.p.key))
        if self.p.key is None:
            msg = "(ROOT)\n" + msg
        return msg


class RedBlackTree(object):
    """Non-Modified Red-Black Tree"""
    def __init__(self, create_node=Node):
        self.nil = create_node(None)
        self.root = self.nil
        self.levels = []
        self.number_of_nodes = 0

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.p = x
        y.p = x.p
        if x.p == self.nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.p = y
        x.p = y.p
        if y == self.nil:
            y.p.left = x
        elif y == y.p.right:
            y.p.right = x
        else:
            y.p.left = x
        x.right = y
        y.p = x

    def insert(self, z):
        """Insert z node into a tree"""
        z = Node(z)
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y == self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.red = True
        self.insert_fixup(z)
        self.number_of_nodes += 1

    def insert_fixup(self, z):
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p.red = False
                    y.red = False
                    z.p.p.red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p.red = False
                    z.p.p.red = True
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p.red = False
                    y.red = False
                    z.p.p.red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p.red = False
                    z.p.p.red = True
                    self.left_rotate(z.p.p)
        self.root.red = False

    def search(self, key, x=None):
        if x is None:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def minimum(self, x=None):
        if x is None:
            x = self.root
        if x == self.nil:
            return
        while x.left != self.nil:
            x = x.left
        return x

    def maximum(self, x=None):
        if x is None:
            x = self.root
        if x == self.nil:
            return
        while x.right != self.nil:
            x = x.right
        return x

    def transplant(self, u, v):
        if u.p == self.nil:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def delete_key(self, z):
        node = self.search(z)
        if node == self.nil:
            return False
        self.delete_node(node)
        self.number_of_nodes -= 1
        return True

    def delete_node(self, z):
        y = z
        y_original_color = y.red
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.red
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z, y)
            y.left = z.left
            y.left.p = y
            y.red = z.red
        if not y_original_color:
            self.delete_node_fixup(x)  # Why are we passing NIL here?

    def delete_node_fixup(self, x):
        while x != self.root and not x.red:
            if x == x.p.left:
                w = x.p.right
                if w.red:  # Case 1: x's sibling w is red
                    w.red = False
                    x.p.red = True
                    self.left_rotate(x.p)
                    w = x.p.right
                if not w.left.red and not w.right.red:  # Case 2: x's sibling w is black, and both of w's children are black
                    w.red = True
                    x = x.p
                else:
                    if not w.red:
                        w.left.red = False
                        w.red = True
                        self.right_rotate(w)
                        w = x.p.right
                    w.red = x.p.red  # Case 4: x's sibling w is black, and w's right child is red
                    x.p.red = False
                    w.right.red = False
                    self.left_rotate(x.p)
                    x = self.root
            elif x == x.p.right:
                w = x.p.left
                if w.red:
                    w.red = False
                    x.p.red = True
                    self.right_rotate(x.p)
                    w = x.p.left
                if not w.right.red and not w.left.red:
                    w.red = True
                    x = x.p
                else:
                    if not w.left.red:  # TODO: Is this an else if... or an elif?
                        w.right.red = False
                        w.red = True
                        self.left_rotate(w)
                        w = x.p.left
                    w.red = x.p.red
                    x.p.red = False
                    w.left.red = False
                    self.right_rotate(x.p)
                    x = self.root
        x.red = False

    def in_order_walk(self, root=None, level=0):
        if level == 0:
            root = self.root
            self.levels = []
        if root:
            self.in_order_walk(root.left, level+1)
            self.levels.append([level, root.key])
            self.in_order_walk(root.right, level+1)
        if level == 0:
            self.print_levels()

    def print_levels(self):
        def _find_max_level(levels):
            max_level = 0
            for node in levels:
                if node[0] > max_level:
                    max_level = node[0]
            return max_level

        def _draw_on_screen(levels, max_level):
            print "-----"
            for i in range(max_level+1):
                values = [x[1] for x in levels if x[0] == i]  # Group all nodes at ith level
                print "Level {}: {}".format(i, values)

        levels = self.levels
        max_level = _find_max_level(levels)
        _draw_on_screen(levels, max_level)

    def black_height(self, root):
        """https://stackoverflow.com/questions/13848011/how-to-check-the-black-height-of-a-node-for-all-paths-to-its-descendent-leaves"""
        if root == self.nil:
            return 1

        left_black_height = self.black_height(root.left)
        if left_black_height == 0:
            return left_black_height

        right_black_height = self.black_height(root.right)
        if right_black_height == 0:
            return right_black_height

        if left_black_height != right_black_height:
            return 0
        else:
            if root.red:
                return left_black_height
            return left_black_height + 1
