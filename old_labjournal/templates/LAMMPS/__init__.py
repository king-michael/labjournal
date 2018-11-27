"""
Init simulation folder
 - copies input.X.lammps file
   - different templates
 - creates build.sh
   - runs build.sh
"""

import os
import sys

sys.path.append("../../")
from old_labjournal.core import XmlConverter


XmlConverter=XmlConverter()
def get_input_templates():
    """
    function to return a dictonary of templates
    FLAG : EM / production
    :returns dict('templatename' = [['Description','FLAG','path/to/file']])"""
    FOLDER_TEMPLATES="input_scripts"
    templates = dict()
    PATH=os.path.dirname(__file__)
    adict = XmlConverter.file_to_dict('overview_files.xml')
    print os.listdir(os.path.join(PATH,FOLDER_TEMPLATES))
    print adict

    return templates

class setup():
    def __init__(self,
                 path='.',        # path where to create the files
                 template=None,   # template to be chosen
                 forcefield=None, # LAMMPS force field file
                 startdata=None,  # LAMMPS start file
                 ):
        pass

    def modify_inputfiles(self):
        """function to modify the input files"""
        pass

if __name__  == "__main__":

    templates = get_input_templates()
    print templates


