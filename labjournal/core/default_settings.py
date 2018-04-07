"""
Settings
"""

from PyQt5.QtCore import QSettings

# ToDo: find a good organization / application name
# Todo: if added we can set the file path by ourself : https://stackoverflow.com/questions/4031838/qsettings-where-is-the-location-of-the-ini-file
settings = QSettings('foo', 'foo')

settings.beginGroup('Database')
settings.setValue('file', '')
settings.endGroup()

settings.beginGroup('MediaWiki')
settings.setValue('prefix', 'http://134.34.112.156:777/mediawiki/index.php/')
settings.setValue('browser', 'browser') # how to open it [browser = defaultbrowser]
settings.endGroup()

settings.beginGroup('InfoEntry')
settings.setValue('tags_max_col', 5) # number of tabs per column
settings.endGroup()

settings.beginGroup('FileFinder')
settings.setValue('pattern', '_info_')
settings.endGroup()

#==============================================================================#
# LAMMPS
#==============================================================================#
settings.beginGroup('LAMMPS')

settings.beginGroup('folders')  # LAMMPS/folders
settings.setValue('production',             'production')  # folder where the production run is
settings.setValue('EM_and_Equilibration',   'EM_and_Equilibration')  # folder where the EM and Equilibration is
settings.setValue('analysis',               'analysis')  # folder where the normal analysis will be saved
settings.setValue('analysis_MetaD',         'analysis_MetaD') # folder where MetaDynamic analysis will be saved
settings.endGroup()  # LAMMPS/folders

settings.beginGroup('pattern')  # LAMMPS/pattern
settings.setValue('trajectory',     'trajectory..*.dcd') # trajectory file with .* = run_no
settings.setValue('logfile',        'log..*.lammps') # log file with .* = run_no
settings.setValue('final_data',     'final_data..*') # final data file with .* = run_no
settings.setValue('final_restart',  'final_restart..*') # final data file with .* = run_no
settings.endGroup()  #  LAMMPS/pattern

settings.beginGroup('thermo')  # LAMMPS/thermo
settings.setValue('xlabel', 'Step') # xlabel for thermo data (possible also 'Time' but risky not work for everything)
settings.setValue('list_keywords', ['PotEng', 'Temp', 'Press', 'Volume']) # list of keywords to use for analysis
settings.setValue('BUFFER_READ', 200) # readin buffer to check for keywords (number of chars in the Step KEYWORDS line)
settings.setValue('save_subfolder','plot_log') # subfolder to save extracted data in
settings.endGroup()  #  LAMMPS/thermo

settings.endGroup()  # LAMMPS



if __name__ == '__main__':
    print "Create Settings"
    print "Orgainization:", settings.organizationName()
    print "Application:", settings.applicationName()
    print "Created settings in:", settings.fileName()
