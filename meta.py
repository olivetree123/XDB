#coding:utf-8

"""
元数据
"""
import os
import ctypes

from config import DB_META_DB, LENGTH
from utils.functions import to_bytes, db_file_path

class MetaStruct(ctypes.Structure):
    # table 元数据
    _fields_ = [
        ("database", ctypes.c_char * LENGTH),
        ("table", ctypes.c_char * LENGTH),
        ("primary_key", ctypes.c_char * LENGTH),
        ("columns", ctypes.c_char * LENGTH),
        ("auto_pk_value", ctypes.c_int),
        ("offset", ctypes.c_int)
    ]

class DBMeta(object):

    def __init__(self):
        self.database = DB_META_DB
        self.db_file = db_file_path(self.database)
    
    def create(self, database, table, primary_key, columns):
        table       = to_bytes(table)
        columns     = to_bytes(columns)
        database    = to_bytes(database)
        primary_key = to_bytes(primary_key)

        meta = MetaStruct()
        meta.database = database
        meta.table = table
        meta.primary_key = primary_key
        meta.columns = columns
        meta.auto_pk_value = 0
        with open(self.db_file, "ab+") as f:
            meta.offset = f.tell()
            f.write(bytes(meta))
        
    def get(self, database, table):
        if not os.path.exists(self.db_file):
            return None
        table = to_bytes(table)
        database = to_bytes(database)
        meta = None
        with open(self.db_file, "rb") as f:
            content = f.read(ctypes.sizeof(MetaStruct))
            while content:
                meta = MetaStruct.from_buffer_copy(content)
                if meta.database == database and meta.table == table:
                    break
                content = f.read(ctypes.sizeof(MetaStruct))
                meta = None
        return meta
    
    def get_next_pk(self, database, table):
        meta = self.get(database, table)
        meta.auto_pk_value = meta.auto_pk_value + 1 if meta else 1
        with open(self.db_file, "rb+") as f:
            f.seek(meta.offset)
            f.write(bytes(meta))
        return meta.auto_pk_value
    