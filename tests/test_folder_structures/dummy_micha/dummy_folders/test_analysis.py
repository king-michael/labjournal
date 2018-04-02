import os,sys
sys.path.append("../../../..")

from analysis.LAMMPS.analysisHandler import *
from analysis.LAMMPS.thermo import *

logger = logging.getLogger('Thermo')
logging.basicConfig(level=logging.DEBUG)

# ana = AnalysisHandler(path='testcase_normalMD',force=True).action_setup_folder()
# ana.action_setup_folder()
AnalysisHandler(path='testcase_normalMD', force=True).action_setup_folder()

Obj_thermo=Thermo(path='testcase_normalMD/analysis')
print Obj_thermo.get_values_safe("Temp", "PotEng", 'Cellx',x="Step")
print Obj_thermo.refine_keywords(["Temp", "PotEng", 'Cellx'])