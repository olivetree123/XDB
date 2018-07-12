#coding:utf-8

"""
每个索引都有一个 btree 文件
"""
import os
import ctypes

from config import BTREE_DB
from structs import IndexStruct
from utils.functions import to_bytes, db_file_path

class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val


class Tree:
    def __init__(self, database, table, key):
        self.root     = None
        self.key      = key
        self.table    = table
        self.database = database
        self.db_file = db_file_path(BTREE_DB.format(DATABASE=database, TABLE=table, KEY=key))
        self._load_from_file()
    
    def _load_from_file(self):
        if not os.path.exists(self.db_file):
            return None
        with open(self.db_file, "rb") as f:
            content = f.read(ctypes.sizeof(IndexStruct))
            while content:
                index = IndexStruct.from_buffer_copy(content)
                self.add(index)
                content = f.read(ctypes.sizeof(IndexStruct))

    def getRoot(self):
        return self.root

    def add(self, val):
        if not isinstance(val, ctypes.Structure):
            raise Exception("Invalid type, structure expected, but {} found".format(type(val)))
        if(self.root == None):
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if(val.value < node.v.value):
            if(node.l != None):
                self._add(val, node.l)
            else:
                node.l = Node(val)
        else:
            if(node.r != None):
                self._add(val, node.r)
            else:
                node.r = Node(val)

    def find(self, val):
        if(self.root != None):
            return self._find(val, self.root)
        else:
            return None

    def _find(self, val, node):
        if(val == node.v.value):
            return node.v
        elif(val < node.v.value and node.l != None):
            return self._find(val, node.l)
        elif(val > node.v.value and node.r != None):
            return self._find(val, node.r)

    def deleteTree(self):
        # garbage collector will do this for us. 
        self.root = None
    
    def saveTree(self):
        if(self.root != None):
            with open(self.db_file, "w+") as f:
                # 清空文件
                pass
            self._saveTree(self.root)
    
    def _saveTree(self, node):
        if(node != None):
            self._saveTree(node.l)
            with open(self.db_file, "ab+") as f:
                node.v.offset = f.tell()
                f.write(bytes(node.v))
            self._saveTree(node.r)

    def printTree(self):
        if(self.root != None):
            self._printTree(self.root)

    def _printTree(self, node):
        if(node != None):
            self._printTree(node.l)
            print(str(node.v.value) + ' ')
            self._printTree(node.r)

# btree = Tree()

if __name__ == "__main__":
    # tree = Tree()
    tree.add(8)
    tree.add(6)
    tree.add(9)
    tree.add(4)
    tree.add(10)
    tree.add(2)
    tree.printTree()