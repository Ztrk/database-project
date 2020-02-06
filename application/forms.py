from PyQt5 import QtCore, QtWidgets, uic
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import DataError, DatabaseError
from utils import from_text, to_text, text_to_date, get_error_message
import astronomy

class AstronomyForm:
    def __init__(self, model, session):
        self.session = session
        self.model = model
        self.dialog = None
        self.edited_entity = None
        self.changed_row = -1

    def add_row(self, parent_window):
        self.dialog = QtWidgets.QDialog(parent_window)
        uic.loadUi('gui/' + self.form, self.dialog)
        self.dialog.button_box.accepted.connect(self.on_accepted)
        self.dialog.open()

    def edit_row(self, position, parent_window):
        self.dialog = QtWidgets.QDialog(parent_window)
        uic.loadUi('gui/' + self.form, self.dialog)
        self.edited_entity = self.model.rows[position]
        self.fill_form(self.edited_entity)
        self.dialog.button_box.accepted.connect(self.on_accepted)
        self.dialog.open()
        self.changed_row = position
    
    def on_accepted(self):
        try:
            if self.edited_entity is None:
                self.on_add_accepted()
            else:
                self.on_edit_accepted()
        except ValueError as error:
            self.session.rollback()
            print(error)
            self.dialog.error_label.setText('Wprowadź datę w formacie DD.MM.RRRR')
        except FlushError as error:
            print(error)
            self.dialog.error_label.setText('Obiekt o tej samej nazwie już istnieje')
        except (DataError, DatabaseError) as error:
            print(error)
            self.dialog.error_label.setText(get_error_message(error.orig.args[0], error.orig.args[1]))
    
    def on_add_accepted(self):
        entity = self.model.type()
        self.set_object_from_form(entity)
        self.model.add_row(entity)
        self.dialog.accept()

    def on_edit_accepted(self):
        self.set_object_from_form(self.edited_entity)
        self.model.edit_row(self.changed_row)
        self.dialog.accept()
        self.edited_entity = None

    def remove_row(self, position, parent_window):
        try:
            self.model.remove_row(position)
        except FlushError as error:
            print(error)
            self.create_error_dialog(parent_window)
        except (DataError, DatabaseError) as error:
            print(error)
            self.create_error_dialog(parent_window, 
                get_error_message(error.orig.args[0], error.orig.args[1]))

    def create_error_dialog(self, parent_window, message=''):
        error_box = QtWidgets.QMessageBox(parent_window)
        error_box.setIcon(QtWidgets.QMessageBox.Critical)
        error_box.setWindowTitle('Błąd')
        error_box.setText('Nie można usunąć obiektu.                                   ')
        error_box.setInformativeText(message)
        error_box.show()
        return error_box

    form = ''
    def set_object_from_form(self, entity):
        raise NotImplementedError('Form should define how to parse a form')

    def fill_form(self, entity):
        raise NotImplementedError('Form should define how to fill a form')

class AstronomerForm(AstronomyForm):
    form = 'form-astronomer.ui'

    def set_object_from_form(self, entity):
        entity.full_name = from_text(self.dialog.full_name_edit.text())
        entity.country = from_text(self.dialog.country_edit.text())
        entity.birth_date = text_to_date(self.dialog.birth_date_edit.text())
        entity.death_date = text_to_date(self.dialog.death_date_edit.text())
        entity.name_mpc = from_text(self.dialog.name_mpc_edit.text())
    
    def fill_form(self, entity):
        self.dialog.full_name_edit.setText(entity.full_name)
        self.dialog.country_edit.setText(entity.country)
        self.dialog.birth_date_edit.setText(to_text(entity.birth_date))
        self.dialog.death_date_edit.setText(to_text(entity.death_date))
        self.dialog.name_mpc_edit.setText(entity.name_mpc)

class ObservatoryForm(AstronomyForm):
    form = 'form-observatory.ui'

class ConstellationForm(AstronomyForm):
    form = 'form-constellation.ui'

    def set_object_from_form(self, entity):
        entity.iau_abbreviation = from_text(self.dialog.iau_abbreviation_edit.text())
        entity.name = from_text(self.dialog.name_edit.text())
        entity.brightest_star = from_text(self.dialog.brightest_star_edit.text())
    
    def fill_form(self, entity):
        self.dialog.iau_abbreviation_edit.setText(entity.iau_abbreviation)
        self.dialog.name_edit.setText(entity.name)
        self.dialog.brightest_star_edit.setText(entity.brightest_star)

class GalaxyGroupForm(AstronomyForm):
    form = 'form-galaxy-group.ui'

class CatalogueForm(AstronomyForm):
    form = 'form-catalogue.ui'

    def set_object_from_form(self, entity):
        entity.name = from_text(self.dialog.name_edit.text())
        entity.abbreviation = from_text(self.dialog.abbreviation_edit.text())
        entity.publishing_year = self.dialog.publishing_year_edit.value()
    
    def fill_form(self, entity):
        self.dialog.name_edit.setText(entity.name)
        self.dialog.abbreviation_edit.setText(entity.abbreviation)
        self.dialog.publishing_year_edit.setValue(entity.publishing_year)
