import serial, time
import xlwt


class Import_to_Excel:

    def __init__(self):
        self.colls = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        self.book = xlwt.Workbook(encoding='utf8')
        self.sheet = self.book.add_sheet('Sheet')
        self.line = 0

    def write_book(self, *args):
        """ Запись параметров в Excel документ """
        row = self.sheet.row(self.line)
        for index, col in enumerate(self.colls):
            value = args[index]
            row.write(index, value)
        self.line += 1

    def save_book(self, name):
        """ Сохранение Excel документа """
        self.book.save(name + '.xls')



class K2_functional:

    COM = 'COM2'
    model = 'Motorola'

    def __init__(self):
        self.port = None
        self.check_deviation_time = 33
        self.cancel = False
        self.check = False
        self.excel_book = Import_to_Excel()


    def connect_com_port(self, port):
        """ Соединение с COM портом """
        self.port = port
        self.com = None
        try:
            self.com = serial.Serial(port, 9600, timeout=1)
            return True
        except serial.SerialException:
            return False


    def send_code(self, code, commande=None):
        """ Отправка команды на COM порт """
        try:
            self.com.write(code)
            if commande:
                return  "Команда '{}' отправлена на {}".format(commande, self.com.port)
        except serial.SerialException:
            return 'Не удается соедениться с ' + self.com.port
        except (NameError, AttributeError):
            return 'Ошибка {}: Нет подключения'.format(self.port)


    def input_frequency(self, f):
        """ Установка заданной частоты на К2-82 """
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
        """ Отправка числовых значений (цифровая клавиатура на К2-82) """
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