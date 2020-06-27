# -*- coding: utf-8 -*-

import tkinter, serial, time
from tkinter import messagebox
from uu import decode


COLOR = 'cornflowerblue'

class K2_functional:

    def __init__(self):
         self.port = None
         self.data = set()
         self.checks = []   #Список проверенных
         self.f = 0
         self.p = 0
         self.kg = 0
         self.chm = 0
         self.chm_max = 0


    def connect_com_port(self, port):
        self.port = port
        self.com = None

        try:
            self.com = serial.Serial(port, 9600, timeout=1)
            return 'Соединение с {} установлено'.format(port)
        except serial.SerialException:
            return 'Не удается соедениться с {}'.format(port)


    def send_code(self, code, commande=None):
        try:
            self.com.write(code)
            if commande:
                return  "Команда '{}' отправлена на {}".format(commande, self.com.port)
        except serial.SerialException:
            return 'Не удается соедениться с ' + self.com.port
        except (NameError, AttributeError):
            return 'Ошибка {}: Нет подключения'.format(self.port)


    def input_frequency(self, f):
        error_message = 'Введите корректную частоту (например 151.825 или 151825)'

        if len(f) == 6:
            f = f[:3] + '.' + f[3:]
        if len(f) == 7:
            for num in f:
                if num == '1':
                    self.send_code(b'0x01')
                elif num == '2':
                    self.send_code(b'0x02')
                elif num == '3':
                    self.send_code(b'0x03')
                elif num == '4':
                    self.send_code(b'0x04')
                elif num == '5':
                    self.send_code(b'0x05')
                elif num == '6':
                    self.send_code(b'0x06')
                elif num == '7':
                    self.send_code(b'0x07')
                elif num == '8':
                    self.send_code(b'0x08')
                elif num == '9':
                    self.send_code(b'0x09')
                elif num == '0':
                    self.send_code(b'0x00')
                elif num == '.' or num == ',':
                    self.send_code(b'0x10')
        else:
            return error_message

        self.send_code(b'0x12')
        return 'Частота {} установлена на приборе'.format(f)


    def check_transmitter(self, window, screen):
        functions = [b'0x26', b'0x20', b'0x29', b'0x20', b'0x33', b'0x15', b'0x09', b'0x10', b'0x05', b'0x13',
                     b'0x20', b'0x17', b'0x15', b'0x20', b'0x17', b'0x15', b'0x20', b'0x17', b'0x00', b'0x10',
                     b'0x03', b'0x14', b'0x27', b'0x03', b'0x13', b'0x17', b'0x01', b'0x13', b'0x23']
        timeout_02_functions = [1, 3, 4, 5, 6, 7, 8, 10, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
        percents = 0


        for step, function in enumerate(functions):
            screen.config(text='Проверяю передатчик. Завершено {}%'.format(round(percents, 1)))
            self.data.add(self.com.readline())
            window.update()

            if step in [11, 16]:
                for _ in range(2):
                    self.send_code(function)
                    time.sleep(0.2)

            self.send_code(function)

            if step == 28:
                time.sleep(0.2)
                self.send_code(function)

            if step in [0, 2, 9]:
                pass#time.sleep(5)
            elif step in timeout_02_functions:
                 pass#time.sleep(0.2)
            elif step == 12:
                pass#time.sleep(10)
            elif step == 15:
                pass#time.sleep(33)

            percents += 3.44827586
        screen.config(text='Проверка завершена')
        self.data.add(self.com.readline())
        self.take_result()


    def take_result(self):
        data_list = []

        for line in self.data:
            data_list.append(line.decode('cp866'))

        data_list.sort()
        for line in data_list:
            if 'Kг= ' in line:
                self.kg = float(line[4:-4])
            elif 'P= ' in line:
                self.p = float(line[3:-6])
            elif 'ЧМ+=  ' in line:
                self.chm = float(line[6:-6])
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
                    self.f = round(self.f,3)
                else:
                    self.f = float(line)
                    self.f = round(self.f,2)



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


# множетели
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
def get_frequency_button_click(event=None):
    frequency = get_frequency.get()
    screen.config(text=functional.input_frequency(frequency))

def check_transmitter_button():
    global param_y
    i = 0   # Индексация по списку проверенных

    functional.check_transmitter(window=window, screen=screen)

    print_inscription(text=functional.f, x=190, y=param_y, width=100, height=20,
                      color='snow3', justify=tkinter.LEFT)
    print_inscription(text=functional.p, x=280, y=param_y, width=80, height=20,
                      color='snow3', justify=tkinter.LEFT)
    print_inscription(text=functional.kg, x=350, y=param_y, width=80, height=20,
                      color='snow3', justify=tkinter.LEFT)
    print_inscription(text=functional.chm, x=410, y=param_y, width=200, height=20,
                      color='snow3', justify=tkinter.LEFT)
    print_inscription(text=functional.chm_max, x=610, y=param_y, width=150, height=20,
                      color='snow3', justify=tkinter.LEFT)
    param_y += 20


def button_cancel_click(event=None):
    # протестировать с потоками, пока что не работает
    pass

def check_receiver_button_click():
    pass


# Функции выбора COM порта в верхнем меню
def menu_com1_choice():
    screen.config(text=functional.connect_com_port('COM1'))

def menu_com2_choice():
    screen.config(text=functional.connect_com_port('COM2'))

def menu_com3_choice():
    screen.config(text=functional.connect_com_port('COM3'))


def init_interface():
    frame = tkinter.Frame(window, borderwidth=2, relief='groove', bg=COLOR)
    frame.place(x=10, y=10, width=1310, height=390)
    down_frame = tkinter.Frame(window, borderwidth=3, relief='groove', bg='snow3')
    down_frame.place(x=180, y=435, width=1100, height=300)

    print_inscription(text='Перед началом работы не забудь нажать ДУ на приборe НА...',
                           x=70, y=20, width=400, height=20)
    print_inscription(text='РЕЖИМ', x=65, y=190, width=160, height=15)
    print_inscription(text='ВЧ', x=340, y=190, width=160, height=15)
    print_inscription(text='НЧ', x=630, y=190, width=160, height=15)
    print_inscription(text='ИЗМЕНЕНИЕ', x=1030, y=190, width=160, height=15)

    print_inscription(text='Частота', x=190, y=440, width=100, height=30, color='snow3', justify=tkinter.LEFT)
    print_inscription(text='Мощность', x=280, y=440, width=80, height=30, color='snow3', justify=tkinter.LEFT)
    print_inscription(text='КНИ', x=350, y=440, width=80, height=30, color='snow3', justify=tkinter.LEFT)
    print_inscription(text='Чувств модуляционного входа',
                      x=410, y=440, width=200, height=30, color='snow3', justify=tkinter.LEFT)
    print_inscription(text='Максимальная девиация', x=610, y=440, width=150, height=30,
                      color='snow3', justify=tkinter.LEFT)

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

# Надписи
def print_inscription(text, x, y, width, height, color=COLOR , justify=tkinter.CENTER):
    inscription = tkinter.Label(window, text=text, bg=color, justify=justify)
    inscription.place(x=x, y=y, width=width, height=height)


# Верхнее меню

def init_top_menu():
    menu_item = tkinter.Menu(window)
    window.config(menu=menu_item)
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
    com_port_menu.add_command(label='COM1', command=menu_com1_choice)
    com_port_menu.add_command(label='COM2', command=menu_com2_choice)
    com_port_menu.add_command(label='COM3', command=menu_com3_choice)

def init_buttons():
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
    check_transmitter = tkinter.Button(window, text='Проверка передатчика',
                                       command=check_transmitter_button)
    check_transmitter.place(x=20, y=435, width=140, height=button_height)
    #Кнопку cancel нужно допилисть
    button_cancel = tkinter.Button(window, text='Esc - Отмена', command=button_cancel_click)
    button_cancel.place(x=20, y=480, width=140, height=button_height)
    # button_cancel.bind('<Button-1>', button_cancel_click)
    label_f = tkinter.Label(window, text='f:')
    label_f.place(x=20, y=525, width=20, height=button_height)
    get_frequency.place(x=40, y=525, width=120, height=30)
    get_frequency.bind('<Return>', get_frequency_button_click)
    get_frequency_button = tkinter.Button(window, text='Установить частоту',
                                          command=get_frequency_button_click)
    get_frequency_button.place(x=20, y=565, width=140, height=button_height)
    check_transmitter = tkinter.Button(window, text='Проверка приемника',
                                       command=check_receiver_button_click)
    check_transmitter.place(x=20, y=610, width=140, height=button_height)


def init_window():
    init_top_menu()
    init_interface()
    init_buttons()


param_y = 480

window = tkinter.Tk()
window.title('К2-82 Alpha-test')
window.minsize(width=1330, height=770)
get_frequency = tkinter.Entry(window, bd=2)

init_window()

screen_frame = tkinter.Frame(window, bd=4, relief='groove', bg=COLOR)
screen_frame.place(x=69, y=49, width=552, height=87)
screen = tkinter.Label(bg='seagreen')
screen.place(x=70, y=50, width=550, height=85)

functional = K2_functional()
functional.connect_com_port('COM2')

print(functional.data)


window.mainloop()