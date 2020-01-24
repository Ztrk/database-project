from PyQt5 import QtWidgets, uic
from astronomicalobject import AstronomicalObject

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, session, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("gui/mainwindow.ui", self)
        self.session = session

        # Fill table selector TreeWidget
        self.fill_table_selector()
        self.table_selector.currentItemChanged.connect(self.item_changed_handler)
    
    def fill_table_selector(self):
        objects = TableSelectorItem(self.table_selector, 'Obiekty astronomiczne')
        current = TableSelectorItem(objects, 'Małe ciała', self.small_bodies_page, AstronomicalObject)
        TableSelectorItem(objects, 'Sztuczne satelity', self.satellites_page, AstronomicalObject)
        TableSelectorItem(objects, 'Roje meteorów', self.meteor_showers_page)
        TableSelectorItem(objects, 'Gwiazdy', self.stars_page)
        TableSelectorItem(objects, 'Galaktyki', self.galaxies_page)
        TableSelectorItem(objects, 'Grupy galaktyk', self.galaxy_groups_page)

        TableSelectorItem(self.table_selector, 'Konstelacje', self.constellations_page)
        TableSelectorItem(self.table_selector, 'Katalogi', self.catalogues_page)
        TableSelectorItem(self.table_selector, 'Obserwacje', self.observations_page)
        TableSelectorItem(self.table_selector, 'Obserwatoria', self.observatories_page)
        TableSelectorItem(self.table_selector, 'Astronomowie', self.astronomers_page)
        self.item_changed_handler(current, None)
    
    def item_changed_handler(self, current, previous):
        if current.page is not None:
            self.stacked_widget.setCurrentWidget(current.page)
            # TODO: when all types implemented remove this if
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
        
class TableSelectorItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, text, page=None, type=None):
        super(TableSelectorItem, self).__init__(parent, [text])
        self.page = page
        self.type = type
        if page is not None:
            self.table = page.findChild(QtWidgets.QTableWidget)
