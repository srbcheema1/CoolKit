#! /usr/bin/env python3
import os,time
import hashlib

from .Colour import Colour

def _dfs_dir(path):
    content = os.listdir(path)
    dir_hash = "+"
    dir_hash += str(os.path.getmtime(path))
    for a in content:
        dir_hash += '-'
        if(os.path.isdir(os.path.join(path,a))):
            val = _dfs_dir(os.path.join(path,a))
            dir_hash += val
        elif(os.path.isfile(os.path.join(path,a))):
            dir_hash += str(os.path.getmtime(os.path.join(path,a)))
    return dir_hash


def get_hash(path):
    '''
    TODO: it is not working properly will maintain it in future
    '''
    return ""
    if(not os.path.exists(path)):
        print(Colour.RED+'path not exist ' + path+Colour.END)
        return ""
    dir_hash = _dfs_dir(path)
    return str(hashlib.sha1(dir_hash.encode('utf-8')).hexdigest())


if __name__ == "__main__":
    path = './srb_test'
    import sys
    if(len(sys.argv)==2):
        path = sys.argv[1]
    dir_hash = get_hash(path)
    print(Colour.CYAN+dir_hash+Colour.END)
