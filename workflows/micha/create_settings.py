from PyQt4.QtCore import QSettings

# ToDo: find a good organization / application name
# Todo: if added we can set the file path by ourself : https://stackoverflow.com/questions/4031838/qsettings-where-is-the-location-of-the-ini-file
settings = QSettings('foo', 'foo')

settings.beginGroup('Database')
settings.setValue('file', '/home/micha/SIM-PhD-King/micha.db')
settings.endGroup()

settings.beginGroup('FileFinder')
settings.setValue('pattern', '_info_')
settings.endGroup()

if __name__ == '__main__':
    print "Create Settings"
    print "Orgainization:", settings.organizationName()
    print "Application:", settings.applicationName()
    print "Created settings in:", settings.fileName()