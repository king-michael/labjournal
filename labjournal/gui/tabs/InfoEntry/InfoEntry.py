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

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QDesktopServices

# import Ui_Form
from Ui_InfoEntry import Ui_Form


# import custom libs
root = "../../.."
sys.path.insert(0, root)
# from core.Database import *
from labjournal.core.databaseModel import *
from labjournal.gui.QtExtensions import FlowLayout

import logging

logger = logging.getLogger('LabJournal')
logging.basicConfig(level=logging.DEBUG)
from PyQt5.QtCore import QSettings

# ToDo: find a good organization / application name
# Todo: if added we can set the file path by ourself : https://stackoverflow.com/questions/4031838/qsettings-where-is-the-location-of-the-ini-file
settings = QSettings('foo', 'foo')


class InfoEntry(QtWidgets.QWidget, Ui_Form):
    def __init__(self, **kwargs):
        # super(self.__class__, self).__init__() # Note: self.__class__ will get recursion depth error
        super(InfoEntry, self).__init__()
        # set defaults
        self.parent = None
        self.ID = None

        self.tags_max_col = settings.value("InfoEntry/tags_max_col", 5)  # how many tags are displayed per row

        # assign kwargs
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        self.db = self.parent.db if self.parent is not None else settings.value('Database/file')
        # Set up the user interface from Designer.
        self.setupUi(self)

        if self.ID is not None:
            self.get_generalInfo()
            self.setup_generalInfo()
            self.fill_tags()

    def get_generalInfo(self):
        """
        get the generalInfo
        """

        session = establish_session('sqlite:///{}'.format(self.db))

        self.sim = session.query(Simulation).filter(Simulation.id == self.ID).one()
        self.list_generalInfo = [
            ['SimID', self.sim.sim_id],
            ['MediaWiki', self.sim.mediawiki],
            ['Path', self.sim.path],
            ['Description', self.sim.description],
        ]

        self.MEDIAWIKI_ID = self.sim.mediawiki  # get MediaWiki ID
        self.path = self.sim.path
        self.sim_tags = self.sim.keywords.filter(Keywords.value.is_(None)).all()
        self.sim_keywords = self.sim.keywords.filter(not_(Keywords.value.is_(None))).all()
        self.tags = [key.name for key in self.sim_tags]
        session.close()

    def create_tag_symbol(self, text):
        """add a tag symbol"""

        btn = QtWidgets.QToolButton(self)
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

    def add_tag(self, tag, ID=None):
        """
        Function to add tag
        should be stored somewhere central
        """
        # ToDo: Central Function, store somewhere else!
        if ID is None: ID = self.ID
        # PUSH
        logger.warn("PUSH change to DB")
        session = establish_session('sqlite:///{}'.format(self.db))
        sim = session.query(Simulation).filter(Simulation.id == self.ID).one()
        print(sim)
        sim.keywords.append(
            Keywords(
                main_id=sim.sim_id,
                name=tag,
                value=None,
            )
        )
        session.commit()
        self.sim_tags = sim.keywords.filter(Keywords.value.is_(None)).all()
        self.tags = [key.name for key in self.sim_tags]
        session.close()
        if self.parent is not None:
            self.parent.MyWidget_LabJournalIndex.build_tree()
    def fill_tags(self):
        """

        Returns
        -------

        """


        """fill tags"""

        layout =FlowLayout()
        self.layout_tags.addLayout(layout,0,0)

        # plus button
        btn = QtWidgets.QToolButton(self)
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
        self.btn_add_tag = btn  # save it
        self.btn_add_tag.clicked.connect(self.btn_add_tag_clicked)  # register action

        layout.addWidget(btn)  # add Label to Widget
        # Todo: Use a flowlayout here
        # http://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html
        # https://doc.qt.io/archives/4.6/layouts-flowlayout.html
        # https://stackoverflow.com/questions/9660080/how-does-one-fill-a-qgridlayout-from-top-left-to-right
        num_tags = len(self.tags)

        # if only one entry, check if entry is empty
        if num_tags == 1:
            if len(self.tags[0]) == 0:
                return
        # add tag symbols
        for i in range(num_tags):
            layout.addWidget(self.create_tag_symbol(self.tags[i]))



    def OLD_fill_tags(self):
        """

        Returns
        -------

        """


        """fill tags"""
        layout = self.layout_tags

        # plus button
        btn = QtWidgets.QToolButton(self)
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
        self.btn_add_tag = btn  # save it
        self.btn_add_tag.clicked.connect(self.btn_add_tag_clicked)  # register action

        layout.addWidget(btn, 0, 0)  # add Label to Widget
        # Todo: Use a flowlayout here
        # http://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html
        # https://doc.qt.io/archives/4.6/layouts-flowlayout.html
        # https://stackoverflow.com/questions/9660080/how-does-one-fill-a-qgridlayout-from-top-left-to-right
        num_tags = len(self.tags)
        # if only one entry, check if entry is empty
        if num_tags == 1:
            if len(self.tags[0]) == 0:
                return
        # add tag symbols
        for i in range(num_tags):
            # i+1 ; because of the added + sign
            row = (i + 1) / self.tags_max_col
            col = (i + 1) % self.tags_max_col
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
            layout = QtWidgets.QGridLayout(frame)

        # setup Labels
        dict_generalInfo_labels = {}

        for i in range(len(header)):
            key = header[i]  # get the key
            value = entry[i]  # get the value
            if key == 'simid': key = 'ID'  # change simid to ID
            label_key = QtWidgets.QLabel()  # create new Label
            label_key.setText(key)  # _translate("Form", "General Informations", None)
            layout.addWidget(label_key, i, 0)  # add Label to Widget

            spacer = QtWidgets.QLabel()  # create new Label
            spacer.setText(" : ")
            layout.addWidget(spacer, i, 1)  # add Label to Widget

            #    label_value = QtWidgets.QPushButton()

            label_value = QtWidgets.QLabel()  # create new Label
            if key == 'MediaWiki':
                label_value.linkActivated.connect(self.event_open_MEDIAWIKI)
                label_value.setText('<a href="{}" style="color:#00a9e0;">{}</a>'.format(value, value))
            else:
                label_value.setText(str(value))  # _translate("Form", "General Informations", None)
            layout.addWidget(label_value, i, 2)  # add Label to Widget
            dict_generalInfo_labels.update({key: [label_key, label_value]})

        if 'ID' in dict_generalInfo_labels.keys():
            label_key, label_value = dict_generalInfo_labels['ID']
            myfont = QtWidgets.QFont()
            myfont.setBold(True)
            label_value.setFont(myfont)


            # modife labels
            # if 'MEDIAWIKI' in dict_generalInfo_labels.keys():
            # label_key, label_value = dict_generalInfo_labels['MEDIAWIKI']
            # label_value.setStyleSheet("QLabel { color : #00a9e0; text-decoration: underline; }");
            # label_value.mousePressEvent = self.event_open_MEDIAWIKI # only works because its created here
            # self.connect(label_value,QtCore.SIGNAL('clicked()'),self.event_open_MEDIAWIKI)

    def event_open_MEDIAWIKI(self, linkstr=""):
        """
        Event: open MediaWiki Entry when link is clicked.

        Parameters
        ----------
        linkstr : str
            not used, but needed to connect the method to linkActivated event

        """
        # Read in settings
        protocol = settings.value("MediaWiki/protocol", 'http')  # get the protocol
        host = settings.value('MediaWiki/host', '134.34.112.156:777')  # get the host address
        path = settings.value('MediaWiki/path', 'mediawiki')  # get the path to the MediaWiki
        # Create link to the mediawiki page
        link = '{}://{}/{}/index.php/{}'.format(protocol, host, path, self.MEDIAWIKI_ID)
        # open the link in the browser
        QDesktopServices.openUrl(QtCore.QUrl(link))

# FIXME on klick on add tag button:
# Traceback(most
# recent
# call
# last):
# File
# "/home/andrejb/Software/labjournal/labjournal/gui/tabs/InfoEntry/InfoEntry.py", line
# 108, in btn_add_tag_clicked
# dlg = DialogAddTag()
# File
# "/home/andrejb/Software/labjournal/labjournal/gui/tabs/InfoEntry/InfoEntry.py", line
# 307, in __init__
# QtWidgets.QDialog.__init__(self, parent)
# File
# "/home/andrejb/Software/labjournal/labjournal/gui/tabs/InfoEntry/InfoEntry.py", line
# 325, in setupUi
#
# AttributeError: 'DialogAddTag'
# object
# has
# no
# attribute
# 'retranslateUi'
#
# Process
# finished
# with exit code 134 (interrupted by signal 6: SIGABRT)

class DialogAddTag(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Add Tag")
        Dialog.resize(400, 60)

        # Line Edit to enter tag
        self.ed_tag = QtWidgets.QLineEdit(Dialog)
        self.ed_tag.setObjectName("ed_tag")
        self.ed_tag.setGeometry(QtCore.QRect(0, 0, 400, 30))

        # Create Yes or No button
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(250, 31, 150, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)

        # connect button
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


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
        tag = str(tag)
    except:
        return False
    if len(tag) == 0: return False
    if tag.find(",") != -1: return False
    return True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = InfoEntry(ID=2,
                       db="/home/micha/SIM-PhD-King/micha.db")

    try:
        import qdarkstyle  # style

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())
