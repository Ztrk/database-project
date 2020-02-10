import datetime
import decimal

def from_text(text):
    if text == '':
        return None
    return text

def to_text(value):
    if value is None:
        return ''
    if isinstance(value, bool):
        if value:
            return 'Tak'
        else:
            return 'Nie'
    if isinstance(value, datetime.date):
        return value.strftime('%d.%m.%Y')
    if isinstance(value, decimal.Decimal):
        return str(value).replace('.', ',')
    return str(value)

def text_to_date(text):
    if text == '':
        return None
    return datetime.datetime.strptime(text, '%d.%m.%Y').date()

def text_to_decimal(text):
    if text == '':
        return None
    text = text.replace(',', '.')
    return decimal.Decimal(text)

def get_error_message(code, message):
    if code == 1048: # ER_BAD_NULL_ERROR
        column = message.split("'")[1]
        return 'Pole ' + column + ' nie może być puste.'
    elif code == 1062: # ER_DUP_ENTRY
        name = message.split("'")[1]
        return 'Obiekt o nazwie ' + name + ' już istnieje.'
    elif code == 1217: # ER_ROW_IS_REFERENCED
        return 'Obiekt jest używany przez inne obiekty. Spróbuj usunąć je najpierw.'
    elif code == 1264: # ER_WARN_DATA_OUT_OF_RANGE
        column = message.split("'")[1]
        return 'Dana w kolumnie ' + column + ' jest poza zakresem.'
    elif code == 1364: # ER_NO_DEFAULT_FOR_FIELD
        column = message.split("'")[1]
        return 'Pole ' + column + ' nie może być puste.'
    elif code == 1406: # ER_DATA_TOO_LONG
        column = message.split("'")[1]
        return 'Wartość w polu ' + column + ' jest za długa.'
    elif code == 3819: # ER_CHECK_CONSTRAINT_VIOLATED
        return 'Podane wartości są niepoprawne.'
    else:
        return 'Nie udało się wykonać akcji.'
