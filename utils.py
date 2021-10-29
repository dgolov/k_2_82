# Утилиты и полезности к основной программе
import math
import tkinter


def print_inscription(window, text, x, y, width, height, text_color = '#000000'):
    """ Печать текста (результаты проверка, надписи интерфейса, инструкции)
        :param window - окно в котором выводим текст
        :param text - текст выводимого сообщения
        :param x - координата х выводимого сообщения
        :param y - координата у выводимго сообщения
        :param width - ширина выводимого сообщения
        :param height - длинна выводимого сообщения
        :param text_color - цвет текста выводимого сообщения (по умолчанию черный)
    """
    inscription = tkinter.Label(window, text=text, foreground = text_color)
    inscription.place(x=x, y=y, width=width, height=height)


class DecibelCalc:
    """ Дополнительная фича к основной программе
        Конвертор децибел в пазы и наоборот
        Открывает дополнительное окно в программе
    """
    def __init__(self):
        self.calc = tkinter.Tk()
        self.info_db = tkinter.Label(self.calc, text='Децибелы (dB)', justify=tkinter.LEFT)
        self.info_tm = tkinter.Label(self.calc, text='Разы', justify=tkinter.CENTER)
        self.get_db = tkinter.Entry(self.calc, bd=2)
        self.get_tm = tkinter.Entry(self.calc, bd=2)
        self.convert_button_db = tkinter.Button(self.calc, text='Конвертировать', command=self.db_to_tm)
        self.convert_button_tm = tkinter.Button(self.calc, text='Конвертировать', command=self.tm_to_db)

    def tm_to_db(self):
        """ Конвертация: Разы в Дб """
        data = self.get_tm.get()
        if ',' in data:
            data = data.replace(',','.')

        try:
            tm = float(data)
            db = round(20 * math.log10(tm), 1)
            last = len(self.get_db.get())

            self.get_db.delete(first=0, last=last)
            self.get_db.insert(0, str(db))
        except ValueError:
            pass

    def db_to_tm(self):
        """ Конвертация: Дб в разы """
        data = self.get_db.get()
        if ',' in data:
            data = data.replace(',','.')

        try:
            db = float(data)
            db /=  2
            tm = round(10 ** (db / 10), 3)
            last = len(self.get_tm.get())

            self.get_tm.delete(first=0, last=last)
            self.get_tm.insert(0, str(tm))
        except ValueError:
            pass

    def show(self):
        """ Отображение дополнительного окна с калькулятором """
        x, y = 40, 20
        width, height = 150, 30

        self.calc.title('Калькулятор децибел')
        self.calc.minsize(width=390, height=170)
        self.calc.iconbitmap('images\\calc.ico')

        self.info_db.place(x=x, y=y, width=width, height=height)
        self.info_tm.place(x=x + 160, y=y, width=width, height=height)
        self.get_db.place(x=x, y=y + 30, width=width, height=height)
        self.get_tm.place(x=x + 160, y=y + 30, width=width, height=height)
        self.convert_button_db.place(x=x, y=y + 70, width=width, height=height)
        self.convert_button_tm.place(x=x + 160, y= y + 70, width=width, height=height)

        self.calc.mainloop()


if __name__ == '__main__':
    calc = DecibelCalc()
    calc.show()
