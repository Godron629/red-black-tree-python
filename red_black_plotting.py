import random

import matplotlib.pyplot as plt
import numpy as np
from pympler import asizeof

from red_black import RedBlackTree


def plot_n_thousand_in_order_inserts():
    for j in [(10, 1000), (100, 10000), (1000, 100000)]:
        black_height = []
        log_height = []
        tree = RedBlackTree()
        for i in range(j[1]):
            tree.insert(i)
            if i % j[0] == 0:
                black_height.append(tree.black_height(tree.root))
                log_height.append(2*np.log2(tree.number_of_nodes + 1))
        del tree

        plt.title("Black Height of Tree During {}k Insertions".format(j[1] / 1000))
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
    """Plots byte size in memory of tree object
    during 100 hundred insertions"""
    tree = RedBlackTree()
    size_of_tree = []
    n_size = []
    for i in range(100):
        tree.insert(i)
        size_of_tree.append(asizeof.asizeof(tree))
        n_size.append(i*350)

    plt.title("Memory Size of Tree During 100 Inserts")
    plt.plot(size_of_tree, label="Byte Size of Tree")
    plt.plot(n_size, label="Worst Case n Size * 350")
    plt.legend()
    plt.show()

def plot_insertion_time():
    """Plots microsecond time of inserting 100 nodes into a
    tree (n times), along with log(number of nodes)"""
    n = 1

    insert_fixup_times = return_list_of_n_lists(n)
    insert_times = return_list_of_n_lists(n)
    log_times = return_list_of_n_lists(n)

    for j in range(n):
        tree = RedBlackTree()
        for i in range(100):
            tree.insert(i, time=True)
            insert_fixup_times[j].append(abs(tree.insert_fixup_time))
            insert_times[j].append(abs(tree.insert_time))
            log_times[j].append(0.002* np.log2(tree.number_of_nodes))
        del tree

    insert_times = average_list_of_lists(insert_times)
    insert_fixup_times = average_list_of_lists(insert_fixup_times)
    log_times = average_list_of_lists(log_times)

    plt.title("Mean Time (u sec) of Inserting 100 nodes 10x")
    plt.plot(insert_fixup_times, "bo", label="Insert Fixup Time")
    plt.plot(insert_times, "ro", label="Insert Time")
    plt.plot(log_times, label="log n")
    plt.legend()
    plt.show()

def plot_deletion_time():
    """Plots microsecond time of deleting 15 nodes from
    a tree (n times), also includes log(number of nodes)"""
    n = 1

    list_of_lists = return_list_of_n_lists(n)
    delete_times = return_list_of_n_lists(n)
    delete_fixup_times = return_list_of_n_lists(n)
    log_times = return_list_of_n_lists(n)

    for j in range(n):
        tree = RedBlackTree()
        for i in range(100):
            tree.insert(i)

        delete_range = list(range(40, 65))
        for i in delete_range:
            tree.delete_key(i, time=True)
            delete_times[j].append(abs(tree.delete_time))
            delete_fixup_times[j].append(abs(tree.delete_fixup_time))
            log_times[j].append(0.001 * np.log2(tree.number_of_nodes))

        del tree

    delete_times = average_list_of_lists(delete_times)
    delete_fixup_times = average_list_of_lists(delete_fixup_times)
    log_times = average_list_of_lists(log_times)

    plt.title("Mean Time (u sec) for 25 deletes from a 100 node tree 10x")
    plt.plot(delete_times, "ro", label="Delete Time)")
    plt.plot(delete_fixup_times, "bo", label="Delete Fixup Time")
    plt.plot(log_times, label="log n")
    plt.legend()
    plt.show()

def average_list_of_lists(a):
    """Returns a list of the mean value of
    the ith value in a list of lists"""
    averages = []
    for i in zip(*a):
        averages.append(sum(i) / float(len(i)))
    return averages

def return_list_of_n_lists(n):
    return [[] for x in xrange(n)]

if __name__ == "__main__":
    """Creating all of these graphs can take up to one minute"""
    plot_n_thousand_in_order_inserts()
    plot_nodes_considered_during_repeated_search()
    plot_size_of_tree_in_memory_during_one_hundred_inserts()
    plot_insertion_time()
    plot_deletion_time()