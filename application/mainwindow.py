from PyQt5 import QtCore, QtWidgets, uic
import astronomy
import astronomy_model as model

class Second(QtWidgets.QDialog):
    def __init__(self, object_type, parent=None):
        super(Second, self).__init__(parent)
        uic.loadUi("gui/form-" + object_type + ".ui", self)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, session, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("gui/mainwindow.ui", self)
        self.session = session
        self.object_type = ""

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
    def __init__(self, parent, text, model=None):
        super(TableSelectorItem, self).__init__(parent, [text])
        self.model = model
