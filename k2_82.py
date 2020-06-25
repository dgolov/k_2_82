# -*- coding: utf-8 -*-
# pyinstaller -F -w k2_82.py
# C:\Users\User\PycharmProjects\k_2_82\k2_82.py

import tkinter, serial, time
from uu import decode, encode

COLOR = 'cornflowerblue'


class Window:
    def __init__(self, com):
        self.com = com
        self.interface_lines = []
        self.window = tkinter.Tk()

    # Функции кнопок
    def __click(self, code):
        try:
            com.write(code)
            self.screen.config(text='Команда отправлена на ' + self.com.port)
        except serial.SerialException:
            self.screen.config(text='Не удается соедениться с ' + self.com.port)
        except (NameError, AttributeError):
            self.screen.config(text='Ошибка COM Port: Нет подключения')

    # Блок кнопок РЕЖИМ функции
    def mode_ust_click(self):
        self.__click(b'0x23')

    def mode_du_click(self):
        self.__click(b'0x24')

    def mode_20w_click(self):
        self.__click(b'0x25')

    def mode_write_click(self):
        self.__click(b'0x22')

    def mode_read_click(self):
        self.__click(b'0x21')

    # ВЧ блок кнопок функции
    def high_frequency_click(self):
        self.__click(b'0x26')

    def high_chm_click(self):
        self.__click(b'0x27')

    def high_dop1_click(self):
        self.screen.config(text='Кнопка не активна')

    def high_pow_click(self):
        self.__click(b'0x29')

    def high_chm_off_click(self):
        self.__click(b'0x30')

    # НЧ блок кнопок функции
    def low_frequency_click(self):
        self.__click(b'0x31')

    def low_kg_click(self):
        self.__click(b'0x32')

    def low_dop2_click(self):
        self.__click(b'0x33')

    def low_voltage_click(self):
        self.__click(b'0x34')

    def low_chm_ext_click(self):
        self.__click(b'0x35')

    # Блок стрелок ИЗМЕНЕНИЕ
    def button_up_click(self):
        self.__click(b'0x16')

    def button_down_click(self):
        self.__click(b'0x17')

    def button_left_click(self):
        self.__click(b'0x18')

    def button_right_click(self):
        self.__click(b'0x19')

    def disconnect_button_click(self):
        self.__click(b'0x20')

    def input_button_click(self):
        self.__click(b'0x15')

    # Цифровая клавиатура функции
    def button_1_click(self):
        self.__click(b'0x01')

    def button_2_click(self):
        self.__click(b'0x02')

    def button_3_click(self):
        self.__click(b'0x03')

    def button_4_click(self):
        self.__click(b'0x04')

    def button_5_click(self):
        self.__click(b'0x05')

    def button_6_click(self):
        self.__click(b'0x06')

    def button_7_click(self):
        self.__click(b'0x07')

    def button_8_click(self):
        self.__click(b'0x08')

    def button_9_click(self):
        self.__click(b'0x09')

    def button_0_click(self):
        self.__click(b'0x00')

    def button_point_click(self):
        self.__click(b'0x10')

    def button_line_click(self):
        self.__click(b'0x11')

    # множетели
    def button_MHz_click(self):
        self.__click(b'0x12')

    def button_kHz_click(self):
        self.__click(b'0x13')

    def button_Hz_click(self):
        self.__click(b'0x14')


    def init_interface(self):
        # Главный экран
        self.window.title('К2-82 версия пиздец')
        self.window.minsize(width=1330, height=780)

        # Фрейм прибора
        frame = tkinter.Frame(self.window, borderwidth=2, relief='groove', bg=COLOR)
        frame.place(x=10, y=10, width=1310, height=390)

        # Линии на приборе
        horizontal_width = 1306
        horizontal_height = 5
        for _ in range(6):
            self.interface_lines.append(tkinter.Label(self.window))
        self.interface_lines[0].place(x=270, y=180, width=horizontal_height, height=217)
        self.interface_lines[1].place(x=560, y=180, width=horizontal_height, height=217)
        self.interface_lines[2].place(x=840, y=12, width=horizontal_height, height=386)
        self.interface_lines[3].place(x=12, y=180, width=horizontal_width, height=horizontal_height)
        self.interface_lines[4].place(x=12, y=210, width=horizontal_width, height=horizontal_height)
        self.interface_lines[5].place(x=12, y=380, width=horizontal_width, height=horizontal_height)

    def print_inscription(self, text, x, y, width, height, color=COLOR):
        # Надписи
        inscription = tkinter.Label(self.window, text=text, bg=color)
        inscription.place(x=x, y=y, width=width, height=height)

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

    def init_screen(self):
        # Экранчик
        self.screen_frame = tkinter.Frame(self.window, borderwidth=2, relief='groove', bg=COLOR)
        self.screen_frame.place(x=69, y=49, width=552, height=87)
        self.screen = tkinter.Label(bg='seagreen')
        self.screen.place(x=70, y=50, width=550, height=85)

    def init_window(self):
        self.init_interface()
        self.init_buttons()
        self.init_screen()
        self.print_inscription(text='Тест сигнала на К2-82 Не забудь нажать ДУ на приборe НА...',
                               x=70, y=20, width=400, height=20)
        self.print_inscription(text='РЕЖИМ', x=65, y=190, width=160, height=15)
        self.print_inscription(text='ВЧ', x=340, y=190, width=160, height=15)
        self.print_inscription(text='НЧ', x=630, y=190, width=160, height=15)
        self.print_inscription(text='ИЗМЕНЕНИЕ', x=1030, y=190, width=160, height=15)
        self.window.mainloop()


# Соединение с COM портом
try:
    com = serial.Serial('COM1', 9600, timeout=1)
except serial.SerialException:
    com = None

window = Window(com)
window.init_window()
