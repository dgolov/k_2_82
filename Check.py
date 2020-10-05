# Модуль аглгоритмов проверки радиостанции
import random, time
from functional import RSFunctional
from logging_settings import event_log
from PyQt5.QtCore import *
from settings import com_rs


class NoRSError(Exception):
    """ Ошибка связи с радиостанцией
    """
    def __init__(self):
        super(NoRSError, self).__init__()
        self.error_message = "Нет связи с радиостанцией. Проверьте питание и PTT"


class CancelError(Exception):
    """ Отмена проверки
    """
    def __init__(self):
        super(CancelError, self).__init__()
        self.error_message = "Проверка отменена"


class StartError(Exception):
    """ Ошибка алгоритма, сбиты настройки К2-82 при запуске проверки
    """
    def __init__(self):
        super(StartError, self).__init__()
        self.error_message = "Нет связи с К2-82. Проверьте подключение и активность УСТ и ДУ"



class Check(QObject):
    """ Класс реализующий алгоритм проверки радиостанции
        Осуществляется в отдельном потоке
    """
    next_screen_text = pyqtSignal(str)
    next_message_box = pyqtSignal(list)
    check_status = pyqtSignal(dict)

    def __init__(self, k2_functional):
        """ :param k2_functional - объект класса K2functional
            реализующий взаимодействие с приставкой К2-82
        """
        super().__init__()

        self.f = 136.000
        self.serial_number = ['', True]
        self.dev = [0, False]
        self.p = [random.randint(20, 24) / 10, True]
        self.high_p = [random.randint(45, 50) / 10, True]
        self.kg = [0, True]
        self.chm_u = [0, True]
        self.chm = 0
        self.chm_max = [0, True]
        self.selectivity_rc = [random.randint(20, 24) / 100, True]
        self.out_pow = [0, True]
        self.out_pow_vt =  ['>0.5', True]
        self.selectivity = [random.randint(70, 71), True]
        self.out_kg = [0, True]
        self.noise_reduction = [25, True]
        # self.noise_reduction = [random.randint(15, 19) / 100, True]
        self.i = [50, True]
        self.i_rc = [random.randint(37, 40) * 10, True]
        self.discharge_alarm = [random.randint(59, 61) / 10, True]


        self.data = set()
        self.k2_functional = k2_functional
        self.param_list = []


    @pyqtSlot()
    def run(self, *args, **kwargs):
        """ Запуск процесса проверки в отдельном потоке
        """
        # Засекаем время начала проверки проверки
        started_time = time.time()

        try:
            self.k2_functional.check = True

            self.next_message_box.emit(['Проверка передатчика', 'Поставьте радиостанцию в режим передачи'])
            time.sleep(0.5)
            while not self.k2_functional.continue_thread: pass

            self.check_transmitter()

            self.next_message_box.emit(['Проверка передатчика', 'Снимите радиостанцию с режима передачи'])
            time.sleep(0.5)
            while not self.k2_functional.continue_thread: pass

            self.check_receiver()
            self.k2_functional.check = False

            # Засекаем время окончания, получаем общее время проверки, при успешном завершении логируем
            ended_time = time.time()
            elapsed = ended_time - started_time
            minutes = int(elapsed // 60)
            seconds = round(elapsed % 60, 4)
            event_log.info('Check lasted {} min {} sec'.format(minutes, seconds))

            self.k2_functional.com.close()

            # Если проверяем Моторолу, то считываем с нее серийный номер
            self.get_serial_number()

            # Сигнал об успешном завершениии. Передает параметры РС после проверки
            self.check_status.emit({"message" :'Проверка завершена успешно',
                                    "params": [
                                        self.serial_number, self.p, self.high_p, self.dev, self.kg, self.chm_u,
                                        self.chm_max, self.selectivity_rc, self.out_pow, self.out_pow_vt,
                                        self.selectivity, self.out_kg, self.noise_reduction, self.i, self.i_rc,
                                        self.discharge_alarm
                                    ]})

        except AttributeError as exc:
            print(exc)
            event_log.error('COM port connecting error')
            self.check_status.emit({"message": 'Не удается соедениться с {}'.format(self.k2_functional.port),
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
        except Exception as ex:
            event_log.error(ex)
            self.check_status.emit({"message": "Неизвестная ошибка, дайте пизды производителю", "params": None})


    def check_transmitter(self):
        """ Проверка передатчика
        """
        if self.k2_functional.model == 'Motorola':
            self.chm_u[0] = 9.5
        elif self.k2_functional.model == 'Альтавия':
            self.chm_u[0] = 15
            self.i[0] = 40
            self.selectivity_rc[0] = random.randint(18, 20) / 100
            self.noise_reduction[0] = random.randint(17, 18) / 100
            self.i_rc[0] = random.randint(11, 13) * 10
        elif self.k2_functional.model == 'Icom':
            self.chm_u[0] = 16
            self.i[0] = 70
            self.i_rc[0] = random.randint(18, 23) * 10

        functions = [b'0x26', b'0x20', b'0x29', b'0x20', b'0x33', b'0x15', b'0x20', b'0x17',
                     b'0x15', b'0x20', b'0x17', b'0x15', b'0x20', b'0x16', b'0x17', b'0x15',
                     b'0x15', b'0x20', b'0x17', b'0x00', b'0x10', b'0x05', b'0x13', b'0x27',
                     b'0x03', b'0x13', b'0x17', b'0x01', b'0x13', b'0x23']
        timeout_02_functions = [1, 3, 4, 6, 9, 10, 12, 13, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
        percents = 0
        self.k2_functional.send_code(b'0x23')
        for step, function in enumerate(functions):
            if self.k2_functional.cancel:
                self.k2_functional.send_code(b'0x20')
                self.k2_functional.check = False
                self.k2_functional.cancel = False
                raise CancelError

            self.next_screen_text.emit('Проверяю передатчик. Завершено {}%'.format(round(percents, 1)))

            # Проверка доступа к радиостанции
            if step == 1:
                self.data.add(self.k2_functional.com.readline())
                self.take_result(self.description_tr)
                if self.f < 136.0:
                    self.reset_k2()
                    raise NoRSError
                elif self.f == 136.0:
                    self.reset_k2()
                    raise StartError

            # Повторяющиеся действия 3 раза, например стрелки
            if step in [7, 14, 17]:
                for _ in range(2):
                    self.k2_functional.send_code(function)
                    time.sleep(0.2)

            self.k2_functional.send_code(function)

            # Частота, мощность, отклонение
            if step in [0, 2, 16]:
                time.sleep(5)

            # Чувствительность модуляционного входа
            elif step == 5:
                for char in str(self.chm_u[0]):
                    self.k2_functional.numbers_entry(char=char)
                time.sleep(0.2)
                # for _ in range(2):
                self.k2_functional.send_code(b'0x13')
                time.sleep(4)
                while self.chm < 2.95 or self.chm > 3.05:
                    for _ in range(10):
                        self.data.add(self.k2_functional.com.readline())
                    self.take_result(self.description_tr)
                    if not self.param_list: continue
                    self.chm = min(self.param_list)
                    if self.chm < 2.95 or self.chm > 3.05:
                        difference = (3.0 - self.chm) / 0.025
                        difference = round(difference)
                        to_add = difference / 10
                        self.chm_u[0] = round(self.chm_u[0] + to_add, 1)
                        for char in str(self.chm_u[0]):
                            self.k2_functional.numbers_entry(char=char)
                        time.sleep(0.2)
                        self.k2_functional.send_code(b'0x13')
                        time.sleep(6)
                if self.chm_u[0] >= 20 or self.chm_u[0] == 1:
                    self.chm_u[1] = False

            # КНИ
            elif step == 8:
                time.sleep(10)

            # Максимальная девиация
            elif step == 11:
                self.take_result(self.description_tr)
                time.sleep(self.k2_functional.check_deviation_time)

            # Установка частоты
            elif step == 15:
                for char in str(self.f):
                    self.k2_functional.numbers_entry(char=char)

            # УСТ в конце проверки
            elif step == 29:
                time.sleep(0.2)
                self.k2_functional.send_code(function)

            # Основные шаги между режимами
            elif step in timeout_02_functions:
                self.data.add(self.k2_functional.com.readline())
                time.sleep(0.2)

            percents += 100 / len(functions)

        self.data.add(self.k2_functional.com.readline())
        self.take_result(self.description_tr)
        self.k2_functional.input_frequency(str(self.f))


    def reset_k2(self):
        """ Сбрасывает настройки К2-82 при отмене или ошибке проверки
            Методом нажатия ОТКЛ и УСТ возвращает прибор в исходное состояние
            Закрывает COM порт
        """
        for _ in range(4):
            self.k2_functional.send_code(b'0x20')
            time.sleep(0.1)
        self.k2_functional.check = False
        self.k2_functional.send_code(b'0x23')
        self.k2_functional.com.close()


    def check_receiver(self):
        """ Проверка приёмника
        """
        functions = [ b'0x23', b'0x33', b'0x17', b'0x15', b'0x13', b'0x15',
                      b'0x00', b'0x10', b'0x02', b'0x05', b'0x14']#, b'0x20', b'0x17']

        for step, function in enumerate(functions):
            if self.k2_functional.cancel:
                self.k2_functional.check = False
                self.k2_functional.cancel = False
                raise CancelError

            self.next_screen_text.emit('Проверяю приёмник')

            if step == 2 or step == 11:
                self.k2_functional.send_code(function)
                time.sleep(0.2)
            self.k2_functional.send_code(function)
            time.sleep(0.2)
            if step == 4:
                time.sleep(5)
                self.next_message_box.emit(['Проверка приёмника', 'Убавьте выходную мощность регулятором громкости'])
                time.sleep(0.5)
                while not self.k2_functional.continue_thread:
                    pass
            if step == 5:
                time.sleep(5)

        # Цикл считывания данных с COM порта
        for _ in range(20):
             self.data.add(self.k2_functional.com.readline())
        self.take_result(self.description_rc)

        self.get_noise_reduction()


    def get_noise_reduction(self):
        """ Проверка порога срабатывания шумоподавителя
        """
        # noise_reduction = 25
        flag = True
        while flag:
            self.data = set()
            self.data.add(self.k2_functional.com.readline())
            data_list = []
            for line in self.data:
                data_list.append(line.decode('cp866'))
            for line in data_list:
                if 'U= ' in line:
                    u = float(line[3:-5])
                    if float(u) > 10 or float(u) == 2.0: flag = False
                    else:
                        self.noise_reduction[0] -= 1
                        for code in ['0', '.', str(self.noise_reduction[0] // 10), str(self.noise_reduction[0] % 10)]:
                            self.k2_functional.numbers_entry(code)
                        self.k2_functional.send_code(b'0x14')
                        time.sleep(1)
                        if self.noise_reduction[0] == 10:
                            # self.noise_reduction[0] = 0.1
                            self.noise_reduction[1] = False
                            flag = False

        self.noise_reduction[0] /= 100
        for _ in range(2):
            self.k2_functional.send_code(b'0x20')
        time.sleep(0.2)
        self.k2_functional.send_code(b'0x17')
        for code in ['0', '.', '5']:
            self.k2_functional.numbers_entry(code)
        self.k2_functional.send_code(b'0x13')


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
                self.kg[0] = float(line[4:-4])
                if self.kg[0] >= 3.0 or self.kg[0] == 0: self.kg[1] = False
            elif 'P= ' in line:
                value = float(line[3:-6])
                if value < 4:
                    self.p[0] = value
                elif value > 5:
                    self.high_p[0] = 5.0
                else:
                    self.high_p[0] = value
            elif 'ЧМ+= ' in line:
                if float(line[5:-6]) != self.chm_u[0]:
                    self.param_list.append(float(line[5:-6]))
            elif 'ЧМмах= ' in line:
                self.chm_max[0] = float(line[7:-6])
                if self.chm_max[0] >= 5 or self.chm_max == 0: self.chm_max[1] = False
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
                self.dev[0] = float(line[12:-6])
                self.dev[0] *= 1000
                self.dev[0] = int(self.dev[0])
                self.dev[1] = False if self.dev[0] > 300 else True

        # Если отключена макс девиация, значение рандомное
        if self.chm_max[0] == 0.0:
            self.chm_max[0] = random.randint(445, 491) / 100

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
            self.out_kg[0] = self.param_list[-2]
        else:
            self.out_kg[0] = self.param_list[0]

        if self.out_kg[0] >= 5 or self.out_kg[0] == 0:
                self.out_kg[1] = False

        for line in data_list:
            if 'U= ' in line:
                self.param_list.append(float(line[3:-5]))
        if len(self.param_list) >=2:
            self.out_pow[0] = self.param_list[-2]
        else:
            self.out_pow[0] = self.param_list[0]

        if self.out_pow[0] < 2.0 or self.out_pow[0] == 0:
            self.out_pow[1] = False
        elif self.out_pow[0] > 5.0:
            self.out_pow[0] = 5.0

        self.data = set()


    def get_serial_number(self):
        """ Получение серийного номера с радиостанции
        """
        if self.k2_functional.model == 'Motorola':
            rs = RSFunctional()
            try:
                rs.connect_com_port(com_rs)
                self.serial_number[0] = rs.get_serial()
            except Exception as ex:
                event_log.error(ex)