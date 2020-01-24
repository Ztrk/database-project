from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("gui/mainwindow.ui", self)

        # Fill table selector TreeWidget
        self.fill_table_selector()
        self.table_selector.currentItemChanged.connect(self.item_changed_handler)
    
    def fill_table_selector(self):
        objects = TableSelectorItem(None, 'Obiekty astronomiczne', self.table_selector)
        TableSelectorItem(self.small_bodies_page, 'Małe ciała', objects)
        TableSelectorItem(self.satellites_page, 'Sztuczne satelity', objects)
        TableSelectorItem(self.meteor_showers_page, 'Roje metorów', objects)
        TableSelectorItem(self.stars_page, 'Gwiazdy', objects)
        TableSelectorItem(self.galaxies_page, 'Galaktyki', objects)
        TableSelectorItem(self.galaxy_groups_page, 'Grupy galaktyk', objects)

        TableSelectorItem(self.constellations_page, 'Konstelacje', self.table_selector)
        TableSelectorItem(self.catalogues_page, 'Katalogi', self.table_selector)
        TableSelectorItem(self.observations_page, 'Obserwacje', self.table_selector)
        TableSelectorItem(self.observatories_page, 'Obserwatoria', self.table_selector)
        TableSelectorItem(self.astronomers_page, 'Astronomowie', self.table_selector)
    
    def item_changed_handler(self, current, previous):
        if current.page is not None:
            self.stacked_widget.setCurrentWidget(current.page)

class TableSelectorItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, page, text, parent):
        super(TableSelectorItem, self).__init__(parent, [text])
        self.page = page
