import random

import matplotlib.pyplot as plt
import numpy as np
from pympler import asizeof

from red_black import RedBlackTree


def plot_ten_thousand_in_order_inserts():
    tree = RedBlackTree()
    black_height = []
    log_height = []

    for i in range(10000):
        tree.insert(i)
        if i % 100 == 0:
            black_height.append(tree.black_height(tree.root))
            log_height.append(2*np.log2(tree.number_of_nodes + 1))

    black_height = np.array(black_height)
    log_height = np.array(log_height)

    plt.title("Black Height of Tree During 10k Insertions")
    plt.plot(black_height, label="Black Height")
    plt.plot(log_height, label = "2 log(n + 1)")
    plt.legend()
    plt.show()

def plot_nodes_considered_during_repeated_search():
    tree = RedBlackTree()
    for i in range(10000):
        tree.insert(i)

    search_list = list(range(10000))
    random.shuffle(search_list)

    nodes_considered = []
    log_considered = []

    for i in search_list[:1000]:
        tree.search(i)
        nodes_considered.append(tree.nodes_considered)
        log_considered.append(2 * np.log2(10000 + 1))

    nodes_considered = np.array(nodes_considered)

    plt.title("All Nodes Considered During 1k Random Searches of 10k Nodes")
    plt.plot(nodes_considered, "ro", label="Nodes Considered", markersize = 0.5)
    plt.plot(log_considered, label="Worst Case log n")
    plt.legend()
    plt.show()

def plot_size_of_tree_in_memory_during_one_hundred_inserts():
    tree = RedBlackTree()
    size_of_tree = []
    n_size = []
    for i in range(100):
        tree.insert(i)
        size_of_tree.append(asizeof.asizeof(tree))
        n_size.append(i*500)

    plt.title("Memory Size of Tree During 100 Inserts")
    plt.plot(size_of_tree, label="Byte Size of Tree")
    plt.plot(n_size, label="Worst Case n Size * 300")
    plt.legend()
    plt.show()

def plot_rotation_time():
    tree = RedBlackTree()
    insert_fixup_times = []
    insert_times = []
    log_times = []

    for i in range(100):
        tree.insert(i)
        insert_fixup_times.append(tree.insert_fixup_time)
        insert_times.append(tree.insert_time)
        log_times.append(0.002 * np.log2(tree.number_of_nodes))

    plt.title("Time (u sec) of Inserting 100 nodes")
    plt.plot(insert_fixup_times, "bo", label="Insert Fixup Time")
    plt.plot(insert_times, "ro", label="Insert Time")
    plt.plot(log_times, label="log n")
    plt.legend()
    plt.show()

def plot_deletion_time():
    tree = RedBlackTree()
    delete_times = []
    delete_fixup_times = []
    log_times = []
    for i in range(100):
        tree.insert(i)

    delete_range = list(range(40, 50))
    for i in delete_range:
        tree.delete_key(i)
        delete_times.append(tree.delete_time)
        delete_fixup_times.append(tree.delete_fixup_time)
        log_times.append(0.002 * np.log2(tree.number_of_nodes))

    plt.title("Time (u) for 10 deletes from a 100 node tree")
    plt.plot(delete_times, "ro", label="Delete Time)")
    plt.plot(delete_fixup_times, "bo", label="Delete Fixup Time")
    plt.plot(log_times, label="log n")
    plt.show()

if __name__ == "__main__":
    #plot_ten_thousand_in_order_inserts()
    #plot_nodes_considered_during_repeated_search()
    #plot_size_of_tree_in_memory_during_one_hundred_inserts()
    #plot_rotation_time()
    plot_deletion_time()