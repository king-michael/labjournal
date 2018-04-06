"""
Default tests for tasks
"""

import sys
import os
from utils.regexHandler import reglob
from shutil import copy2
from analysis.LAMMPS.analysisHandler import AnalysisHandler
sys.path.append("../../../../")
import workflows.tasks as tasks

ROOT=os.path.realpath("../../../../")

path = "/home/micha/SIM-PhD-King/tmp_test_labjournal/"
path+= "ubiquitin/atomistic/ub.N25CP.D32CP.D58CP_pH7_CaCl2-0.075M_charmm-raiteri/simulation"

print "Use location:\n {}".format(path)

print "Create Analysis folder"
ana = AnalysisHandler(path=path)
ana.action_setup_folder()
path_analysis = os.path.join(path,'analysis')

print "Create Thermodynamic plots"
path_plots = os.path.join(path_analysis,'plots')

list_logfiles = [os.path.basename(i) for i in sorted(reglob(path_analysis, 'log..*.lammps'))]
print "List of logfiles:\n", list_logfiles
# tasks.LAMMPS.task_thermodata(sorted(reglob(path_analysis, 'log..*.lammps')), out_path=path_plots)

print "write input file to remove water"
datafile = [os.path.basename(i) for i in reglob(path, '.*.data')]
datafile.pop(datafile.index('system_start.data'))
datafile = datafile[0]
print "Datafile : ", datafile
forcefield = [os.path.basename(i) for i in reglob(path, 'ff.*.lammps')+reglob(path, 'ff.*.lmp')][0]
print "ForceField : ", forcefield
tasks.LAMMPS.write_lammpsrerun_remove_water(inputfile=datafile,
                                            forcefield=os.path.join(os.path.relpath(path,path_analysis),
                                                                    forcefield),
                                            cmap='../charmmc36.cmap',
                                            path=path_analysis)

print "lmp -in input.analysis.remove_water.lammps -v run_no 1"

