from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import astronomy

objectType = ""


class Second(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        uic.loadUi("gui/add-" + objectType + ".ui", self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, session, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("gui/mainwindow.ui", self)
        self.session = session
        self.current_page = None

        # Fill table selector TreeWidget
        self.fill_table_selector()
        self.table_selector.currentItemChanged.connect(self.item_changed_handler)

        self.actionAdd.triggered.connect(self.add_to_table)
        self.actionRemove.triggered.connect(self.remove_from_table)
        self.actionEdit.triggered.connect(self.edit_table)

    def fill_table_selector(self):
        objects = TableSelectorItem(self.table_selector, 'Obiekty astronomiczne')
        current = TableSelectorItem(objects, 'Małe ciała', self.small_bodies_page, astronomy.AstronomicalObject)
        TableSelectorItem(objects, 'Sztuczne satelity', self.satellites_page, astronomy.AstronomicalObject)
        TableSelectorItem(objects, 'Roje meteorów', self.meteor_showers_page)
        TableSelectorItem(objects, 'Gwiazdy', self.stars_page)
        TableSelectorItem(objects, 'Galaktyki', self.galaxies_page)
        TableSelectorItem(objects, 'Grupy galaktyk', self.galaxy_groups_page)

        TableSelectorItem(self.table_selector, 'Konstelacje', self.constellations_page, astronomy.Constellation)
        TableSelectorItem(self.table_selector, 'Katalogi', self.catalogues_page)
        TableSelectorItem(self.table_selector, 'Obserwacje', self.observations_page)
        TableSelectorItem(self.table_selector, 'Obserwatoria', self.observatories_page)
        TableSelectorItem(self.table_selector, 'Astronomowie', self.astronomers_page)
        self.item_changed_handler(current, None)

    def item_changed_handler(self, current, previous):
        if current.page is not None:
            self.stacked_widget.setCurrentWidget(current.page)
            # TODO: when all types implemented remove this if
            self.current_page = current.page
            if current.type is not None:
                self.fill_table(current.type, current.table)

    def fill_table(self, type, table):
        rows = self.session.query(type)
        table.setRowCount(rows.count())
        for i, entity in enumerate(rows):
            row = entity.to_row()
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(value)
                table.setItem(i, j, item)

    def add_to_table(self):
        # Add others (or come up with more generalized approach)
        global objectType
        objects = {
            self.constellations_page: "constellation",
            self.observatories_page: "observatory",
            self.astronomers_page: "astronomer"
        }
        objectType = objects.get(self.current_page, "Wrong")
        if objectType == "Wrong":
            return
        dialog = Second(self)
        # self.dialogs.append(dialog)
        dialog.show()

    def remove_from_table(self):
        pass

    def edit_table(self):
        pass


class TableSelectorItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, text, page=None, type=None):
        super(TableSelectorItem, self).__init__(parent, [text])
        self.page = page
        self.type = type
        if page is not None:
            self.table = page.findChild(QtWidgets.QTableWidget)
    #     self.Add.clicked.connect(self.AddAction)
    #
