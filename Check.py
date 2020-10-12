# Модуль аглгоритмов проверки радиостанции
import random, time
from functional import RSFunctional
from logging_settings import event_log
from PyQt5.QtCore import *
from settings import CODES, CHECK_TX_CODES, CHECK_RX_CODES



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
    # Настройка сигналов из потока
    next_screen_text = pyqtSignal(str)
    next_message_box = pyqtSignal(list)
    check_status = pyqtSignal(dict)

    def __init__(self, k2_functional, rs_functional):
        """ :param k2_functional - объект класса K2functional
            реализующий взаимодействие с приставкой К2-82
        """
        super().__init__()

        self.f = 136.000
        self.serial_number = {'value': '', 'is_correct': True}
        self.dev = {'value': '-', 'is_correct': False}
        self.p = {'value': '-', 'is_correct': True}
        self.high_p = {'value': '-', 'is_correct': True}
        self.kg = {'value': '-', 'is_correct': True}
        self.chm_u = {'value': '-', 'is_correct': True}
        self.chm = 0
        self.chm_max = {'value': '-', 'is_correct': True}
        self.selectivity_rc = {'value': '-', 'is_correct': True}
        self.out_pow = {'value': '-', 'is_correct': True}
        self.out_pow_vt =  {'value': '-', 'is_correct': True}
        self.selectivity = {'value': '-', 'is_correct': True}
        self.out_kg = {'value': '-', 'is_correct': True}
        self.noise_reduction = {'value': '-', 'is_correct': True}
        self.i = {'value': '-', 'is_correct': True}
        self.i_rc = {'value': '-', 'is_correct': True}
        self.discharge_alarm = {'value': random.randint(59, 61) / 10, 'is_correct': True}
        self.charge = self.manipulator = {'value': '-', 'is_correct': True}

        self.data = set()
        self.k2_functional = k2_functional
        self.rs_functional = rs_functional
        self.param_list = []


    @pyqtSlot()
    def run(self, *args, **kwargs):
        """ Запуск процесса проверки в отдельном потоке
        """
        # Засекаем время начала проверки проверки
        started_time = time.time()

        try:
            self.k2_functional.check = True

            if self.k2_functional.check_tx:
                self.next_message_box.emit(['Проверка передатчика', 'Поставьте радиостанцию в режим передачи'])
                time.sleep(0.5)
                while not self.k2_functional.continue_thread: pass

                self.check_transmitter()

                self.next_message_box.emit(['Проверка передатчика', 'Снимите радиостанцию с режима передачи'])
                time.sleep(0.5)
                while not self.k2_functional.continue_thread: pass
            else:
                if self.k2_functional.random_values: self.default_tx_values()

            if self.k2_functional.check_rx:
                self.check_receiver()
                self.k2_functional.check = False
            else:
                if self.k2_functional.random_values: self.default_rx_values()

            # Засекаем время окончания, получаем общее время проверки, при успешном завершении логируем
            ended_time = time.time()
            elapsed = ended_time - started_time
            minutes = int(elapsed // 60)
            seconds = round(elapsed % 60, 4)
            event_log.info('Check lasted {} min {} sec'.format(minutes, seconds))

            self.k2_functional.com.close()

            # Если проверяем Моторолу, то считываем с нее серийный номер
            self.serial_number['value'] = self.get_serial_number()

            # Сигнал об успешном завершениии. Передает параметры РС после проверки
            self.check_status.emit({"message" :'Проверка завершена успешно',
                                    "params": [
                                        self.serial_number, self.p, self.high_p, self.dev, self.kg, self.chm_u,
                                        self.chm_max, self.selectivity_rc, self.out_pow, self.out_pow_vt,
                                        self.selectivity, self.out_kg, self.noise_reduction, self.i, self.i_rc,
                                        self.discharge_alarm, self.charge, self.manipulator,
                                    ]})

        except AttributeError as exc:
            event_log.error(exc)
            self.check_status.emit({
                "message": 'Не удается соедениться с {}'.format(self.k2_functional.port),
                "params": None
            })
        except NoRSError as no_rs:
            event_log.warning('RS connecting error')
            self.check_status.emit({
                "message": no_rs.error_message,
                "params": None
            })
        except CancelError as cancel:
            event_log.info('Cancel check')
            self.check_status.emit({
                "message": cancel.error_message,
                "params": None
            })
        except StartError as algorithm_er:
            event_log.warning('Start check error')
            self.check_status.emit({
                "message": algorithm_er.error_message,
                "params": None
            })
        except Exception as ex:
            event_log.error(ex)
            self.check_status.emit({
                "message": "Неизвестная ошибка, дайте пизды производителю",
                "params": None
            })


    def check_transmitter(self):
        """ Проверка передатчика
        """
        if self.k2_functional.model == 'Motorola':
            self.chm_u['value'] = 9.5
            self.i['value'] = 50
            self.i_rc = {'value': random.randint(37, 40) * 10, 'is_correct': True}
        elif self.k2_functional.model == 'Альтавия':
            self.chm_u['value'] = 15
            self.i['value'] = 40
            self.selectivity_rc['value'] = random.randint(18, 20) / 100
            self.noise_reduction['value'] = random.randint(17, 18) / 100
            self.i_rc['value'] = random.randint(11, 13) * 10
        elif self.k2_functional.model == 'Icom':
            self.chm_u['value'] = 16
            self.i['value'] = 70
            self.i_rc['value'] = random.randint(18, 23) * 10

        functions = CHECK_TX_CODES
        timeout_02_functions = [1, 3, 4, 6, 9, 10, 12, 13, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
        percents = 0
        self.k2_functional.send_code(CODES['УСТ'])
        for step, function in enumerate(functions):
            if self.k2_functional.cancel:
                self.k2_functional.send_code(CODES['ОТКЛ'])
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

            if step == 2:
                self.next_message_box.emit([
                    'Проверка передатчика',
                    'Снимите с передачи и переключите уровень мощности'
                ])
                time.sleep(0.5)
                while not self.k2_functional.continue_thread: pass
                time.sleep(3)

            # Чувствительность модуляционного входа
            elif step == 5:
                for char in str(self.chm_u['value']):
                    self.k2_functional.numbers_entry(char=char)
                time.sleep(0.2)
                # for _ in range(2):
                self.k2_functional.send_code(CODES['mV/kHz'])
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
                        self.chm_u['value'] = round(self.chm_u['value'] + to_add, 1)
                        for char in str(self.chm_u['value']):
                            self.k2_functional.numbers_entry(char=char)
                        time.sleep(0.2)
                        self.k2_functional.send_code(CODES['mV/kHz'])
                        time.sleep(6)
                if self.chm_u['value'] >= 20 or self.chm_u['value'] == 1:
                    self.chm_u['is_correct'] = False

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
            self.k2_functional.send_code(CODES['ОТКЛ'])
            time.sleep(0.1)
        self.k2_functional.check = False
        self.k2_functional.send_code(CODES['УСТ'])
        self.k2_functional.com.close()


    def check_receiver(self):
        """ Проверка приёмника
        """
        self.out_pow_vt['value'] = '>0.5'
        self.selectivity['value'] = random.randint(70, 71)

        if self.k2_functional.model == 'Альтавия':
            self.selectivity_rc['value'] = random.randint(18, 20) / 100

        else:
            self.selectivity_rc['value'] = random.randint(20, 24) / 100

        functions = CHECK_RX_CODES

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
        noise_reduction = 25
        flag = True
        while flag:
            self.data = set()
            self.data.add(self.k2_functional.com.readline())
            data_list = []
            for line in self.data:
                data_list.append(line.decode('cp866'))
            for line in data_list:
                flag, noise_reduction = self.noise_reduction_decrypt(flag, line, noise_reduction)

        self.noise_reduction['value'] = noise_reduction / 100
        for _ in range(2):
            self.k2_functional.send_code(CODES['ОТКЛ'])
        time.sleep(0.2)
        self.k2_functional.send_code(CODES['ВНИЗ'])
        for code in ['0', '.', '5']:
            self.k2_functional.numbers_entry(code)
        self.k2_functional.send_code(CODES['mV/kHz'])


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
                self.kg['value'] = float(line[4:-4])
                if self.kg['value'] >= 3.0 or self.kg['value'] == 0: self.kg['is_correct'] = False
            elif 'P= ' in line:
                self.decrypt_power(line)
            elif 'ЧМ+= ' in line:
                if float(line[5:-6]) != self.chm_u['value']:
                    self.param_list.append(float(line[5:-6]))
            elif 'ЧМмах= ' in line:
                self.chm_max['value'] = float(line[7:-6])
                if self.chm_max['value'] >= 5 or self.chm_max == 0: self.chm_max[1] = False
            elif 'f=' in line:
                self.f = self.decrypt_frequency(line)
            elif 'Отклонение= ' in line:
                dev = float(line[12:-6])
                dev *= 1000
                self.dev['value'] = int(dev)
                self.dev['is_correct'] = False if self.dev['value'] > 300 else True

        # Если отключена макс девиация, значение рандомное
        if self.chm_max['value'] == 0.0:
            self.chm_max['value'] = random.randint(445, 491) / 100

        self.data = set()


    def decrypt_power(self, line):
        """
        Расшифровка выходной мащности радиостанции
        :param line: Строка со значением мощности полученная с К2-82 через COM порт
        """
        value = float(line[3:-6])
        if value == 0:
            return False
        if value < 4:
            self.p['value'] = value
        elif value > 5:
            self.high_p['value'] = 5.0
        else:
            self.high_p['value'] = value


    def decrypt_frequency(self, line):
        """
        Расшифровка частоты радиостанции
        :param line: Строка со значением частоты полученная с К2-82 через COM порт
        :return: расшифрованная и отформатированная частота
        """
        line = line[2:9]
        if line[6] == '6' or line[6] == '4':
            line = line[:3] + line[4:]
            line = line[:5] + '5'
            line = line[:3] + '.' + line[3:]
            return float(line)
        elif line[6] == '5':
            f = float(line)
            return round(f, 3)
        else:
            f = float(line)
            return round(f, 2)


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
            self.out_kg['value'] = self.param_list[-2]
        else:
            self.out_kg['value'] = self.param_list[0]

        if self.out_kg['value'] >= 5 or self.out_kg['value'] == 0:
                self.out_kg['is_correct'] = False

        for line in data_list:
            if 'U= ' in line:
                self.param_list.append(float(line[3:-5]))
        if len(self.param_list) >=2:
            self.out_pow['value'] = self.param_list[-2]
        else:
            self.out_pow['value'] = self.param_list[0]

        if self.out_pow['value'] < 2.0 or self.out_pow['value'] == 0:
            self.out_pow['is_correct'] = False
        elif self.out_pow['value'] > 5.0:
            self.out_pow['value'] = 5.0

        self.data = set()


    def noise_reduction_decrypt(self, flag, line, noise_reduction):
        """
        Расшифровка параметра порога срабатывания шумоподавителя
        :param flag: - Пока флаг True выполняется счтывание с К2-82 и корректировка напряжения
        :param line: - Строка значений К2-82 которая пришла с ком порта
        :param noise_reduction: - значение порога срабатывание шумоподавителя
        :return: Возвращаем флаг который определяет найдено значение или нет и само значение шумоподавителя
        """
        if 'Kг=' in line:
            kg = float(line[3:-4])
            if kg == 99.0:
                noise_reduction += 1
                flag = False
        if 'U= ' in line:
            u = float(line[3:-5])
            if float(u) > 10 or float(u) == 2.0: flag = False
            elif ' мВ' in line: flag = False
            else:
                noise_reduction -= 1
                entry_list = ['0', '.', str(noise_reduction // 10), str(noise_reduction % 10)]
                for char in entry_list:
                    self.k2_functional.numbers_entry(char)
                self.k2_functional.send_code(CODES['uV/Hz'])
                time.sleep(1)
                if noise_reduction == 10:
                    self.noise_reduction['is_correct'] = False
                    flag = False
        return flag, noise_reduction


    def get_serial_number(self):
        """ Получение серийного номера с радиостанции
        """
        if self.k2_functional.model == 'Motorola':
            rs = RSFunctional()
            try:
                rs.connect_com_port(self.rs)
                return rs.get_serial()
            except Exception as ex: event_log.error(ex)


    def default_tx_values(self):
        """ Рандомные значения для параметров передатчика
        """
        self.dev['value'] = random.randint(15, 290)
        self.dev['is_correct'] = True
        self.p['value'] = random.randint(200, 300) / 100
        if self.k2_functional.model == 'Радий':
            self.high_p['value'] = '-'
        else:
            self.high_p['value'] = random.randint(400, 500) / 100
        self.kg['value'] = random.randint(8, 20) / 10
        if self.k2_functional.model == 'Motorola':
            self.chm_u['value'] = random.randint(90, 100) / 10
        if self.k2_functional.model in ['Альтавия', 'Радий', 'Icom']:
            self.chm_u['value'] = random.randint(140, 180) / 10
        self.chm_max['value'] = random.randint(410, 495) / 100


    def default_rx_values(self):
        """ Рандомные значения для параметров приемника
        """
        if self.k2_functional.model == 'Альтавия':
            self.out_pow['value'] = random.randint(200, 265) / 100
            self.selectivity_rc['value'] = random.randint(16, 19) / 100
            self.noise_reduction['value'] = random.randint(13, 16) / 100
        else:
            self.out_pow['value'] = random.randint(400, 495) / 100
            self.selectivity_rc['value'] = random.randint(20, 24) / 100
            self.noise_reduction['value'] = random.randint(15, 20) / 100
        self.out_pow_vt['value'] = '>0.5'
        self.selectivity['value'] = random.randint(70, 71)
        self.out_kg['value'] = random.randint(100, 300) / 100
        if self.k2_functional.model == 'Motorola':
            self.i['value'] = 50
            self.i_rc['value'] = random.randint(37, 40) * 10
        elif self.k2_functional.model == 'Альтавия':
            self.i['value'] = 40
            self.i_rc['value'] = random.randint(11, 14) * 10
        elif self.k2_functional.model == 'Радий':
            self.i['value'] = 40
            self.i_rc['value'] = random.randint(27, 29) * 10
        elif self.k2_functional.model == 'Icom':
            self.i['value'] = 70
            self.i_rc['value'] = random.randint(24, 27) * 10