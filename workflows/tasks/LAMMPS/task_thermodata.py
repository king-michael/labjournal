"""
Task to create all a Picture for all the Thermodata

Details:

Author:
    Michael King <michael.king@uni-konstanz.de>
"""

__author__ = "Michael King"

import sys,os
import matplotlib.pyplot as plt
sys.path.append("../../..")
from external_libs.pizza.log import log as Pizzalog


def task_thermodata(flist,**kwargs):
    """
    Task to plot the Thermodynamic Data
    :param flist: list of logfiles to use
    :param list_keywords: List of keywords to use ['Step', 'Temp', 'Press', 'PotEng']
    :param path: path to save the file in
    :param fname: name of the picture file ['thermodynamic_data.png']
    """
    default=dict(
        list_keywords=['Step', 'Temp', 'Press', 'PotEng'],
        list_axis=['Steps [10^3]', 'Temperature [K]', 'Pressure', 'Potential Energy'],
        path='.',
        fname='thermodynamic_data.png',
    )
    setting=default
    setting.update(kwargs)
    if type(flist) == type(str):
        flist=[flist]
    keywords = setting['list_keywords']
    data = []
    for f in flist:
        lg = Pizzalog(f)
        data.extend(zip(*lg.get(*keywords)))
    data = zip(*data)

    nkeywords = len(keywords)
    fig, axes = plt.subplots(nkeywords-1)
    for i in range(1,nkeywords):
        ax = axes[i-1]
        ax.set_title(keywords[i])
        ax.plot(data[0],data[i])
        ax.set_xlabel(setting['list_axis'][0])
        ax.set_ylabel(setting['list_axis'][i])

    fig.tight_layout()
    fig.savefig(os.path.join(setting['path'],setting['fname']))

if __name__ == '__main__':

    logfile = ['/home/micha/labjournal/tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD/analysis/log.1.lammps',
               '/home/micha/labjournal/tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD/analysis/log.1.lammps']
    task_thermodynamic(logfile, path = "/home/micha/labjournal/tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD/analysis/")