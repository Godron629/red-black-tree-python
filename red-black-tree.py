class Node(object):
    """docstring for Node"""
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None
        self.red = False
        self.parent = None


class RedBlackTree(object):
    """docstring for RedBlackTree"""
    def __init__(self):
        self.nil = Node(None)
        self.root = self.nil

    def left_rotate(self, x):
        y = x.right
        x.right = y.left  # Turn y's left subtree into x's right subtree
        if y.left is not self.nil:
            y.left.parent = x
        y.parent = x.parent  # Link x's parent to y
        if x.parent is self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x  # Put x on y's left
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right  # Turn y's right subtree into x's left subtree
        if y.right is not self.nil:
            y.right.parent = x
        y.parent = x.parent  # Link x's parent to y
        if x.parent is self.nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x # Put x on y's right
        x.parent = y

    def insert(self, z):
        y = self.nil
        x = self.root
        while x is not self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = None
        z.right = None
        z.color = "Red"
        self.insert_fixup(z)

    def insert_fixup(self, z):
        while z.parent.red:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.left_rotate(z.parent.parent)
        self.root.red = False


if __name__ == "__main__":
    tree = RedBlackTree()
    tree.insert(Node(5))