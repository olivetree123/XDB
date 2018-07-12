#coding:utf-8
import os

from config import DB_DIR_PATH

def to_bytes(value):
    if isinstance(value, str):
        return bytes(value, "utf8")
    if isinstance(value, int):
        return value
    if not isinstance(value, bytes):
        raise Exception("Type Error: bytes expect, but {} found, value = {}".format(type(value), value))

def db_file_path(database):
    if not os.path.exists(DB_DIR_PATH):
        os.makedirs(DB_DIR_PATH)
    return os.path.join(DB_DIR_PATH, database+".db")
    
