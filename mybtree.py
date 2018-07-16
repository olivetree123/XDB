#coding:utf-8
import time

class Node(object):

    def __init__(self, tree, contents=None, ancestry_node=None):
        self.degree = 4
        self.contents = contents if contents else []
        self.children = []
        self.ancestry = ancestry_node
        self.tree = tree
    
    def _add(self, item):
        self.contents.append(item)
        self.split()
        
    def insert(self, item):
        i = 0
        while i < len(self.contents):
            if item < self.contents[i]:
                break
            i += 1
        if not self.children:
            self.contents.insert(i, item)
            self.split()
        else:
            i = len(self.contents) - 1 if i >= len(self.contents) else i
            i = i+1 if item > self.contents[i] else i
            child = self.children[i]
            child.insert(item)
    
    def split(self):
        if len(self.contents) < self.degree:
            return
        mid = len(self.contents) // 2
        if self.ancestry:
            self.ancestry._add(self.contents[mid])
        else:
            self.ancestry = Node(self.tree, [self.contents[mid]])
            self.ancestry.children.append(self)
            self.tree.root = self.ancestry
        right_children = self.contents[mid+1:]
        right_node = Node(self.tree, right_children, self.ancestry)
        self.ancestry.children.append(right_node)
        self.contents = self.contents[:mid]


class BTree(object):

    def __init__(self):
        self.root = None
    
    def insert(self, item):
        assert isinstance(item, (int, str))
        if not self.root:
            self.root = Node(self, [item])
            return
        self.root.insert(item)


if __name__ == "__main__":
    bt = BTree()
    bt.insert(5)
    bt.insert(6)
    bt.insert(4)
    bt.insert(3)
    # time.sleep(10)
    bt.insert(9)
    bt.insert(20)
    bt.insert(19)
    bt.insert(21)
    bt.insert(15)
    bt.insert(22)
    bt.insert(23)
    bt.insert(24)
    bt.insert(25)
    bt.insert(26)
    print(bt.root.contents)
    print(bt.root.children)
    print(bt.root.children[0].contents)
    print(bt.root.children[1].contents)
    # print(bt.root.children[2].contents)
    # print(bt.root.children[3].contents)
    print(bt.root.children[0].children[0].contents)
