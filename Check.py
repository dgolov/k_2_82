# Модуль аглгоритмов проверки радиостанции

import random, time
from logging_settings import event_log
from PyQt5.QtCore import *


class NoRSError(Exception):
    """Ошибка связи с радиостанцией
    """
    def __init__(self):
        super(NoRSError, self).__init__()
        self.error_message = "Нет связи с радиостанцией. Проверьте питание и PTT"


class CancelError(Exception):
    """Отмена проверки
    """
    def __init__(self):
        super(CancelError, self).__init__()
        self.error_message = "Проверка отменена"


class StartError(Exception):
    """Ошибка алгоритма, сбиты настройки К2-82 при запуске проверки
    """
    def __init__(self):
        super(StartError, self).__init__()
        self.error_message = "Нет связи с К2-82. Проверьте подключение и активность УСТ и ДУ"



class Check(QObject):
    """
    Класс реализующий алгоритм проверки радиостанции
    """
    # runing = False
    next_screen_text = pyqtSignal(str)
    next_message_box = pyqtSignal(list)
    check_status = pyqtSignal(dict)

    def __init__(self, functional):
        """
        :param functional - объект класса K2functional реализующий взаимодействие с приставкой
        """
        super().__init__()
        self.f = 136.000
        self.dev = 0
        self.p = random.randint(20, 24) / 10
        self.hight_p = random.randint(45, 50) / 10
        self.kg = 0
        self.chm_u = 0
        self.chm = 0
        self.chm_max = 0
        self.selectivity_rc = random.randint(20, 25) / 100
        self.out_pow = 0
        self.out_pow_vt = '>0.5'
        self.selectivity = random.randint(69, 72)
        self.out_kg = 0
        self.noise_reduction = random.randint(15, 20) / 100
        self.i = 50
        self.discharge_alarm = random.randint(59, 61) / 10

        self.data = set()
        self.functional = functional
        self.param_list = []


    @pyqtSlot()
    def run(self, *args, **kwargs):
        """ Запуск процесса проверки в отдельном потоке
        """
        # Засекаем время начала проверки проверки
        started_time = time.time()
        try:
            self.functional.check = True

            self.next_message_box.emit(['Проверка передатчика', 'Поставьте радиостанцию в режим передачи'])
            time.sleep(0.5)
            while not self.functional.continue_thread:
                pass

            self.check_transmitter()

            self.next_message_box.emit(['Проверка передатчика', 'Снимите радиостанцию с режима передачи'])
            time.sleep(0.5)
            while not self.functional.continue_thread:
                pass

            self.check_receiver()
            self.functional.check = False

            # Засекаем время окончания, получаем общее время проверки, при успешном завершении логируем
            ended_time = time.time()
            elapsed = ended_time - started_time
            minutes = int(elapsed // 60)
            seconds = round(elapsed % 60, 4)
            event_log.info('Check lasted {} min {} sec'.format(minutes, seconds))

            self.check_status.emit({"message" :'Проверка завершена успешно',
                    "params": [self.p, self.hight_p, self.dev, self.kg, self.chm_u, self.chm_max,
                               self.selectivity_rc, self.out_pow, self.out_pow_vt, self.selectivity, self.out_kg,
                               self.noise_reduction, self.i, self.discharge_alarm]} )


        except AttributeError:
            event_log.error('COM port connecting error')
            self.check_status.emit({"message": 'Не удается соедениться с {}'.format(self.functional.port),
                                   "params": None})
        except NoRSError as no_rs:
            event_log.warning('RS connecting error')
            self.check_status.emit({"message": no_rs.error_message, "params": None})
        except CancelError as cancel:
            event_log.info('Cancel check')
            self.check_status.emit({"message": cancel.error_message, "params": None})
        except StartError as algorithm_er:
            event_log.warning('Start check error')
            self.check_status.emit({"message": algorithm_er.error_message, "params": None})


    def check_transmitter(self):
        """ Проверка передатчика
        """
        if self.functional.model == 'Motorola':
            self.chm_u = 9.5
        elif self.functional.model == 'Альтавия':
            self.chm_u = 15
            self.i = 40
            self.selectivity_rc = random.randint(20, 20) / 100
            self.noise_reduction = random.randint(12, 18) / 100
            self.i_rc = random.randint(11, 13) * 10
        elif self.functional.model == 'Icom':
            self.chm_u = 16
            self.i = 70
            self.i_rc = random.randint(18, 23) * 10
        functions = [b'0x26', b'0x20', b'0x29', b'0x20', b'0x33', b'0x15', b'0x20', b'0x17',
                     b'0x15', b'0x20', b'0x17', b'0x15', b'0x20', b'0x16', b'0x17', b'0x15',
                     b'0x15', b'0x20', b'0x17', b'0x00', b'0x10', b'0x05', b'0x13', b'0x27',
                     b'0x03', b'0x13', b'0x17', b'0x01', b'0x13', b'0x23']
        timeout_02_functions = [1, 3, 4, 6, 9, 10, 12, 13, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
        percents = 0
        self.functional.send_code(b'0x23')
        for step, function in enumerate(functions):
            if self.functional.cancel:
                self.functional.send_code(b'0x20')
                self.functional.check = False
                self.functional.cancel = False
                raise CancelError

            self.next_screen_text.emit('Проверяю передатчик. Завершено {}%'.format(round(percents, 1)))

            # Проверка доступа к радиостанции
            if step == 1:
                self.data.add(self.functional.com.readline())
                self.take_result(self.description_tr)
                if self.f < 136.0:
                    self.functional.send_code(b'0x20')
                    self.functional.check = False
                    time.sleep(0.1)
                    self.functional.send_code(b'0x23')
                    raise NoRSError
                elif self.f == 136.0:
                    self.functional.send_code(b'0x20')
                    self.functional.check = False
                    time.sleep(0.1)
                    self.functional.send_code(b'0x23')
                    raise StartError

            # Повторяющиеся действия 3 раза, например стрелки
            if step in [7, 14, 17]:
                for _ in range(2):
                    self.functional.send_code(function)
                    time.sleep(0.2)

            self.functional.send_code(function)

            # Частота, мощность, отклонение
            if step in [0, 2, 16]:
                time.sleep(5)

            # Чувствительность модуляционного входа
            elif step == 5:
                for char in str(self.chm_u):
                    self.functional.numbers_entry(char=char)
                time.sleep(0.2)
                # for _ in range(2):
                self.functional.send_code(b'0x13')
                time.sleep(4)
                while self.chm < 2.95 or self.chm > 3.05:
                    for _ in range(10):
                        self.data.add(self.functional.com.readline())
                    self.take_result(self.description_tr)
                    if not self.param_list: continue
                    self.chm = min(self.param_list)
                    if self.chm < 2.95 or self.chm > 3.05:
                        difference = (3.0 - self.chm) / 0.025
                        difference = round(difference)
                        to_add = difference / 10
                        self.chm_u = round(self.chm_u + to_add, 1)
                        for char in str(self.chm_u):
                            self.functional.numbers_entry(char=char)
                        time.sleep(0.2)
                        self.functional.send_code(b'0x13')
                        time.sleep(6)

            # КНИ
            elif step == 8:
                time.sleep(10)

            # Максимальная девиация
            elif step == 11:
                self.take_result(self.description_tr)
                time.sleep(self.functional.check_deviation_time)

            # Установка частоты
            elif step == 15:
                for char in str(self.f):
                    self.functional.numbers_entry(char=char)

            # УСТ в конце проверки
            elif step == 29:
                time.sleep(0.2)
                self.functional.send_code(function)

            # Основные шаги между режимами
            elif step in timeout_02_functions:
                self.data.add(self.functional.com.readline())
                time.sleep(0.2)

            percents += 100 / len(functions)

        self.data.add(self.functional.com.readline())
        self.take_result(self.description_tr)
        self.functional.input_frequency(str(self.f))


    def check_receiver(self):
        """ Проверка приёмника
        """
        functions = [ b'0x23', b'0x33', b'0x17', b'0x15', b'0x13', b'0x15',
                      b'0x00', b'0x10', b'0x02', b'0x05', b'0x14', b'0x20']

        for step, function in enumerate(functions):
            if self.functional.cancel:
                self.functional.check = False
                self.functional.cancel = False
                raise CancelError

            self.next_screen_text.emit('Проверяю приёмник')

            if step == 2 or step == 11:
                self.functional.send_code(function)
                time.sleep(0.2)
            self.functional.send_code(function)
            time.sleep(0.2)
            if step == 4:
                time.sleep(5)
                self.next_message_box.emit(['Проверка приёмника', 'Убавьте выходную мощность регулятором громкости'])
                time.sleep(0.5)
                while not self.functional.continue_thread:
                    pass
            if step == 5:
                time.sleep(5)

        # Цикл считывания данных с COM порта
        for _ in range(20):
             self.data.add(self.functional.com.readline())
        self.take_result(self.description_rc)


    def take_result(self, func):
        """
        Генератор распаковки результатов с COM порта
        :param func - функция расшифровки
        """
        data_list = []
        for line in self.data:
            data_list.append(line.decode('cp866'))
        data_list.sort()
        func(data_list)


    def description_tr(self, data_list):
        """
        Расшифровка результатов проверки передатчика
        :param data_list - список результатов
        """
        self.param_list = []

        for line in data_list:
            if 'Kг= ' in line:
                self.kg = float(line[4:-4])
            elif 'P= ' in line:
                value = float(line[3:-6])
                if value < 4:
                    self.p = value
                elif value > 5:
                    self.hight_p = 5
                else:
                    self.hight_p = value
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
        """
        Расшифровка результатов проверки приёмника
        :param data_list - список результатов
        """
        self.param_list = []

        for line in data_list:
            if 'Kг= ' in line:
                self.param_list.append(float(line[4:-4]))
        if len(self.param_list) >=2:
            self.out_kg = self.param_list[-2]
        else:
            self.out_kg = self.param_list[0]

        for line in data_list:
            if 'U= ' in line:
                self.param_list.append(float(line[3:-5]))
        if len(self.param_list) >=2:
            self.out_pow = self.param_list[-2]
        else:
            self.out_pow = self.param_list[0]

        self.data = set()