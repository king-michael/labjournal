

# Begin import system libs
from __future__ import print_function
import os, sys
import numpy as np
# End import system libs

# Begin import my libs
sys.path.insert(0,'../..')
from utils.regexHandler import reglob
from external_libs.pizza.log import log as PizzaLog
# End import my libs
from PyQt4.QtCore import QSettings
settings = QSettings('foo', 'foo')
import logging
logger = logging.getLogger('Thermo')
#logging.basicConfig(level=logging.DEBUG)


class Thermo():
    def __init__(self, logfile=None, path=None, **kwargs):
        """
Module to run analysis of logfiles
        """
        # =============================================================================#
        #   Start Defaults just in case the are not in our default file
        # =============================================================================#
        # patterns
        self.pattern_logfile = 'log..*.lammps'
        # other
        self.list_keywords = [str(i.toString()) for i in settings.value('LAMMPS/thermo/list_keywords',
                                            ['PotEng', 'Temp', 'Press', 'Volume']).toList()]
        self.xlabel = str(settings.value('LAMMPS/thermo/xlabel',
                                     'Step').toString())  # xlabel for thermo data
        self.BUFFER_READ = settings.value('LAMMPS/thermo/BUFFER_READ',
                                          200).toInt()[0] # read buffer for LOGFILES
        self.save_subfolder = str(settings.value('LAMMPS/thermo/save_subfolder',
                                             'plot_log').toString())
        # =============================================================================#

        # use input
        self.CWD = path if path is not None else os.path.realpath(os.path.curdir)
        self.logfile = logfile if logfile is not None else self.get_logfile(self.CWD)
        # set kwargs
        self.kwargs = kwargs
        for k, v in kwargs.iteritems():
            setattr(self, k, v)  # set kwargs to object

        if not hasattr(self, 'path_to_save'): self.path_to_save = os.path.join(self.CWD, self.save_subfolder)
        self.possible_keywords = self.get_keywords(self.logfile)  # get the possible keywords in the file
        self.lg = PizzaLog(self.logfile)

    def get_logfile(self, path):
        """find logfile in folder (only used if not provided before)"""
        logfile = sorted(reglob(path, self.pattern_logfile))
        if len(logfile) == 0:
            raise RuntimeError("Logfile not found")
        elif len(logfile) > 1:
            raise NotImplementedError(
                "Not implemented to use class thermo on multiple files\nFiles: {}".format(logfile))
        return logfile[0]

    def get_keywords(self, logfile):
        """get all possible keywords from the logfile"""
        if type(logfile) == type([]):
            return [self.get_keywords(i) for i in logfile]

        with open(logfile, 'r') as fp:
            txt = fp.read()
        i = txt.find("Step ")
        tmp = txt[i:i + self.BUFFER_READ]
        list_keywords = tmp.split('\n')[0].strip().split(" ")
        return list_keywords

    def refine_keywords(self, keywords):
        """refine the keywords so that they can be used with the file (delete not supported ones)"""
        if type(keywords) == type(str()): keywords = [keywords]
        if not hasattr(self, 'possible_keywords'): self.possible_keywords = self.get_keywords(self.logfile)
        return [keyword for keyword in keywords if keyword in self.possible_keywords]

    def get_values(self, *keywords, **x):
        """return the values to the given Keywords
        if define x use x else use self.xlabel
        """
        x = x['x'] if 'x' in x else self.xlabel  # get the parameter x
        return np.array(self.lg.get(x, *keywords)).T

    def get_values_safe(self, *keywords, **x):
        """return the values to the given Keywords but checks them before
        if define x use x else use self.xlabel
        """
        if not hasattr(self, 'possible_keywords'): self.possible_keywords = self.get_keywords(self.logfile)
        if ('x' in x and x['x'] in self.possible_keywords):  # get the parameter x
            x = x['x']
        else:
            logger.warning("Cant use this keyword '{}' for x (not in logfile), fall back to default ('{}')".format(x['x'],
                                                                                                        self.xlabel))
            x = self.xlabel

        return self.get_values(*self.refine_keywords(keywords), x=x)

    def __getitem__(self, keyword):
        """can be used as object['keyword']"""
        if not hasattr(self, 'possible_keywords'): self.possible_keywords = self.get_keywords(self.logfile)
        if keyword not in self.possible_keywords:
            raise StandardError("Keyword not in logfile.\nUse: {}".format(self.possible_keywords))
        return np.array(self.lg.get(keyword)).T

    def extract_single(self, keywords=None, mode='dat'):
        """Extract the data for every single keyword in a single file
        if keywords is None use self.keywords
        Saves them as Step_{}.dat
        if mode='npy' saves them as numpy file
        if mode == 'npz' saves them as a npz file (with array + keywords)
        else: saves them as plain text with keywords in header
        """
        if keywords is None:
            keywords = self.list_keywords

        if type(keywords) == type([]):
            for keyword in keywords:
                self.extract_single(keyword)
        else:  # POSSIBLE BUG HERE IN FUTURE IF THERE COMES A QString or sth like this
            if keywords in self.possible_keywords:
                #log.debug("Extract: {} {} from {}".format(self.xlabel, keywords, self.logfile), lvl=1)
                data = np.array(self.lg.get(self.xlabel, keywords)).T
                # Save location
                SAVETO = os.path.join(self.path_to_save, "{}_{}".format(self.xlabel, keywords))
                if not os.path.exists(self.path_to_save):
                    os.mkdir(self.path_to_save)
                # decide in which format
                if mode == 'npy':  # saves as numpy object
                    np.save(SAVETO, data)
                elif mode == 'npz':  # saves them as npz object, with data=data and header=header
                    np.savez(SAVETO, data=data, header=[self.xlabel, keywords])
                else:  # saves as datafile
                    np.savetxt(SAVETO + ".dat", data,
                               header=self.xlabel + " " + keywords)
                #log.debug("Saved to: {}.{}".format(SAVETO, mode))
            else:
                print("Keyword [ {} ] not in file: {}\n use: {}".format(keywords, self.logfile, self.possible_keywords))

    def extract_all(self, keywords=None, mode='dat'):
        """Extract all keywords in one file
        if keywords is None use self.keywords.
        saves them as Step_all.dat
        if mode='npy' saves them as numpy file
        if mode == 'npz' saves them as a npz file (with array + keywords)
        else: saves them as plain text with keywords in header
        """
        if keywords is None:
            keywords = self.list_keywords

        data = np.array(self.lg.get(self.xlabel, *keywords)).T  # get data
        #log.debug("Extract: {} from {}".format([self.xlabel] + keywords, self.logfile), lvl=1)
        # Save location
        SAVETO = os.path.join(self.path_to_save, "{}_all".format(self.xlabel))
        if not os.path.exists(self.path_to_save):
            os.mkdir(self.path_to_save)
        # decide in which save format
        if mode == 'npy':  # saves as numpy object
            np.save(SAVETO.format(self.xlabel), data)
        elif mode == 'npz':  # saves them as npz object, with data=data and header=header
            np.savez(SAVETO.format(self.xlabel, keywords), data=data,
                     header=[self.xlabel].extend(keywords))
        else:  # saves as datafile
            np.savetxt(SAVETO + ".dat".format(self.xlabel), data,
                       header=self.xlabel.join([" " + i for i in keywords]))
        #log.debug("Saved to: {}.{}".format(SAVETO, mode))
