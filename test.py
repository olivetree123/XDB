#coding:utf-8
import ctypes

from index import Index
from meta import DBMeta
from utils.functions import to_bytes

class BucketStruct(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_int),
        ("name", ctypes.c_char * 50),
        ("public", ctypes.c_bool)
    ]


class Bucket(object):

    def __init__(self):
        self.database = "hista"
        self.table = "bucket"
        self.primary_key = "id"
        self.meta  = DBMeta()
        self.index = Index(self.database, self.table, self.primary_key)
        self.db_file = "hista.db"
        r = self._is_table_exists()
        if not r:
            print("table does not exist, create it now.")
            self.create_table()
    
    def _is_table_exists(self):
        meta = self.meta.get(database=self.database, table=self.table)
        r = True if meta else False
        return r
        
    def add(self, name, public):
        pk_value = self.meta.get_next_pk(database=self.database, table=self.table)
        bucket = BucketStruct()
        bucket.id     = pk_value
        bucket.name   = to_bytes(name)
        bucket.public = public
        with open(self.db_file, "ab") as f:
            data_offset = f.tell()
            f.write(bytes(bucket))
        self.index.create(value=pk_value, data_offset=data_offset)
        return bucket

    def find(self, name):
        name = to_bytes(name)
        bucket = None
        with open(self.db_file, "rb") as f:
            content = f.read(ctypes.sizeof(BucketStruct))
            while content:
                bucket = BucketStruct.from_buffer_copy(content)
                if bucket.name == name:
                    break
                content = f.read(ctypes.sizeof(BucketStruct))
                bucket = None
        return bucket
    
    def find_by_index(self, value):
        value = to_bytes(value)
        index = self.index.get(value=value)
        if not index:
            print("index not found.")
            return
        with open(self.db_file, "rb") as f:
            f.seek(index.data_offset)
            content = f.read(ctypes.sizeof(BucketStruct))
        bucket = BucketStruct.from_buffer_copy(content)
        return bucket

    def create_table(self):
        self.meta.create(database=self.database, table=self.table, primary_key=self.primary_key, columns="columns")

if __name__ == "__main__":
    bucket_name = "gaojian3"
    bucket = Bucket()
    # bb = bucket.add(name=bucket_name, public=1)
    # print("new bucket id = ", bb.id)
    # b = bucket.find(bucket_name)
    b = bucket.find_by_index(3)
    if b:
        print("bucket id = ", b.id)
        print("bucket name = ", b.name)
        print("bucket public = ", b.public)
    else:
        print("bucket {} not found".format(bucket_name))
    # bucket.index.btree.printTree()
    