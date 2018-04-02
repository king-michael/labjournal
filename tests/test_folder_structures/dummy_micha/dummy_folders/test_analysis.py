import os,sys
sys.path.append("../../../..")

from analysis.LAMMPS.analysisHandler import *
from analysis.LAMMPS.thermo import *

logger = logging.getLogger('Thermo')
logging.basicConfig(level=logging.DEBUG)

ana = AnalysisHandler(path='testcase_normalMD',force=True)
ana.action_setup_folder()


Obj_thermo=Thermo(logfile='testcase_normalMD/analysis/log.1.lammps')
print Obj_thermo.get_values_safe("Temp", "PotEng", 'Cellx',x="Step")
print Obj_thermo.refine_keywords(["Temp", "PotEng", 'Cellx'])