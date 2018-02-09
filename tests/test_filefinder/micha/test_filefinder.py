"""
Test the fileFinder
"""

import logging
logger = logging.getLogger('LabJournal')
logging.basicConfig(level=logging.DEBUG)

import sys
sys.path.append("../../..")

from utils.fileFinder import *

fileFinder = FileFinder(
    pattern='_info_',
    path='./SIM-PhD-King')
print fileFinder.find_files()