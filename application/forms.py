import datetime
from decimal import InvalidOperation
from PyQt5 import QtCore, QtWidgets, uic
from sqlalchemy import func, text
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
        self.edited_entity = self.model.rows[position]
        self.set_up()
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
            self.dialog.error_label.setText('Wprowadź liczbę w formacie 22,222')
        except FlushError as error:
            print(error)
            self.dialog.error_label.setText('Obiekt o tej samej nazwie już istnieje')
        except (DataError, DatabaseError) as error:
            print(error)
            self.dialog.error_label.setText(self.get_error_message(error.orig.args[0], error.orig.args[1]))
    
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
    
    def get_error_message(self, code, message):
        return get_error_message(code, message)

    form = ''

    def set_up(self):
        pass

    def set_object_from_form(self, entity):
        raise NotImplementedError('Form should define how to parse a form')

    def fill_form(self, entity):
        raise NotImplementedError('Form should define how to fill a form')


class AstronomerForm(AstronomyForm):
    form = 'form-astronomer.ui'

    def get_error_message(self, code, message):
        if code == 3819: # ER_CHECK_CONSTRAINT_VIOLATED
            constraint = message.split("'")[1]
            if constraint == 'astronomer_date_check':
                return 'Data zgonu powinna późniejsza niż data urodzenia.'
        return get_error_message(code, message)

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

    def get_error_message(self, code, message):
        if code == 3819: # ER_CHECK_CONSTRAINT_VIOLATED
            constraint = message.split("'")[1]
            if constraint == 'latitude_check':
                return 'Szerokość geograficzna powinna być pomiędzy -90 a 90 stopni.'
            elif constraint == 'longitude_check':
                return 'Długość geograficzna powinna być pomiędzy -180 a 180 stopni.'
            elif constraint == 'coordinates_present':
                return 'Podaj obie współrzędne.'
        return get_error_message(code, message)


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

    def get_error_message(self, code, message):
        if code == 3819: # ER_CHECK_CONSTRAINT_VIOLATED
            constraint = message.split("'")[1]
            if constraint == 'galaxy_group_right_ascension_check':
                return 'Rektasencja powinna być pomiędzy 0 a 24.'
            elif constraint == 'galaxy_group_declination_check':
                return 'Deklinacja powinna być pomiędzy -90 a 90.'
            elif constraint == 'galaxy_group_distance_check':
                return 'Dystans powinien być większy lub równy 0.'
        return get_error_message(code, message)

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

    def get_error_message(self, code, message):
        if code == 3819: # ER_CHECK_CONSTRAINT_VIOLATED
            constraint = message.split("'")[1]
            if constraint == 'galaxy_right_ascension_check':
                return 'Rektasencja powinna być pomiędzy 0 a 24.'
            elif constraint == 'galaxy_declination_check':
                return 'Deklinacja powinna być pomiędzy -90 a 90.'
            elif constraint == 'galaxy_distance_check':
                return 'Dystans powinien być większy lub równy 0.'
            elif constraint == 'galaxy_diameter_check':
                return 'Średnica powinna być większa lub równy 0.'
        return get_error_message(code, message)

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

    def get_error_message(self, code, message):
        if code == 3819: # ER_CHECK_CONSTRAINT_VIOLATED
            constraint = message.split("'")[1]
            if constraint == 'star_right_ascension_check':
                return 'Rektasencja powinna być pomiędzy 0 a 24.'
            elif constraint == 'star_declination_check':
                return 'Deklinacja powinna być pomiędzy -90 a 90.'
            elif constraint == 'star_distance_check':
                return 'Dystans powinien być większy lub równy 0.'
            elif constraint == 'star_parallax_check':
                return 'Paralaksa powinna być większa lub równa 0.'
            elif constraint == 'star_mass_check':
                return 'Masa powinna być większa lub równa 0.'
            elif constraint == 'star_radius_check':
                return 'Promień powinien być większy lub równy 0.'
        return get_error_message(code, message)

    def set_up(self):
        for galaxy in self.session.query(astronomy.Galaxy):
            self.dialog.galaxy_edit.addItem(galaxy.name, galaxy.name)
        self.dialog.constellation_edit.addItem('', None)
        for constellation in self.session.query(astronomy.Constellation):
            self.dialog.constellation_edit.addItem(constellation.name, constellation.iau_abbreviation)


    def set_object_from_form(self, entity):
        entity.name = from_text(self.dialog.name_edit.text())
        entity.spectral_type = from_text(self.dialog.spectral_type_edit.text())
        entity.right_ascension = text_to_decimal(self.dialog.right_ascension_edit.text())
        entity.declination = text_to_decimal(self.dialog.declination_edit.text())
        entity.apparent_magnitude = text_to_decimal(self.dialog.apparent_magnitude_edit.text())
        entity.absolute_magnitude = text_to_decimal(self.dialog.absolute_magnitude_edit.text())
        entity.distance = text_to_decimal(self.dialog.distance_edit.text())
        entity.parallax = text_to_decimal(self.dialog.parallax_edit.text())
        entity.mass = text_to_decimal(self.dialog.mass_edit.text())
        entity.radius = text_to_decimal(self.dialog.radius_edit.text())
        entity.galaxy = self.dialog.galaxy_edit.currentData()
        entity.constellation = self.dialog.constellation_edit.currentData()
    
    def fill_form(self, entity):
        self.dialog.name_edit.setText(entity.name)
        self.dialog.spectral_type_edit.setText(entity.spectral_type)
        self.dialog.right_ascension_edit.setText(to_text(entity.right_ascension))
        self.dialog.declination_edit.setText(to_text(entity.declination))
        self.dialog.apparent_magnitude_edit.setText(to_text(entity.apparent_magnitude))
        self.dialog.absolute_magnitude_edit.setText(to_text(entity.absolute_magnitude))
        self.dialog.distance_edit.setText(to_text(entity.distance))
        self.dialog.parallax_edit.setText(to_text(entity.parallax))
        self.dialog.mass_edit.setText(to_text(entity.mass))
        self.dialog.radius_edit.setText(to_text(entity.radius))
        self.dialog.galaxy_edit.setCurrentText(entity.galaxy)
        if entity.constellation is not None:
            constellation = self.session.query(astronomy.Constellation).\
                filter_by(iau_abbreviation=entity.constellation).first()
            self.dialog.constellation_edit.setCurrentText(constellation.name)


class SmallBodyForm(AstronomyForm):
    form = 'form-small-body.ui'

    def get_error_message(self, code, message):
        if code == 3819: # ER_CHECK_CONSTRAINT_VIOLATED
            constraint = message.split("'")[1]
            if constraint == 'small_body_period_check':
                return 'Okres musi być większy lub równy 0.'
            elif constraint == 'small_body_eccentricity_check':
                return 'Ekscentryczność powinna być większa lub równa 0.'
            elif constraint == 'small_body_semi_major_axis_check':
                return 'Półoś wielka powinna być większa lub równa 0.'
            elif constraint == 'small_body_inclination_check':
                return 'Inklinacja powinna być pomiędzy 0 a 180 stopni.'
            elif constraint == 'small_body_mass_check':
                return 'Masa powinna być większa lub równa 0.'
            elif constraint == 'small_body_diameter_check':
                return 'Średnica powinna być większa lub równa 0.'
        return get_error_message(code, message)

    def set_up(self):
        self.dialog.type_edit.addItem('Asteroida')
        self.dialog.type_edit.addItem('Kometa')
        self.dialog.type_edit.addItem('Planeta')
        self.dialog.type_edit.addItem('Satelita')
        self.dialog.orbited_body_edit.addItem('', None)
        for small_body in self.session.query(astronomy.SmallBody):
            self.dialog.orbited_body_edit.addItem(small_body.name, small_body)
        for star in self.session.query(astronomy.Star):
            self.dialog.orbited_body_edit.addItem(star.name, star)

    def set_object_from_form(self, entity):
        entity.name = from_text(self.dialog.name_edit.text())
        entity.type = self.dialog.type_edit.currentText()
        entity.diameter = text_to_decimal(self.dialog.diameter_edit.text())
        entity.mass = text_to_decimal(self.dialog.mass_edit.text())
        entity.temperature = text_to_decimal(self.dialog.temperature_edit.text())
        entity.period = text_to_decimal(self.dialog.period_edit.text())
        entity.eccentricity = text_to_decimal(self.dialog.eccentricity_edit.text())
        entity.semi_major_axis = text_to_decimal(self.dialog.semi_major_axis_edit.text())
        entity.inclination = text_to_decimal(self.dialog.inclination_edit.text())
        orbited_body = self.dialog.orbited_body_edit.currentData()
        if isinstance(orbited_body, astronomy.Star):
            entity.orbited_star = orbited_body.name
        else:
            entity.orbited_star = None
        if isinstance(orbited_body, astronomy.SmallBody):
            entity.orbited_small_body = orbited_body.name
        else:
            entity.orbited_small_body = None
    
    def fill_form(self, entity):
        self.dialog.name_edit.setText(entity.name)
        self.dialog.type_edit.setCurrentText(entity.type)
        self.dialog.diameter_edit.setText(to_text(entity.diameter))
        self.dialog.mass_edit.setText(to_text(entity.mass))
        self.dialog.temperature_edit.setText(to_text(entity.temperature))
        self.dialog.period_edit.setText(to_text(entity.period))
        self.dialog.eccentricity_edit.setText(to_text(entity.eccentricity))
        self.dialog.semi_major_axis_edit.setText(to_text(entity.semi_major_axis))
        self.dialog.inclination_edit.setText(to_text(entity.inclination))
        self.dialog.orbited_body_edit.setCurrentText(entity.orbited_star)
        if entity.orbited_small_body is not None:
            self.dialog.orbited_body_edit.setCurrentText(entity.orbited_small_body)


class SatelliteForm(AstronomyForm):
    form = 'form-satellite.ui'

    def get_error_message(self, code, message):
        if code == 3819: # ER_CHECK_CONSTRAINT_VIOLATED
            constraint = message.split("'")[1]
            if constraint == 'satellite_period_check':
                return 'Okres musi być większy lub równy 0.'
            elif constraint == 'satellite_inclination_check':
                return 'Inklinacja powinna być pomiędzy 0 a 180 stopni.'
            elif constraint == 'satellite_date_check':
                return 'Data zniszczenia musi być później niż data startu.'
        return get_error_message(code, message)

    def set_up(self):
        self.dialog.orbited_body_edit.addItem('', None)
        for small_body in self.session.query(astronomy.SmallBody):
            self.dialog.orbited_body_edit.addItem(small_body.name, small_body)
        for star in self.session.query(astronomy.Star):
            self.dialog.orbited_body_edit.addItem(star.name, star)

    def set_object_from_form(self, entity):
        entity.name = from_text(self.dialog.name_edit.text())
        entity.type = from_text(self.dialog.type_edit.text())
        entity.country = from_text(self.dialog.country_edit.text())
        entity.start_date = text_to_date(self.dialog.start_date_edit.text())
        entity.end_date = text_to_date(self.dialog.end_date_edit.text())
        entity.period = text_to_decimal(self.dialog.period_edit.text())
        entity.apoapsis = text_to_decimal(self.dialog.apoapsis_edit.text())
        entity.periapsis = text_to_decimal(self.dialog.periapsis_edit.text())
        entity.inclination = text_to_decimal(self.dialog.inclination_edit.text())
        orbited_body = self.dialog.orbited_body_edit.currentData()
        if isinstance(orbited_body, astronomy.Star):
            entity.orbited_star = orbited_body.name
        else:
            entity.orbited_star = None
        if isinstance(orbited_body, astronomy.SmallBody):
            entity.orbited_small_body = orbited_body.name
        else:
            entity.orbited_small_body = None
    
    def fill_form(self, entity):
        self.dialog.name_edit.setText(entity.name)
        self.dialog.type_edit.setText(to_text(entity.type))
        self.dialog.country_edit.setText(to_text(entity.country))
        self.dialog.start_date_edit.setText(to_text(entity.start_date))
        self.dialog.end_date_edit.setText(to_text(entity.end_date))
        self.dialog.period_edit.setText(to_text(entity.period))
        self.dialog.apoapsis_edit.setText(to_text(entity.apoapsis))
        self.dialog.periapsis_edit.setText(to_text(entity.periapsis))
        self.dialog.inclination_edit.setText(to_text(entity.inclination))
        self.dialog.orbited_body_edit.setCurrentText(entity.orbited_star)
        if entity.orbited_small_body is not None:
            self.dialog.orbited_body_edit.setCurrentText(entity.orbited_small_body)


class MeteorShowerForm(AstronomyForm):
    form = 'form-meteor-shower.ui'

    def get_error_message(self, code, message):
        if code == 3819: # ER_CHECK_CONSTRAINT_VIOLATED
            constraint = message.split("'")[1]
            if constraint == 'meteor_shower_right_ascension_check':
                return 'Rektasencja powinna być pomiędzy 0 a 24.'
            elif constraint == 'meteor_shower_declination_check':
                return 'Deklinacja powinna być pomiędzy -90 a 90.'
            elif constraint == 'meteor_shower_velocity_check':
                return 'Prędkość powinna być większa lub równa 0.'
            elif constraint == 'meteor_shower_zhr_check':
                return 'ZHR powinno być większe lub równe 0.'
        return get_error_message(code, message)

    def set_object_from_form(self, entity):
        entity.name = from_text(self.dialog.name_edit.text())
        begin_date = self.dialog.begin_date_edit.date()
        entity.begin_date = datetime.date(2004, begin_date.month(), begin_date.day())
        end_date = self.dialog.end_date_edit.date()
        entity.end_date = datetime.date(2004, end_date.month(), end_date.day())
        peak_date = self.dialog.peak_date_edit.date()
        entity.peak_date = datetime.date(2004, peak_date.month(), peak_date.day())
        entity.right_ascension = text_to_decimal(self.dialog.right_ascension_edit.text())
        entity.declination = text_to_decimal(self.dialog.declination_edit.text())
        entity.velocity = text_to_decimal(self.dialog.velocity_edit.text())
        entity.zhr = text_to_decimal(self.dialog.zhr_edit.text())
        entity.activity = from_text(self.dialog.activity_edit.text())
    
    def fill_form(self, entity):
        self.dialog.name_edit.setText(entity.name)
        begin_date = QtCore.QDate(2004, entity.begin_date.month, entity.end_date.day)
        self.dialog.begin_date_edit.setDate(begin_date)
        end_date = QtCore.QDate(2004, entity.end_date.month, entity.end_date.day)
        self.dialog.end_date_edit.setDate(end_date)
        peak_date = QtCore.QDate(2004, entity.peak_date.month, entity.peak_date.day)
        self.dialog.peak_date_edit.setDate(peak_date)
        self.dialog.right_ascension_edit.setText(to_text(entity.right_ascension))
        self.dialog.declination_edit.setText(to_text(entity.declination))
        self.dialog.velocity_edit.setText(to_text(entity.velocity))
        self.dialog.zhr_edit.setText(to_text(entity.zhr))
        self.dialog.activity_edit.setText(to_text(entity.activity))


class CatalogueForm(AstronomyForm):
    form = 'form-catalogue.ui'

    def set_up(self):
        if self.edited_entity is not None:
            self.dialog.catalogue_objects_button.clicked.connect(self.edit_objects_handle)
        else:
            self.dialog.catalogue_objects_button.setVisible(False)
    
    def edit_objects_handle(self):
        self.catalogue_object_form = CatalogueObjectForm(self.session, self.dialog, self.edited_entity)

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


class CatalogueObjectForm:
    def __init__(self, session, parent_window, catalogue):
        self.session = session
        self.catalogue = catalogue
        self.dialog = QtWidgets.QDialog(parent_window)
        uic.loadUi('gui/form-catalogue-object.ui', self.dialog)
        self.fill_lists()
        self.dialog.to_catalogue_button.clicked.connect(self.to_catalogue_handle)
        self.dialog.from_catalogue_button.clicked.connect(self.from_catalogue_handle)
        self.dialog.button_box.accepted.connect(self.accepted_handle)
        self.dialog.open()
    
    def fill_lists(self):
        objects = self.session.query(astronomy.AstronomicalObject)
        for object in objects:
            item = QtWidgets.QListWidgetItem(object.name)
            item.setData(QtCore.Qt.UserRole, object)
            if object not in self.catalogue.objects:
                self.dialog.objects_list.addItem(item)
            else:
                self.dialog.catalogue_objects_list.addItem(item)

    def to_catalogue_handle(self):
        row = self.dialog.objects_list.currentRow()
        item = self.dialog.objects_list.takeItem(row)
        self.dialog.catalogue_objects_list.addItem(item)

    def from_catalogue_handle(self):
        row = self.dialog.catalogue_objects_list.currentRow()
        item = self.dialog.catalogue_objects_list.takeItem(row)
        self.dialog.objects_list.addItem(item)

    def accepted_handle(self):
        print('Accepted')
        self.catalogue.objects = []
        for i in range(0, self.dialog.catalogue_objects_list.count()):
            item = self.dialog.catalogue_objects_list.item(i)
            self.catalogue.objects.append(item.data(QtCore.Qt.UserRole))
        self.session.commit()
        self.dialog.accept()


class ProceduresForm:
    def __init__(self, session, parent_window):
        self.session = session
        self.dialog = QtWidgets.QDialog(parent_window)
        uic.loadUi('gui/form-procedures.ui', self.dialog)
        self.fill_combobox()
        self.dialog.angle_to_number_button.clicked.connect(self.angle_to_number_handle)
        self.dialog.number_to_angle_button.clicked.connect(self.number_to_angle_handle)
        self.dialog.compute_period_button.clicked.connect(self.period_from_orbit_handle)
        self.dialog.show()

    def fill_combobox(self):
        for small_body in self.session.query(astronomy.SmallBody):
            if small_body.orbited_star == 'Sun' or small_body.orbited_small_body == 'Earth':
                self.dialog.objects_combobox.addItem(small_body.name)
        for satellite in self.session.query(astronomy.Satellite):
            if satellite.orbited_star == 'Sun' or satellite.orbited_small_body == 'Earth':
                self.dialog.objects_combobox.addItem(satellite.name)
    
    def angle_to_number_handle(self):
        degrees = self.dialog.degrees_edit.value()
        minutes = self.dialog.minutes_edit.value()
        seconds = self.dialog.seconds_edit.value()
        result = self.session.execute(func.angle_to_decimal(degrees, minutes, seconds)).scalar()
        if result == 0:
            text = '0'
        else:
            text = to_text(result)
        self.dialog.result_number_edit.setText(text + '°')

    def number_to_angle_handle(self):
        angle = self.dialog.number_edit.value()
        call = text('CALL decimal_to_angle(:angle, @degrees, @minutes, @seconds)').bindparams(angle=angle)
        self.session.execute(call)
        degrees, minutes, seconds = self.session.execute('SELECT @degrees, @minutes, @seconds').fetchone()
        if seconds == 0:
            seconds = 0
        self.dialog.result_angle_edit.setText(str(degrees) + '° ' + str(minutes) + "' " + to_text(seconds) + '"')

    def period_from_orbit_handle(self):
        print(self.dialog.objects_combobox.currentText())
        name = self.dialog.objects_combobox.currentText()
        call = text('CALL period_from_orbit(:name)').bindparams(name=name)
        self.session.execute(call)
        self.session.commit()
        self.dialog.result_label.setText('Procedura wykonana pomyślnie')
