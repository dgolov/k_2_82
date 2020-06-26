# -*- coding: utf-8 -*-

import tkinter, serial, time

from uu import decode, encode

COLOR = 'cornflowerblue'


class Window:
    def __init__(self):
        self.com = None
        self.interface_lines = []
        self.window = tkinter.Tk()
        self.port = 'COM2'
        self.data = []
        self.cansel = False
        self.check = False

    # Функции кнопок
    def __click(self, commande, code):
        try:
            self.com.write(code)
            self.screen.config(text="Команда '{}' отправлена на {}".format(commande, self.com.port))
        except serial.SerialException:
            self.screen.config(text='Не удается соедениться с ' + self.com.port)
        except (NameError, AttributeError):
            self.screen.config(text='Ошибка {}: Нет подключения'.format(self.port))

    # Блок кнопок РЕЖИМ функции
    def mode_ust_click(self):
        text = 'УСТ'
        self.__click(commande=text, code=b'0x23')

    def mode_du_click(self):
        text = 'ДУ'
        self.__click(commande=text, code=b'0x24')

    def mode_20w_click(self):
        text = '20W'
        self.__click(commande=text, code=b'0x25')

    def mode_write_click(self):
        text = 'ЗАПИСЬ'
        self.__click(commande=text, code=b'0x22')

    def mode_read_click(self):
        text = 'ВЫВОД'
        self.__click(commande=text, code=b'0x21')

    # ВЧ блок кнопок функции
    def high_frequency_click(self):
        text = 'ВЧ ЧАСТ'
        self.__click(commande=text, code=b'0x26')

    def high_chm_click(self):
        text = 'ВЧ ЧМ'
        self.__click(commande=text, code=b'0x27')

    def high_dop1_click(self):
        self.screen.config(text='Кнопка не активна')

    def high_pow_click(self):
        text = 'МОЩН'
        self.__click(commande=text, code=b'0x29')

    def high_chm_off_click(self):
        text = 'ВЧ ЧМ ОТКЛ'
        self.__click(commande=text, code=b'0x30')

    # НЧ блок кнопок функции
    def low_frequency_click(self):
        text = 'НЧ ЧАСТ'
        self.__click(commande=text, code=b'0x31')

    def low_kg_click(self):
        text = 'НЧ КГ'
        self.__click(commande=text, code=b'0x32')

    def low_dop2_click(self):
        text = 'НЧ ДОП2'
        self.__click(commande=text, code=b'0x33')

    def low_voltage_click(self):
        text = 'НЧ НАПР'
        self.__click(commande=text, code=b'0x34')

    def low_chm_ext_click(self):
        text = 'НЧ ЧМ ВНЕШН'
        self.__click(commande=text, code=b'0x35')

    # Блок стрелок ИЗМЕНЕНИЕ
    def button_up_click(self):
        text = 'ВВЕРХ'
        self.__click(commande=text, code=b'0x16')

    def button_down_click(self):
        text = 'ВНИЗ'
        self.__click(commande=text, code=b'0x17')

    def button_left_click(self):
        text = 'ВЛЕВО'
        self.__click(commande=text, code=b'0x18')

    def button_right_click(self):
        text = 'ВПРАВО'
        self.__click(commande=text, code=b'0x19')

    def disconnect_button_click(self):
        text = 'ОТКЛ'
        self.__click(commande=text, code=b'0x20')

    def input_button_click(self):
        text = 'ВВОД'
        self.__click(commande=text, code=b'0x15')

    # Цифровая клавиатура функции
    def button_1_click(self):
        text = '1'
        self.__click(commande=text, code=b'0x01')

    def button_2_click(self):
        text = '2'
        self.__click(commande=text, code=b'0x02')

    def button_3_click(self):
        text = '3'
        self.__click(commande=text, code=b'0x03')

    def button_4_click(self):
        text = '4'
        self.__click(commande=text, code=b'0x04')

    def button_5_click(self):
        text = '5'
        self.__click(commande=text, code=b'0x05')

    def button_6_click(self):
        text = '6'
        self.__click(commande=text, code=b'0x06')

    def button_7_click(self):
        text = '7'
        self.__click(commande=text, code=b'0x07')

    def button_8_click(self):
        text = '8'
        self.__click(commande=text, code=b'0x08')

    def button_9_click(self):
        text = '9'
        self.__click(commande=text, code=b'0x09')

    def button_0_click(self):
        text = '0'
        self.__click(commande=text, code=b'0x00')

    def button_point_click(self):
        text = '.'
        self.__click(commande=text, code=b'0x10')

    def button_line_click(self):
        text = '-'
        self.__click(commande=text, code=b'0x11')

    # множетели
    def button_MHz_click(self):
        text = 'V/MHz'
        self.__click(commande=text, code=b'0x12')

    def button_kHz_click(self):
        text = 'mV/kHz'
        self.__click(commande=text, code=b'0x13')

    def button_Hz_click(self):
        text = 'uV/Hz'
        self.__click(commande=text, code=b'0x14')

    # Функция ввода частоты с клавиатуры
    def get_frequency_button_click(self, event=None):
        frequency = self.get_frequency.get()
        error_message = 'Введите корректную частоту (например 151.825 или 151825)'

        if len(frequency) == 6:
            frequency = frequency[:3] + '.' + frequency[3:]
        if len(frequency) == 7:
            for num in frequency:
                if num == '1':
                    self.button_1_click()
                elif num == '2':
                    self.button_2_click()
                elif num == '3':
                    self.button_3_click()
                elif num == '4':
                    self.button_4_click()
                elif num == '5':
                    self.button_5_click()
                elif num == '6':
                    self.button_6_click()
                elif num == '7':
                    self.button_7_click()
                elif num == '8':
                    self.button_8_click()
                elif num == '9':
                    self.button_9_click()
                elif num == '0':
                    self.button_0_click()
                elif num == '.' or num == ',':
                    self.button_point_click()
        else:
            self.screen.config(text=error_message)
            return
        self.button_MHz_click()
        self.screen.config(text='Частота {} установлена на приборе'.format(frequency))

    def init_interface(self):
        # Главный экран
        self.window.title('К2-82 Alpha-test')
        self.window.minsize(width=1330, height=770)

        # Фрейм прибора
        frame = tkinter.Frame(self.window, borderwidth=2, relief='groove', bg=COLOR)
        frame.place(x=10, y=10, width=1310, height=390)
        down_frame = tkinter.Frame(self.window, borderwidth=3, relief='groove', bg='snow3')
        down_frame.place(x=180, y=435, width=1100, height=300)

        self.print_inscription(text='Перед началом работы не забудь нажать ДУ на приборe НА...',
                               x=70, y=20, width=400, height=20)
        self.print_inscription(text='РЕЖИМ', x=65, y=190, width=160, height=15)
        self.print_inscription(text='ВЧ', x=340, y=190, width=160, height=15)
        self.print_inscription(text='НЧ', x=630, y=190, width=160, height=15)
        self.print_inscription(text='ИЗМЕНЕНИЕ', x=1030, y=190, width=160, height=15)

        # Линии на приборе
        horizontal_width = 1306
        horizontal_height = 5
        for _ in range(6):
            self.interface_lines.append(tkinter.Label(self.window, bg='snow3'))
        self.interface_lines[0].place(x=270, y=180, width=horizontal_height, height=217)
        self.interface_lines[1].place(x=560, y=180, width=horizontal_height, height=217)
        self.interface_lines[2].place(x=840, y=12, width=horizontal_height, height=386)
        self.interface_lines[3].place(x=12, y=180, width=horizontal_width, height=horizontal_height)
        self.interface_lines[4].place(x=12, y=210, width=horizontal_width, height=horizontal_height)
        self.interface_lines[5].place(x=12, y=380, width=horizontal_width, height=horizontal_height)

    # Надписи
    def print_inscription(self, text, x, y, width, height, color=COLOR):
        inscription = tkinter.Label(self.window, text=text, bg=color)
        inscription.place(x=x, y=y, width=width, height=height)

    # Функции выбора COM порта в верхнем меню
    def menu_com1_choice(self):
        try:
            self.com = serial.Serial('COM1', 9600, timeout=1)
            self.screen.config(text='Соединение с COM1 установлено')
            self.port = 'COM1'
        except serial.SerialException:
            self.screen.config(text='Не удается соедениться с COM1')

    def menu_com2_choice(self):
        try:
            self.com = serial.Serial('COM2', 9600, timeout=1)
            self.screen.config(text='Соединение с COM2 установлено')
            self.port = 'COM2'
        except serial.SerialException:
            self.screen.config(text='Не удается соедениться с COM2')

    def menu_com3_choice(self):
        try:
            self.com = serial.Serial('COM3', 9600, timeout=1)
            self.screen.config(text='Соединение с COM3 установлено')
            self.port = 'COM3'
        except serial.SerialException:
            self.screen.config(text='Не удается соедениться с COM3')

    # Верхнее меню
    def init_top_menu(self):
        menu_item = tkinter.Menu(self.window)
        self.window.config(menu=menu_item)
        file_menu = tkinter.Menu(menu_item, tearoff=0)
        settings_menu = tkinter.Menu(menu_item, tearoff=0)
        help_menu = tkinter.Menu(menu_item, tearoff=0)
        menu_item.add_cascade(label='Файл', menu=file_menu)
        menu_item.add_cascade(label='Настройки', menu=settings_menu)
        menu_item.add_cascade(label='Справка', menu=help_menu)
        file_menu.add_command(label='Открыть')
        file_menu.add_command(label='Сохранить')
        com_port_menu = tkinter.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label='COM port', menu=com_port_menu)
        com_port_menu.add_command(label='COM1', command=self.menu_com1_choice)
        com_port_menu.add_command(label='COM2', command=self.menu_com2_choice)
        com_port_menu.add_command(label='COM3', command=self.menu_com3_choice)

    def init_buttons(self):
        button_width = 80
        button_height = 30
        x = 50
        y = 230

        # Первый блок РЕЖИМ
        mode_ust = tkinter.Button(self.window, text='УСТ', command=self.mode_ust_click)
        mode_ust.place(x=x, y=y, width=button_width, height=button_height)
        mode_du = tkinter.Button(self.window, text='ДУ', command=self.mode_du_click)
        mode_du.place(x=x, y=y + 45, width=button_width, height=button_height)
        mode_20w = tkinter.Button(self.window, text='20 W', command=self.mode_20w_click)
        mode_20w.place(x=x, y=y + 45 * 2, width=button_width, height=button_height)
        mode_write = tkinter.Button(self.window, text='ЗАПИСЬ', command=self.mode_write_click)
        mode_write.place(x=x + 110, y=y, width=button_width, height=button_height)
        mode_read = tkinter.Button(self.window, text='ВЫВОД', command=self.mode_read_click)
        mode_read.place(x=x + 110, y=y + 45, width=button_width, height=button_height)

        # Второй блок ВЧ
        high_frequency = tkinter.Button(self.window, text='ЧАСТ', command=self.high_frequency_click)
        high_frequency.place(x=x + 270, y=y, width=button_width, height=button_height)
        high_chm = tkinter.Button(self.window, text='ЧМ', command=self.high_chm_click)
        high_chm.place(x=x + 270, y=y + 45, width=button_width, height=button_height)
        high_dop1 = tkinter.Button(self.window, text='ДОП 1', command=self.high_dop1_click)
        high_dop1.place(x=x + 270, y=y + 45 * 2, width=button_width, height=button_height)
        high_pow = tkinter.Button(self.window, text='МОЩН', command=self.high_pow_click)
        high_pow.place(x=x + 390, y=y, width=button_width, height=button_height)
        high_chm_off = tkinter.Button(self.window, text='ЧМ ОТКЛ', command=self.high_chm_off_click)
        high_chm_off.place(x=x + 390, y=y + 45, width=button_width, height=button_height)

        # Третий блок НЧ
        low_frequency = tkinter.Button(self.window, text='ЧАСТ', command=self.low_frequency_click)
        low_frequency.place(x=x + 560, y=y, width=button_width, height=button_height)
        low_kg = tkinter.Button(self.window, text='КГ', command=self.low_kg_click)
        low_kg.place(x=x + 560, y=y + 45, width=button_width, height=button_height)
        low_dop2 = tkinter.Button(self.window, text='ДОП 2', command=self.low_dop2_click)
        low_dop2.place(x=x + 560, y=y + 45 * 2, width=button_width, height=button_height)
        low_voltage = tkinter.Button(self.window, text='НАПР', command=self.low_voltage_click)
        low_voltage.place(x=x + 670, y=y, width=button_width, height=button_height)
        low_chm_ext = tkinter.Button(self.window, text='ЧМ ВНЕШ', command=self.low_chm_ext_click)
        low_chm_ext.place(x=x + 670, y=y + 45, width=button_width, height=button_height)

        # стрелки ИЗМЕНЕНИЕ
        button_up = tkinter.Button(self.window, text='вверх', command=self.button_up_click)
        button_up.place(x=x + 930, y=y, width=button_width, height=button_height)
        button_left = tkinter.Button(self.window, text='влево', command=self.button_left_click)
        button_left.place(x=x + 840, y=y + 45, width=button_width, height=button_height)
        button_down = tkinter.Button(self.window, text='вниз', command=self.button_down_click)
        button_down.place(x=x + 930, y=y + 45 * 2, width=button_width, height=button_height)
        button_right = tkinter.Button(self.window, text='вправо', command=self.button_right_click)
        button_right.place(x=x + 1020, y=y + 45, width=button_width, height=button_height)
        input_button = tkinter.Button(self.window, text='ВВОД', command=self.input_button_click)
        input_button.place(x=x + 1150, y=y, width=button_width, height=button_height)
        disconnect_button = tkinter.Button(self.window, text='ОТКЛ', command=self.disconnect_button_click)
        disconnect_button.place(x=x + 1150, y=y + 45 * 2, width=button_width, height=button_height)

        # Цифровая клавиатура
        button_1 = tkinter.Button(self.window, text='1', command=self.button_1_click)
        button_1.place(x=x + 1150, y=y - 50 * 2, width=button_width, height=button_height)
        button_5 = tkinter.Button(self.window, text='5', command=self.button_5_click)
        button_5.place(x=x + 1150, y=y - 50 * 3, width=button_width, height=button_height)
        button_9 = tkinter.Button(self.window, text='9', command=self.button_9_click)
        button_9.place(x=x + 1150, y=y - 50 * 4, width=button_width, height=button_height)
        button_0 = tkinter.Button(self.window, text='0', command=self.button_0_click)
        button_0.place(x=x + 1040, y=y - 50 * 2, width=button_width, height=button_height)
        button_4 = tkinter.Button(self.window, text='4', command=self.button_4_click)
        button_4.place(x=x + 1040, y=y - 50 * 3, width=button_width, height=button_height)
        button_8 = tkinter.Button(self.window, text='8', command=self.button_8_click)
        button_8.place(x=x + 1040, y=y - 50 * 4, width=button_width, height=button_height)
        button_point = tkinter.Button(self.window, text=',', command=self.button_point_click)
        button_point.place(x=x + 930, y=y - 50 * 2, width=button_width, height=button_height)
        button_3 = tkinter.Button(self.window, text='3', command=self.button_3_click)
        button_3.place(x=x + 930, y=y - 50 * 3, width=button_width, height=button_height)
        button_7 = tkinter.Button(self.window, text='7', command=self.button_7_click)
        button_7.place(x=x + 930, y=y - 50 * 4, width=button_width, height=button_height)
        button_line = tkinter.Button(self.window, text='-', command=self.button_line_click)
        button_line.place(x=x + 820, y=y - 50 * 2, width=button_width, height=button_height)
        button_2 = tkinter.Button(self.window, text='2', command=self.button_2_click)
        button_2.place(x=x + 820, y=y - 50 * 3, width=button_width, height=button_height)
        button_6 = tkinter.Button(self.window, text='6', command=self.button_6_click)
        button_6.place(x=x + 820, y=y - 50 * 4, width=button_width, height=button_height)

        # Множетели частот и напряжения Мега/Кило/Герцы и Милли/Микро/Вольты
        button_MHz = tkinter.Button(self.window, text='V/MHz', command=self.button_MHz_click)
        button_MHz.place(x=x + 670, y=y - 50 * 4, width=button_width, height=button_height)
        button_kHz = tkinter.Button(self.window, text='mV/kHz', command=self.button_kHz_click)
        button_kHz.place(x=x + 670, y=y - 50 * 3, width=button_width, height=button_height)
        button_Hz = tkinter.Button(self.window, text='uV/Hz', command=self.button_Hz_click)
        button_Hz.place(x=x + 670, y=y - 50 * 2, width=button_width, height=button_height)

        # Нижнее меню
        check_transmitter = tkinter.Button(self.window, text='Проверка передатчика',
                                           command=self.check_transmitter_click)
        check_transmitter.place(x=20, y=435, width=140, height=button_height)
        button_cansel = tkinter.Button(self.window, text='Esc - Отмена', command=self.button_cansel_click)
        button_cansel.place(x=20, y=480, width=140, height=button_height)
        button_cansel.bind('<Button-1>', self.button_cansel_click)
        label_f = tkinter.Label(self.window, text='f:')
        label_f.place(x=20, y=525, width=20, height=button_height)
        self.get_frequency = tkinter.Entry(self.window, bd=2)
        self.get_frequency.place(x=40, y=525, width=120, height=30)
        self.get_frequency.bind('<Return>', self.get_frequency_button_click)
        get_frequency_button = tkinter.Button(self.window, text='Установить частоту',
                                              command=self.get_frequency_button_click)
        get_frequency_button.place(x=20, y=565, width=140, height=button_height)
        check_transmitter = tkinter.Button(self.window, text='Проверка приемника',
                                           command=self.low_dop2_click)
        check_transmitter.place(x=20, y=610, width=140, height=button_height)

    def init_screen(self):
        # Экранчик
        self.screen_frame = tkinter.Frame(self.window, bd=4, relief='groove', bg=COLOR)
        self.screen_frame.place(x=69, y=49, width=552, height=87)
        self.screen = tkinter.Label(bg='seagreen')
        self.screen.place(x=70, y=50, width=550, height=85)

    # Автоматическая проверка приёмника
    def check_transmitter_click(self):
        self.screen.config(text='Идет проверка приемника')
        functions = [self.high_frequency_click, self.disconnect_button_click, self.high_pow_click,
                     self.disconnect_button_click, self.low_dop2_click, self.input_button_click,
                     self.button_9_click, self.button_point_click, self.button_5_click, self.button_kHz_click,
                     self.disconnect_button_click, self.button_down_click, self.input_button_click,
                     self.disconnect_button_click, self.button_down_click, self.input_button_click,
                     self.disconnect_button_click, self.button_down_click, self.button_0_click,
                     self.button_point_click, self.button_3_click, self.button_Hz_click, self.high_chm_click,
                     self.button_3_click, self.button_kHz_click, self.button_down_click, self.button_1_click,
                     self.button_kHz_click]
        timeout_02_functions = [1, 3, 4, 5, 6, 7, 8, 10, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

        for step, function in enumerate(functions):
            if self.cansel:
                return
            if step == 11:
                for _ in range(2):
                    function()
                    time.sleep(0.2)
            elif step == 16:
                for _ in range(2):
                    function()
                    time.sleep(0.2)

            function()

            if step in [0, 2, 9]:
                time.sleep(5)
                self.data.append(self.com.readline())
            elif step in timeout_02_functions:
                 time.sleep(0.2)
            elif step == 12:
                time.sleep(10)
                self.data.append(self.com.readline())
            elif step == 15:
                time.sleep(35)
                self.data.append(self.com.readline())

        self.screen.config(text='Проверка завершена')

    def button_cansel_click(self, event=None):
        self.cansel = True

    def init_window(self):
        # Соединение с COM портом
        try:
            self.com = serial.Serial(self.port, 9600, timeout=1)
        except serial.SerialException:
            self.com = None

        self.init_top_menu()
        self.init_interface()
        self.init_buttons()
        self.init_screen()




# Инициализация интерфейса
k2 = Window()
k2.init_window()

k2.window.mainloop()