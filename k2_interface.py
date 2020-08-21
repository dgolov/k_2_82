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
        self.resize(1670, 942)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images\\icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setWindowTitle("К2-82 v 0.4")
        self.k2_functional.connect_com_port(self.k2_functional.COM)

        # Задний фон
        # oImage = QImage("images\\logo (2).png")
        # sImage = oImage.scaled(QSize(1520, 942))
        # palette = QPalette()
        # palette.setBrush(QPalette.Window, QBrush(sImage))
        # self.setPalette(palette)

        self.init_device()
        self.init_buttons()
        self.init_table()
        self.init_menu()

        self.setCentralWidget(self.main_window)

        self.statusBar().showMessage('COM порт: {}'.format(self.k2_functional.COM))


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
        label = QtWidgets.QLabel('Перед началом работы не забудь активировать кнопки УСТ и ДУ на приборе.',
                                 self.k2_frame)
        label.setGeometry(QtCore.QRect(60, 20, 700, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        label.setFont(font)

        label_mode = QtWidgets.QLabel('Режим', self.k2_frame)
        label_mode.setGeometry(QtCore.QRect(20, 210, 281, 20))
        font.setPointSize(11)
        label_mode.setFont(font)
        label_mode.setAlignment(QtCore.Qt.AlignCenter)
        label_hight = QtWidgets.QLabel('ВЧ', self.k2_frame)
        label_hight.setGeometry(QtCore.QRect(295, 210, 271, 20))
        label_hight.setFont(font)
        label_hight.setStyleSheet("color: rgb(18, 18, 18);")
        label_hight.setAlignment(QtCore.Qt.AlignCenter)
        label_low = QtWidgets.QLabel('НЧ', self.k2_frame)
        label_low.setGeometry(QtCore.QRect(575, 210, 301, 20))
        label_low.setFont(font)
        label_low.setStyleSheet("color: rgb(18, 18, 18);")
        label_low.setAlignment(QtCore.Qt.AlignCenter)
        label_measurement = QtWidgets.QLabel('Измерение', self.k2_frame)
        label_measurement.setGeometry(QtCore.QRect(893, 210, 531, 20))
        label_measurement.setFont(font)
        label_measurement.setStyleSheet("color: rgb(18, 18, 18);")
        label_measurement.setAlignment(QtCore.Qt.AlignCenter)

        # Линии на приборе
        line_3 = QtWidgets.QFrame(self.k2_frame)
        line_3.setGeometry(QtCore.QRect(280, 200, 20, 209))
        line_3.setFrameShape(QtWidgets.QFrame.VLine)
        line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        line_4 = QtWidgets.QFrame(self.k2_frame)
        line_4.setGeometry(QtCore.QRect(560, 200, 20, 209))
        line_4.setFrameShape(QtWidgets.QFrame.VLine)
        line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        line_5 = QtWidgets.QFrame(self.k2_frame)
        line_5.setGeometry(QtCore.QRect(875, 1, 20, 408))
        line_5.setFrameShape(QtWidgets.QFrame.VLine)
        line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        line = QtWidgets.QFrame(self.k2_frame)
        line.setGeometry(QtCore.QRect(1, 190, 1428, 20))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line_2 = QtWidgets.QFrame(self.k2_frame)
        line_2.setGeometry(QtCore.QRect(1, 230, 1428, 20))
        line_2.setFrameShape(QtWidgets.QFrame.HLine)
        line_2.setFrameShadow(QtWidgets.QFrame.Sunken)


    def init_buttons(self):
        """ Инициализация всех кнопок в программе
        """
        button_width = 93
        button_height = 30

         # Кнопки на приборе
        button_mhz = QPushButton("V/MHz", self.main_window)
        button_mhz.setGeometry(QtCore.QRect(800, 90, button_width, button_height))
        button_mhz.clicked.connect(self.button_mhz_click)
        button_khz = QPushButton("mV/kHz", self.main_window)
        button_khz.setGeometry(QtCore.QRect(800, 140, button_width, button_height))
        button_khz.clicked.connect(self.button_khz_click)
        button_hz = QPushButton("uV/Hz", self.main_window)
        button_hz.setGeometry(QtCore.QRect(800, 190, button_width, button_height))
        button_hz.clicked.connect(self.button_hz_click)
        button_2 = QPushButton("2", self.main_window)
        button_2.setGeometry(QtCore.QRect(1000, 140, button_width, button_height))
        button_2.clicked.connect(self.button_2_click)
        button_line = QPushButton("-", self.main_window)
        button_line.setGeometry(QtCore.QRect(1000, 190, button_width, button_height))
        button_line.clicked.connect(self.button_line_click)
        button_6 = QPushButton("6", self.main_window)
        button_6.setGeometry(QtCore.QRect(1000, 90, button_width, button_height))
        button_6.clicked.connect(self.button_6_click)
        button_point = QPushButton(".", self.main_window)
        button_point.setGeometry(QtCore.QRect(1110, 190, button_width, button_height))
        button_point.clicked.connect(self.button_point_click)
        button_7 = QPushButton("7", self.main_window)
        button_7.setGeometry(QtCore.QRect(1110, 90, button_width, button_height))
        button_7.clicked.connect(self.button_7_click)
        button_3 = QPushButton("3", self.main_window)
        button_3.setGeometry(QtCore.QRect(1110, 140, button_width, button_height))
        button_3.clicked.connect(self.button_3_click)
        button_0 = QPushButton("0", self.main_window)
        button_0.setGeometry(QtCore.QRect(1220, 190, button_width, button_height))
        button_0.clicked.connect(self.button_0_click)
        button_9 = QPushButton("9", self.main_window)
        button_9.setGeometry(QtCore.QRect(1330, 90, button_width, button_height))
        button_9.clicked.connect(self.button_9_click)
        button_1 = QtWidgets.QPushButton("1", self.main_window)
        button_1.setGeometry(QtCore.QRect(1330, 190, button_width, button_height))
        button_1.clicked.connect(self.button_1_click)
        button_8 = QtWidgets.QPushButton("8", self.main_window)
        button_8.setGeometry(QtCore.QRect(1220, 90, button_width, button_height))
        button_8.clicked.connect(self.button_8_click)
        button_5 = QtWidgets.QPushButton("5", self.main_window)
        button_5.setGeometry(QtCore.QRect(1330, 140, button_width, button_height))
        button_5.clicked.connect(self.button_5_click)
        button_4 = QtWidgets.QPushButton("4", self.main_window)
        button_4.setGeometry(QtCore.QRect(1220, 140, button_width, button_height))
        button_4.clicked.connect(self.button_4_click)
        mode_20w = QtWidgets.QPushButton("20W", self.main_window)
        mode_20w.setGeometry(QtCore.QRect(100, 400, button_width, button_height))
        mode_20w.clicked.connect(self.mode_20w_click)
        mode_write = QtWidgets.QPushButton("ЗАПИСЬ", self.main_window)
        mode_write.setGeometry(QtCore.QRect(210, 300, button_width, button_height))
        mode_write.clicked.connect(self.mode_write_click)
        mode_ust = QPushButton("УСТ", self.main_window)
        mode_ust.setGeometry(QtCore.QRect(100, 300, button_width, button_height))
        mode_ust.clicked.connect(self.mode_ust_click)
        mode_du = QtWidgets.QPushButton("ДУ", self.main_window)
        mode_du.setGeometry(QtCore.QRect(100, 350, button_width, button_height))
        mode_du.clicked.connect(self.mode_du_click)
        mode_read = QtWidgets.QPushButton("ВВОД", self.main_window)
        mode_read.setGeometry(QtCore.QRect(210, 350, button_width, button_height))
        mode_read.clicked.connect(self.mode_read_click)
        high_frequency = QtWidgets.QPushButton("ЧАСТ", self.main_window)
        high_frequency.setGeometry(QtCore.QRect(370, 300, button_width, button_height))
        high_frequency.clicked.connect(self.high_frequency_click)
        high_pow = QtWidgets.QPushButton("МОЩН", self.main_window)
        high_pow.setGeometry(QtCore.QRect(480, 300, button_width, button_height))
        high_pow.clicked.connect(self.high_pow_click)
        high_chm_off = QtWidgets.QPushButton("ЧМ ОТКЛ", self.main_window)
        high_chm_off.setGeometry(QtCore.QRect(480, 350, button_width, button_height))
        high_chm_off.clicked.connect(self.high_chm_off_click)
        high_dop1 = QtWidgets.QPushButton("ДОП1", self.main_window)
        high_dop1.setGeometry(QtCore.QRect(370, 400, button_width, button_height))
        high_dop1.clicked.connect(self.high_dop1_click)
        high_chm = QtWidgets.QPushButton("ЧМ", self.main_window)
        high_chm.setGeometry(QtCore.QRect(370, 350, button_width, button_height))
        high_chm.clicked.connect(self.high_chm_click)
        low_frequency = QtWidgets.QPushButton("ЧАСТ", self.main_window)
        low_frequency.setGeometry(QtCore.QRect(650, 300, button_width, button_height))
        low_frequency.clicked.connect(self.low_frequency_click)
        low_voltage = QtWidgets.QPushButton("НАПР", self.main_window)
        low_voltage.setGeometry(QtCore.QRect(760, 300, button_width, button_height))
        low_voltage.clicked.connect(self.low_voltage_click)
        low_chm_ext = QtWidgets.QPushButton("ЧМ ВНЕШН", self.main_window)
        low_chm_ext.setGeometry(QtCore.QRect(760, 350, button_width, button_height))
        low_chm_ext.clicked.connect(self.low_chm_ext_click)
        low_dop2 = QtWidgets.QPushButton("ДОП2", self.main_window)
        low_dop2.setGeometry(QtCore.QRect(650, 400, button_width, button_height))
        low_dop2.clicked.connect(self.low_dop2_click)
        low_kg = QtWidgets.QPushButton("КГ", self.main_window)
        low_kg.setGeometry(QtCore.QRect(650, 350, button_width, button_height))
        low_kg.clicked.connect(self.low_kg_click)
        button_up = QtWidgets.QPushButton("Вверх", self.main_window)
        button_up.setGeometry(QtCore.QRect(1110, 300, button_width, button_height))
        button_up.clicked.connect(self.button_up_click)
        button_right = QtWidgets.QPushButton("Вправо", self.main_window)
        button_right.setGeometry(QtCore.QRect(1220, 350, button_width, button_height))
        button_right.clicked.connect(self.button_right_click)
        button_left = QtWidgets.QPushButton("Вниз", self.main_window)
        button_left.setGeometry(QtCore.QRect(1110, 400, button_width, button_height))
        button_left.clicked.connect(self.button_down_click)
        button_down = QtWidgets.QPushButton("Влево", self.main_window)
        button_down.setGeometry(QtCore.QRect(1000, 350, button_width, button_height))
        button_down.clicked.connect(self.button_left_click)
        disconnect_button = QtWidgets.QPushButton("ОТКЛ", self.main_window)
        disconnect_button.setGeometry(QtCore.QRect(1330, 400, button_width, button_height))
        disconnect_button.clicked.connect(self.disconnect_button_click)
        input_button = QtWidgets.QPushButton("ВВОД", self.main_window)
        input_button.setGeometry(QtCore.QRect(1330, 300, button_width, button_height))
        input_button.clicked.connect(self.input_button_click)

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


    def init_table(self):
        """ Инициализация таблицы результатов
        """
        #TODO реализовать сохранение параметров в ведомость (уже готовую)
        coll_names = ["№ РC", "№ АКБ", "Ёмкость", "P", "Выс. P", "Откл.", "КНИ", "ЧМ", "Max дев.", "Чувств.",
                      "Вых. P", "Вых P.", "Избер.", "КНИ", "Шумодав", "Деж реж.", "I пр.", "I прд.", "Раздяд\nАКБ"]
        rows, cols = 20, 19

        self.result_table.setGeometry(QtCore.QRect(220, 480, 1421, 391))
        self.result_table.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.result_table.setMouseTracking(True)
        self.result_table.setAutoFillBackground(True)
        self.result_table.setStyleSheet("background-color: rgb(248, 248, 248);")
        self.result_table.setFrameShape(QtWidgets.QFrame.Panel)
        self.result_table.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.result_table.setMidLineWidth(1)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setGridStyle(QtCore.Qt.DashLine)

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
            item.setText(coll_names[coll])

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
        com1_action.triggered.connect(self.menu_com1_choice)
        com2_action = QAction('&COM2', self)
        com2_action.triggered.connect(self.menu_com2_choice)
        com3_action = QAction('&COM3', self)
        com3_action.triggered.connect(self.menu_com3_choice)
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

        # tool_bar = self.addToolBar('Проверка')
        # tool_bar.addAction(check_action)


    def click_button(self, text, code):
        """ Функция нажатия кнопки
            Осуществляет отправку сигнала на COM порт и вывод текста на экран приложения
            :param text - текст, который будет выводиться на экран
            :param code - код, который будет отправлен на COM порт
        """
        self.k2_functional.connect_com_port(self.k2_functional.COM)
        result = self.k2_functional.send_code(command=text, code=code)
        self.screen_text.setText(result)
        self.k2_functional.com.close()


    # Блок кнопок РЕЖИМ функции
    def mode_ust_click(self):
        self.click_button(text='УСТ', code=b'0x23')

    def mode_du_click(self):
        self.click_button(text='ДУ', code=b'0x24')

    def mode_20w_click(self):
        self.click_button(text='20W', code=b'0x25')

    def mode_write_click(self):
        self.click_button(text='ЗАПИСЬ', code=b'0x22')

    def mode_read_click(self):
        self.click_button(text='ВЫВОД', code=b'0x21')


    # ВЧ блок кнопок функции
    def high_frequency_click(self):
        self.click_button(text='ВЧ ЧАСТ', code=b'0x26')

    def high_chm_click(self):
        self.click_button(text='ВЧ ЧМ', code=b'0x27')

    def high_dop1_click(self):
        self.screen_text.setText('Кнопка не активна')

    def high_pow_click(self):
        self.click_button(text='МОЩН', code=b'0x29')

    def high_chm_off_click(self):
        self.click_button(text='ВЧ ЧМ ОТКЛ', code=b'0x30')

    # НЧ блок кнопок функции
    def low_frequency_click(self):
        self.click_button(text='НЧ ЧАСТ', code=b'0x31')

    def low_kg_click(self):
        self.click_button(text='НЧ КГ', code=b'0x32')

    def low_dop2_click(self):
        self.click_button(text='НЧ ДОП2', code=b'0x33')

    def low_voltage_click(self):
        self.click_button(text='НЧ НАПР', code=b'0x34')

    def low_chm_ext_click(self):
        self.click_button(text='НЧ ЧМ ВНЕШН', code=b'0x35')


    # Блок стрелок ИЗМЕНЕНИЕ
    def button_up_click(self):
        self.click_button(text='ВВЕРХ', code=b'0x16')

    def button_down_click(self):
        self.click_button(text='ВНИЗ', code=b'0x17')

    def button_left_click(self):
        self.click_button(text='ВЛЕВО', code=b'0x18')

    def button_right_click(self):
        self.click_button(text='ВПРАВО', code=b'0x19')

    def disconnect_button_click(self):
        self.click_button(text='ОТКЛ', code=b'0x20')

    def input_button_click(self):
        self.click_button(text='ВВОД', code=b'0x15')

    # Цифровая клавиатура функции
    def button_1_click(self):
        self.click_button(text='1', code=b'0x01')

    def button_2_click(self):
        self.click_button(text='2', code=b'0x02')

    def button_3_click(self):
        self.click_button(text='3', code=b'0x03')

    def button_4_click(self):
        self.click_button(text='4', code=b'0x04')

    def button_5_click(self):
        self.click_button(text='5', code=b'0x05')

    def button_6_click(self):
        self.click_button(text='6', code=b'0x06')

    def button_7_click(self):
        self.click_button(text='7', code=b'0x07')

    def button_8_click(self):
        self.click_button(text='8', code=b'0x08')

    def button_9_click(self):
        self.click_button(text='9', code=b'0x09')

    def button_0_click(self):
        self.click_button(text='0', code=b'0x00')

    def button_point_click(self):
        self.click_button(text='.', code=b'0x10')

    def button_line_click(self):
        self.click_button(text='-', code=b'0x11')

    # Множетели
    def button_mhz_click(self):
        self.click_button(text='V/MHz', code=b'0x12')

    def button_khz_click(self):
        self.click_button(text='mV/kHz', code=b'0x13')

    def button_hz_click(self):
        self.click_button(text='uV/Hz', code=b'0x14')

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
                cell_info = QtWidgets.QTableWidgetItem(str(param).replace('.', ','))
                self.result_table.setItem(self.row, col, cell_info)
                col += 1
                if col == 1 or col == 16:
                    col += 2

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


    def get_com_connect_info(self):
        """ Получение информации о состоянии подключения COM порта
        """
        is_connect = self.k2_functional.connect_com_port(self.k2_functional.COM)
        if is_connect:
            text = 'Соединение с {} установлено'.format(self.k2_functional.COM)
            self.statusBar().showMessage('COM: {}'.format(self.k2_functional.COM))
        else:
            text = 'Не удается соедениться с {}'.format(self.k2_functional.COM)
        self.screen_text.setText(text)

    # Функции меню Настройки - выбор COM порта
    def menu_com1_choice(self):
        """ Подключение к COM 1
        """
        self.k2_functional.COM = 'COM1'
        self.get_com_connect_info()

    def menu_com2_choice(self):
        """ Подключение к COM 2
        """
        self.k2_functional.COM = 'COM2'
        self.get_com_connect_info()

    def menu_com3_choice(self):
        """ Подключение к COM 3
        """
        self.k2_functional.COM = 'COM3'
        self.get_com_connect_info()


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
    '''v 0.4

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
    '''
    )