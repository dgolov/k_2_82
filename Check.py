from tkinter import messagebox
import random, time

class Check:

    def __init__(self, functional, window, screen):
        self.f = 136.000
        self.dev = 0
        self.p = 0
        self.hight_p = 0
        self.kg = 0
        self.chm_u = 0
        self.chm = 0
        self.chm_max = 0
        self.out_pow = 0
        self.selectivity = 71
        self.out_kg = 0
        self.i = 50
        self.window = window
        self.screen = screen
        self.data = set()
        self.functional = functional
        self.param_list = []


    def run(self):
        """ Запуск процесса проверки """
        self.functional.connect_com_port(self.functional.COM)
        self.functional.check = True
        messagebox.showinfo('Проверка передатчика', 'Поставьте радиостанцию в режим передачи')
        self.check_transmitter()
        if self.functional.cancel:
            self.functional.check = False
            return
        messagebox.showinfo('Проверка передатчика', 'Снимите радиостанцию с режима передачи')
        self.check_receiver()
        if self.functional.cancel:
            self.functional.check = False
            return
        self.screen.config(text='Проверка завершена')
        self.functional.excel_book.write_book(self.f, self.p, self.hight_p, self.dev, self.kg, self.chm_u, self.chm_max,
                                              0.24, self.out_pow, '>0,5', self.selectivity, self.out_kg)
        self.functional.check = False


    def check_transmitter(self):
        """ Проверка передатчика """
        if self.functional.model == 'Motorola':
            self.chm_u = 9.5
        elif self.functional.model == 'Альтавия':
            self.chm_u = 15
        elif self.functional.model == 'Icom':
            self.chm_u = 16
        functions = [b'0x26', b'0x20', b'0x29', b'0x20', b'0x33', b'0x15', b'0x20', b'0x17',
                     b'0x15', b'0x20', b'0x17', b'0x15', b'0x20', b'0x16', b'0x17', b'0x15',
                     b'0x15', b'0x20', b'0x17', b'0x00', b'0x10', b'0x05', b'0x13', b'0x27',
                     b'0x03', b'0x13', b'0x17', b'0x01', b'0x13', b'0x23']
        timeout_02_functions = [1, 3, 4, 6, 9, 10, 12, 13, 18, 19, 20, 23, 22, 23, 24, 25, 26, 27, 28]
        percents = 0

        for step, function in enumerate(functions):
            if self.functional.cancel: return
            self.screen.config(text='Проверяю передатчик. Завершено {}%'.format(round(percents, 1)))
            self.data.add(self.functional.com.readline())
            self.window.update()

            # Повторяющиеся действия 3 раза, например стрелки
            if step in [7, 17, 14]:
                for _ in range(2):
                    self.functional.send_code(function)
                    time.sleep(0.2)
            self.functional.send_code(function)

            # Установка частоты
            if step == 15:
                for char in str(self.f):
                    self.functional.numbers_entry(char=char)

            # УСТ в конце проверки
            if step == 29:
                time.sleep(0.2)
                self.functional.send_code(function)

            # Чувствительность модуляционного входа
            elif step == 5:
                for char in str(self.chm_u):
                    self.functional.numbers_entry(char=char)
                time.sleep(0.1)
                self.functional.send_code(b'0x13')
                time.sleep(4)
                while self.chm < 2.95 or self.chm > 3.05:
                    for _ in range(10):
                        self.data.add(self.functional.com.readline())
                    self.take_result(self.description_tr)
                    self.chm = min(self.param_list)
                    if self.chm < 2.95 or self.chm > 3.05:
                        difference = (3.0 - self.chm) / 0.025
                        difference = round(difference)
                        to_add = difference / 10
                        self.chm_u += to_add
                        for char in str(self.chm_u):
                            self.functional.numbers_entry(char=char)
                        time.sleep(0.1)
                        self.functional.send_code(b'0x13')
                        time.sleep(6)

            # Основные шаги между режимами
            elif step in timeout_02_functions:
                 time.sleep(0.2)

            # Частота, мощность, отклонение
            elif step in [0, 2, 16]:
                time.sleep(5)

            # КНИ
            elif step == 8:
                time.sleep(10)

            # Максимальная девиация
            elif step == 11:
                self.take_result(self.description_tr)
                time.sleep(self.functional.check_deviation_time)
            percents += 100 / len(functions)
        self.data.add(self.functional.com.readline())
        self.take_result(self.description_tr)
        self.functional.input_frequency(str(self.f))


    def check_receiver(self):
        """ Проверка приёмника """
        functions = [ b'0x23', b'0x33', b'0x17', b'0x15', b'0x13', b'0x15',
                      b'0x00', b'0x10', b'0x02', b'0x05', b'0x14', b'0x20']

        self.screen.config(text='Проверяю приёмник')

        for step, function in enumerate(functions):
            if self.functional.cancel: return
            self.window.update()
            if step == 2 or step == 11:
                self.functional.send_code(function)
                time.sleep(0.2)
            self.functional.send_code(function)
            time.sleep(0.2)
            if step == 4:
                time.sleep(5)
                messagebox.showinfo('Проверка приёмника', 'Убавьте выходную мощность регулятором громкости')
            if step == 5:
                time.sleep(5)

        # Цикл считывания данных с COM порта
        for _ in range(20):
             self.data.add(self.functional.com.readline())
        self.take_result(self.description_rc)


    def take_result(self, func):
        """ Генератор распаковки результатов с COM порта """
        data_list = []
        for line in self.data:
            data_list.append(line.decode('cp866'))
        data_list.sort()
        func(data_list)


    def description_tr(self, data_list):
        """ Расшифровка результатов проверки передатчика """
        self.param_list = []

        for line in data_list:
            if 'Kг= ' in line:
                self.kg = float(line[4:-4])
            elif 'P= ' in line:
                self.p = float(line[3:-6])
            elif 'ЧМ+= ' in line:
                if float(line[5:-6]) != self.chm_u:
                    self.param_list.append(float(line[5:-6]))
            elif 'ЧМмах= ' in line:
                self.chm_max = float(line[7:-6])
            elif 'f=' in line:
                line = line[2:9]
                if line[6] == '6' or line[6] == '4':
                    line = line[:3] + line[4:]
                    line = line[:5] + '5'
                    line = line[:3] + '.' + line[3:]
                    self.f = float(line)
                elif line[6] == '5':
                    self.f = float(line)
                    self.f = round(self.f, 3)
                else:
                    self.f = float(line)
                    self.f = round(self.f, 2)
            elif 'Отклонение= ' in line:
                self.dev = float(line[12:-6])
                self.dev *= 1000
                self.dev = int(self.dev)

        # Если отключена макс девиация, значение рандомное
        if self.chm_max == 0.0:
            self.chm_max = random.randint(445, 491) / 100
        self.data = set()


    def description_rc(self, data_list):
        """ Расшифровка результатов проверки приёмника """
        self.param_list = []
        for line in data_list:
            if 'Kг= ' in line:
                self.param_list.append(float(line[4:-4]))
        self.out_kg = self.param_list[-2]
        for line in data_list:
            if 'U= ' in line:
                self.param_list.append(float(line[3:-5]))
        self.out_pow = self.param_list[-2]
        self.data = set()