#! /usr/bin/env python3
import hashlib
import os
import sys
import time


try:
    import click
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback,os
    sys.stderr.write(err)
    if(os.environ['HOME'] == 'srb'):
        traceback.print_exc()
    sys.exit(1)

def findCheckSumMD5(fname):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(fname, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


def _dfs_dir(path):
    content = os.listdir(path)
    dir_hash = "+"
    for a in content:
        if(os.path.isdir(os.path.join(path,a))):
            val = _dfs_dir(os.path.join(path,a))
            dir_hash += val
        elif(os.path.isfile(os.path.join(path,a))):
            dir_hash += '-'
            dir_hash += str(findCheckSumMD5(os.path.join(path,a)))
    return dir_hash


def get_hash(path):
    if(not os.path.exists(path)):
        click.secho('path does not exist: '+path,fg='red')
        return ""
    dir_hash = _dfs_dir(path)
    return str(hashlib.md5(dir_hash.encode('utf-8')).hexdigest())


if __name__ == "__main__":
    path = './srb_test'
    if(len(sys.argv)==2):
        path = sys.argv[1]
    dir_hash = get_hash(path)
    print(dir_hash)
