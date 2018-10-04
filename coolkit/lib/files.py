import os

from .abs_path import abs_path

def verify_folder(folder,debug=False):
    '''
    similar to mkdir -p
    '''
    folder = abs_path(folder)
    if not os.path.exists(folder):
        if(debug): print('creating folder '+ folder)
        os.makedirs(folder)
    elif os.path.isfile(folder):
        if(debug): print('there exists file of same name')

def verify_file(file_path,debug=False):
    file_path = abs_path(file_path)
    parent_dir = os.path.join(file_path,os.pardir)
    verify_folder(parent_dir)
    if not os.path.exists(file_path):
        if(debug): print('creating file '+ file_path)
        file_ = open(file_path, 'w')
        file_.close()
    elif os.path.isdir(file_path):
        if(debug): print('there exists folder of same name')
