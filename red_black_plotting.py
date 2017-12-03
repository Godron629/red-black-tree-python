from red_black import RedBlackTree

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    tree = RedBlackTree()
    for i in range(100):
        tree.insert(i)

        i = 5