from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QTreeWidget,
                             QTreeWidgetItem)
from PyQt5.QtCore import Qt
import sys
from simdb.databaseModel import Keywords, Main, create_engine, sessionmaker


class SimpleTreeWidget(QWidget):
    def __init__(self):
        super(SimpleTreeWidget, self).__init__()
        self._header = ['entry_id', 'path', 'keywords', 'description', 'type']

        # define default parameters
        self.nested_mode = True  # Entries are nested.

        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.setLayout(self.vboxLayout)

        self.treeWidget = QTreeWidget()

        # Adding the widgets
        self.vboxLayout.addWidget(self.treeWidget)
        self.treeWidget.setHeaderLabel("TreeWidget oO")

        self.header = self._header
        self.build_tree()

    @property
    def header(self):
        """
        Function get get the current header.

        Returns
        -------
        header : List[str]
            current header of the treeWidget
        """
        return self._header

    @header.setter
    def header(self, header):
        """
        Function to set the current header of the treeWidget.

        Parameters
        ----------
        header : List[str]
            List of header items.

        Raises
        -------
        AssertionError
            If one of the items is not in the Maintable.
        """
        # sanity check
        assert all([h in Main.__dict__ for h in header]),  'invalid header\n:{}'.format(header)

        self._header = header
        for i, header in enumerate(header):
            self.treeWidget.headerItem().setText(i, header)

    def map_tooltip(self, key, sim):
        """
        Mapping function to create the tooltip.
        Parameters
        ----------
        key : str
            keyword
        sim : Main
            Simulation object.

        Returns
        -------
        tooltip : str
            Tooltip for the keyword.
        """
        tooltip = ""
        if key in ['entry_id', 'path', 'description', 'type']:
            tooltip = "Url:\n {}\n".format(sim.url)+\
                      "Path:\n {}\n".format(sim.path)+\
                      "Details:\n {}".format(sim.description)
        elif key == 'keywords':
            tags = "\n ".join([key.name for key in sorted(sim.keywords, key=lambda x: x.name)
                              if key.value is None or key.value == 'None'])
            keywords = "\n ".join(["{} = {}".format(key.name, key.value)
                                    for key in sorted(sim.keywords, key=lambda x: x.name)
                                     if key.value is not None and key.value != 'None'])
            tooltip = "Tags:\n {}\nKeywords:\n {}".format(tags, keywords)
        return tooltip

    def fill_child(self, child, sim):
        """
        Function to fill the QTreeWidgetItem with informations.

        Parameters
        ----------
        child : QTreeWidgetItem
            child item ot fill with informations
        sim : Main
            Database Main object

        Returns
        -------
        child : QTreeWidgetItem
            return the child with new informations.
        """
        child.setData(0, Qt.UserRole, sim.id)  # set Data in the item (ID of the table)
        for i, key in enumerate(self.header):

            value = getattr(sim, key)

            if key == 'keywords':
                value = "; ".join(["{}={}".format(kw.name, kw.value)
                                   if kw.value is not None and kw.value != '' else kw.name
                                   for kw in sim.keywords])

            child.setText(i, value)
            child.setToolTip(i, self.map_tooltip(key, sim))

    def add_children2parent(self, sim, parent):
        """
        Function to add children to the parent.

        Parameters
        ----------
        sim : Main
            Simulation object
        parent : QTreeWidgetItem
            parent item
        """
        children = sim.children
        if len(children) == 0:
            return None
        for sim_child in children:
            child = QTreeWidgetItem(parent)
            self.fill_child(child=child, sim=sim_child.child)
            self.childItems.append(child)
            if len(sim_child.child.children) != 0:
                self.add_children2parent(sim=sim_child.child, parent=child)

    def build_tree(self):
        """
        Function to build the tree of the treewidget
        Returns
        -------

        """

        # EXPERIMENTAL
        db_path = 'micha_raw.db'

        engine = create_engine('sqlite:///{}'.format(db_path))
        Session = sessionmaker(bind=engine)
        session = Session()

        if self.nested_mode:
            sims = session.query(Main).filter(~Main.parents.any()).order_by(Main.entry_id).all()
        else:
            sims = session.query(Main).order_by(Main.entry_id).all()

        # Adding the child to the top level item
        self.childItems = []
        for i, sim in enumerate(sims):
            child = QTreeWidgetItem(self.treeWidget)
            self.fill_child(child=child, sim=sim)
            self.childItems.append(child)
            if self.nested_mode and len(sim.children) != 0:
                self.add_children2parent(sim=sim, parent=child)

        # some general options
        self.treeWidget.sortByColumn(0, Qt.AscendingOrder)
        self.treeWidget.expandAll()



    def filter_tree(self, filtertext):
        """Filter treeWidget"""
        n_cols = len(self.header)
        if len(filtertext) != 0:
            # hide all items
            for item in self.childItems:
                item.setHidden(True)

            for i in range(n_cols): # number of columns
                for item in self.treeWidget.findItems(filtertext,Qt.MatchContains | Qt.MatchRecursive, column=i):
                    item.setHidden(False) # turn items on again if they match
        else:
            # show items
            for item in self.childItems:
                item.setHidden(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeWidgetDialog = SimpleTreeWidget()
    treeWidgetDialog.show()
    #treeWidgetDialog.filter_tree("polymorphism")
    sys.exit(app.exec_())