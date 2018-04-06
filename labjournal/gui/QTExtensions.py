"""
QT objects extensions
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


# check : http://popdevelop.com/2010/05/an-example-on-how-to-make-qlabel-clickable/
# class ExtendedQLabel(QLabel):
#     def __init__(self,parent):
#         QLabel.__init__(self, parent)
#
#     # def mousePressEvent(self, ev):
#     #     self.emit(SIGNAL('clicked()'))
#
#     def mouseReleaseEvent(self, ev):
#         self.emit(SIGNAL('clicked()'))
#
#     def wheelEvent(self, ev):
#         self.emit(SIGNAL('scroll(int)'), ev.delta())

class ExtendedQLabel(QLabel):
        def __init(self, parent):
            QLabel.__init__(self, parent)

        def mousePressEvent(self, ev):
            self.emit(SIGNAL('clicked()'))
            self.clicked.emit()

class ClickableLabel(QLabel):
    """
    clicked signal definition
    """
    clicked = pyqtSignal()
    def __init__(self, text = "", parent = None):
        super(ClickableLabel, self).__init__(text, parent)
        self.setText(text)
        self.clicked.connect(self.onClicked)
    def onClicked(self):
        text = self.text()
        text = "<center><font color=red>" + text + "</font></center>"
        self.setText(text)
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

def clickable(widget):
    """
    Usage:
        clickable(label1).connect(self.showText1)
    """
    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)