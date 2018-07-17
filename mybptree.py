#coding:utf-8
import time
import copy

class Node(object):

    def __init__(self, tree, contents=None, ancestry_node=None):
        self.degree = 4
        self.contents = contents if contents else []
        self.children = []
        self.ancestry = ancestry_node
        self.tree = tree
        self.next = None
    
    def _add(self, item):
        self.contents.append(item)
        self.split()
    
    def _add_children(self, children):
        if isinstance(children, Node):
            self.children.append(children)
            children.ancestry = self
        elif isinstance(children, (list, tuple)):
            self.children = children
            for child in children:
                child.ancestry = self
        
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
            self.ancestry.children[-1] = self
        else:
            self.ancestry = Node(self.tree, [self.contents[mid]])
            self.ancestry.children.append(self)
            self.tree.root = self.ancestry
        right_children = self.contents[mid:]
        right_node = Node(self.tree, right_children, self.ancestry)
        self.ancestry.children.append(right_node)
        self.contents = self.contents[:mid]
        self.next = right_node
        if self.children:
            # right_node.children = self.children[mid+1:]
            # for child in right_node.children:
            #     child.ancestry = right_node
            # self.children = self.children[:mid+1]
            # for child in self.children:
            #     child.ancestry = self
            right_node._add_children(self.children[mid+1:])
            self._add_children(self.children[:mid+1])


class BpTree(object):

    def __init__(self):
        self.root = None
    
    def insert(self, item):
        assert isinstance(item, (int, str))
        if not self.root:
            self.root = Node(self, [item])
            return
        self.root.insert(item)


if __name__ == "__main__":
    bt = BpTree()
    bt.insert(5)
    bt.insert(6)
    bt.insert(4)
    bt.insert(3)
    bt.insert(9)
    bt.insert(20)
    bt.insert(19)
    bt.insert(21)
    bt.insert(22)
    # time.sleep(3)
    bt.insert(23)

    # bt.insert(24)
    # bt.insert(25)
    # bt.insert(26)
    print(bt.root.contents)
    # print(bt.root.children[0].contents)
    # print(bt.root.children[1].contents)
    print("++++++ LEVEL 2 ++++++")
    for x in bt.root.children:
        print(x.contents)

    # print(bt.root.children[2].contents)
    # print(bt.root.children[3].contents)

    print("++++++ LEVE 3 +++++++")
    xx = [x for x in bt.root.children[0].children]
    for x in xx:
        print(x.contents)
    
    print("++++++ LEVE 3 +++++++")
    xx = [x for x in bt.root.children[1].children]
    for x in xx:
        print(x.contents)
    
    # print(bt.root.children[0].children[4].contents)
    # print(bt.root.children[1].children)
    # print(bt.root.children[1].children[1].contents)
    
