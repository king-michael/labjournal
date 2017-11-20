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

# import Ui_Form
from Ui_tab_InfoEntry import Ui_Form

# import custom libs
sys.path.append("..")
from core.Database import *
from core.settings import settings


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


class GUi_tab_InfoEntry(QtGui.QWidget, Ui_Form):
    def __init__(self,**kwargs):
        #super(self.__class__, self).__init__() # Note: self.__class__ will get recursion depth error
        super(GUi_tab_InfoEntry,self).__init__()
        # set defaults
        self.parent = None
        self.ID=None
        self.settings={
            'mediawiki' : {  # MediaWiki settings
                'prefix'  : "http://134.34.112.156:777/mediawiki/index.php/",  # prefix
                'browser' : 'browser',  # how to open it [browser = defaultbrowser]
            },  # MediaWiki settings
            'tags_max_col' : 5
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
            self.fill_tags()

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

        self.MEDIAWIKI_ID= adict['mediawiki'] # get MediaWiki ID
        self.tags = adict['tags'].split(",")

        if len(self.tags) ==1 and len(self.tags[0]) == 0:
            self.tags = [] # remove and empty list


    def create_tag_symbol(self,text):
        """add a tag symbol"""

        btn = QtGui.QToolButton(self)
        btn.setText(text)
        font = btn.font()
        font.setBold(True)
        btn.setFont(font)
        btn.setStyleSheet("""
            background-color: #00a9e0;
            color: rgb(255, 255, 255);
            border: 0 px;
            border-radius: 15;
            """)

        return btn

    def btn_add_tag_clicked(self):
        "Event if add_tag button is clicked"
        dlg = DialogAddTag()
        if dlg.exec_():
            tag = dlg.get_tag()
            if valid_tag(tag):
                print("DEBUG: Try to add tag: {}".format(tag))
                self.add_tag(tag)
                self.fill_tags()

    def add_tag(self,tag,ID=None):
        """
        Function to add tag
        should be stored somewhere central
        """
        # ToDo: Central Function, store somewhere else!
        if ID is None: ID = self.ID
        self.tags.append(tag)
        print("DEBUG: Added tag: {} to ID: {}".format(tag,ID))
        tag_string=",".join(self.tags)
        print("DEBUG: tag_string: {}".format(tag_string))
        self.DBAPI.df.loc[ID, 'tags']=tag_string
        if self.parent is not None:
            self.parent.MyWidget_LabJournalIndex.build_tree()

    def fill_tags(self):
        """fill tags"""
        layout = self.layout_tags

        # plus button
        btn = QtGui.QToolButton(parent=self)
        btn.setText("+")
        font = btn.font()
        font.setBold(True)
        btn.setFont(font)
        btn.setStyleSheet("""
                    background-color: #808080;
                    color: #00a9e0;
                    border: 0 px;
                    border-radius: 15;
                    """)
        self.btn_add_tag=btn # save it
        self.btn_add_tag.clicked.connect(self.btn_add_tag_clicked) # register action

        layout.addWidget(btn, 0, 0)  # add Label to Widget

        num_tags = len(self.tags)
        # if only one entry, check if entry is empty
        if num_tags == 1:
            if len(self.tags[0]) == 0:
                return
        # add tag symbols
        for i in range(num_tags):
            # i+1 ; because of the added + sign
            row = (i+1) / self.settings['tags_max_col']
            col = (i+1) % self.settings['tags_max_col']
            tag = self.tags[i]
            layout.addWidget(self.create_tag_symbol(tag), row, col)  # add Label to Widget


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
        header=list(header)
        header.remove('tags')

        for i in range(len(header)):
            key = header[i]  # get the key
            value = entry[i]  # get the value
            if key == 'simid': key='ID'  # change simid to ID
            label_key = QtGui.QLabel()  # create new Label
            label_key.setText(_fromUtf8(key))  # _translate("Form", "General Informations", None)
            layout.addWidget(label_key,i,0)  # add Label to Widget

            spacer = QtGui.QLabel()  # create new Label
            spacer.setText(" : ")
            layout.addWidget(spacer, i, 1)  # add Label to Widget


            #    label_value = QtGui.QPushButton()

            label_value = QtGui.QLabel()  # create new Label
            if   key == 'mediawiki':
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


class DialogAddTag(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

    def setupUi(self,Dialog):
        Dialog.setObjectName("Add Tag")
        Dialog.resize(400, 60)

        # Line Edit to enter tag
        self.ed_tag = QtGui.QLineEdit(Dialog)
        self.ed_tag.setObjectName("ed_tag")
        self.ed_tag.setGeometry(QtCore.QRect(0, 0, 400, 30))

        # Create Yes or No button
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(250, 31, 150, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)

        # connect button
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        # self.label.setText(
        #     QtGui.QApplication.translate("Dialog", "Set example value:", None, QtGui.QApplication.UnicodeUTF8))
    def get_tag(self):
        return str(self.ed_tag.text())


def valid_tag(tag):
    """
    function to check if tag is valid
     -> str(tag) is possible !
     -> len(tag) > 0
     -> no comma !
    Save somewhere in a main folder
    """
    # ToDO: see doc string, move it to some central place
    try:
        tag=str(tag)
    except:
        return False
    if len(tag) == 0: return False
    if tag.find(",") != -1: return False
    return True


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GUi_tab_InfoEntry(ID=2)

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass
    window.show()
    sys.exit(app.exec_())
