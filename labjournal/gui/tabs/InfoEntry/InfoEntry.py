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
import logging

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QSettings

from Ui_InfoEntry import Ui_Form

from labjournal.core.databaseModel import *
from labjournal.gui.QtExtensions import FlowLayout

# ToDo: find a good organization / application name
# Todo: if added we can set the file path by ourself : https://stackoverflow.com/questions/4031838/qsettings-where-is-the-location-of-the-ini-file
logger = logging.getLogger('LabJournal')

APPLICATION_NAME = 'foo'
COMPANY_NAME = 'foo'
settings = QSettings(APPLICATION_NAME, COMPANY_NAME)


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

        # Add more design options
        self.layout_tags = FlowLayout()  # Create a FlowLayout for the tags
        self.layout_tags_keywords.addLayout(self.layout_tags,0,1)  # add it to the GridLayout
        self.layout_keywords = FlowLayout()  # Create a FlowLayout for the keywords
        self.layout_tags_keywords.addLayout(self.layout_keywords, 1, 1)  # add it to the GridLayout

        if self.ID is not None:
            self.get_generalInfo()
            self.setup_generalInfo()
            self.fill_tags_keywords()

    def get_generalInfo(self):
        """
        get the generalInfo
        """

        session = establish_session('sqlite:///{}'.format(self.db))

        self.sim = session.query(Main).filter(Main.id == self.ID).one()
        self.list_generalInfo = [
            ['SimID', self.sim.entry_id],
            ['MediaWiki', self.sim.mediawiki],
            ['Path', self.sim.path],
            ['Description', self.sim.description],
        ]

        self.MEDIAWIKI_ID = self.sim.mediawiki  # get MediaWiki ID
        self.path = self.sim.path
        self.sim_tags = self.sim.keywords.filter(Keywords.value.is_(None)).all()
        self.sim_keywords = self.sim.keywords.filter(not_(Keywords.value.is_(None))).all()
        self.tags = [key.name for key in self.sim_tags]
        self.keywords = dict({(key.name,key.value) for key in self.sim_keywords})
        print(self.keywords)
        session.close()

    def btn_add_tag_clicked(self):
        "Event if add_tag button is clicked"
        dlg = DialogAddTag()
        if dlg.exec_():
            tag = dlg.get_tag()
            if valid_tag(tag):
                print("DEBUG: Try to add tag: {}".format(tag))
                self.add_tag(tag)
                self.fill_tags_keywords()

    def add_tag(self, tag):
        """
        Function to add tag
        should be stored somewhere central
        """

        tag_split = tag.split("=",1)
        value = None if len(tag_split) == 1 else tag_split[1].strip()
        tag = tag_split[0].strip()
        if tag in self.tags:
            if value is None:
                QtWidgets.QMessageBox.warning(self, "Tag exists",
                    "The selected tag already exists for this simulation.",
                    QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
                return

        # ToDo: Central Function, store somewhere else!
        # PUSH
        logger.warn("PUSH change to DB")
        session = establish_session('sqlite:///{}'.format(self.db))
        sim = session.query(Main).filter(Main.id == self.ID).one()
        keyword = sim.keywords.filter(Keywords.main_id == sim.id, Keywords.name == tag).one_or_none()
        if keyword is not None:
            keyword.value=value
        else:
            sim.keywords.append(
                Keywords(
                    main_id=sim.id,
                    name=tag,
                    value=value,
                )
            )
        session.commit()
        # Todo: create a method for the refreshment routine (multiple times in this file)
        # reset the variables
        self.sim_tags = sim.keywords.filter(Keywords.value.is_(None)).all()
        self.sim_keywords = sim.keywords.filter(not_(Keywords.value.is_(None))).all()
        self.tags = [key.name for key in self.sim_tags]
        self.keywords = dict({(key.name,key.value) for key in self.sim_keywords})
        # clsoe the session
        session.close()
        if self.parent is not None:
            self.parent.MyWidget_LabJournalIndex.build_tree()

    def remove_tag(self,tag):
        """
        Function to remove the tag

        Parameters
        ----------
        tag : str
            tag name
        """
        tag_split = tag.split("=", 1)
        value = None if len(tag_split) == 1 else tag_split[1].strip()
        tag = tag_split[0].strip()

        logger.warn("PUSH change to DB")
        session = establish_session('sqlite:///{}'.format(self.db))
        sim = session.query(Main).filter(Main.id == self.ID).one()
        keyword = sim.keywords.filter(Keywords.main_id == sim.id, Keywords.name == tag).one()  # Explode if not one
        session.delete(keyword)  # delete the keyword
        session.commit()  # push the change to the database
        # reset the variables
        self.sim_tags = sim.keywords.filter(Keywords.value.is_(None)).all()
        self.sim_keywords = sim.keywords.filter(not_(Keywords.value.is_(None))).all()
        self.tags = [key.name for key in self.sim_tags]
        self.keywords = dict({(key.name, key.value) for key in self.sim_keywords})
        session.close()  # close thte session

    def sideMenu_addContent(self,parent):
        """Creates Content in the sideMenu"""
        label = QtWidgets.QLabel()
        label.setText("Save a stupid function to test in the button")
        label.setWordWrap(True)
        parent.layout_sideMenu.addWidget(label)  # add the pushButton to the sideMenu
        btn = QtWidgets.QPushButton("Debug Button")  # create a pushButton for a new database Entry
        btn.clicked.connect(self.fill_tags_keywords)  # connect it to the event
        parent.layout_sideMenu.addWidget(btn)  # add the pushButton to the sideMenu

    def fill_tags_keywords(self):
        """
        Function to fill the keywords and tags
        """

        # Clear layout tags
        for i in range(self.layout_tags.count()):    # do it for all items
            child = self.layout_tags.takeAt(0)  # get the first child
            self.layout_tags.removeItem(child)  # remove it from the widget
            child.widget().deleteLater()  # delete child

        # Clear layout keywords
        for i in range(self.layout_keywords.count()):  # do it for all items
            child = self.layout_keywords.takeAt(0)  # get the first child
            self.layout_keywords.removeItem(child)  # remove it from the widget
            child.widget().deleteLater()  # delete child

        # add PlusButton tags
        self.btn_add_tag = PlusButton()  # get the PlusButton
        self.btn_add_tag.clicked.connect(self.btn_add_tag_clicked)  # register action
        self.layout_tags.addWidget(self.btn_add_tag)  # add Label to Widget

        # add PlusButton keywords
        self.btn_add_tag = PlusButton()  # get the PlusButton
        self.btn_add_tag.clicked.connect(self.btn_add_tag_clicked)  # register action
        self.layout_keywords.addWidget(self.btn_add_tag)  # add Label to Widget

        # add the tags
        for tag in self.tags:
            self.layout_tags.addWidget(TagSymbol(tag,self))  # create a new tagsymbol

        # add the tags
        for tag,value in self.keywords.iteritems():
            self.layout_keywords.addWidget(TagSymbol("{} = {}".format(tag,value),self))  # create a new tagsymbol

    def setup_generalInfo(self):
        """
        Fill generalInfo Box
        """

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
            label_key.setText(key)   # _translate("Form", "General Informations", None)
            font = label_key.font()  # get the font of the label
            font.setBold(True)       # set it to Bold
            label_key.setFont(font)  # set font of the label
            layout.addWidget(label_key, i, 0)  # add Label to Widget

            spacer = QtWidgets.QLabel()  # create new Label
            spacer.setText(" : ")
            font = spacer.font()  # get the font of the label
            font.setBold(True)  # set it to Bold
            spacer.setFont(font)  # set font of the label
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


class DialogAddTag(QtWidgets.QDialog):
    """
    Dialog that opens to add a Tag
    """
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        # type: (QtWidgets.QDialog) -> None
        """Function to initialize the Setup of the User Interface

        Parameters
        ----------
        Dialog : QtWidgets.QDialog
            QtWidget to apply the User Interface on
        Returns
        -------

        """

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

        # connect button
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)


    def get_tag(self):
        return str(self.ed_tag.text())


class  PlusButton(QtWidgets.QToolButton):
    def __init__(self):
        """
        Plus Button for adding tags or keywords
        """
        super(QtWidgets.QToolButton, self).__init__()
        self.setText("+")
        font = self.font()
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet("""
        background-color: #808080;
        color: #00a9e0;
        border: 0 px;
        border-radius: 15;
        """)

class TagSymbol(QtWidgets.QToolButton):
    def __init__(self,text,parent):
        """
        Plus Button for adding tags or keywords

        Parameters
        ----------
        text : str
            Text to be displayed
        parent : QtWidget(InfoEntry)
            parent of the tag (connect method to it)
        """

        super(QtWidgets.QToolButton, self).__init__()

        self.parent = parent  # save parent

        # setup the tag symbol
        self.setText(text)
        font = self.font()
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet("""QToolButton {
        background-color: #00a9e0;
        color: rgb(255, 255, 255);
        border: 0 px;
        border-radius: 15;
        } """)

        # set the contextMenuPolicy
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # use customContextMenu (because of dropdown)
        self.customContextMenuRequested.connect(self.on_context_menu)  # contect to signal

        # Define the context menu
        self.popMenu = QtWidgets.QMenu(self)
        # define action to delete tag
        action_delete = QtWidgets.QAction('change', self)
        action_delete.setToolTip('change tag/keyword')
        action_delete.triggered.connect(self.event_change_tag)
        self.popMenu.addAction(action_delete)
        # self.popMenu.addSeparator()
        # define action to change the tag
        action_delete = QtWidgets.QAction('remove', self)
        action_delete.setToolTip('removes the tag/keyword')
        action_delete.triggered.connect(self.event_delete_tag)
        self.popMenu.addAction(action_delete)

    def on_context_menu(self,point):
        """
        Function to display the context menu
        """
        self.popMenu.exec_(self.mapToGlobal(point))

    def event_delete_tag(self):
        """
        Event called to delete the tag
        connects to method in parent
        """
        self.parent.remove_tag(self.text())
        self.parent.fill_tags_keywords()  # refresh the tag/keyword symbols

    def event_change_tag(self):
        """
        Event called to change tag
        connects to method in parent
        """

        dlg = DialogAddTag()  # popup dialog
        dlg.ed_tag.setText(self.text())  # set the defualt text
        dlg.ed_tag.setPlaceholderText(self.text())  # set PlaceholderText (so we can see what was there before)
        if dlg.exec_():
            tag = dlg.get_tag()  # get the tag
            if len(tag.strip()) == 0:  # incase we changed it to empty
                self.parent.remove_tag(self.text())  # delete the original tag
            if valid_tag(tag):
                print("DEBUG: Try to change tag: {} ==> {}".format(self.text(),tag))
                # check if the tag is the same, else delete the original
                if self.text().split("=",1)[0].strip() != tag.split("=", 1)[0].strip():
                    self.parent.remove_tag(self.text())  # delete the original if its a renaming
                self.parent.add_tag(tag)  # add/update a new tag
                self.parent.fill_tags_keywords()  # refresh the tag/keyword symbols

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
    import os
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../..')))  # add module to path
    logging.basicConfig(level=logging.DEBUG)
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
