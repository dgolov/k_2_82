# Модуль с алгоритмами функционалов радиостанции и приставки К2-82
import re
import serial
import time
import xlwt
from settings import CODES


class ImportToExcel:
    """ Класс для выгрузки результатов проверки радиостанции в Excel документ для дальнейшего копирования в ведомость
        * Создание Excel файла и запись в него результатов
        * Сохранение Excel файла под указанным именем в заданную директорию пользователем
    """

    def __init__(self):
        self.cols = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L')
        self.book = xlwt.Workbook(encoding='utf8')
        self.sheet = self.book.add_sheet('Sheet')
        self.line = 0

    def write_book(self, *args) -> None:
        """ Запись результатов проверки в Excel документ
            :param args - упакованные результаты проверки радиостанции
        """
        row = self.sheet.row(self.line)

        for index, col in enumerate(self.cols):
            row.write(index, args[index])
        self.line += 1

    def save_book(self, name: str) -> None:
        """ Сохранение Excel документа
            :param name - имя сохраняемого Excel файла
        """
        self.book.save(name + '.xls')


class Functional:
    """ Общий класс функционала для устройств подключенных к COM портам """

    def __init__(self):
        self.port = None
        self.com = None

    def connect_com_port(self, port: int) -> bool:
        """ Соединение с COM портом
            :param port - название ком порта
        """
        self.port = port
        self.com = None

        try:
            self.com = serial.Serial(port, 9600, timeout=1)
            return True
        except serial.SerialException:
            return False

    def set_com_value(self, port: int) -> None:
        """ :param port:
        """
        self.port = port


class RSFunctional(Functional):
    """ Функционал подключеия к радиостанции
        Получение серийного номера
    """

    def __init__(self):
        super(RSFunctional, self).__init__()
        self._sn_pattern = r'672[a-zA-Z0-9]{7}'

    def get_serial(self) -> str:
        """ Получение серийного номера с радиостанции
        """
        self.com.write(b'\xf2\x23\x01\xe9')  # ASCII: 'т#<SON>й'
        result = self.com.readline()
        serial_number_in = result.decode('cp1251')
        serial_number_format = re.search(self._sn_pattern, serial_number_in)

        # Перевод радиостанции в обычный режим из режима тестирования
        self.com.write(b'\xf1\x10\xfe')
        self.com.close()

        return str(serial_number_format[0])


class K2Functional(Functional):
    """ Класс основного функционала приставки К2-82
        * Соединение с ком портом (Унаследовано из класса RSFunctional)
        * Отправка команды на К2-82
        * Установка частоты на К2-82
        * Отправка числовых значений на К2-82
    """
    model = 'Motorola GP340'

    def __init__(self):
        super(K2Functional, self).__init__()
        self.check_deviation = True  # Проверка максимальной девиации
        self.check_tx = True  # Проверять передатчик
        self.check_rx = True  # Проверять приёмник
        self.cancel = False  # Отмена проверки
        self.next = False  # Пропуск шага проверки
        self.check = False  # Флаг говорящий о том что проверка идет в данный момент
        self.excel_book = ImportToExcel()  # Объект книги Excel для сохранения ведомостей
        self.continue_thread = True  # Продолжать выполнение потока. Останавливается при всплывающих сообщениях
        self.random_values = False  # Рандомные значения

    def send_code(self, code, command=None) -> str:
        """ Отправка команды на COM порт
            :param code - ASCII код отправляемый на прибор
            :param command - указание нужно ли отображать на дисплее что команда отправлена
        """
        try:
            self.com.write(code)
            if command:
                return f"Команда '{command}' отправлена на {self.com.port}"
        except serial.SerialException:
            return 'Не удается соедениться с ' + self.com.port
        except (NameError, AttributeError):
            return f'Ошибка {self.port}: Нет подключения'

    def input_frequency(self, f: str) -> str:
        """ Установка заданной частоты на К2-82
            :param f - частота
        """
        error_message = 'Введите корректную частоту (например 151.825 или 151825)'
        for char in f:
            if char.isalpha():
                return error_message

        if ',' in f:
            f = f.replace(',', '.')
        elif '.' not in f:
            f = f[:3] + '.' + f[3:]

        if self.connect_com_port(self.com.port):
            f += '0' * (7 - len(f))
            if len(f) == 7:
                self.numbers_entry(*f)
            else:
                return error_message
        else:
            return 'Не удается соедениться с ' + self.com.port

        self.send_code(CODES['V/MHz'])
        return f'Частота {f} установлена на приборе'

    def numbers_entry(self, *args) -> None:
        """ Отправка списка числовых значений на прибор (цифровая клавиатура на К2-82)
            :param args - произвольное колличество чисел которые вводим на К2-82
        """
        for char in args:
            if char.isnumeric():
                self.send_code(CODES[char])
            elif char == '.' or char == ',':
                self.send_code(CODES['.'])
            time.sleep(0.1)
