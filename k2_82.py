# -*- coding: utf-8 -*-

import tkinter
from tkinter import messagebox
import check, k2_functional
from tkinter import filedialog


COLOR = 'cornflowerblue'


# Блок кнопок РЕЖИМ функции
def mode_ust_click():
    text = 'УСТ'
    result = functional.send_code(commande=text, code=b'0x23')
    screen.config(text=result)

def mode_du_click():
    text = 'ДУ'
    result = functional.send_code(commande=text, code=b'0x24')
    screen.config(text=result)

def mode_20w_click():
    text = '20W'
    result = functional.send_code(commande=text, code=b'0x25')
    screen.config(text=result)

def mode_write_click():
    text = 'ЗАПИСЬ'
    result = functional.send_code(commande=text, code=b'0x22')
    screen.config(text=result)

def mode_read_click():
    text = 'ВЫВОД'
    result = functional.send_code(commande=text, code=b'0x21')
    screen.config(text=result)


# ВЧ блок кнопок функции
def high_frequency_click():
    text = 'ВЧ ЧАСТ'
    result = functional.send_code(commande=text, code=b'0x26')
    screen.config(text=result)

def high_chm_click():
    text = 'ВЧ ЧМ'
    result = functional.send_code(commande=text, code=b'0x27')
    screen.config(text=result)

def high_dop1_click():
    screen.config(text='Кнопка не активна')

def high_pow_click():
    text = 'МОЩН'
    result = functional.send_code(commande=text, code=b'0x29')
    screen.config(text=result)

def high_chm_off_click():
    text = 'ВЧ ЧМ ОТКЛ'
    result = functional.send_code(commande=text, code=b'0x30')
    screen.config(text=result)


# НЧ блок кнопок функции
def low_frequency_click():
    text = 'НЧ ЧАСТ'
    result = functional.send_code(commande=text, code=b'0x31')
    screen.config(text=result)

def low_kg_click():
    text = 'НЧ КГ'
    result = functional.send_code(commande=text, code=b'0x32')
    screen.config(text=result)

def low_dop2_click():
    text = 'НЧ ДОП2'
    result = functional.send_code(commande=text, code=b'0x33')
    screen.config(text=result)

def low_voltage_click():
    text = 'НЧ НАПР'
    result = functional.send_code(commande=text, code=b'0x34')
    screen.config(text=result)

def low_chm_ext_click():
    text = 'НЧ ЧМ ВНЕШН'
    result = functional.send_code(commande=text, code=b'0x35')
    screen.config(text=result)


# Блок стрелок ИЗМЕНЕНИЕ
def button_up_click():
    text = 'ВВЕРХ'
    result = functional.send_code(commande=text, code=b'0x16')
    screen.config(text=result)

def button_down_click():
    text = 'ВНИЗ'
    result = functional.send_code(commande=text, code=b'0x17')
    screen.config(text=result)

def button_left_click():
    text = 'ВЛЕВО'
    result = functional.send_code(commande=text, code=b'0x18')
    screen.config(text=result)

def button_right_click():
    text = 'ВПРАВО'
    result = functional.send_code(commande=text, code=b'0x19')
    screen.config(text=result)

def disconnect_button_click():
    text = 'ОТКЛ'
    result = functional.send_code(commande=text, code=b'0x20')
    screen.config(text=result)

def input_button_click():
    text = 'ВВОД'
    result = functional.send_code(commande=text, code=b'0x15')
    screen.config(text=result)


# Цифровая клавиатура функции
def button_1_click():
    text = '1'
    result = functional.send_code(commande=text, code=b'0x01')
    screen.config(text=result)

def button_2_click():
    text = '2'
    result = functional.send_code(commande=text, code=b'0x02')
    screen.config(text=result)

def button_3_click():
    text = '3'
    result = functional.send_code(commande=text, code=b'0x03')
    screen.config(text=result)

def button_4_click():
    text = '4'
    result = functional.send_code(commande=text, code=b'0x04')
    screen.config(text=result)

def button_5_click():
    text = '5'
    result = functional.send_code(commande=text, code=b'0x05')
    screen.config(text=result)

def button_6_click():
    text = '6'
    result = functional.send_code(commande=text, code=b'0x06')
    screen.config(text=result)

def button_7_click():
    text = '7'
    result = functional.send_code(commande=text, code=b'0x07')
    screen.config(text=result)

def button_8_click():
    text = '8'
    result = functional.send_code(commande=text, code=b'0x08')
    screen.config(text=result)

def button_9_click():
    text = '9'
    result = functional.send_code(commande=text, code=b'0x09')
    screen.config(text=result)

def button_0_click():
    text = '0'
    result = functional.send_code(commande=text, code=b'0x00')
    screen.config(text=result)

def button_point_click():
    text = '.'
    result = functional.send_code(commande=text, code=b'0x10')
    screen.config(text=result)

def button_line_click():
    text = '-'
    result = functional.send_code(commande=text, code=b'0x11')
    screen.config(text=result)


# Множетели
def button_MHz_click():
    text = 'V/MHz'
    result = functional.send_code(commande=text, code=b'0x12')
    screen.config(text=result)

def button_kHz_click():
    text = 'mV/kHz'
    result = functional.send_code(commande=text, code=b'0x13')
    screen.config(text=result)

def button_Hz_click():
    text = 'uV/Hz'
    result = functional.send_code(commande=text, code=b'0x14')
    screen.config(text=result)


# Нижнее меню
def set_model_motorola():
    """ Выбор модели радиостанции """
    functional.model = 'Motorola'
    print_inscription(text='Модель - {}'.format(functional.model), bg_color = 'gray95',
                      text_color = 'blue4', x=310, y=410, width=110, height=20)

def set_model_altavia():
    """ Выбор модели радиостанции """
    functional.model = 'Альтавия'
    print_inscription(text='Модель - {}'.format(functional.model), bg_color = 'gray95',
                      text_color = 'blue4', x=310, y=410, width=110, height=20)

def set_model_icom():
    """ Выбор модели радиостанции """
    functional.model = 'Icom'
    print_inscription(text='Модель - {}      '.format(functional.model), bg_color = 'gray95',
                      text_color = 'blue4', x=310, y=410, width=110, height=20)

def check_rs_button_click():
    """ Кнопка запуска цикла проверки радиостанции """
    global param_y

    try:
        new_check = check.Check(functional, window, screen)
        new_check.run()
        if functional.cancel:
            functional.cancel = False
            screen.config(text='Проверка отменена')
            return
        param_y += 20

        print_inscription(text=new_check.f, x=190, y=param_y, width=100, height=20,
                          bg_color='snow3', justify=tkinter.LEFT)
        color = 'red' if new_check.p < 2 else '#000000'
        print_inscription(text=new_check.p, x=280, y=param_y, width=80, height=20,
                              bg_color='snow3', text_color = color, justify=tkinter.LEFT)
        if functional.model == 'Motorola':
            color = 'red' if new_check.dev > 300 else '#000000'
        else:
            color = 'red' if new_check.dev > 600 else '#000000'
        print_inscription(text=new_check.dev, x=350, y=param_y, width=100, height=20,
                          bg_color='snow3', text_color = color, justify=tkinter.LEFT)
        color = 'red' if new_check.kg > 3 else '#000000'
        print_inscription(text=new_check.kg, x=435, y=param_y, width=70, height=20,
                          bg_color='snow3', text_color = color, justify=tkinter.LEFT)
        color = 'red' if new_check.chm_u > 20 else '#000000'
        print_inscription(text=new_check.chm_u, x=495, y=param_y, width=70, height=20,
                          bg_color='snow3', text_color = color, justify=tkinter.LEFT)
        color = 'red' if new_check.chm_max > 5 else '#000000'
        print_inscription(text=new_check.chm_max, x=575, y=param_y, width=150, height=20,
                          bg_color='snow3', text_color = color, justify=tkinter.LEFT)
        if functional.model != 'Альтавия':
            color = 'red' if new_check.out_pow < 2 else '#000000'
        else: color = '#000000'
        print_inscription(text=new_check.out_pow, x=725, y=param_y, width=150, height=30,
                          bg_color='snow3', text_color = color, justify=tkinter.LEFT)
        color = 'red' if new_check.out_kg > 5 else '#000000'
        print_inscription(text=new_check.out_kg, x=875, y=param_y, width=70, height=30,
                          bg_color='snow3', text_color = color, justify=tkinter.LEFT)
    except AttributeError:
        screen.config(text='Не удается соедениться с {}'.format(functional.port))

def button_cancel_click():
    """ Кнопка отмены цикла проверки """
    if functional.check:
        functional.cancel = True

def get_frequency_button_click(event=None):
    """ Кнопка установки частоты на К2-82 """
    try:
        frequency = get_frequency.get()
        screen.config(text=functional.input_frequency(frequency))
    except AttributeError:
        screen.config(text='Не удается соедениться с {}'.format(functional.port))

def deviation_flag_click():
    """ Флаг пропуска девиации """
    if off_deviation_flag.get():
        functional.check_deviation_time = 0
    else:
        functional.check_deviation_time = 33


# Функции в верхнем меню
def get_com_connect_info():
    """ Получение информации о состоянии подключения COM порта """
    connect = functional.connect_com_port(functional.COM)
    if connect:
        text = 'Соединение с {} установлено'.format(functional.COM)
        color = 'blue4'
    else:
        text = 'Не удается соедениться с {}'.format(functional.COM)
        color = 'red'
    screen.config(text=text)
    print_inscription(text='COM порт - {}'.format(functional.port), bg_color='gray95',
                      text_color=color, x=190, y=410, width=100, height=20)

def menu_com1_choice():
    """ Подключение к COM 1 """
    functional.COM = 'COM1'
    get_com_connect_info()

def menu_com2_choice():
    """ Подключение к COM 2 """
    functional.COM = 'COM2'
    get_com_connect_info()

def menu_com3_choice():
    """ Подключение к COM 3 """
    functional.COM = 'COM3'
    get_com_connect_info()

def save_file():
    """ Сохранение параметров в файл Excel """
    name = filedialog.asksaveasfilename(filetypes=(('Excel', '*.xls'), ('Все файлы','*.*')))
    if name != '':
        functional.excel_book.save_book(name)

def show_info():
    """Меню справка - о программе"""
    messagebox.showinfo('О программе',
'''v 0.2.1 dev

- Добавлена  возможность  выбора  модели радиостанции.
(Нужно для  подставления  конкретных значений во время
измерения  чувствительности  модуляционного входа, тем
самым  ускоряя  процесс  проведения  цикла технического
обслуживания)

- Добавлено   отображение  состояния   COM  порта  (если
ошибка  подключения,  то  текст подсвечивается  красным
цветом) и отображение выбранной модели радиостанции
(по умолчанию - Motorola)

- Корректно считывает чувствительность  модуляционного
входа

- Считывает  правильные значения  выходной мощности и
КНИ  приемника  с   К2-82.   (Бывает  скачок  на  приборе  и
программа  могла  считать  некорректные значения после
этого скачка)

- Параметры  неудовлетворяющие  норме  подсвечиваются
красным цветом

-------------------------------------------------------------------------------

Для запуска  цикла проверки  радиостанции:
    - Деактивировать все кнопки на приборе
    - Активировать  кнопку   ДУ на приборе
    - Нажать  "Проверка  параметров"
    - Следовать дальнейшим инструкциям

После завершения цикла проверки необходимо измерить
чувствительность   приёмника      и    порог  срабатывания
шумоподавителя.

Для  ускорения   цикла   проверки   активировать  пропуск
девиации.  Для  быстрой  усановки  частоты с  компьютера
ввести частоту в поле f:
(например   151825   151.825   151,825)    и   нажать   кнопку
"Установить    частоту".    Для   корректной   установки,   на
приборе   должно  быть  активно   меню   редактирования
сигнала    (либо     включены   кнопки   УСТ    и    ДУ,    либо
отключены все кнопки кроме ДУ)

Все кнопки в программе соответствуют кнопкам К2-82.

-------------------------------------------------------------------------------


                                                    Разработчик Голов Д.Е. ©
                                                    ООО  "Телеком - Сервис"
'''
)


def init_interface():
    """ Инициализация основного интерфейса программы """
    frame = tkinter.Frame(window, borderwidth=2, relief='groove', bg=COLOR)
    frame.place(x=10, y=10, width=1310, height=390)
    down_frame = tkinter.Frame(window, borderwidth=3, relief='groove', bg='snow3')
    down_frame.place(x=180, y=435, width=1100, height=300)

    print_inscription(text='Перед началом работы не забудь нажать ДУ на приборe (Остальные кнопки должны быть неактивны)',
                           x=55, y=20, width=600, height=20)
    print_inscription(text='РЕЖИМ', x=65, y=190, width=160, height=15)
    print_inscription(text='ВЧ', x=340, y=190, width=160, height=15)
    print_inscription(text='НЧ', x=630, y=190, width=160, height=15)
    print_inscription(text='ИЗМЕНЕНИЕ', x=1030, y=190, width=160, height=15)

    print_inscription(text='Частота', x=190, y=440, width=100, height=30, bg_color='snow3', justify=tkinter.LEFT)
    print_inscription(text='Мощность', x=280, y=440, width=80, height=30, bg_color='snow3', justify=tkinter.LEFT)
    print_inscription(text='Отклонение', x=350, y=440, width=100, height=30, bg_color='snow3', justify=tkinter.LEFT)
    print_inscription(text='КНИ', x=435, y=440, width=70, height=30, bg_color='snow3', justify=tkinter.LEFT)
    print_inscription(text='ЧМ', x=495, y=440, width=70, height=30, bg_color='snow3', justify=tkinter.LEFT)
    print_inscription(text='Максимальная девиация', x=575, y=440, width=150, height=30,
                      bg_color='snow3', justify=tkinter.LEFT)
    print_inscription(text='Выходная мощьность', x=725, y=440, width=150, height=30,
                      bg_color='snow3', justify=tkinter.LEFT)
    print_inscription(text='КНИ', x=875, y=440, width=70, height=30, bg_color='snow3', justify=tkinter.LEFT)

    # Линии на приборе
    interface_lines = []
    horizontal_width = 1306
    horizontal_height = 5
    for _ in range(6):
        interface_lines.append(tkinter.Label(window, bg='snow3'))
    interface_lines[0].place(x=270, y=180, width=horizontal_height, height=217)
    interface_lines[1].place(x=560, y=180, width=horizontal_height, height=217)
    interface_lines[2].place(x=840, y=12, width=horizontal_height, height=386)
    interface_lines[3].place(x=12, y=180, width=horizontal_width, height=horizontal_height)
    interface_lines[4].place(x=12, y=210, width=horizontal_width, height=horizontal_height)
    interface_lines[5].place(x=12, y=380, width=horizontal_width, height=horizontal_height)


def print_inscription(text, x, y, width, height, bg_color=COLOR, text_color = '#000000', justify=tkinter.CENTER):
    """ Печать текста (результаты проверка, надписи интерфейса, инструкции) """
    inscription = tkinter.Label(window, text=text, bg=bg_color, foreground = text_color, justify=justify)
    inscription.place(x=x, y=y, width=width, height=height)


def init_top_menu():
    """ Инициализация верхнего меню """
    menu_item = tkinter.Menu(window)
    window.config(menu=menu_item)
    file_menu = tkinter.Menu(menu_item, tearoff=0)
    settings_menu = tkinter.Menu(menu_item, tearoff=0)
    help_menu = tkinter.Menu(menu_item, tearoff=0)
    menu_item.add_cascade(label='Файл', menu=file_menu)
    menu_item.add_cascade(label='Настройки', menu=settings_menu)
    menu_item.add_cascade(label='Справка', menu=help_menu)
    file_menu.add_command(label='Открыть')
    file_menu.add_command(label='Сохранить', command=save_file)
    com_port_menu = tkinter.Menu(settings_menu, tearoff=0)
    settings_menu.add_cascade(label='COM port', menu=com_port_menu)
    model_menu = tkinter.Menu(settings_menu, tearoff=0)
    settings_menu.add_cascade(label='Выбор радиостанции', menu=model_menu)
    com_port_menu.add_command(label='COM1', command=menu_com1_choice)
    com_port_menu.add_command(label='COM2', command=menu_com2_choice)
    com_port_menu.add_command(label='COM3', command=menu_com3_choice)
    model_menu.add_command(label='Motorola', command=set_model_motorola)
    model_menu.add_command(label='Альтавия', command=set_model_altavia)
    model_menu.add_command(label='Icom', command=set_model_icom)
    help_menu.add_command(label='О программе', command=show_info)


def init_buttons():
    """ Инициализация кнопок """
    button_width = 80
    button_height = 30
    x = 50
    y = 230

    # Первый блок РЕЖИМ
    mode_ust = tkinter.Button(window, text='УСТ', command=mode_ust_click)
    mode_ust.place(x=x, y=y, width=button_width, height=button_height)
    mode_du = tkinter.Button(window, text='ДУ', command=mode_du_click)
    mode_du.place(x=x, y=y + 45, width=button_width, height=button_height)
    mode_20w = tkinter.Button(window, text='20 W', command=mode_20w_click)
    mode_20w.place(x=x, y=y + 45 * 2, width=button_width, height=button_height)
    mode_write = tkinter.Button(window, text='ЗАПИСЬ', command=mode_write_click)
    mode_write.place(x=x + 110, y=y, width=button_width, height=button_height)
    mode_read = tkinter.Button(window, text='ВЫВОД', command=mode_read_click)
    mode_read.place(x=x + 110, y=y + 45, width=button_width, height=button_height)

    # Второй блок ВЧ
    high_frequency = tkinter.Button(window, text='ЧАСТ', command=high_frequency_click)
    high_frequency.place(x=x + 270, y=y, width=button_width, height=button_height)
    high_chm = tkinter.Button(window, text='ЧМ', command=high_chm_click)
    high_chm.place(x=x + 270, y=y + 45, width=button_width, height=button_height)
    high_dop1 = tkinter.Button(window, text='ДОП 1', command=high_dop1_click)
    high_dop1.place(x=x + 270, y=y + 45 * 2, width=button_width, height=button_height)
    high_pow = tkinter.Button(window, text='МОЩН', command=high_pow_click)
    high_pow.place(x=x + 390, y=y, width=button_width, height=button_height)
    high_chm_off = tkinter.Button(window, text='ЧМ ОТКЛ', command=high_chm_off_click)
    high_chm_off.place(x=x + 390, y=y + 45, width=button_width, height=button_height)

    # Третий блок НЧ
    low_frequency = tkinter.Button(window, text='ЧАСТ', command=low_frequency_click)
    low_frequency.place(x=x + 560, y=y, width=button_width, height=button_height)
    low_kg = tkinter.Button(window, text='КГ', command=low_kg_click)
    low_kg.place(x=x + 560, y=y + 45, width=button_width, height=button_height)
    low_dop2 = tkinter.Button(window, text='ДОП 2', command=low_dop2_click)
    low_dop2.place(x=x + 560, y=y + 45 * 2, width=button_width, height=button_height)
    low_voltage = tkinter.Button(window, text='НАПР', command=low_voltage_click)
    low_voltage.place(x=x + 670, y=y, width=button_width, height=button_height)
    low_chm_ext = tkinter.Button(window, text='ЧМ ВНЕШ', command=low_chm_ext_click)
    low_chm_ext.place(x=x + 670, y=y + 45, width=button_width, height=button_height)

    # стрелки ИЗМЕНЕНИЕ
    button_up = tkinter.Button(window, text='вверх', command=button_up_click)
    button_up.place(x=x + 930, y=y, width=button_width, height=button_height)
    button_left = tkinter.Button(window, text='влево', command=button_left_click)
    button_left.place(x=x + 840, y=y + 45, width=button_width, height=button_height)
    button_down = tkinter.Button(window, text='вниз', command=button_down_click)
    button_down.place(x=x + 930, y=y + 45 * 2, width=button_width, height=button_height)
    button_right = tkinter.Button(window, text='вправо', command=button_right_click)
    button_right.place(x=x + 1020, y=y + 45, width=button_width, height=button_height)
    input_button = tkinter.Button(window, text='ВВОД', command=input_button_click)
    input_button.place(x=x + 1150, y=y, width=button_width, height=button_height)
    disconnect_button = tkinter.Button(window, text='ОТКЛ', command=disconnect_button_click)
    disconnect_button.place(x=x + 1150, y=y + 45 * 2, width=button_width, height=button_height)

    # Цифровая клавиатура
    button_1 = tkinter.Button(window, text='1', command=button_1_click)
    button_1.place(x=x + 1150, y=y - 50 * 2, width=button_width, height=button_height)
    button_5 = tkinter.Button(window, text='5', command=button_5_click)
    button_5.place(x=x + 1150, y=y - 50 * 3, width=button_width, height=button_height)
    button_9 = tkinter.Button(window, text='9', command=button_9_click)
    button_9.place(x=x + 1150, y=y - 50 * 4, width=button_width, height=button_height)
    button_0 = tkinter.Button(window, text='0', command=button_0_click)
    button_0.place(x=x + 1040, y=y - 50 * 2, width=button_width, height=button_height)
    button_4 = tkinter.Button(window, text='4', command=button_4_click)
    button_4.place(x=x + 1040, y=y - 50 * 3, width=button_width, height=button_height)
    button_8 = tkinter.Button(window, text='8', command=button_8_click)
    button_8.place(x=x + 1040, y=y - 50 * 4, width=button_width, height=button_height)
    button_point = tkinter.Button(window, text=',', command=button_point_click)
    button_point.place(x=x + 930, y=y - 50 * 2, width=button_width, height=button_height)
    button_3 = tkinter.Button(window, text='3', command=button_3_click)
    button_3.place(x=x + 930, y=y - 50 * 3, width=button_width, height=button_height)
    button_7 = tkinter.Button(window, text='7', command=button_7_click)
    button_7.place(x=x + 930, y=y - 50 * 4, width=button_width, height=button_height)
    button_line = tkinter.Button(window, text='-', command=button_line_click)
    button_line.place(x=x + 820, y=y - 50 * 2, width=button_width, height=button_height)
    button_2 = tkinter.Button(window, text='2', command=button_2_click)
    button_2.place(x=x + 820, y=y - 50 * 3, width=button_width, height=button_height)
    button_6 = tkinter.Button(window, text='6', command=button_6_click)
    button_6.place(x=x + 820, y=y - 50 * 4, width=button_width, height=button_height)

    # Множетели частот и напряжения Мега/Кило/Герцы и Милли/Микро/Вольты
    button_MHz = tkinter.Button(window, text='V/MHz', command=button_MHz_click)
    button_MHz.place(x=x + 670, y=y - 50 * 4, width=button_width, height=button_height)
    button_kHz = tkinter.Button(window, text='mV/kHz', command=button_kHz_click)
    button_kHz.place(x=x + 670, y=y - 50 * 3, width=button_width, height=button_height)
    button_Hz = tkinter.Button(window, text='uV/Hz', command=button_Hz_click)
    button_Hz.place(x=x + 670, y=y - 50 * 2, width=button_width, height=button_height)

    # Нижнее меню
    model_menu = tkinter.Menubutton(window, text='Выбор радиостанции', borderwidth=2, relief=tkinter.RAISED)
    model_menu.pack()
    model_menu.place(x=20, y=435, width=140, height=button_height)
    model_menu.menu = tkinter.Menu(model_menu, tearoff=0)
    model_menu['menu'] = model_menu.menu
    model_menu.menu.add_command(label='Motorola\t\t\t\t\t\t', command=set_model_motorola)
    model_menu.menu.add_command(label='Альтавия', command=set_model_altavia)
    model_menu.menu.add_command(label='Icom', command=set_model_icom)
    check_rs_button = tkinter.Button(window, text='Проверка параметров',
                                       command=check_rs_button_click)
    check_rs_button.place(x=20, y=475, width=140, height=button_height)
    button_cancel = tkinter.Button(window, text='Отмена', command=button_cancel_click)
    button_cancel.place(x=20, y=520, width=140, height=button_height)
    # button_cancel.bind('<Button-1>', button_cancel_click)
    label_f = tkinter.Label(window, text='f:')
    label_f.place(x=20, y=565, width=20, height=button_height)
    get_frequency.place(x=40, y=565, width=120, height=30)
    get_frequency.bind('<Return>', get_frequency_button_click)
    get_frequency_button = tkinter.Button(window, text='Установить частоту',
                                          command=get_frequency_button_click)
    get_frequency_button.place(x=20, y=605, width=140, height=button_height)
    deviation_flag = tkinter.Checkbutton(window, text='Пропуск девиации', variable=off_deviation_flag,
                                         onvalue=True, offvalue=False, command=deviation_flag_click)
    deviation_flag.place(x=20, y=645, width=140, height=button_height)


if __name__ == '__main__':
    param_y = 440
    functional = k2_functional.K2_functional()
    connect = functional.connect_com_port(functional.COM)

    window = tkinter.Tk()
    window.title('К2-82 v 0.2.1 dev')
    window.minsize(width=1330, height=770)
    get_frequency = tkinter.Entry(window, bd=2)
    off_deviation_flag = tkinter.BooleanVar()

    color = 'blue4' if connect else 'red'
    print_inscription(text='COM порт - {}'.format(functional.port), bg_color='gray95',
                      text_color=color, x=190, y=410, width=100, height=20)
    print_inscription(text='Модель - {}'.format(functional.model), bg_color = 'gray95',
                      text_color = 'blue4', x=310, y=410, width=110, height=20)
    # print_inscription(text='Разработчик Голов Д.Е. ©', bg_color = 'gray95', text_color = 'blue4',
    #                  x=1150, y=742, width=140, height=20)

    init_top_menu()
    init_interface()
    init_buttons()
    param_y += 20

    screen_frame = tkinter.Frame(window, bd=4, relief='groove', bg=COLOR)
    screen_frame.place(x=69, y=49, width=552, height=87)
    screen = tkinter.Label(bg='seagreen')
    screen.place(x=70, y=50, width=550, height=85)


    window.mainloop()