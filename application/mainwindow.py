from PyQt5 import QtCore, QtWidgets, uic
import astronomy
import astronomy_model as model


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, session, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("gui/mainwindow.ui", self)
        self.session = session
        self.current_model = None

        # Fill table selector TreeWidget
        self.fill_table_selector()
        self.table_selector.currentItemChanged.connect(self.item_changed_handler)

        self.action_add.triggered.connect(self.add_to_table)
        self.action_remove.triggered.connect(self.remove_from_table)
        self.action_edit.triggered.connect(self.edit_table)

    def fill_table_selector(self):
        objects = TableSelectorItem(self.table_selector, 'Obiekty astronomiczne')
        TableSelectorItem(objects, 'Małe ciała', model.SmallBodyModel(self.session))
        TableSelectorItem(objects, 'Sztuczne satelity', model.SatelliteModel(self.session))
        TableSelectorItem(objects, 'Roje meteorów', model.MeteorShowerModel(self.session))
        TableSelectorItem(objects, 'Gwiazdy', model.StarModel(self.session))
        TableSelectorItem(objects, 'Galaktyki', model.GalaxyModel(self.session))
        TableSelectorItem(objects, 'Grupy galaktyk', model.GalaxyGroupModel(self.session))

        TableSelectorItem(self.table_selector, 'Konstelacje', model.ConstellationModel(self.session))
        TableSelectorItem(self.table_selector, 'Katalogi', model.CatalogueModel(self.session))
        TableSelectorItem(self.table_selector, 'Obserwacje', model.ObservationModel(self.session))
        TableSelectorItem(self.table_selector, 'Obserwatoria', model.ObservatoryModel(self.session))
        TableSelectorItem(self.table_selector, 'Astronomowie', model.AstronomerModel(self.session))

    def item_changed_handler(self, current, previous):
        if current.model is not None:
            self.table_view.setModel(current.model)
            self.current_model = current.model

    def add_to_table(self):
        if self.current_model is not None:
            self.current_model.add_row(self)

    def remove_from_table(self):
        if self.current_model is not None:
            selected_row = self.table_view.currentIndex().row()
            if selected_row >= 0:
                self.current_model.remove_row(selected_row)

    def edit_table(self):
        if self.current_model is not None:
            selected_row = self.table_view.currentIndex().row()
            if selected_row >= 0:
                self.current_model.edit_row(selected_row, self)


class TableSelectorItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, text, model=None):
        super(TableSelectorItem, self).__init__(parent, [text])
        self.model = model
