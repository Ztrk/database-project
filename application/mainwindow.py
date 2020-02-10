from PyQt5 import QtCore, QtWidgets, uic
import sqlalchemy as db
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
        self.action_edit.triggered.connect(lambda: self.edit_table(self.action_date_to_JD.isChecked()))
        self.action_date_to_JD.toggled.connect(lambda: self.jd_to_date(self.action_date_to_JD.isChecked()))
        # print(User.query.filter_by(username='admin').first())

    def closeEvent(self, event):
        if self.action_date_to_JD.isChecked():
            try:
                result = self.session.execute("CALL AllJDToDate();")
                result.close()
                astronomy.Astronomer.death_date.property.columns[0].type = db.Date()
                astronomy.Astronomer.birth_date.property.columns[0].type = db.Date()
                # astronomy.Astronomer.birth_date = db.Column('data_urodzenia', db.Date)
                # astronomy.Astronomer.death_date = db.Column('data_zgonu', db.Date)
                self.session.commit()
            except:
                self.session.rollback()
                raise

    def fill_table_selector(self):
        objects = TableSelectorItem(self.table_selector, 'Obiekty astronomiczne')
        TableSelectorItem(objects, 'Małe ciała', self.session, model.SmallBodyModel, forms.AstronomyForm)
        TableSelectorItem(objects, 'Sztuczne satelity', self.session, model.SatelliteModel, forms.AstronomyForm)
        TableSelectorItem(objects, 'Roje meteorów', self.session, model.MeteorShowerModel, forms.AstronomyForm)
        TableSelectorItem(objects, 'Gwiazdy', self.session, model.StarModel, forms.StarForm)
        TableSelectorItem(objects, 'Galaktyki', self.session, model.GalaxyModel, forms.GalaxyForm)
        TableSelectorItem(objects, 'Grupy galaktyk', self.session, model.GalaxyGroupModel, forms.GalaxyGroupForm)

        TableSelectorItem(self.table_selector, 'Konstelacje', self.session, model.ConstellationModel, forms.ConstellationForm)
        TableSelectorItem(self.table_selector, 'Katalogi', self.session, model.CatalogueModel, forms.CatalogueForm)
        TableSelectorItem(self.table_selector, 'Obserwacje', self.session, model.ObservationModel, forms.ObservationForm)
        TableSelectorItem(self.table_selector, 'Obserwatoria', self.session, model.ObservatoryModel, forms.ObservatoryForm)
        TableSelectorItem(self.table_selector, 'Astronomowie', self.session, model.AstronomerModel, forms.AstronomerForm)

    def item_changed_handler(self, current):
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

    def edit_table(self, isJD):
        if self.current_form is not None:
            selected_row = self.table_view.currentIndex().row()
            if selected_row >= 0:
                # if self.current_form.model.type.birth_date.property.columns[0].type == db.Date and isJD:
                #     self.current_form.model.type.birth_date.property.columns[0].type = db.Numeric()
                #     self.current_form.model.type.death_date.property.columns[0].type = db.Numeric()
                # print(self.current_form.dialog)
                self.current_form.edit_row(selected_row, self)

    def jd_to_date(self, isJD):
        if isJD:
            try:
                result = self.session.execute('CALL AllDateToJD();')
                result.close()
                self.session.commit()
                astronomy.Astronomer.death_date.property.columns[0].type = db.Numeric()
                astronomy.Astronomer.birth_date.property.columns[0].type = db.Numeric()
                # astronomy.Astronomer.birth_date = db.Column('data_urodzenia', db.Numeric)
                # astronomy.Astronomer.death_date = db.Column('data_zgonu', db.Numeric)
                self.update()
                # astronomy.Astronomer.birth_date.property.columns[0].type = db.Numeric()
                # astronomy.Astronomer.death_date.property.columns[0].type = db.Numeric()
                # print(astronomy.Galaxy.diameter.property.columns)
                # print(astronomy.Astronomer.death_date.name)
            except:
                self.session.rollback()
                raise
        else:
            try:
                result = self.session.execute("CALL AllJDToDate();")
                result.close()
                self.session.commit()
                astronomy.Astronomer.death_date.property.columns[0].type = db.Date()
                astronomy.Astronomer.birth_date.property.columns[0].type = db.Date()
                # astronomy.Astronomer.birth_date = db.Column('data_urodzenia', db.Date)
                # astronomy.Astronomer.death_date = db.Column('data_zgonu', db.Date)
                self.update()
                # print(astronomy.Astronomer.death_date.property.columns[0].type)
            except:
                self.session.rollback()
                raise


class TableSelectorItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, text, session=None, model=None, form=None):
        super(TableSelectorItem, self).__init__(parent, [text])
        if model is not None:
            self.model = model(session)
            self.form = form(self.model, session)
        else:
            self.model = None
            self.form = None
