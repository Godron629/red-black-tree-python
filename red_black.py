import timeit

class Node(object):
    """Red-Black Tree Node
    - Similar to a binary tree node with additional color property"""
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None
        self.red = False
        self.parent = None

    def __str__(self):
        msg = ("Key: {}\nRed: {}\nLeft: {}\nRight: {}\nParent: {}"
               .format(
                   self.key,
                   self.red,
                   self.left.key,
                   self.right.key,
                   self.parent.key
               ))

        if self.parent.key is None:
            msg = "(ROOT)\n" + msg

        return msg


class RedBlackTree(object):
    """Non-Modified Red-Black Tree
    - Introduction to Algorithms 3620 Project
    - Cormen, Thomas H.., et al. Introduction to Algorithms. 3rd ed., MIT Press, 2009."""
    def __init__(self, create_node=Node):
        self.nil = create_node(None)
        self.root = self.nil
        self.levels = []
        self.number_of_nodes = 0
        self.nodes_considered = 0
        self.insert_time = 0
        self.delete_time = 0
        self.insert_fixup_time = 0
        self.delete_fixup_time = 0

    def left_rotate(self, x):
        """
        ...       ...
         x          y
          \   =>   /
           y      x

        """
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        """
        ...       ...
         x          y
          \   <=   /
           y      x

        """
        x = y.left
        y.left = x.right

        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y == self.nil:
            y.parent.left = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, new_node, time=False):
        """Insert new_node into a tree by way of binary search"""
        if time:
            insert_start_time = timeit.timeit()

        new_node = Node(new_node)
        y = self.nil
        x = self.root

        while x != self.nil:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right
        new_node.parent = y
        if y == self.nil:
            self.root = new_node
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node

        new_node.left = self.nil
        new_node.right = self.nil
        new_node.red = True

        if time:
            insert_end_time = timeit.timeit()
            self.insert_time = insert_end_time - insert_start_time
            insert_fixup_start_time = timeit.timeit()

        self.insert_fixup(new_node)

        if time:
            insert_fixup_end_time = timeit.timeit()
            self.insert_fixup_time = insert_fixup_end_time - insert_fixup_start_time
        self.number_of_nodes += 1

    def insert_fixup(self, new_node):
        """Fix potential violations of Red-Black properties
        resulting from insertion of new_node

        Red-Black Properties:
        - 1: Every node is either red or black
        - 2: The root is black
        - 3: Every leaf (NIL) is black
        - 4: If a node is red, then both its children are black
        - 5: For each node, all simple paths from the node to descendant
             leaves contain the same number of black nodes"""

        while new_node.parent.red:
            # Parent of new_node is a left child
            if new_node.parent == new_node.parent.parent.left:
                uncle = new_node.parent.parent.right
                # Case 1: new_node's uncle is red
                # - Color uncle and parent black
                if uncle.red:
                    new_node.parent.red = False
                    uncle.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    # Case 2: new_node's uncle is black and new_node is a right child
                    # - left_rotate and continue as if new_node was its parent
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.left_rotate(new_node)
                    # Case 3: new_node's uncle is black and new_node is a left child
                    # - right_rotate and continue as if new_node was its parent
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.right_rotate(new_node.parent.parent)
            # Parent of new_node is a right child: The same routine as above with L/R reversed
            else:
                uncle = new_node.parent.parent.left
                if uncle.red:
                    new_node.parent.red = False
                    uncle.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.right_rotate(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.left_rotate(new_node.parent.parent)
        self.root.red = False

    def search(self, key, root=None):
        """Binary Search to find key in tree rooted at root"""
        self.nodes_considered = 0

        if root is None:
            root = self.root

        while root != self.nil and key != root.key:
            self.nodes_considered += 1
            if key < root.key:
                root = root.left
            else:
                root = root.right

        return root

    def minimum(self, root=None):
        """Find the minimum node of a tree rooted at root"""
        if root is None:
            root = self.root

        if root == self.nil:
            return
        while root.left != self.nil:
            root = root.left

        return root

    def maximum(self, root=None):
        """Find the maximum node of a tree rooted at root"""
        if root is None:
            root = self.root

        if root == self.nil:
            return
        while root.right != self.nil:
            root = root.right

        return root

    def transplant(self, u, v):
        """Replace subtree rooted at u with subtree rooted at v
        - Used in delete_node"""
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_key(self, key, time=False):
        """Precursor to delete_node, where we search for the node
        and exit appropriately if the node is not found"""
        node = self.search(key)
        if node == self.nil:
            return False
        self.delete_node(node, time=time)
        self.number_of_nodes -= 1
        return True

    def delete_node(self, node, time=False):
        if time:
            delete_node_start = timeit.timeit()

        y = node
        y_original_color = y.red

        if node.left == self.nil:
            x = node.right
            self.transplant(node, node.right)
        elif node.right == self.nil:
            x = node.left
            self.transplant(node, node.left)

        else:
            y = self.minimum(node.right)
            y_original_color = y.red
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.red = node.red

        if time:
            delete_node_end = timeit.timeit()
            self.delete_time = delete_node_end - delete_node_start
            delete_fixup_start = timeit.timeit()

        if not y_original_color:
            self.delete_node_fixup(x)

        if time:
            delete_fixup_end = timeit.timeit()
            self.delete_fixup_time = delete_fixup_end - delete_fixup_start

    def delete_node_fixup(self, node):
        while node != self.root and not node.red:
            # node is a left child
            if node == node.parent.left:
                sibling = node.parent.right
                # Case 1: Sibling  is red
                # - Since w must have black children,
                # -- Switch the color of node's sibling and parent
                # -- Perform left_rotate on nodes parent
                if sibling.red:
                    sibling.red = False
                    node.parent.red = True
                    self.left_rotate(node.parent)
                    sibling = node.parent.right
                # Case 2: Sibling is black, both sibling's children are black
                if not sibling.left.red and not sibling.right.red:
                    sibling.red = True
                    node = node.parent
                else:
                    # Case 3: Sibling is black, and has a red left child and black right child
                    # - Switch the colors of sibling and its left child
                    # - Perform right_rotation on sibling
                    if not sibling.red:
                        sibling.left.red = False
                        sibling.red = True
                        self.right_rotate(sibling)
                        sibling = node.parent.right
                    # Case 4: Sibling is black and sibling's right child is red
                    sibling.red = node.parent.red
                    node.parent.red = False
                    sibling.right.red = False
                    self.left_rotate(node.parent)
                    node = self.root
            # node is a right child, perform the same routine but with L/R exchanged
            elif node == node.parent.right:
                sibling = node.parent.left
                if sibling.red:
                    sibling.red = False
                    node.parent.red = True
                    self.right_rotate(node.parent)
                    sibling = node.parent.left
                if not sibling.right.red and not sibling.left.red:
                    sibling.red = True
                    node = node.parent
                else:
                    if not sibling.left.red:
                        sibling.right.red = False
                        sibling.red = True
                        self.left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.red = node.parent.red
                    node.parent.red = False
                    sibling.left.red = False
                    self.right_rotate(node.parent)
                    node = self.root
        node.red = False

    def in_order_walk(self, root=None, level=0):
        """In-order-walk the binary tree and make a list that
        is an approximate representation of the tree """
        if level == 0:
            root = self.root
            self.levels = []
        if root:
            self.in_order_walk(root.left, level+1)
            self.levels.append([level, root.key])
            self.in_order_walk(root.right, level+1)
        if level == 0:
            self._print_levels()

    def _print_levels(self):
        def __find_max_level(levels):
            max_level = 0
            for node in levels:
                if node[0] > max_level:
                    max_level = node[0]
            return max_level

        def __draw_on_screen(levels, max_level):
            print "-----"
            for i in range(max_level+1):
                values = [x[1] for x in levels if x[0] == i]  # Group all nodes at ith level
                print "Level {}: {}".format(i, values)

        levels = self.levels
        max_level = __find_max_level(levels)
        __draw_on_screen(levels, max_level)

    def black_height(self, root):
        """Find the height of a tree counting only black nodes
        - Source: https://stackoverflow.com/questions/13848011/how-to-check-the-black-height-of-a-node-for-all-paths-to-its-descendent-leaves"""
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
