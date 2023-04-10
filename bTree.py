import struct
from bisect import bisect_left
import read_csv_save_binary as data

class BTreeNode:
    def __init__(self, leaf=False):
        self.keys = []
        self.child = []
        self.leaf = leaf

    def insert(self, key, order):
        i = bisect_left(self.keys, key)
        if self.leaf:
            self.keys.insert(i, key)
        else:
            if len(self.child[i].keys) == order - 1:
                self.split_child(i, order)
                if key > self.keys[i]:
                    i += 1
            self.child[i].insert(key, order)

    def split_child(self, i, order):
        y = self.child[i]
        x = BTreeNode(leaf=y.leaf)
        self.child.insert(i+1, x)
        self.keys.insert(i, y.keys[order//2-1])
        x.keys = y.keys[order//2:]
        y.keys = y.keys[:order//2-1]
        if not y.leaf:
            x.child = y.child[order//2:]
            y.child = y.child[:order//2]

    def search(self, key):
        i = bisect_left([k[1] for k in self.keys], key)
        if i < len(self.keys) and self.keys[i][1] == key:
            return self
        elif self.leaf:
            return None
        else:
            return self.child[i].search(key)

class BTree:
    def __init__(self, order):
        self.root = None
        self.order = order

    def insert(self, key):
        if not self.root:
            self.root = BTreeNode(leaf=True)
            self.root.keys.append(key)
        else:
            if len(self.root.keys) == self.order - 1:
                x = BTreeNode()
                x.child.append(self.root)
                x.split_child(0, self.order)
                i = 0 if key < x.keys[0] else 1
                x.child[i].insert(key, self.order)
                self.root = x
            else:
                self.root.insert(key, self.order)

    def search(self, key):
        if not self.root:
            return None
        else:
            return self.root.search(key)