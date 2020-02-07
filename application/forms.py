import datetime
from decimal import InvalidOperation
from PyQt5 import QtCore, QtWidgets, uic
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import DataError, DatabaseError
from utils import from_text, to_text, text_to_date, text_to_decimal, get_error_message
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
        self.set_up()
        self.dialog.button_box.accepted.connect(self.on_accepted)
        self.dialog.open()

    def edit_row(self, position, parent_window):
        self.dialog = QtWidgets.QDialog(parent_window)
        uic.loadUi('gui/' + self.form, self.dialog)
        self.set_up()
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
        except InvalidOperation as error:
            self.session.rollback()
            print(error)
            self.dialog.error_label.setText('Wprowadź liczbę w formacie 12,2442')
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

    def set_up(self):
        pass

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

    def set_object_from_form(self, entity):
        entity.iau_code = from_text(self.dialog.iau_code_edit.text())
        entity.latitude = text_to_decimal(self.dialog.latitude_edit.text())
        entity.longitude = text_to_decimal(self.dialog.longitude_edit.text())
        entity.country = from_text(self.dialog.country_edit.text())
        entity.full_name = from_text(self.dialog.full_name_edit.text())
        entity.name_mpc = from_text(self.dialog.name_mpc_edit.text())
    
    def fill_form(self, entity):
        self.dialog.iau_code_edit.setText(entity.iau_code)
        self.dialog.latitude_edit.setText(to_text(entity.latitude))
        self.dialog.longitude_edit.setText(to_text(entity.longitude))
        self.dialog.country_edit.setText(entity.country)
        self.dialog.full_name_edit.setText(entity.full_name)
        self.dialog.name_mpc_edit.setText(entity.name_mpc)


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

    def set_object_from_form(self, entity):
        entity.name = from_text(self.dialog.name_edit.text())
        entity.right_ascension = text_to_decimal(self.dialog.right_ascension_edit.text())
        entity.declination = text_to_decimal(self.dialog.declination_edit.text())
        entity.distance = text_to_decimal(self.dialog.distance_edit.text())
        entity.radial_velocity = text_to_decimal(self.dialog.radial_velocity_edit.text())
    
    def fill_form(self, entity):
        self.dialog.name_edit.setText(entity.name)
        self.dialog.right_ascension_edit.setText(to_text(entity.right_ascension))
        self.dialog.declination_edit.setText(to_text(entity.declination))
        self.dialog.distance_edit.setText(to_text(entity.distance))
        self.dialog.radial_velocity_edit.setText(to_text(entity.radial_velocity))


class GalaxyForm(AstronomyForm):
    form = 'form-galaxy.ui'

    def set_up(self):
        self.dialog.galaxy_group_edit.addItem('', None)
        for galaxy_group in self.session.query(astronomy.GalaxyGroup):
            self.dialog.galaxy_group_edit.addItem(galaxy_group.name, galaxy_group.name)
        self.dialog.orbited_galaxy_edit.addItem('', None)
        for galaxy in self.session.query(astronomy.Galaxy):
            self.dialog.orbited_galaxy_edit.addItem(galaxy.name, galaxy.name)
        self.dialog.constellation_edit.addItem('', None)
        for constellation in self.session.query(astronomy.Constellation):
            self.dialog.constellation_edit.addItem(constellation.name, constellation.iau_abbreviation)

    def set_object_from_form(self, entity):
        entity.name = from_text(self.dialog.name_edit.text())
        entity.galaxy_type = from_text(self.dialog.galaxy_type_edit.text())
        entity.right_ascension = text_to_decimal(self.dialog.right_ascension_edit.text())
        entity.declination = text_to_decimal(self.dialog.declination_edit.text())
        entity.apparent_magnitude = text_to_decimal(self.dialog.apparent_magnitude_edit.text())
        entity.absolute_magnitude = text_to_decimal(self.dialog.absolute_magnitude_edit.text())
        entity.distance = text_to_decimal(self.dialog.distance_edit.text())
        entity.diameter = text_to_decimal(self.dialog.diameter_edit.text())
        entity.galaxy_group = self.dialog.galaxy_group_edit.currentData()
        entity.orbited_galaxy = self.dialog.orbited_galaxy_edit.currentData()
        entity.constellation = self.dialog.constellation_edit.currentData()
    
    def fill_form(self, entity):
        self.dialog.name_edit.setText(entity.name)
        self.dialog.galaxy_type_edit.setText(entity.galaxy_type)
        self.dialog.right_ascension_edit.setText(to_text(entity.right_ascension))
        self.dialog.declination_edit.setText(to_text(entity.declination))
        self.dialog.apparent_magnitude_edit.setText(to_text(entity.apparent_magnitude))
        self.dialog.absolute_magnitude_edit.setText(to_text(entity.absolute_magnitude))
        self.dialog.distance_edit.setText(to_text(entity.distance))
        self.dialog.diameter_edit.setText(to_text(entity.diameter))
        self.dialog.galaxy_group_edit.setCurrentText(entity.galaxy_group)
        self.dialog.orbited_galaxy_edit.setCurrentText(entity.orbited_galaxy)
        if entity.constellation is not None:
            constellation = self.session.query(astronomy.Constellation).\
                filter_by(iau_abbreviation=entity.constellation).first()
            self.dialog.constellation_edit.setCurrentText(constellation.name)


class StarForm(AstronomyForm):
    form = 'form-star.ui'

    def set_object_from_form(self, entity):
        entity.name = from_text(self.dialog.name_edit.text())
        entity.right_ascension = text_to_decimal(self.dialog.right_ascension_edit.text())
        entity.declination = text_to_decimal(self.dialog.declination_edit.text())
        entity.distance = text_to_decimal(self.dialog.distance_edit.text())
    
    def fill_form(self, entity):
        self.dialog.name_edit.setText(entity.name)
        self.dialog.right_ascension_edit.setText(to_text(entity.right_ascension))
        self.dialog.declination_edit.setText(to_text(entity.declination))
        self.dialog.distance_edit.setText(to_text(entity.distance))


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


class ObservationForm(AstronomyForm):
    form = 'form-observation.ui'

    def set_up(self):
        for name, in self.session.query(astronomy.AstronomicalObject.name):
            self.dialog.astronomical_object_edit.addItem(name)

        for full_name, in self.session.query(astronomy.Astronomer.full_name):
            self.dialog.astronomer_edit.addItem(full_name)

        for full_name, iau_code in self.session.query(astronomy.Observatory.full_name, 
                astronomy.Observatory.iau_code):
            self.dialog.observatory_edit.addItem(full_name, iau_code)
        
        self.dialog.date_edit.setMinimumDate(QtCore.QDate(1000, 1, 1))

    def set_object_from_form(self, entity):
        entity.astronomical_object = self.dialog.astronomical_object_edit.currentText()
        entity.astronomer = self.dialog.astronomer_edit.currentText()
        entity.observatory = self.dialog.observatory_edit.currentData()
        date = self.dialog.date_edit.date()
        entity.date = datetime.date(date.year(), date.month(), date.day())
        entity.is_discovery = self.dialog.is_discovery_edit.isChecked()
    
    def fill_form(self, entity):
        self.dialog.astronomical_object_edit.setCurrentText(entity.astronomical_object)
        self.dialog.astronomer_edit.setCurrentText(entity.astronomer)

        # TODO: Better handling of duplicate observatory names
        observatory = self.session.query(astronomy.Observatory).filter_by(iau_code=entity.observatory).first()
        self.dialog.observatory_edit.setCurrentText(observatory.full_name)

        date = QtCore.QDate(entity.date.year, entity.date.month, entity.date.day)
        self.dialog.date_edit.setDate(date)
        self.dialog.is_discovery_edit.setChecked(entity.is_discovery)
