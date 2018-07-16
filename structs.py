#coding:utf-8
import ctypes

class IndexStruct(ctypes.Structure):
    # 相当于索引
    _fields_ = [
        # ("database", ctypes.c_char * LENGTH),
        # ("table", ctypes.c_char * LENGTH),
        # ("key", ctypes.c_char * LENGTH),
        ("value", ctypes.c_int),
        # ("offset", ctypes.c_int),
        ("data_offset", ctypes.c_int)
    ]