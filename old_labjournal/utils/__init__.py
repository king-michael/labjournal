#!/usr/bin/env python
"""usefull functions"""
from __future__ import print_function
from contextlib import contextmanager
import os



#=========================================================#
# Funktion to implement pushd
#=========================================================#
@contextmanager
def pushd(newDir):
    """implementation of pushd in python"""
    previousDir = os.getcwd()
    os.chdir(newDir)
    yield
    os.chdir(previousDir)

#=========================================================#
# Funktion to create relative symlinks
#=========================================================#
def relsymlink(src,dst):
    """create a relative symlink from src to dst
    src  - dst
    str  - str   : normal symlink
    list - str   : links all src to folder dst
    list - list  : links all src to the corresponding dst entry
    """
    if type(src) == type(list()) or type(src) == type(tuple):
        if type(dst) == type(list()) or type(dst) == type(tuple):
            assert len(src) == len(dst),"Length of list of src files != length of list of destinations"
            for s,d in zip(src,dst): # case we have a list and a list
                relsymlink(s,d)
        else:
            if os.path.isdir(dst):
                for s in src: # case we have a list and only one target
                    relsymlink(s,dst)
            else:
                raise AssertionError("try to link a list of files to a single file, please chose a directory")
    else: # case we have one source and one target
        if os.path.isdir(dst):  # case its a dir , we have to add / at the end
            relpath=os.path.relpath(src, os.path.dirname(dst+"/"))
            srcpath=os.path.join(dst, os.path.basename(src))
        else:  # case its a file, every thing works fine
            relpath = os.path.relpath(src, os.path.dirname(dst))
            srcpath=dst
        if not os.path.exists(srcpath):  # check if file exists
            os.symlink(relpath, srcpath)



if __name__ == '__main__':
    # Test pushd
    print("#" + 38 * "=" + "#")
    print("# test pushd")
    print("#" + 38 * "=" + "#")
    print("CWD: {}".format(os.getcwd()))
    print('pushd("/tmp")')
    with pushd("/tmp"):
        print("CWD: {}".format(os.getcwd()))
        print("os.chdir('/')")
        os.chdir('/')
        print("CWD: {}".format(os.getcwd()))
    print("end")
    print("CWD: {}".format(os.getcwd()))
    print("#"+38*"="+"#")


    # Test relsymlink
    #relsymlink("./test.dat", "./system.dat")
    #relsymlink(["/tmp/test.dat"], "./system.dat")