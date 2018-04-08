"""
Settings Dialog
"""

import logging
import sys
import os
import pkg_resources
from functools import partial

from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtCore import QSettings

from Ui_DialogSettings import Ui_Dialog

logger = logging.getLogger('LabJournal')

APPLICATION_NAME='foo'
COMPANY_NAME='foo'
PATH_TO_DEFAULT_CONFIG = os.path.join(pkg_resources.resource_filename('labjournal', ''), "default_conifg.ini")

class DialogSettings(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        """
        Settings Dialog
        """

        super(DialogSettings, self).__init__(parent)
        self.setupUi(self)  # where to display

        self.list_pages=[
            ('General', SettingsGeneral),      # General settings
            ('MediaWiki', SettingsMediaWiki),  # page for MediaWiki settings
            ('LAMMPS', SettingsLAMMPS),        # page for LAMMPS settings
        ]
        self.dict_changed_options = dict()

        self.listWidget.itemSelectionChanged.connect(self.on_listWidget_itemSelectionChanged)
        for i, (k,v) in enumerate(self.list_pages):
            item = QtWidgets.QListWidgetItem()
            item.setText(k)
            self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(0)

        # Connect buttonBox
        self.buttonBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_defaults)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply_settings)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.event_accepted)

    def on_listWidget_itemSelectionChanged(self):
        """
        Function invoked when itemselection changes
        deletes the old widget
        sets the new one
        """

        if hasattr(self,'pageWidget'):  # if we have a pageWidget delete it
            self.pageWidget.deleteLater()

        i = self.listWidget.currentRow()  # get the current index
        self.pageWidget = self.list_pages[i][1](self)  # get the widget and activate it
        self.layout_frame.addWidget(self.pageWidget)   # set the widget in the layout
        # Todo: morph frame to scrollalbe area
        # https://stackoverflow.com/questions/20041385/python-pyqt-setting-scroll-area?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

    def apply_settings(self):
        """
        Function to apply Settings
        Returns
        -------

        """
        settings = QSettings(COMPANY_NAME,APPLICATION_NAME)  # loads the user config
        for k, v in self.dict_changed_options.iteritems():
            logger.debug("DialogSettings:set {} = {}".format(k,v))
            settings.setValue(k,v)  # set settings
        del settings

    def restore_defaults(self):
        """
        Function to return the default settings
        """

        # get the path to the default default_conifg.ini
        logger.debug('DialogSettings:restore_defaults')
        #path_to_config = os.path.join(pkg_resources.resource_filename('labjournal', ''), "default_conifg.ini")

        default_settings = QSettings(PATH_TO_DEFAULT_CONFIG, QSettings.IniFormat)  # load the default config
        settings = QSettings(COMPANY_NAME,APPLICATION_NAME)  # loads the user config

        # copy all default values
        for key in default_settings.allKeys():
            settings.setValue(key,default_settings.value(key))

        del settings  # push the write out

    def event_accepted(self):
        """
        Event when we press OK
        """
        self.apply_settings()  # apply settings
        self.accept()  # close


class SettingsTemplate(QtWidgets.QWidget):
    """
    Template for Settings tabs
    """
    def __init__(self,parent=None):
        super(SettingsTemplate, self).__init__(parent)
        self.parent = self if parent is None else parent

        self.page_title = "Template"
        self.group=""
        self.list_options = [] # list of options; we need to overwrite this
        self.dict_changed_options = dict()  # dummy purpose, if parent is None

    def setupUi(self):
        """
        Function to setup the Ui
        """
        # init Layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.layout()
        # add page title
        self.label = QtWidgets.QLabel(self.page_title)
        self.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        )
        layout.addWidget(self.label)
        # add line
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(line)
        # add frame
        self.frame = QtWidgets.QFrame()
        self.frame.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        )
        layout.addWidget(self.frame)
        layout_tmp = QtWidgets.QVBoxLayout()
        self.frame.setLayout(layout_tmp)
        self.layout_main = QtWidgets.QVBoxLayout()
        layout_tmp.addLayout(self.layout_main)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_tmp.addItem(spacerItem1)

    def auto_fill(self):
        """

        Returns
        -------

        """
        default_settings = QSettings(PATH_TO_DEFAULT_CONFIG, QSettings.IniFormat)  # load the default config
        settings = QSettings(COMPANY_NAME, APPLICATION_NAME)  # loads the user config

        settings.beginGroup(self.group)  # enter the group
        default_settings.beginGroup(self.group)  # enter the group

        layout_grid = QtWidgets.QGridLayout()  # create GridLayout, so everything gets aligned

        for i, row in enumerate(self.list_options):
            if len(row) == 1:
                print row
                # add line
                line = QtWidgets.QFrame()
                layout_tmp = QtWidgets.QVBoxLayout()
                label = QtWidgets.QLabel()
                label.setText(row[0][1])
                myFont = QtGui.QFont()
                myFont.setBold(True)
                label.setFont(myFont)
                layout_tmp.addWidget(label)
                line.setLayout(layout_tmp)
                layout_grid.addWidget(line,i,0)
            elif len(row) == 3 or len(row) == 4:  # if its an entry
                name = row[0]
                settings_key = row[1]
                description = row[2]
                # Create Label
                label = QtWidgets.QLabel()
                label.setText(name)
                label.setToolTip(description)
                layout_grid.addWidget(label,i,0)

                # Create Spacer
                spacer = QtWidgets.QLabel()
                spacer.setText(" : ")
                layout_grid.addWidget(spacer, i, 1)

                # Create LineEdit

                value = settings.value(settings_key,
                                       default_settings.value(settings_key))  # get the value, use default if not there

                if  len(row) == 3:
                    line_edit = QtWidgets.QLineEdit(self)
                    # ToDo: find a better Method to save Lists
                    if type(value) == list:
                        value = "#LIST: "+", ".join([str(ii) for ii in value])
                    line_edit.setText(value)
                    line_edit.setToolTip(description)
                    layout_grid.addWidget(line_edit, i, 2)
                    line_edit.textChanged.connect(partial(self.on_changeEvent, i, line_edit))
                else:
                    options=row[3]
                    comboBox = QtWidgets.QComboBox()
                    comboBox.setToolTip(description)
                    comboBox.setEditable(True)
                    comboBox.addItems(options)
                    comboBox.currentTextChanged.connect(partial(self.on_changeEvent, i,comboBox))
                    completer = QtWidgets.QCompleter(options)
                    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                    comboBox.setCompleter(completer)
                    layout_grid.addWidget(comboBox, i, 2)

        self.layout_main.addLayout(layout_grid)  # add layout to widget

        settings.endGroup()  # self.group

    def on_changeEvent(self, i, widget):
        """
        Function on change event

        Parameters
        ----------
        event : QEvents
            event SIGNAL
        i : int
            index of self.list_options entry

        """

        # get the value, dependend on the widget type
        if type(widget) == QtWidgets.QComboBox:  # check if its a comboBox
            value = widget.currentText()
        elif type(widget) ==QtWidgets.QLineEdit:  # check if its a lineEdit
            value = widget.text()
        if value.strip().startswith("#LIST: "):
            value = [ii.strip() for ii in value.replace("#LIST: ",'').split(',')]
        _, settings_str, _ = self.list_options[i]  # get settings string
        key="{}/{}".format(self.group,settings_str) if len(self.group) != 0 else settings_str  # create key

        self.parent.dict_changed_options[key]=value


class SettingsGeneral(SettingsTemplate):
    def __init__(self,parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.parent = self if parent is None else parent

        self.page_title='General'
        self.setupUi()



class SettingsMediaWiki(SettingsTemplate):
    def __init__(self,parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.parent=self if parent is None else parent

        self.page_title='MediaWiki'
        self.setupUi()

        self.group = 'MediaWiki'
        self.list_options = [
            # Normal: label, settings_str, description, options
            # Group: [label, settings_str],
            ('Protocol', 'protocol','Protoctol used to connect to the MediaWiki', ['http', 'https']),  # settings for protocol
            ('Host Server', 'host', 'MediaWiki Server'),
            ('path', 'path', 'URL path on the MediaWiki Server'),
        ]

        self.auto_fill()

class SettingsLAMMPS(SettingsTemplate):
    def __init__(self,parent):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.parent = self if parent is None else parent
        self.page_title='MediaWiki'
        self.setupUi()

        self.group = 'LAMMPS'
        self.list_options = [
            # Normal: label, settings_str, description, options
            # Group: [label, settings_str],
            # GROUP folders
            (['Folders',                'folders'],), # group
            ('EM_and_Equilibration',    'folders/EM_and_Equilibration', "Folder the run the EM and Equilibration"),
            ('roduction',               'folders/production', "Folder the run the production"),
            ('analysis',                'folders/analysis', 'Analysis folder'),
            ('analysis_MetaD',          'folders/analysis_MetaD', 'Analysis folder for MetaDynamic'),
            # GROUP pattern
            (['Pattern',                'pattern'],),  # group
            ('final_data',              'pattern/final_data', 'pattern for final_data'),
            ('final_restart',           'pattern/final_restart', 'pattern for final_restart'),
            ('logfile',                 'pattern/logfile', 'pattern for logfile'),
            ('trajectory',              'pattern/trajectory', 'pattern for trajectory'),
            # GROUP thermo
            (['Thermo',        'thermo'],),  # group
            ('list_keywords',  'thermo/list_keywords', 'List of thermo keywords to be used'),
            ('save_subfolder', 'thermo/save_subfolder', 'Folder to save plots in'),
            ('xlabel',         'thermo/xlabel', 'Default xlabel of thermo plots'),
        ]

        self.auto_fill()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.path.append('../../../')

    app = QtWidgets.QApplication(sys.argv)
    dialog = DialogSettings()

    try:
        import qdarkstyle  # style

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    dialog.show()
    sys.exit(app.exec_())
