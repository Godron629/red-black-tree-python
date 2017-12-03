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
        tree.insert_key(5)
        self.assertNode(tree.root, 5)

    def test_insert_one_hundred_keys(self):
        tree = self.tree
        for i in range(100):
            tree.insert_key(i)

        self.assertEqual(tree.number_of_nodes, 100)


    def test_right_rotate(self):
        tree = self.tree

        for i in [3, 5, 2, 1]:
            tree.insert_key(i)

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
            tree.insert_key(i)

        self.assertNode(tree.root, 3)
        self.assertNode(tree.root.left, 1)
        self.assertNode(tree.root.right, 6)
        self.assertNode(tree.root.right.right, 8, red=True)

        tree.left_rotate(tree.root.right)

        self.assertNode(tree.root, 3)
        self.assertNode(tree.root.left, 1)
        self.assertNode(tree.root.right, 8, red=True)
        self.assertNode(tree.root.right.left, 6)



