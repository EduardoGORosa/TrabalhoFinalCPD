import struct
import bisect
import read_csv_save_binary as data

data_file = 'data.bin'
index_file = 'index.bin'
inserted = 0


class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t
 
    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)
 
    def insert_non_full(self, x, k):
        global inserted
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1     
            x.keys[i + 1] = k
            inserted += 1  
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
                i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
            if k > x.keys[i]:
                i += 1
            self.insert_non_full(x.child[i], k)
 
    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t - 1]
 
    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)
 
    def search_key(self, k, x=None):
        if x is not None:
            i = 0
            while i < len(x.keys) and k > x.keys[i]:
                i += 1
            if i < len(x.keys) and k == x.keys[i]:
                return (x, i)
            elif x.leaf:
                return None
            else:
                return self.search_key(k, x.child[i]) 
        else:
            return self.search_key(k, self.root)




def main():
    global inserted
    B = BTree(3)
    games = data.read_from_csv_file()
    for i,game in enumerate(games):
        #print(int(game['appid']))
        B.insert(int(game['appid']))
        if int(game['appid']) > 33333:
          break

    B.print_tree(B.root)
    print(inserted)


if __name__ == '__main__':
    main()