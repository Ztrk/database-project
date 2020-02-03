from PyQt5 import QtCore, QtWidgets, uic
import astronomy

class Second(QtWidgets.QDialog):
    def __init__(self, object_type, parent=None):
        super(Second, self).__init__(parent)
        uic.loadUi("gui/form-" + object_type + ".ui", self)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, session, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("gui/mainwindow.ui", self)
        self.session = session
        self.current_page = None
        self.object_type = ""

        # Fill table selector TreeWidget
        self.fill_table_selector()
        self.table_selector.currentItemChanged.connect(self.item_changed_handler)

        self.action_add.triggered.connect(self.add_to_table)
        self.action_remove.triggered.connect(self.remove_from_table)
        self.action_edit.triggered.connect(self.edit_table)
        self.astronomers_table.setModel(AstronomerModel(session))

    def fill_table_selector(self):
        objects = TableSelectorItem(self.table_selector, 'Obiekty astronomiczne')
        current = TableSelectorItem(objects, 'Małe ciała', self.small_bodies_page, astronomy.AstronomicalObject)
        TableSelectorItem(objects, 'Sztuczne satelity', self.satellites_page, astronomy.AstronomicalObject)
        TableSelectorItem(objects, 'Roje meteorów', self.meteor_showers_page)
        TableSelectorItem(objects, 'Gwiazdy', self.stars_page)
        TableSelectorItem(objects, 'Galaktyki', self.galaxies_page)
        TableSelectorItem(objects, 'Grupy galaktyk', self.galaxy_groups_page)

        TableSelectorItem(self.table_selector, 'Konstelacje', self.constellations_page, astronomy.Constellation)
        TableSelectorItem(self.table_selector, 'Katalogi', self.catalogues_page, astronomy.Catalogue)
        TableSelectorItem(self.table_selector, 'Obserwacje', self.observations_page, astronomy.Observation)
        TableSelectorItem(self.table_selector, 'Obserwatoria', self.observatories_page, astronomy.Observatory)
        TableSelectorItem(self.table_selector, 'Astronomowie', self.astronomers_page, astronomy.Astronomer)
        self.item_changed_handler(current, None)

    def item_changed_handler(self, current, previous):
        if current.page is not None:
            self.stacked_widget.setCurrentWidget(current.page)
            self.current_page = current.page
            # TODO: when all types are implemented remove this if
            if current.type is not None:
                self.fill_table(current.type, current.table)

    def fill_table(self, type, table):
        rows = self.session.query(type)
        if table is None:
            return
        table.setRowCount(rows.count())
        for i, entity in enumerate(rows):
            row = entity.to_row()
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                table.setItem(i, j, item)

    def add_to_table(self):
        # Add others (or come up with more generalized approach)
        objects = {
            self.constellations_page: "constellation",
            self.observatories_page: "observatory",
            self.astronomers_page: "astronomer"
        }
        self.object_type = objects.get(self.current_page, "Wrong")
        if self.object_type == "Wrong":
            return
        dialog = Second(self.object_type, self)
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

class AstronomerModel(QtCore.QAbstractTableModel):
    def __init__(self, session, *args, **kwargs):
        super(AstronomerModel, self).__init__(*args, **kwargs)
        self.session = session
        self.type = astronomy.Astronomer
        self.query = self.session.query(self.type)
        self.rows = self.query.all()
    
    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return 5

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            astronomer = self.rows[index.row()]
            return str(self.to_row(astronomer)[index.column()])

    def to_row(self, astronomer):
        return [astronomer.full_name, astronomer.country, astronomer.birth_date,
            astronomer.death_date, astronomer.name_mpc]
