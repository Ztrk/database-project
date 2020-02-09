from sqlalchemy import func, text
from PyQt5 import QtCore, QtWidgets, uic
import astronomy
import astronomy_model as model
import forms


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, session, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("gui/mainwindow.ui", self)
        self.session = session
        self.current_model = None
        self.current_form = None

        # Fill table selector TreeWidget
        self.fill_table_selector()
        self.table_selector.currentItemChanged.connect(self.item_changed_handler)

        self.action_add.triggered.connect(self.add_to_table)
        self.action_remove.triggered.connect(self.remove_from_table)
        self.action_edit.triggered.connect(self.edit_table)
        self.action_execute.triggered.connect(self.execute_handle)

    def fill_table_selector(self):
        objects = TableSelectorItem(self.table_selector, 'Obiekty astronomiczne')
        TableSelectorItem(objects, 'Małe ciała', self.session, model.SmallBodyModel, forms.SmallBodyForm)
        TableSelectorItem(objects, 'Sztuczne satelity', self.session, model.SatelliteModel, forms.SatelliteForm)
        TableSelectorItem(objects, 'Roje meteorów', self.session, model.MeteorShowerModel, forms.MeteorShowerForm)
        TableSelectorItem(objects, 'Gwiazdy', self.session, model.StarModel, forms.StarForm)
        TableSelectorItem(objects, 'Galaktyki', self.session, model.GalaxyModel, forms.GalaxyForm)
        TableSelectorItem(objects, 'Grupy galaktyk', self.session, model.GalaxyGroupModel, forms.GalaxyGroupForm)

        TableSelectorItem(self.table_selector, 'Konstelacje', self.session, model.ConstellationModel, forms.ConstellationForm)
        TableSelectorItem(self.table_selector, 'Katalogi', self.session, model.CatalogueModel, forms.CatalogueForm)
        TableSelectorItem(self.table_selector, 'Obserwacje', self.session, model.ObservationModel, forms.ObservationForm)
        TableSelectorItem(self.table_selector, 'Obserwatoria', self.session, model.ObservatoryModel, forms.ObservatoryForm)
        TableSelectorItem(self.table_selector, 'Astronomowie', self.session, model.AstronomerModel, forms.AstronomerForm)

    def item_changed_handler(self, current, previous):
        if current.model is not None:
            self.table_view.setModel(current.model)
            self.current_model = current.model
            self.current_form = current.form

    def add_to_table(self):
        if self.current_form is not None:
            self.current_form.add_row(self)

    def remove_from_table(self):
        if self.current_form is not None:
            selected_row = self.table_view.currentIndex().row()
            if selected_row >= 0:
                self.current_form.remove_row(selected_row, self)

    def edit_table(self):
        if self.current_form is not None:
            selected_row = self.table_view.currentIndex().row()
            if selected_row >= 0:
                self.current_form.edit_row(selected_row, self)
    
    def execute_handle(self):
        print(self.session.execute(func.angle_to_decimal(-11, 37, 58)).scalar())
        call = text('CALL decimal_to_angle(:angle, @degrees, @minutes, @seconds)').bindparams(angle=12.7230)
        self.session.execute(call)
        result = self.session.execute('SELECT @degrees, @minutes, @seconds').fetchone()
        print(result)
        call = text('CALL period_from_orbit(:name)').bindparams(name='asdf')
        self.session.execute(call)
        print('Executing')


class TableSelectorItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, text, session=None, model=None, form=None):
        super(TableSelectorItem, self).__init__(parent, [text])
        if model is not None:
            self.model = model(session)
            self.form = form(self.model, session)
        else:
            self.model = None
            self.form = None
