# Модуль с алгоритмом функционала приставки К2-82
import re
import serial, time
import xlwt


class ImportToExcel:
    """
    Класс для выгрузки результатов проверки радиостанции в Excel документ для
    дальнейшего копирования в ведомость
    * Создание Excel файла и запись в него результатов
    * Сохранение Excel файла под указанным именем в заданную директорию пользователем
    """

    def __init__(self):
        self.cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        self.book = xlwt.Workbook(encoding='utf8')
        self.sheet = self.book.add_sheet('Sheet')
        self.line = 0

    def write_book(self, *args):
        """
        Запись результатов проверки в Excel документ
        :param args - упакованные результаты проверки радиостанции
        """
        row = self.sheet.row(self.line)
        for index, col in enumerate(self.cols):
            value = args[index]
            row.write(index, value)
        self.line += 1

    def save_book(self, name):
        """
        Сохранение Excel документа
        :param name - имя сохраняемого Excel файла
        """
        self.book.save(name + '.xls')



class RSFunctional:
    def __init__(self):
        self.port = None
        self.com = None
        self._sn_pattern = r'672[a-zA-Z0-9]{7}'

    def connect_com_port(self, port):
        """
        Соединение с COM портом
        :param port - название ком порта
        """
        self.port = port
        self.com = None

        try:
            self.com = serial.Serial(port, 9600, timeout=1)
            return True
        except serial.SerialException:
            return False

    def get_serial(self):
        self.com.write(b'\xf2\x23\x01\xe9')
        result = self.com.readline()
        serial_number_in = result.decode('cp1251')
        serial_number_format = re.search(self._sn_pattern, serial_number_in)

        # Перевод радиостанции в обычный режим из режима тестирования
        self.com.write(b'\xf1\x10\xfe')
        self.com.close()

        return str(serial_number_format[0])



class K2Functional(RSFunctional):
    """
    Класс основного функционала приставки К2-82
    * Соединение с ком портом
    * Отправка команды на К2-82
    * Установка частоты на К2-82
    * Отправка числовых значений на К2-82
    """

    COM = 'COM2'
    model = 'Motorola'

    def __init__(self):
        super(K2Functional, self).__init__()
        #self.port = None
        self.check_deviation_time = 33
        self.cancel = False
        self.check = False
        #self.com = None
        self.com_rs = None
        self.excel_book = ImportToExcel()
        self.continue_thread = True


    # def connect_com_port(self, port):
    #     """
    #     Соединение с COM портом
    #     :param port - название ком порта
    #     """
    #     self.port = port
    #     self.com = None
    #
    #     try:
    #         self.com = serial.Serial(port, 9600, timeout=1)
    #         return True
    #     except serial.SerialException:
    #         return False


    def send_code(self, code, command=None):
        """
        Отправка команды на COM порт
        :param code - ASCII код отправляемый на прибор
        :param command - указание нужно ли отображать на дисплее что команда отправлена
        """
        try:
            self.com.write(code)
            if command:
                return  "Команда '{}' отправлена на {}".format(command, self.com.port)
        except serial.SerialException:
            return 'Не удается соедениться с ' + self.com.port
        except (NameError, AttributeError):
            return 'Ошибка {}: Нет подключения'.format(self.port)


    def input_frequency(self, f):
        """
        Установка заданной частоты на К2-82
        :param f - частота
        """
        error_message = 'Введите корректную частоту (например 151.825 или 151825)'

        if len(f) == 3:
            f += '.000'
        elif len(f) == 5:
            f += '00'
        elif len(f) == 6:
            if f[3] == '.':
                f += '0'
            else:
                f = f[:3] + '.' + f[3:]
        if len(f) == 7:
            for char in f:
                self.numbers_entry(char=char)
        else:
            return error_message

        self.send_code(b'0x12')
        return 'Частота {} установлена на приборе'.format(f)


    def numbers_entry(self, char):
        """
        Отправка числовых значений (цифровая клавиатура на К2-82)
        :param char - число которое вводим на К2-82
        """
        if char == '1':
            self.send_code(b'0x01')
        elif char == '2':
            self.send_code(b'0x02')
        elif char == '3':
            self.send_code(b'0x03')
        elif char == '4':
            self.send_code(b'0x04')
        elif char == '5':
            self.send_code(b'0x05')
        elif char == '6':
            self.send_code(b'0x06')
        elif char == '7':
            self.send_code(b'0x07')
        elif char == '8':
            self.send_code(b'0x08')
        elif char == '9':
            self.send_code(b'0x09')
        elif char == '0':
            self.send_code(b'0x00')
        elif char == '.' or char == ',':
            self.send_code(b'0x10')
        time.sleep(0.1)