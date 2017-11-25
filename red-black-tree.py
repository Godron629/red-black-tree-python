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
        msg = "Key: {}\nRed: {}\nLeft: {}\nRight: {}\nParent: {}".format(self.key, self.red, self.left.key,
                                                                     self.right.key, self.p.key)
        if self.isNil:
            return "(NIL)"
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


if __name__ == "__main__":
    tree = RedBlackTree()
    tree.insert(5)
    tree.insert(10)
    tree.insert(15)
    tree.insert(1)
    tree.insert(3)

    i = 5