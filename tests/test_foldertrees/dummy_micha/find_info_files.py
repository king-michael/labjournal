"""
Script to find all Simulation info files
"""

import os
from glob import glob

import sys
sys.path.append('../../test_database_handler')


def find_files(fname,start_dir):
    # Get files
    files = []
    for dir,_,_ in os.walk(start_dir):
        files.extend(glob(os.path.join(dir,fname)))
    return files

def get_data_from_file(fname):
    """retrieve the data from the file"""
    adict = {}
    with open(fname, 'r') as fp:
        for line in fp:
            line_strip = line.strip()
            if len(line_strip) == 0: continue  # empty lines
            if line_strip[0] in ['#']: continue  # comments
            line_split = line_strip.split(":", 1)  # max split 1
            adict[line_split[0].strip()] = line_split[1].strip()
    return adict

if __name__ == '__main__':
    fname = '_info_'  # name of the files which should be found
    start_dir = 'SIM-PhD-King'  # base folder

    print "Search files for pattern: {}".format(fname)
    files = find_files(fname,start_dir)
    print ' found: {} files "{}"'.format(len(files),fname)

    print "get the file informations"
    exp_list=[]
    for fname in files:
        adict =  get_data_from_file(fname)
        adict['path'] = os.path.realpath(os.path.dirname(fname))
        exp_list.append(adict)


    print "delete old databasefile"
    try:
        os.system('rm ./test.db')
        print('deleted ./test.db')
    except:
        pass

    print "Connect to database"
    import databaseHandler as db
    print "Create Tables"
    db.setup_database()

    print "Add simulations to table"

    for adcit in exp_list:
        kwargs={}
        for key,value in adcit.iteritems():
            if  key == 'ID':
                kwargs['simid']=value
            elif key == 'MEDIAWIKI':
                kwargs['mediawiki'] = value
            elif key == 'path':
                kwargs['path']=value
        db.create_SimulationEntry(**kwargs)
    print 'Commit new entries'
    db.session.commit()

    print 'Show results'
    db.debug_print_sims()