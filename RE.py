#! /home/alexmakh/anaconda3/bin/python3
# Импорт библиотек
import argparse
import re
import PyPDF2 as pd

try:
    # Задание функции, которая будет находить регулярные выражения
    def rebmf(pdf):
        print('Enter RE:', end='')
        red = input()           # Ввод регулярного выражения (далее - РВ)
        text = ""               # Переменная для цикла "Вывод функции"
        file = pd.PdfFileReader(open(pdf, mode='rb'),
                                strict=False)  # Загрузка-чтение pdf-файла
        red = ".*" + red + ".*"
        refinder = []
        for i in range(file.getNumPages()):
            text = file.getPage(i).extractText()
            refinder += re.findall(red, text)  # Поиск соответствий
            # Получение текста i-той страницы (в PyPDF2 отсутствует возможность
            # выделить весь текст файла сразу), поэтому
            # просто зацикливаем выделение по страницам
        # Делаем так для того, чтобы на выходе получать целую строку с РВ
        for i in range(len(refinder)):
            print(refinder[i], '\n')

    def save_text(pdf):
        text = ''
        word, txt, other = ['w', 'word'], ['t', 'txt'], ['o', 'other']
        file = pd.PdfFileReader(open(pdf, mode='rb'), strict=False)
        for i in range(file.getNumPages()):
            text += file.getPage(i).extractText()
        print('''Do you want to save your text to txt, word or other type of file? [w/t/o]
    if you don't want to continue, type any key, execept 'w', 't' and 'o' ''')
        kur = input().lower()
        if kur in txt:
            print('enter your destination (with filename): ')
            dest = input()

            if '.txt' not in dest:
                dest = dest + '.txt'
            with open('{}'.format(dest), 'w') as f:
                f.write(text)
            print('successfully saved into', dest)
        elif kur in word:
            print('enter your destination (with filename): ')
            dest = input()
            if '.word' not in dest:
                dest = dest + '.word'
            with open('{}'.format(dest), 'w') as f:
                f.write(text)
            print('successfully saved into', dest)
        elif kur in other:
            print('enter your destination (with filename and file type (.***)): ')
            dest = input()
            with open('{}'.format(dest), 'w') as f:
                f.write(text)
            print('successfully saved into', dest)
        else:
            print('thank you for using!')

    # Задание еще одной функции (чисто для интереса), которая будет выводить
    # количество страниц в открываемом pdf-файле
    def lox(pdf):
        p = "Number of pages in file - " + str(pd.PdfFileReader(
            open(pdf, mode='rb'),  # В переменную записывается исходнозаданная
            strict=False).getNumPages())  # строка и количество страниц
        print(p)

    # Тепрь создаем интерфейс консоли с помощью argparce
    parser = argparse.ArgumentParser(
        prog=''' 'BETA' PDF-worker''',
        epilog='Thanks for using this program!',
        description='RE finder, word/txt converter, page counter!')
    parser.add_argument(
        'pdf', metavar='PDF', type=str,  # Теперь задаем аргументы
        help='''PDF-File for opening
        if no positional arguments - converting your file to word/txt''')
    parser.add_argument('-r', '--regular', action='append_const', const=rebmf,
                        dest='func', help='''Get the RE from your PDF''')
    parser.add_argument('-c', '--count', action='append_const', const=lox,
                        dest='func', help='''count pages from PDF''')
    parser.add_argument('-s', '--save', action='append_const', const=save_text,
                        dest='func',
                        help='save PDF text to txt/word/other file type')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1')
    # А также свойства аргументов: имя опционального и позиционного аргументов,
    # справка, а также значение(какая из функций активируется) для опцион.
    # аргумента по умолчанию и по вызову, тип данных для позиционного аргумента
    args = parser.parse_args()  # Команда для записи того, что ввели с консоли
    for i in args.func:
        i(args.pdf)

except KeyboardInterrupt:
    print('\nThank you for using!')
except FileNotFoundError:
    print('No such pdf file')
except pd.utils.PdfReadError:
    print('Not a PDF file')
except Exception:
    print('Something went wrong...')
