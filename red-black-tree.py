class Node(object):
    """docstring for Node"""
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None
        self.red = False
        self.p = None
        self.isNil = False

    def __str__(self):
        if self.isNil:
            return "(NIL)"
        msg = ("Key: {}\nRed: {}\nLeft: {}\nRight: {}\nParent: {}"
               .format(self.key, self.red, self.left.key, self.right.key, self.p.key))
        if self.p.key is None:
            msg = "(ROOT)\n" + msg
        return msg


class RedBlackTree(object):
    """docstring for RedBlackTree"""
    def __init__(self, create_node=Node):
        self.nil = create_node(None)
        self.nil.isNil = True

        self.root = self.nil

    def left_rotate(self, x):
        y = x.right
        x.right = y.left  # Turn y's left subtree into x's right subtree
        if y.left is not self.nil:
            y.left.p = x
        y.p = x.p  # Link x's parent to y
        if x.p is self.nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x  # Put x on y's left
        x.p = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right  # Turn y's right subtree into x's left subtree
        if y.right is not self.nil:
            y.right.p = x
        y.p = x.p  # Link x's parent to y
        if x.p is self.nil:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x # Put x on y's right
        x.p = y

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

    def insert_fixup(self, z):
        while z.p.red:
            if z.p is z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p.red = False
                    y.red = False
                    z.p.p.red = True
                    z = z.p.p
                else:
                    if z is z.p.right:
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
                    if z is z.p.left:
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
            return self.nil
        while x.left != self.nil:
            x = x.left
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
            self.delete_node_fixup(x)

    def delete_node_fixup(self, x):
        while x != self.root and not x.red:
            if x == x.p.left:
                w = x.p.right
                if w.red:
                    w.red = False
                    x.p.red = True
                    self.left_rotate(x.p)
                    w = x.p.right
                if not w.left.red and not w.right.red:
                    w.red = True
                    x = x.p
                elif not w.red.red:
                    w.left.red = False
                    w.red = True
                    self.right_rotate(w)
                    w = x.p.right
                w.red = x.p.color
                x.p.red = False
                w.right.red = False
                self.left_rotate(x.p)
                x = self.root
            else:
                w = x.p.left
                if w.red:
                    w.red = False
                    x.p.red = True
                    self.right_rotate(x.p)
                    w = x.p.left
                if not w.right.red and not w.left.red:
                    w.red = True
                    x = x.p
                elif not w.red:
                    w.right.red = False
                    w.red = True
                    self.left_rotate(w)
                    w = x.p.left
                w.red = x.p.color
                x.p.red = False
                w.left.red = False
                self.right_rotate(x.p)
                x = self.root
        x.red = False


if __name__ == "__main__":
    tree = RedBlackTree()
    tree.insert(5)
    tree.insert(10)
    tree.insert(15)
    tree.insert(1)
    tree.insert(3)

    print tree.search(99)


    i = 5