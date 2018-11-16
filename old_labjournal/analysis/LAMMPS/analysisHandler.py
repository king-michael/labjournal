"""\
AnalysisHandler for LAMMPS

Details:

Author:
    Michael King <michael.king@uni-konstanz.de>
"""

__author__ = 'Michael King'

import os
import subprocess
import pkg_resources

from old_labjournal.utils import pushd

STR_build_folders=open(
    os.path.join(pkg_resources.resource_filename('old_labjournal', ''),
                 'templates', 'LAMMPS', 'analysis', 'analysis.sh'),
    'r'
).read()
"""The template for analysis.sh"""


class AnalysisHandler:
    def __init__(self,**kwargs):  
        """\
        AnalysisHandler for LAMMPS

        :param kwargs:

            path:  current working directory ['.']

            fname: filename of the analysis file [analysis.sh]

            force: force rewrite [False] (```EXPERIMENTAL```)

            verbose: [False]

        """
        self.fname = 'analysis.sh' # Filename
        self.path = '.' # current working directory
        self.force=False # force rewrite
        self.verbose=False # set verbose

        for k,v in kwargs.iteritems(): # set kwargs
            setattr(self,k,v)

        self.pathtofile=os.path.join(self.path,self.fname) # set path to file

    def write_analysisfile_init(self):
        """
        Initialize the Analysis file
        
        Returns
        -------
        None, None
        """

        if not os.path.exists(self.pathtofile) or self.force:
            with open(self.pathtofile, 'w') as fp:
                fp.write(STR_build_folders)

    def action_setup_folder(self,**kwargs):
        """
        Create the Analysis folder

        :return: 0 / 1 for success / error
        """
        for k,v in kwargs.iteritems(): # set kwargs
            setattr(self,k,v)

        self.write_analysisfile_init() # write analysis file
        with pushd(self.path): # go in analysis folder
            # run analysis
            process = subprocess.Popen(['bash analysis.sh'],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      shell=True)
            process.wait() # wait till it is finished
        #Launch the shell command:
        output, error = process.communicate()
        if len(error) != 0: # if we got an Error
            print(error)
            return 1

        if self.verbose: # if we want to have a status message
            print("Created analysis folder and linked trajectories/logfiles")

        return 0

if __name__ == '__main__':
    import sys
    sys.path.insert(0, os.path.realpath(
                        os.path.join(os.path.dirname(__file__), '../../..')
                        )
                    )
    ana = AnalysisHandler()
