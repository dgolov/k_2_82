# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.13.2
#
import io, csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QMainWindow, QPushButton, QAction, qApp, QMessageBox
from PyQt5.QtGui import QIcon
from functional import K2Functional
from check import Check
from logging_settings import event_log
from utils import DecibelCalc
from settings import *



class UiMainWindow(QMainWindow):
    """ Окно пользовательского интерфейса программы
        Новая версия переписанная на библиотеке PyQt 5 заменив Tkiner
    """
    def __init__(self):
        super().__init__()
        self.main_window = QtWidgets.QWidget(self)
        self.k2_frame = QtWidgets.QFrame(self.main_window)
        self.screen_frame = QtWidgets.QFrame(self.k2_frame)
        self.screen_text = QtWidgets.QLabel(self.screen_frame)
        self.row = 0
        self.result_table = QtWidgets.QTableWidget(self.main_window)
        self.k2_functional = K2Functional()
        self.choice_of_the_model = QtWidgets.QComboBox(self.main_window)
        self.get_frequency = QtWidgets.QTextEdit(self.main_window)
        self.thread = None
        self.db_calc = DecibelCalc()


    def init_ui(self):
        """ Инициализация интерфейса
        """
        self.resize(1670, 980)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images\\icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setWindowTitle("К2-82 v {}".format(VERSION))

        self.init_device()
        self.init_buttons()
        self.init_table()
        self.init_menu()

        self.setCentralWidget(self.main_window)

        self.k2_functional.connect_com_port(self.k2_functional.COM)
        try:
            self.k2_functional.com.close()
            self.screen_text.setText('Соединение с {} установлено'.format(self.k2_functional.COM))
        except AttributeError:
            self.screen_text.setText('Не удается соединениться с {}'.format(self.k2_functional.COM))

        self.statusBar().showMessage('COM порт К2-82: {}    |   COM порт радиостанции: {}'.format(com, com_rs))


    def init_device(self):
        """ Инициализация приборной панели, надписей и линей на ней
        """
        # Прибор и экран
        self.k2_frame.setGeometry(QtCore.QRect(40, 40, 1431, 411))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.k2_frame.setFont(font)
        self.k2_frame.setStyleSheet("background-color: rgb(76, 153, 230);")
        self.k2_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.k2_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.screen_frame.setGeometry(QtCore.QRect(60, 60, 641, 101))
        self.screen_frame.setTabletTracking(False)
        self.screen_frame.setToolTipDuration(1)
        self.screen_frame.setStyleSheet("background-color: rgb(0, 170, 127);")
        self.screen_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.screen_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.screen_frame.setLineWidth(1)
        self.screen_frame.setMidLineWidth(1)

        self.screen_text.setGeometry(QtCore.QRect(20, 19, 591, 61))
        font.setPointSize(10)
        font.setWeight(50)
        self.screen_text.setFont(font)
        self.screen_text.setTextFormat(QtCore.Qt.PlainText)
        self.screen_text.setAlignment(QtCore.Qt.AlignCenter)

        # Надписи на приборе
        font = QtGui.QFont()
        font.setWeight(50)
        labels = ['Перед началом работы не забудь активировать кнопки УСТ и ДУ на приборе.',
                 'Режим', 'ВЧ', 'НЧ', 'Измерение']
        labels_geometry = [(60, 20, 700, 20), (20, 210, 281, 20), (295, 210, 271, 20), (575, 210, 301, 20),
                    (893, 210, 531, 20)]
        for i in range(5):
            font.setPointSize(11)
            label = QtWidgets.QLabel(self.k2_frame)
            label.setText(labels[i])
            label.setGeometry(QtCore.QRect(*labels_geometry[i]))
            if i == 0: font.setPointSize(9)
            else:
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setStyleSheet("color: rgb(18, 18, 18);")
            label.setFont(font)

        # Линии на приборе
        for i in range(5):
            line = QtWidgets.QFrame(self.k2_frame)

            if i == 0: line.setGeometry(QtCore.QRect(280, 200, 20, 209))
            elif i == 1: line.setGeometry(QtCore.QRect(560, 200, 20, 209))
            elif i == 2: line.setGeometry(QtCore.QRect(875, 1, 20, 408))
            elif i == 3: line.setGeometry(QtCore.QRect(1, 190, 1428, 20))
            elif i == 4: line.setGeometry(QtCore.QRect(1, 230, 1428, 20))

            if i in range(3): line.setFrameShape(QtWidgets.QFrame.VLine)
            else: line.setFrameShape(QtWidgets.QFrame.HLine)

            line.setFrameShadow(QtWidgets.QFrame.Sunken)


    def init_buttons(self):
        """ Инициализация всех кнопок в программе
        """
        button_width = 93
        button_height = 30

         # Кнопки на приборе
        button_mhz = QPushButton("V/MHz", self.main_window)
        button_mhz.setGeometry(QtCore.QRect(800, 90, button_width, button_height))
        button_mhz.clicked.connect(lambda: self.click_button(text='V/MHz', code=CODES['V/MHz']))
        button_khz = QPushButton("mV/kHz", self.main_window)
        button_khz.setGeometry(QtCore.QRect(800, 140, button_width, button_height))
        button_khz.clicked.connect(lambda: self.click_button(text='mV/kHz', code=CODES['mV/kHz']))
        button_hz = QPushButton("uV/Hz", self.main_window)
        button_hz.setGeometry(QtCore.QRect(800, 190, button_width, button_height))
        button_hz.clicked.connect(lambda: self.click_button(text='uV/Hz', code=CODES['uV/Hz']))
        button_2 = QPushButton("2", self.main_window)
        button_2.setGeometry(QtCore.QRect(1000, 140, button_width, button_height))
        button_2.clicked.connect(lambda: self.click_button(text='2', code=CODES['2']))
        button_line = QPushButton("-", self.main_window)
        button_line.setGeometry(QtCore.QRect(1000, 190, button_width, button_height))
        button_line.clicked.connect(lambda: self.click_button(text='-', code=CODES['-']))
        button_6 = QPushButton("6", self.main_window)
        button_6.setGeometry(QtCore.QRect(1000, 90, button_width, button_height))
        button_6.clicked.connect(lambda: self.click_button(text='6', code=CODES['6']))
        button_point = QPushButton(".", self.main_window)
        button_point.setGeometry(QtCore.QRect(1110, 190, button_width, button_height))
        button_point.clicked.connect(lambda: self.click_button(text='.', code=CODES['.']))
        button_7 = QPushButton("7", self.main_window)
        button_7.setGeometry(QtCore.QRect(1110, 90, button_width, button_height))
        button_7.clicked.connect(lambda: self.click_button(text='7', code=CODES['7']))
        button_3 = QPushButton("3", self.main_window)
        button_3.setGeometry(QtCore.QRect(1110, 140, button_width, button_height))
        button_3.clicked.connect(lambda: self.click_button(text='3', code=CODES['3']))
        button_0 = QPushButton("0", self.main_window)
        button_0.setGeometry(QtCore.QRect(1220, 190, button_width, button_height))
        button_0.clicked.connect(lambda: self.click_button(text='0', code=CODES['0']))
        button_9 = QPushButton("9", self.main_window)
        button_9.setGeometry(QtCore.QRect(1330, 90, button_width, button_height))
        button_9.clicked.connect(lambda: self.click_button(text='9', code=CODES['9']))
        button_1 = QtWidgets.QPushButton("1", self.main_window)
        button_1.setGeometry(QtCore.QRect(1330, 190, button_width, button_height))
        button_1.clicked.connect(lambda: self.click_button(text='1', code=CODES['1']))
        button_8 = QtWidgets.QPushButton("8", self.main_window)
        button_8.setGeometry(QtCore.QRect(1220, 90, button_width, button_height))
        button_8.clicked.connect(lambda: self.click_button(text='8', code=CODES['8']))
        button_5 = QtWidgets.QPushButton("5", self.main_window)
        button_5.setGeometry(QtCore.QRect(1330, 140, button_width, button_height))
        button_5.clicked.connect(lambda: self.click_button(text='5', code=CODES['5']))
        button_4 = QtWidgets.QPushButton("4", self.main_window)
        button_4.setGeometry(QtCore.QRect(1220, 140, button_width, button_height))
        button_4.clicked.connect(lambda: self.click_button(text='4', code=CODES['4']))
        mode_20w = QtWidgets.QPushButton("20W", self.main_window)
        mode_20w.setGeometry(QtCore.QRect(100, 400, button_width, button_height))
        mode_20w.clicked.connect(lambda: self.click_button(text='20W', code=CODES['20W']))
        mode_write = QtWidgets.QPushButton("ЗАПИСЬ", self.main_window)
        mode_write.setGeometry(QtCore.QRect(210, 300, button_width, button_height))
        mode_write.clicked.connect(lambda: self.click_button(text='ЗАПИСЬ', code=CODES['ЗАПИСЬ']))
        mode_ust = QPushButton("УСТ", self.main_window)
        mode_ust.setGeometry(QtCore.QRect(100, 300, button_width, button_height))
        mode_ust.clicked.connect(lambda: self.click_button(text='УСТ', code=CODES['УСТ']))
        mode_du = QtWidgets.QPushButton("ДУ", self.main_window)
        mode_du.setGeometry(QtCore.QRect(100, 350, button_width, button_height))
        mode_du.clicked.connect(lambda: self.click_button(text='ДУ', code=CODES['ДУ']))
        mode_read = QtWidgets.QPushButton("ВЫВОД", self.main_window)
        mode_read.setGeometry(QtCore.QRect(210, 350, button_width, button_height))
        mode_read.clicked.connect(lambda: self.click_button(text='ВЫВОД', code=CODES['ВЫВОД']))
        high_frequency = QtWidgets.QPushButton("ЧАСТ", self.main_window)
        high_frequency.setGeometry(QtCore.QRect(370, 300, button_width, button_height))
        high_frequency.clicked.connect(lambda: self.click_button(text='ВЧ ЧАСТ', code=CODES['ВЧ ЧАСТ']))
        high_pow = QtWidgets.QPushButton("МОЩН", self.main_window)
        high_pow.setGeometry(QtCore.QRect(480, 300, button_width, button_height))
        high_pow.clicked.connect(lambda: self.click_button(text='МОЩН', code=CODES['МОЩН']))
        high_chm_off = QtWidgets.QPushButton("ЧМ ОТКЛ", self.main_window)
        high_chm_off.setGeometry(QtCore.QRect(480, 350, button_width, button_height))
        high_chm_off.clicked.connect(lambda: self.click_button(text='ВЧ ЧМ ОТКЛ', code=CODES['ВЧ ЧМ ОТКЛ']))
        high_dop1 = QtWidgets.QPushButton("ДОП1", self.main_window)
        high_dop1.setGeometry(QtCore.QRect(370, 400, button_width, button_height))
        high_dop1.clicked.connect(lambda: self.screen_text.setText('Кнопка не активна'))
        high_chm = QtWidgets.QPushButton("ЧМ", self.main_window)
        high_chm.setGeometry(QtCore.QRect(370, 350, button_width, button_height))
        high_chm.clicked.connect(lambda: self.click_button(text='ВЧ ЧМ', code=CODES['ВЧ ЧМ']))
        low_frequency = QtWidgets.QPushButton("ЧАСТ", self.main_window)
        low_frequency.setGeometry(QtCore.QRect(650, 300, button_width, button_height))
        low_frequency.clicked.connect(lambda: self.click_button(text='НЧ ЧАСТ', code=CODES['НЧ ЧАСТ']))
        low_voltage = QtWidgets.QPushButton("НАПР", self.main_window)
        low_voltage.setGeometry(QtCore.QRect(760, 300, button_width, button_height))
        low_voltage.clicked.connect(lambda: self.click_button(text='НЧ НАПР', code=CODES['НЧ НАПР']))
        low_chm_ext = QtWidgets.QPushButton("ЧМ ВНЕШН", self.main_window)
        low_chm_ext.setGeometry(QtCore.QRect(760, 350, button_width, button_height))
        low_chm_ext.clicked.connect(lambda: self.click_button(text='НЧ ЧМ ВНЕШН', code=CODES['НЧ ЧМ ВНЕШН']))
        low_dop2 = QtWidgets.QPushButton("ДОП2", self.main_window)
        low_dop2.setGeometry(QtCore.QRect(650, 400, button_width, button_height))
        low_dop2.clicked.connect(lambda: self.click_button(text='НЧ ДОП2', code=CODES['НЧ ДОП2']))
        low_kg = QtWidgets.QPushButton("КГ", self.main_window)
        low_kg.setGeometry(QtCore.QRect(650, 350, button_width, button_height))
        low_kg.clicked.connect(lambda: self.click_button(text='НЧ КГ', code=CODES['НЧ КГ']))
        button_up = QtWidgets.QPushButton("Вверх", self.main_window)
        button_up.setGeometry(QtCore.QRect(1110, 300, button_width, button_height))
        button_up.clicked.connect(lambda: self.click_button(text='ВВЕРХ', code=CODES['ВВЕРХ']))
        button_right = QtWidgets.QPushButton("Вправо", self.main_window)
        button_right.setGeometry(QtCore.QRect(1220, 350, button_width, button_height))
        button_right.clicked.connect(lambda: self.click_button(text='ВПРАВО', code=CODES['ВПРАВО']))
        button_left = QtWidgets.QPushButton("Вниз", self.main_window)
        button_left.setGeometry(QtCore.QRect(1110, 400, button_width, button_height))
        button_left.clicked.connect(lambda: self.click_button(text='ВНИЗ', code=CODES['ВНИЗ']))
        button_down = QtWidgets.QPushButton("Влево", self.main_window)
        button_down.setGeometry(QtCore.QRect(1000, 350, button_width, button_height))
        button_down.clicked.connect(lambda: self.click_button(text='ВЛЕВО', code=CODES['ВЛЕВО']))
        disconnect_button = QtWidgets.QPushButton("ОТКЛ", self.main_window)
        disconnect_button.setGeometry(QtCore.QRect(1330, 400, button_width, button_height))
        disconnect_button.clicked.connect(lambda: self.click_button(text='ОТКЛ', code=CODES['ОТКЛ']))
        input_button = QtWidgets.QPushButton("ВВОД", self.main_window)
        input_button.setGeometry(QtCore.QRect(1330, 300, button_width, button_height))
        input_button.clicked.connect(lambda: self.click_button(text='ВВОД', code=CODES['ВВОД']))

        # Кнопки слева от таблицы
        self.choice_of_the_model.setGeometry(QtCore.QRect(30, 490, 171, button_height))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images\\model.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.choice_of_the_model.addItem(icon4, "   Motorola")
        self.choice_of_the_model.addItem(icon4, "   Альтавия")
        self.choice_of_the_model.addItem(icon4, "   Icom")

        check_rs_button = QtWidgets.QPushButton('Проверка параметров', self.main_window)
        check_rs_button.setGeometry(QtCore.QRect(30, 540, 171, button_height))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images\\start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        check_rs_button.setIcon(icon1)
        check_rs_button.clicked.connect(self.check_rs_button_click)

        button_cancel = QtWidgets.QPushButton('   Отмена проверки    ', self.main_window)
        button_cancel.setGeometry(QtCore.QRect(30, 590, 171, button_height))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images\\cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button_cancel.setIcon(icon2)
        button_cancel.clicked.connect(self.button_cancel_click)

        self.get_frequency.setGeometry(QtCore.QRect(60, 639, 140, 28))
        label_f = QtWidgets.QLabel('f:', self.main_window)
        label_f.setGeometry(QtCore.QRect(40, 636, 21, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        label_f.setFont(font)

        get_frequency_button = QtWidgets.QPushButton('  Установить частоту ', self.main_window)
        get_frequency_button.setGeometry(QtCore.QRect(30, 690, 171, button_height))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images\\frequency.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        get_frequency_button.setIcon(icon3)
        get_frequency_button.clicked.connect(self.get_frequency_button_click)

        deviation_flag = QtWidgets.QCheckBox('Пропуск max девиации', self.main_window)
        deviation_flag.setGeometry(QtCore.QRect(32, 740, 161, 21))
        deviation_flag.stateChanged.connect(self.deviation_flag_click)

        # Очиста таблицы
        clear_table_button = QtWidgets.QPushButton('Очистить таблицу', self.main_window)
        clear_table_button.setGeometry(QtCore.QRect(1450, 900, 171, button_height))
        clear_table_button.clicked.connect(self.clear_table)


    def init_table(self):
        """ Инициализация таблицы результатов
        """
        rows, cols = 20, 19

        self.result_table.setGeometry(QtCore.QRect(220, 480, 1421, 405))
        self.result_table.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.result_table.setMouseTracking(True)
        self.result_table.setAutoFillBackground(True)
        self.result_table.setStyleSheet("background-color: rgb(248, 248, 248);")
        self.result_table.setFrameShape(QtWidgets.QFrame.Panel)
        self.result_table.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.result_table.setMidLineWidth(1)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setGridStyle(QtCore.Qt.DashLine)
        self.result_table.itemChanged.connect(self.table_update)

        self.result_table.setColumnCount(cols)
        self.result_table.setRowCount(rows)

        for row in range(rows):
            item = QtWidgets.QTableWidgetItem()
            self.result_table.setVerticalHeaderItem(row, item)
            item.setText(str(row + 1))

        for coll in range(cols):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(8)
            font.setWeight(50)
            item.setFont(font)
            item.setBackground(QtGui.QColor(85, 170, 255))
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setForeground(brush)
            self.result_table.setHorizontalHeaderItem(coll, item)
            item.setText(COLL_NAMES[coll])

        self.result_table.horizontalHeader().setCascadingSectionResizes(True)
        self.result_table.horizontalHeader().setDefaultSectionSize(72)
        self.result_table.horizontalHeader().setMinimumSectionSize(40)
        self.result_table.verticalHeader().setCascadingSectionResizes(False)
        self.result_table.verticalHeader().setDefaultSectionSize(30)
        self.result_table.verticalHeader().setHighlightSections(True)

        self.result_table.installEventFilter(self)

    def eventFilter(self, source, event):
        """ Принимает и обрабатывает события копировать и вставить
            :param event - входящие событие
            :param source - QObject
        """
        if event.type() == QtCore.QEvent.KeyPress and event.matches(QtGui.QKeySequence.Copy):
            self.copy_selection()
            return True
        return super().eventFilter(source, event)


    def table_update(self, item):
        """ Автозамена введенных пользователем значений в таблице
            В поле емкость акб 'n' и 'N' автоматически заменяется на 'N/R'
            При вводе '-' в поле № АКБ автоматически добавляется '-' в поле емкость акб
            :param item - ячейка в которую вводятся данные
        """
        text = item.text().upper()
        if (text == 'N') and item.column() == 2:
            item.setText('N/R')
        elif text == '-' and item.column() == 1:
            cell_info = QtWidgets.QTableWidgetItem('-')
            column = item.column()
            row = item.row()
            self.result_table.setItem(row, column + 1, cell_info)
        elif (text == 'Б' or text == 'B' or text == ',') and item.column() == 1:
            item.setText('Б/Н')
        elif item.column() == 17:
            if str(text).isdigit():         # Если текст состоит только из цифр (например 123) то делим это
                text = float(text) / 100    # значение на 100 чтобы получить корректное значение 1,23
            item.setText(str(text).replace('.', ','))
        else:
            item.setText(text)


    def copy_selection(self):
        """ Копирование данных из таблицы в формате Excel
            Комбинация клавиш для копирования: ctrl+с
        """
        selection = self.result_table.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            QtWidgets.qApp.clipboard().setText(stream.getvalue())


    def clear_table(self):
        """ Очистка таблицы
        """
        self.result_table.clear()
        self.row = 0
        self.init_table()


    def init_menu(self):
        """ Инициализация меню
        """
        menu_bar = self.menuBar()
        check_action = QAction(QIcon('images\\start.png'), '&Проверка параметров', self)
        check_action.setShortcut('Ctrl+A')
        check_action.triggered.connect(self.check_rs_button_click)
        exit_action = QAction(QIcon('images\\exit.png'), '&Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)
        help_action = QAction('&О программе', self)
        help_action.setShortcut('Ctrl+F1')
        help_action.triggered.connect(self.show_info)
        com1_action = QAction('&COM1', self)
        com1_action.triggered.connect(lambda: self.choice_com_port(com_port='COM1'))
        com2_action = QAction('&COM2', self)
        com2_action.triggered.connect(lambda: self.choice_com_port(com_port='COM2'))
        com3_action = QAction('&COM3', self)
        com3_action.triggered.connect(lambda: self.choice_com_port(com_port='COM3'))
        decibel_calc_action = QAction(QIcon('images\\calc.ico'), '&Калькулятор децибел', self)
        decibel_calc_action.triggered.connect(self.db_calc.show)

        file_menu = menu_bar.addMenu('&Файл')
        file_menu.addAction(check_action)
        file_menu.addAction(exit_action)
        settings_menu = menu_bar.addMenu('&Настройки')
        com_menu = settings_menu.addMenu('&COM порт')
        com_menu.addAction(com1_action)
        com_menu.addAction(com2_action)
        com_menu.addAction(com3_action)
        utils_menu = menu_bar.addMenu('&Утилиты')
        utils_menu.addAction(decibel_calc_action)
        help_menu = menu_bar.addMenu('&Справка')
        help_menu.addAction(help_action)


    def click_button(self, text, code):
        """ Функция нажатия кнопки
            Осуществляет отправку сигнала на COM порт и вывод текста на экран приложения
            :param text - текст, который будет выводиться на экран
            :param code - код, который будет отправлен на COM порт
        """
        if not self.k2_functional.check:
            self.k2_functional.connect_com_port(self.k2_functional.COM)
        result = self.k2_functional.send_code(command=text, code=code)
        self.screen_text.setText(result)
        if not self.k2_functional.check:
            try:
                self.k2_functional.com.close()
            except AttributeError:
                pass


    def check_rs_button_click(self):
        """ Кнопка запуска цикла проверки радиостанции
            Запускает отдельный поток для проверки и формирует получение сигналов из этого потока
        """
        self.thread = QThread()
        self.k2_functional.model = self.choice_of_the_model.currentText()[3:]
        self.k2_functional.connect_com_port(self.k2_functional.COM)

        self.new_check = Check(self.k2_functional)
        self.new_check.moveToThread(self.thread)
        self.new_check.next_screen_text.connect(self.screen_text.setText)
        self.new_check.next_message_box.connect(self.message_box)
        self.new_check.check_status.connect(self.get_check_result)

        self.thread.started.connect(self.new_check.run)
        self.thread.start()


    def get_check_result(self, check_result):
        """ Принимает сигнал с результатами из потока
            выводит сообщение о статусе завершения проверки на зеленый экран
            заполняет таблицу полученными результатами
            :param check_result - словарь dict с результатами проверки и сообщением о статусе проверки
        """
        self.screen_text.setText(check_result['message'])

        if check_result['params'] is not None:
            col = 0
            for param in check_result['params']:
                if col == 16:
                    try:
                        item = self.result_table.item(self.row, col).text()
                        if item != '':
                            col += 2
                            continue
                    except Exception:
                        pass
                cell_info = QtWidgets.QTableWidgetItem(str(param[0]).replace('.', ','))
                if not param[1]:
                    cell_info.setForeground(QtGui.QColor(250, 0, 0))
                self.result_table.setItem(self.row, col, cell_info)
                col += 1
                if col == 1:
                    col += 2
                if col == 17:
                    col += 1

            self.row += 1

        self.thread.terminate()
        self.thread = None


    def message_box(self, message):
        """ Сигнал из потока запускающий message box с инструкциями для пользователя
            Пока пользователь не отреагирует на сообщение проверка продолжаться не будет
            :param message - список из заголовка всплывающего окна и
                             сообщения выводимого в сплывающем окне
        """
        self.k2_functional.continue_thread = False
        QMessageBox.information(self, message[0], message[1])
        self.k2_functional.continue_thread = True


    def button_cancel_click(self):
        """ Кнопка отмены цикла проверки
        """
        if self.k2_functional.check:
            self.k2_functional.cancel = True
            self.thread.terminate()


    def get_frequency_button_click(self, event=None):
        """
        Кнопка установки частоты на К2-82
        :param event - событие отмены, кнопка с клавиатуры
        """
        frequency = self.get_frequency.toPlainText()
        try:
            self.screen_text.setText(self.k2_functional.input_frequency(frequency))
        except AttributeError:
            event_log.error('COM port connecting error')
            self.screen_text.setText('Не удается соедениться с {}'.format(self.k2_functional.port))


    def deviation_flag_click(self, state):
        """ Флаг пропуска девиации
            :param state - статус флажка пропуска максимальной девиации
        """
        if state == Qt.Checked:
            self.k2_functional.check_deviation_time = 0.2
        else:
            self.k2_functional.check_deviation_time = 33


    def choice_com_port(self, com_port):
        """ Получение информации о состоянии подключения COM порта
            :param com_port - название COM порта
        """
        global com
        com = com_port
        is_connect = self.k2_functional.connect_com_port(com_port)
        if is_connect:
            text = 'Соединение с {} установлено'.format(com_port)
            self.statusBar().showMessage('COM: {}'.format(com_port))
        else:
            text = 'Не удается соедениться с {}'.format(com_port)
        self.screen_text.setText(text)
        self.statusBar().showMessage('COM порт К2-82: {}    |   COM порт радиостанции: {}'.format(com, com_rs))


    def save_file(self):
        """ Сохранение параметров в файл Excel
        """
        pass
        # name = filedialog.asksaveasfilename(filetypes=(('Excel', '*.xls'), ('Все файлы','*.*')))
        # if name != '':
        #     functional.excel_book.save_book(name)


    def show_info(self):
        """ Меню справка - о программе
        """
        QMessageBox.information(self, 'О программе',
    '''v {}

    Автомотизированное проведение  технического
    обслуживания  с  использованием установки для
    измерения    параметров   радиостанций    К2-82

    -------------------------------------------------------------------------------

    Для запуска  цикла проверки  радиостанции необходимо:
        - Деактивировать все кнопки на приборе кроме УСТ и ДУ
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
                                                        2020 г.
    '''.format(VERSION)
    )