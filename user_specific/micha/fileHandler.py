"""
_info_ fileHandler
"""

import logging
logger = logging.getLogger('LabJournal')
logger.info("fileHandler: imported from: %s",__file__)

class FileHandler():
    def __init__(self):
        print "YEAH"