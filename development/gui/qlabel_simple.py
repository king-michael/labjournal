from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QLabel)
from PyQt5.QtCore import QSize, Qt
import sys

class KeywordLabel(QLabel):
    def __init__(self,keyword='', value=None, parent=None):
        super(QLabel, self).__init__(parent)

        stylesheet = " ".join([
            'border-radius: 10px;',
            'background: rgb(170, 170, 255);',
            'color: white;'
        ])
        self.setStyleSheet(stylesheet)

        self.setMinimumSize(QSize(40, 40))
        self.setAlignment(Qt.AlignCenter)

        # set text
        if value is None:
            text = "<span style='font-size:18pt; font-weight:600;'>{}</span>".format(keyword)
        else:
            text = "<span style='font-size:10pt; font-weight:600;'>{}</span><br>".format(keyword)
            text += "<span style='font-size:18pt; font-weight:600;'>{}</span>".format(value)
        self.setText(text)


class SimpleTreeWidget(QWidget):
    def __init__(self):
        super(SimpleTreeWidget, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.setLayout(self.vboxLayout)

        label = QLabel("simple Label")
        self.vboxLayout.addWidget(label)

        label = QLabel("css Label")
        label.setStyleSheet("border-radius: 10px; background: red; color: #4A0C46;")
        label.setMinimumSize(QSize(40,40))
        label.setAlignment(Qt.AlignCenter)
        self.vboxLayout.addWidget(label)

        text = "<span style='font-size:10pt; font-weight:600;'>keyword</span><br>"
        text+= "<span style='font-size:18pt; font-weight:600;'>value</span>"
        label = QLabel(text)
        label.setStyleSheet("border-radius: 10px; background: rgb(170, 170, 255); color: white;")
        label.setMinimumSize(QSize(40, 40))
        label.setAlignment(Qt.AlignCenter)
        self.vboxLayout.addWidget(label)

        label = KeywordLabel('engine','LAMMPS')
        self.vboxLayout.addWidget(label)

        label = KeywordLabel('only a tag')
        self.vboxLayout.addWidget(label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeWidgetDialog = SimpleTreeWidget()
    treeWidgetDialog.show()
    sys.exit(app.exec_())