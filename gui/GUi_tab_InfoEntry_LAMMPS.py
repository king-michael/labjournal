#!/usr/bin/env python
"""
# Details:
#   Wrapper around UiInfoEntry_LAMMPS.py
# Authors:
#   Michael King <michael.king@uni-konstanz.de>
# History:
#   -
# Last modified: 17.10.2017
# ToDo:
#   -
# Bugs:
#   -
"""

from __future__ import print_function
from PyQt4 import QtCore, QtGui
import sys

from Ui_tab_InfoEntry_LAMMPS import Ui_Form

# import webbrowser

sys.path.append("..")
from core.Database import *
from core.settings import settings
import MyQt
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class GUi_tab_InfoEntry_LAMMPS(QtGui.QWidget, Ui_Form):
    def __init__(self,**kwargs):
        super(self.__class__,self).__init__()
        # set defaults
        self.parent = None
        self.ID=None
        self.settings={
            'mediawiki' : {  # MediaWiki settings
                'prefix'  : "http://134.34.112.156:777/mediawiki/index.php/",  # prefix
                'browser' : 'browser',  # how to open it [browser = defaultbrowser]
            },  # MediaWiki settings
        }
        self.settings['mediawiki'].update(settings['mediawiki'])
        # assign kwargs
        for k,v in kwargs.iteritems():
            setattr(self,k,v)

        # Set up the user interface from Designer.
        self.setupUi(self)

        try:
            self.DBAPI = self.parent.DBAPI
        except:
            log.info("Parents Don't have a database, use own")
            self.DBAPI = simpleAPI()

        if self.ID is not None:
            self.get_generalInfo()
            self.setup_generalInfo()

    def get_generalInfo(self):
        """get the generalInfo
        and setup a few variables:
        self.list_generalInfo : stores the informations
            self.list_generalInfo=zip(header, entry)
            header, entry = zip(*self.list_generalInfo)

        self.MEDIAWIKI_ID : MEDIAWIKI_ID

        """
        header, entry = self.DBAPI.get_entry(self.ID, header='formated')
        self.list_generalInfo=zip(header, entry)
        adict=dict(self.list_generalInfo)

        if 'mediawiki' in adict:  # get MediaWiki ID
            self.MEDIAWIKI_ID= adict['mediawiki']

    def setup_generalInfo(self):
        """Fill generalInfo Box"""

        # get general informations
        header, entry = zip(*self.list_generalInfo)

        # get layout
        frame = self.frame_generalInfo
        layout = frame.layout()
        if layout is None:
             layout = QtGui.QGridLayout(frame)

        # setup Labels
        dict_generalInfo_labels={}
        for i in range(len(header)):
            key = header[i]  # get the key
            value = entry[i]  # get the value

            label_key = QtGui.QLabel()  # create new Label
            label_key.setText(_fromUtf8(key))  # _translate("Form", "General Informations", None)
            layout.addWidget(label_key,i,0)  # add Label to Widget

            spacer = QtGui.QLabel()  # create new Label
            spacer.setText(" : ")
            layout.addWidget(spacer, i, 1)  # add Label to Widget


            #    label_value = QtGui.QPushButton()

            label_value = QtGui.QLabel()  # create new Label
            if key == 'mediawiki':
                label_value.linkActivated.connect(self.event_open_MEDIAWIKI)
                label_value.setText('<a href="{}" style="color:#00a9e0;">{}</a>'.format(value,value))
            else:
                label_value.setText(str(value))  # _translate("Form", "General Informations", None)
            layout.addWidget(label_value, i, 2)  # add Label to Widget
            dict_generalInfo_labels.update({key : [label_key,label_value]})

        if 'ID' in dict_generalInfo_labels.keys():
            label_key, label_value = dict_generalInfo_labels['ID']
            myfont = QtGui.QFont()
            myfont.setBold(True)
            label_value.setFont(myfont)
        # modife labels
        #if 'MEDIAWIKI' in dict_generalInfo_labels.keys():
            #label_key, label_value = dict_generalInfo_labels['MEDIAWIKI']
            #label_value.setStyleSheet("QLabel { color : #00a9e0; text-decoration: underline; }");
            #label_value.mousePressEvent = self.event_open_MEDIAWIKI # only works because its created here
            #self.connect(label_value,QtCore.SIGNAL('clicked()'),self.event_open_MEDIAWIKI)

        btn = MyQt.ClickableLabel()
        btn.setText("DAS IST EIN TEST")
        self.connect(btn, QtCore.SIGNAL('clicked()'), self.event_open_MEDIAWIKI)
        layout.addWidget(btn)

    def event_open_MEDIAWIKI(self,linkStr):
        """Event open MediaWiki
        Opens the MediaWiki Entry
        """
        link=self.settings['mediawiki']['prefix']+str(self.MEDIAWIKI_ID)
        if self.settings['mediawiki']['browser'] == 'app':
            pass

        else:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))
            #    webbrowser.open(link)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GUi_tab_InfoEntry_LAMMPS(ID=2)

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass
    window.show()
    sys.exit(app.exec_())
