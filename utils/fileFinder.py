"""
Description:
 - class to find all finds in sub dirs matching a pattern

authors:
  Michael King <michael.king@uni-konstanz.de>

last modified: 09.02.2018
"""
from PyQt4.QtCore import QSettings
import os,sys
sys.path.append("../")
from glob import glob
import logging
logger = logging.getLogger('LabJournal')

settings = QSettings('foo', 'foo')



fileHandler = str(settings.value('general/fileHandler', 'user_specific.micha.fileHandler').toString())
import importlib
FileHandler = getattr(importlib.import_module(fileHandler), 'FileHandler')
fileHandler = FileHandler()


class FileFinder():
    def __init__(self,
                 pattern = None, # pattern to be found
                 path='.', # root path
                 ):
        """
        finds all files matching the pattern from root
        :param pattern: if not defined take the pattern from Settings ['_info_']
        :param path: root folder, where to start
        """

        if pattern is None:

            pattern=str(settings.value("FileFinder/pattern", '_info_').toString())
        self.pattern=pattern
        self.path = path
        logger.info('FileFinder: pattern: %s', self.pattern)
        logger.info('FileFinder: path: %s', os.path.realpath(self.path))

    def find_files(self,pattern=None,path=None):
        """
        Find files matching pattern in the folder and subfolders of root
        :param pattern:
        :param root:
        :return: list(/path/to/files)
        """
        if pattern is None:
            pattern=self.pattern
        if path is None:
            path = self.path
        # Get files
        files = []
        for dir,_,_ in os.walk(path):
            files.extend(glob(os.path.join(dir,pattern)))
        return files

