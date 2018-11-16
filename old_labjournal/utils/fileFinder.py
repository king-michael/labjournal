"""
Description:
 - class to find all finds in sub dirs matching a pattern

authors:
  Michael King <michael.king@uni-konstanz.de>

last modified: 09.02.2018
"""
from PyQt5.QtCore import QSettings
import os,sys
from glob import glob
import logging
logger = logging.getLogger('LabJournal')

APPLICATION_NAME = 'foo'
COMPANY_NAME = 'foo'
settings = QSettings(APPLICATION_NAME, COMPANY_NAME)


# FIXME auskommentiert weil gebugt, braucht man das?
#fileHandler = str(settings.value('general/fileHandler', 'old_labjournal.user_specific.micha.fileHandler'))
#import importlib
#FileHandler = getattr(importlib.import_module(fileHandler), 'FileHandler')
#fileHandler = FileHandler()


class FileFinder():
    def __init__(self,
                 pattern = None, # pattern to be found
                 path='.', # root path
                 dir_ignore=[]
                 ):
        """
        finds all files matching the pattern from root
        :param pattern: if not defined take the pattern from Settings ['_info_']
        :param path: root folder, where to start
        """

        if pattern is None:
            pattern=str(settings.value("FileFinder/pattern", '_info_'))
        self.pattern=pattern
        self.path = path
        self.dir_ignore=dir_ignore
        logger.info('FileFinder: pattern: %s', self.pattern)
        logger.info('FileFinder: path: %s', os.path.realpath(self.path))
        logger.info('FileFinder: dir_ignore: %s', dir_ignore)

    def find_files(self,pattern=None,path=None,dir_ignore=None):
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
        if dir_ignore is None:
            dir_ignore = self.dir_ignore
        exclude = set(dir_ignore)
        # Get files
        output = []
        for root, dirs, files in os.walk(path, topdown=True):
            #dirs[:] = [d for d in dirs if d not in exclude]
            [dirs.remove(d) for d in list(dirs) for ex in exclude if d.startswith(ex)]
            # flag_ignore=False
            # for ignore in dir_ignore:
            #     if os.path.basename(dir).startswith(ignore):
            #         flag_ignore=True
            # if not flag_ignore:
            output.extend(glob(os.path.join(root,pattern)))
        return output

