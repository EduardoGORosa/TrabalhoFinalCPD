import struct
import bisect
import read_csv_save_binary as data

data_file = 'data.bin'
index_file = 'index.bin'
order = 4

class BTreeNode:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf

    def is_full(self, order):
        return len(self.keys) >= (2*order)-1


class BTree:
    def __init__(self, order=3):
        self.root = BTreeNode(True)
        self.order = order
    
    def search(self, key, node = None):
        node = self.root if node == None else None

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i+=1
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)
        elif node.leaf:
            return None
        else:
            return self.search(key, node.children[i])
        
    def split_child(self, x, i):
        t = self.order

        y = x.children[i]

        z = BTreeNode(y.leaf)
        x.children.insert(i + 1, z)

        x.keys.insert(i, y.keys[t - 1])

        z.keys = y.keys[t:(2*t) - 1]
        y.keys = y.keys[0: t - 1]

        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t - 1]
    
    def insert(self, k):
        t = self.order
        root = self.root

        if len(root.keys) == 2 * t - 1:
            new_root = BTreeNode()
            self.root = new_root
            new_root.children.insert(0, root)
            self.split_child(new_root, 0)
            self.insert_non_full(new_root, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        t = self.order
        i = len(x.keys) - 1

        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k

def test_btree():

    btree = BTree(1005)
    games = data.read_from_csv_file()
    for game in games:
        #print(int(game['appid']))
        btree.insert(int(game['appid']))

    print(f"              {len(btree.root.keys)}")
    print(f"{len(btree.root.children[0].keys)}                 {len(btree.root.children[1].keys)}")
    print(f"{len(btree.root.children[0].keys)}                 {len(btree.root.children[1].keys)}")


test_btree()