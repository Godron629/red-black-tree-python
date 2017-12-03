from unittest import TestCase
from red_black import RedBlackTree

class TestRedBlackTree(TestCase):
    def assertNode(self, node, key, red=False):
        self.assertEqual(node.key, key)
        self.assertEqual(node.red, red)

    def setUp(self):
        self.tree = RedBlackTree()

    def tearDown(self):
        del self.tree

    def test_insert_one_key(self):
        tree = self.tree
        tree.insert(5)
        self.assertNode(tree.root, 5)

    def test_insert_one_hundred_keys(self):
        tree = self.tree
        for i in range(100):
            tree.insert(i)

        self.assertEqual(tree.number_of_nodes, 100)

    def test_right_rotate(self):
        tree = self.tree

        for i in [3, 5, 2, 1]:
            tree.insert(i)

        root = tree.root
        self.assertNode(root, 3)
        self.assertNode(root.left, 2)
        self.assertNode(root.right, 5)
        self.assertNode(root.left.left, 1, red=True)

        tree.right_rotate(root.left)

        self.assertNode(root, 3)
        self.assertNode(root.left, 1, red=True)
        self.assertNode(root.right, 5)
        self.assertNode(root.left.right, 2)

    def test_left_rotate(self):
        tree = self.tree

        for i in [3, 1, 6, 8]:
            tree.insert(i)

        self.assertNode(tree.root, 3)
        self.assertNode(tree.root.left, 1)
        self.assertNode(tree.root.right, 6)
        self.assertNode(tree.root.right.right, 8, red=True)

        tree.left_rotate(tree.root.right)

        self.assertNode(tree.root, 3)
        self.assertNode(tree.root.left, 1)
        self.assertNode(tree.root.right, 8, red=True)
        self.assertNode(tree.root.right.left, 6)

    def test_minimum_of_tree(self):
        tree = self.tree

        for i in range(1, 51):
            tree.insert(i)

        minimum = tree.minimum()
        self.assertNode(minimum, 1)

        minimum = tree.minimum(tree.root.left)
        self.assertNode(minimum, 1)

        minimum = tree.minimum(tree.root.right)
        self.assertNode(minimum, 17)

    def test_maximum_of_tree(self):
        tree = self.tree

        for i in range(1, 51):
            tree.insert(i)

        maximum = tree.maximum()
        self.assertNode(maximum, 50, red=True)

        maximum = tree.maximum(tree.root.left)
        self.assertNode(maximum, 15)

        maximum = tree.maximum(tree.root.right)
        self.assertNode(maximum, 50, red=True)

    def test_minimum_of_empty_tree(self):
        tree = self.tree
        self.assertEqual(None, tree.minimum())

    def test_maximum_of_empty_tree(self):
        tree = self.tree
        self.assertEqual(None, tree.maximum())

    def test_delete_key_that_doesnt_exist(self):
        tree = self.tree
        self.assertFalse(tree.delete_key(6))

    def test_delete_single_key(self):
        tree = self.tree
        tree.insert(5)
        tree.delete_key(5)
        self.assertEqual(tree.search(5), tree.nil)
        self.assertEqual(tree.number_of_nodes, 0)

    def test_delete_fix_up_case_1(self):
        """This tests case 2 as well but oh well"""
        tree = self.tree
        for i in [2, 3, 7, 9, 5]:
            tree.insert(i)

        tree.root.right.red = True
        tree.root.right.right.red = False
        tree.root.right.left.red = False

        tree.delete_node_fixup(tree.root.left)

        self.assertNode(tree.root, 7)
        self.assertNode(tree.root.left, 3)
        self.assertNode(tree.root.right, 9)
        self.assertNode(tree.root.left.left, 2)
        self.assertNode(tree.root.left.right, 5, red=True)

    def test_random(self):
        tree = self.tree
        for i in [3, 7, 2, 9, 8, 5]:
            tree.insert(i)

        tree.delete_key(3)
        tree.delete_key(2)
        tree.delete_key(7)


        tree.in_order_walk()