#coding:utf-8

"""
索引
"""
import os
import ctypes

from btree import Tree
from structs import IndexStruct
from config import DATA_META_DB, LENGTH
from utils.functions import to_bytes, db_file_path


# class IndexStruct(ctypes.Structure):
#     # 相当于索引
#     _fields_ = [
#         ("database", ctypes.c_char * LENGTH),
#         ("table", ctypes.c_char * LENGTH),
#         ("key", ctypes.c_char * LENGTH),
#         ("value", ctypes.c_int),
#         ("offset", ctypes.c_int),
#         ("data_offset", ctypes.c_int)
#     ]


class Index(object):

    def __init__(self, database, table, key):
        self.key = key
        self.table = table
        self.database = database
        self.btree = Tree(self.database, self.table, self.key)
        self.db_file = db_file_path(DATA_META_DB)

    def create(self, value, data_offset):
        # key      = to_bytes(key)
        value    = to_bytes(value)
        # table    = to_bytes(table)
        # database = to_bytes(database)
        index = IndexStruct()
        # index.database = self.database
        # index.table = self.table
        # index.key = self.key
        index.value = value
        index.offset = 0
        index.data_offset = data_offset
        self.btree.add(index)
        self.btree.saveTree()
        # with open(self.db_file, "ab+") as f:
        #     index.offset = f.tell()
        #     f.write(bytes(index))
    
    def get(self, value):
        # if not os.path.exists(self.db_file):
        #     return None
        # key      = to_bytes(key)
        # value    = to_bytes(value)
        # table    = to_bytes(table)
        # database = to_bytes(database)
        index = self.btree.find(value)
        # index = None
        # with open(self.db_file, "rb") as f:
        #     content = f.read(ctypes.sizeof(IndexStruct))
        #     while content:
        #         index = IndexStruct.from_buffer_copy(content)
        #         if index.database == database and index.table == table and index.key == key and index.value == value:
        #             break
        #         content = f.read(ctypes.sizeof(IndexStruct))
        #         index = None
        return index
