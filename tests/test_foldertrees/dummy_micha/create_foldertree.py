'''
Script to create a dummy folder tree

Target:
 - check file finder
 - build up a folder-tree for a dummy database
'''

import os, sys

sys.path.append('../../..')
from utils import pushd

def create_foldertree(folder_tree,path='.'):
    '''takes a dict and creates the keys as folders
    if the value is a dict, create all subfolders recursively'''

    for folder, item in folder_tree.iteritems():
        # create folder
        if not os.path.exists(folder):
            os.mkdir(folder)
        with pushd(folder):
            # if this is the final folder:
            if type(item) is str:
                with open('_info_', 'w') as fp:
                    fp.write('ID : {}\n'.format(item))
                    fp.write('MEDIAWIKI : {}\n'.format(item))

            # handle subfolders
            if type(item) is dict:
                create_foldertree(item, folder)


folder_tree={
    'SIM-PhD-King' : {
        'ubiquitin' : {
            'ub_CaCl2' : 'MK0001',
            'ub_NaCl' : 'MK0002',
        },
        'CaCO3' : {
            'coarse-grained' : {
                'development' : {
                    'dev01' : 'MK0003',
                    'dev02' : 'MK0004'
                },
                'nucleation' : {
                    'model1' : 'MK0005',
                    'model2' : 'MK0006'
                }
            },
            'atomistic' : {
                'reference' : 'MK0007'
            }
        }
    }
}

create_foldertree(folder_tree)
