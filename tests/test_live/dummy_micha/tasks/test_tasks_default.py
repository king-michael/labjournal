"""
Default tests for tasks
"""

import os
import sys
sys.path.append("../../../../")

from labjournal.analysis.LAMMPS.analysisHandler import AnalysisHandler

from labjournal.utils.regexHandler import reglob
from labjournal.workflows import tasks
from labjournal.utils import pushd


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


pattern = 'trajectory..*.dcd'

def get_asterix(pattern,match):
    pattern_split = pattern.split('.*')
    match_wo_prefix = match.split(pattern_split[0])[1]
    asterix = match_wo_prefix.split(pattern_split[1])[0]
    return asterix

def get_run_no_min_max(pattern,list_matches):
    list_run_nos = [int(get_asterix(pattern,match)) for match in list_matches]
    return list_run_nos[0], list_run_nos[-1]

list_trajectories = [os.path.basename(i) for i in sorted(reglob(path_analysis, pattern))]

run_no_from,run_no_to = get_run_no_min_max(pattern,list_trajectories)

print "Run Lammps for run_no: {} -> {}".format(run_no_from,run_no_to)

import subprocess
LMP_EXE='lmp'
LMP_ARGS=" -in input.analysis.remove_water.lammps -v run_no {}"
for run_no in range(run_no_from,run_no_to):
    cmd = LMP_EXE + LMP_ARGS.format(run_no)
    proc = subprocess.call(cmd,cwd=path_analysis,shell=True)

