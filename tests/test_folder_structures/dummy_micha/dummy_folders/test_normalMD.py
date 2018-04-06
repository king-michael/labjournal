#/usr/bin/env python
'''
Testcase for a normalMD
'''
import sys
sys.path.append("../../../..")

from labjournal.utils import pushd
# Import Test library

#=========================================================#
# Testcase LAMMPS setup_folders
with pushd("testcase_normalMD"): # go in folder

    #Obj_setup=analysis.LAMMPS.setup_folders(pattern_startstructure='at_calcite_6x6x2_graf_1961..*')
    #Obj_setup.create_folder_analysis()
    #Obj_setup.get_file_lists()


    Obj_thermo= labjournal.analysis.LAMMPS.Thermo(path="./analysis/analysis_1")
    #Obj_thermo.extract_single()
    #Obj_thermo.extract_all(mode='npz')

    #print(estimate_pattern_startstructure())
    #print(Obj_thermo.get_values("Temp", "PotEng",x="Time"))
    Obj_thermo.get_values_safe("Temp", "PotEng",x="teest")