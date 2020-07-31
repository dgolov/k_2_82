import math, tkinter



def decibel_calc():

    def tm_to_db():
        data = get_tm.get()

        if ',' in data:
            data = data.replace(',','.')

        tm = float(data)
        db = round(20 * math.log10(tm), 1)
        last = len(get_db.get())

        get_db.delete(first=0, last=last)
        get_db.insert(0, str(db))

    def db_to_tm():
        data = get_db.get()

        if ',' in data:
            data = data.replace(',','.')

        db = float(data)
        db /=  2
        tm = round(10 ** (db / 10), 3)
        last = len(get_tm.get())

        get_tm.delete(first=0, last=last)
        get_tm.insert(0, str(tm))


    x = 40
    y = 20
    width = 150
    height = 30

    calc = tkinter.Tk()
    calc.title('Калькулятор децибел')
    calc.minsize(width=390, height=170)

    info_db = tkinter.Label(calc, text='Децибелы (dB)', justify=tkinter.LEFT)
    info_db.place(x=x, y=y, width=width, height=height)
    info_tm = tkinter.Label(calc, text='Разы', justify=tkinter.CENTER)
    info_tm.place(x=x + 160, y=y, width=width, height=height)


    get_db = tkinter.Entry(calc, bd=2)
    get_db.place(x=x, y=y + 30, width=width, height=height)
    get_tm = tkinter.Entry(calc, bd=2)
    get_tm.place(x=x + 160, y=y + 30, width=width, height=height)


    convert_button_db = tkinter.Button(calc, text='Конвертировать', command=db_to_tm)
    convert_button_db.place(x=x, y=y + 70, width=width, height=height)
    convert_button_tm = tkinter.Button(calc, text='Конвертировать', command=tm_to_db)
    convert_button_tm.place(x=x + 160, y= y + 70, width=width, height=height)

    calc.mainloop()


if __name__ == '__main__':
    decibel_calc()