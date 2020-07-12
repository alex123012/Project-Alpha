#! /home/alexmakh/anaconda3/bin/python3
# Импорт библиотек
import argparse
import re
import PyPDF2 as pd
import io
import pdfminer
import subprocess
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

try:
    def lox(pdf):
        p = "Number of pages in file - " + str(pd.PdfFileReader(
            open(pdf, mode='rb'),  # В переменную записывается исходнозаданная
            strict=False).getNumPages())  # строка и количество страниц
        print(p)

    # Задание функции, которая будет находить регулярные выражения
    def rebmf(pdf, page=None):
        red = input('Enter RE: ')  # Ввод регулярного выражения (далее - РВ)
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
        if page is True:
            print(
                "Number of pages in file - " + str(file.getNumPages()))

    # converts pdf, returns its text content as a string
    def conv(fname, pages=None):
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        output = io.StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)

        infile = open(fname, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
        return text

    def save_pdf(pdf, redactor=None):
        print('extracting text...')
        text = conv(pdf)  # get string of text content of pdf
        kur = input('''Do you want to save your PDF file text to txt, word or other type of file?
if you don't want to continue, type any key, execept 'w', 't' and 'o': [w/t/o] ''').lower()
        perev = {'w': 'docx', 'word': 'docx', 't': 'txt', 'txt': 'txt'}
        if kur in perev:
            textFilename = input('enter your destination (with filename): ')

            if textFilename.split('.')[-1] != perev[kur]:
                textFilename = textFilename + '.' + perev[kur]
            textFile = open(textFilename, "w")  # make text file
            textFile.write(text)  # write text to text file

            print('\nsuccessfully converted ', end='')
        elif kur == 'o' or kur == 'other':
            textFilename = input(
                'enter your destination (with filename and file type (.***)): '
            )

            textFile = open(textFilename, "w")  # make text file
            textFile.write(text)  # write text to text file

            print('\nsuccessfully converted ', end='')
        else:
            print('thank you for using!')
        if redactor is not None:
            subprocess.call([redactor, textFilename])
            print('and edited ', end='')
        print(textFilename)

    # Задание еще одной функции (чисто для интереса), которая будет выводить
    # количество страниц в открываемом pdf-файле

    # Тепрь создаем интерфейс консоли с помощью argparce
    parser = argparse.ArgumentParser(
        prog=''''BETA' PDF-worker''',
        epilog='Thanks for using this program!',
        description='RE finder, word/txt converter, page counter!')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(
        title=None,
        metavar='options'
    )

    convert = subparsers.add_parser('convert',
                                    help='convert and/or edit text from PDF')
    convert.add_argument('-r', '--redactor', action='store', dest='enter',
                         help='type text editor name')
    convert.add_argument('-p', '--pages', action='store', dest='Enter',
                         help='type page number to convert/edit')
    convert.set_defaults(func=save_pdf)

    reg = subparsers.add_parser('re', help='Find information from PDF text')
    reg.set_defaults(func=rebmf)
    reg.add_argument('-c', '--count', action='store_true', dest='enter',
                     help='count pages from PDF')

    parser.add_argument(
        'pdf', metavar='PDF', type=str,  # Теперь задаем аргументы
        help='PDF-File for opening')

    # А также свойства аргументов: имя опционального и позиционного аргументов,
    # справка, а также значение(какая из функций активируется) для опцион.
    # аргумента по умолчанию и по вызову, тип данных для позиционного аргумента

    args = parser.parse_args()  # Команда для записи того, что ввели с консоли
    # if 'subprocess' in str(args.func):
    args.func(args.pdf, args.enter)

except KeyboardInterrupt:
    print('\nThank you for using!')
except FileNotFoundError:
    print('No such PDF file')
except pd.utils.PdfReadError:
    print('Not a PDF file')
except pdfminer.pdfparser.PDFSyntaxError:
    print('Not a PDF file')
except UnboundLocalError:
    print()
# except TypeError:
#     print('Type at least one optional argument')
except Exception:
    print('''Something went wrong... Please, contact developer:
e-mail: makhonin.a.ru@gmail.com''')
