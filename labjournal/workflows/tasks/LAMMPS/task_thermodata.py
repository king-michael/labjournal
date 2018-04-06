"""
Task to create all a Picture for all the Thermodata

Details:

Author:
    Michael King <michael.king@uni-konstanz.de>
"""

__author__ = "Michael King"

import os
import sys

import matplotlib.pyplot as plt

sys.path.append("../../..")
from labjournal.external_libs import log as Pizzalog


def task_thermodata(flist, # type: list or str
                    list_keywords=['Step', 'Temp', 'Press', 'PotEng'], # type: list[str]
                    list_axis=['Steps [10^3]', 'Temperature [K]', 'Pressure', 'Potential Energy'], # type: list[str]
                    out_path='.', # type: str
                    out_fname='thermodynamic_data.png', # type: str
                    ):
    """
    Task to plot the Thermodynamic Data

    Parameters
    ----------
    flist : list or str
        List of logfiles to use
    list_keywords : list[str]
        List of keywords to use (default is ['Step', 'Temp', 'Press', 'PotEng'])
    list_axis : list[str]

    out_path : str
         path to save the file in (default is '.')
    out_fname : str
        name of the picture file (default is 'thermodynamic_data.png')

    Returns
    -------

    """

    if type(flist) == type(str):
        flist=[flist]
    data = []
    for f in flist:
        lg = Pizzalog(f)
        data.extend(zip(*lg.get(*list_keywords)))
    data = zip(*data)

    nkeywords = len(list_keywords)
    fig, axes = plt.subplots(nkeywords-1)
    for i in range(1,nkeywords):
        ax = axes[i-1]
        ax.set_title(list_keywords[i])
        ax.plot(data[0],data[i])
        ax.set_xlabel(list_axis[0])
        ax.set_ylabel(list_axis[i])

    fig.tight_layout()
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    fig.savefig(os.path.join(out_path,out_fname))

if __name__ == '__main__':

    logfile = ['/home/micha/labjournal/tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD/analysis/log.1.lammps',
               '/home/micha/labjournal/tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD/analysis/log.1.lammps']
    task_thermodata(logfile, path = "/home/micha/labjournal/tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD/analysis/")