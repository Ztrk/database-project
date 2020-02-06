import datetime

def from_text(text):
    if text == '':
        return None
    return text

def to_text(value):
    if value is None:
        return ''
    if isinstance(value, datetime.date):
        return value.strftime('%d.%m.%Y')
    return str(value)

def text_to_date(text):
    if text == '':
        return None
    return datetime.datetime.strptime(text, '%d.%m.%Y').date()

def get_error_message(code, message):
    if code == 1048: # ER_BAD_NULL_ERROR
        column = message.split("'")[1]
        return 'Kolumna ' + column + ' nie może być pusta.'
    elif code == 1217: # ER_ROW_IS_REFERENCED
        return 'Obiekt jest używany przez inne obiekty. Spróbuj usunąć je najpierw.'
    elif code == 1364: # ER_NO_DEFAULT_FOR_FIELD
        column = message.split("'")[1]
        return 'Kolumna ' + column + ' nie może być pusta.'
    else:
        return message
