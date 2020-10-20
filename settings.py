# Общие настройки и константы
import os
from logging_settings import event_log


# Название файла конфигураций (для запоминания настроек COM портов)
CONFIG_FILE_NAME = 'config.ini'

# Версия программы
VERSION = '0.5.3'

# Коды К2-82
CODES = {
    'УСТ': b'0x23',
    'ДУ': b'0x24',
    '20W': b'0x25',
    'ЗАПИСЬ': b'0x22',
    'ВЫВОД': b'0x21',
    'ВЧ ЧАСТ': b'0x26',
    'ВЧ ЧМ': b'0x27',
    'МОЩН': b'0x29',
    'ВЧ ЧМ ОТКЛ': b'0x30',
    'НЧ ЧАСТ': b'0x31',
    'НЧ КГ': b'0x32',
    'НЧ ДОП2': b'0x33',
    'НЧ НАПР': b'0x34',
    'НЧ ЧМ ВНЕШН': b'0x35',
    'ВВЕРХ': b'0x16',
    'ВНИЗ': b'0x17',
    'ВЛЕВО': b'0x18',
    'ВПРАВО': b'0x19',
    'ОТКЛ': b'0x20',
    'ВВОД': b'0x15',
    '1': b'0x01',
    '2': b'0x02',
    '3': b'0x03',
    '4': b'0x04',
    '5': b'0x05',
    '6': b'0x06',
    '7': b'0x07',
    '8': b'0x08',
    '9': b'0x09',
    '0': b'0x00',
    '.': b'0x10',
    '-': b'0x11',
    'V/MHz': b'0x12',
    'mV/kHz': b'0x13',
    'uV/Hz': b'0x14',
}

# Коды проверки передатчика
CHECK_TX_CODES = [
    CODES['ВНИЗ'], CODES['0'], CODES['.'], CODES['5'], CODES['mV/kHz'], CODES['ВЧ ЧМ'], CODES['3'], CODES['mV/kHz'],
    CODES['ВНИЗ'], CODES['1'], CODES['mV/kHz'], CODES['УСТ']
]

# Коды проверки приемника
CHECK_RX_CODES = [
    CODES['УСТ'], CODES['НЧ ДОП2'], CODES['ВНИЗ'], CODES['ВВОД'], CODES['mV/kHz'], CODES['ВВОД'], CODES['0'],
    CODES['.'], CODES['2'], CODES['5'], CODES['uV/Hz']
]


# Названия колонок в таблице
COLL_NAMES = [
    "№ РC", "№ АКБ", "Ёмкость", "P", "Выс. P", "Откл.", "КНИ", "ЧМ", "Max дев.", "Чувств.", "Вых. P",
    "Вых P.", "Избер.", "КНИ", "Шумодав", "Деж реж.", "I пр.", "I прд.", "Раздяд\nАКБ", 'ЗУ', 'Тангента'
]

#Руководство пользователя
USER_MANUAL_PATH = os.path.normcase('files/user manual.docx')

def open_user_manual():
    try:
        os.startfile(USER_MANUAL_PATH)
    except Exception as exc:
        event_log.error(exc)