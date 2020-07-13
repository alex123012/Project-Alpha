#! /home/alexmakh/anaconda3/bin/python3

#####################
# importing modules #
#####################
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
    ##################
    # RE finder func #
    ##################
    def rebmf(pdf, page=None):
        red = input('Enter RE: ')  # Entering RE
        text = ""
        file = pd.PdfFileReader(open(pdf, mode='rb'),
                                strict=False)  # Reading PDF file
        red = ".*" + red + ".*"  # string for RE find all line
        refinder = []

        for i in range(file.getNumPages()):  # Obtaining i page of file
            text = file.getPage(i).extractText()  # Extracting text from page
            refinder.append(re.findall(red, text))  # RE finding
        for i in range(len(refinder)):  # Printing all lines fith RE
            print(refinder[i], '\n')

        if page is True:  # Printing page amount
            print(
                "Number of pages in file - " + str(file.getNumPages()))

    ######################################################
    # converts pdf, returns its text content as a string #
    ######################################################
    def conv(fname, pages=None):
        if pages is None:
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

    ##########################################
    # Saving PDF text to another format file #
    ##########################################
    def save_pdf(pdf, redactor=None, page=None):
        print('extracting text...')
        text = conv(pdf, page)  # get string of text content of pdf
        kur = input('''Do you want to save your PDF file text to txt, word or other type of file?
if you don't want to continue, type any key, execept 'w', 't' and 'o': [w/t/o] ''').lower()
        perev = {'w': 'docx', 'word': 'docx', 't': 'txt', 'txt': 'txt'}
        if kur in perev:
            textFilename = input('enter your destination (with filename): ')

            if textFilename.split('.')[-1] != perev[kur]:
                textFilename = textFilename + '.' + perev[kur]
            textFile = open(textFilename, "w")  # make text file
            textFile.write(text)  # write text to text file
            print('successfully converted to', textFilename)

        elif kur == 'o' or kur == 'other':
            textFilename = input(
                'enter your destination (with filename and file type (.***)): '
            )

            textFile = open(textFilename, "w")  # make text file
            textFile.write(text)  # write text to text file
            print('successfully converted to', textFilename)

        else:
            print('thank you for using!')
        if redactor is not None:
            subprocess.run([redactor, textFilename])
            print('edited', textFilename)
    ################
    # Argparce CLI #
    ################
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
    convert.add_argument('-p', '--pages', action='store', dest='page',
                         help='type page number to convert/edit')
    convert.set_defaults(func=save_pdf)

    reg = subparsers.add_parser('re', help='Find information from PDF text')
    reg.set_defaults(func=rebmf)
    reg.add_argument('-c', '--count', action='store_true', dest='enter',
                     help='count pages from PDF')

    parser.add_argument(
        'pdf', metavar='PDF', type=str,  # Теперь задаем аргументы
        help='PDF-File for opening')

    args = parser.parse_args()  # Parsing args
    # Running functions
    if args.page is not None:
        args.func(args.pdf, args.enter, args.page)
    else:
        args.func(args.pdf, args.enter)
######################
# Analyze exceptions #
######################
except KeyboardInterrupt:
    print('\nThank you for using!')
except FileNotFoundError:
    print('No such PDF file')
except pd.utils.PdfReadError:
    print('Not a PDF file')
except pdfminer.pdfparser.PDFSyntaxError:
    print('Not a PDF file')
except Exception:
    print('''Something went wrong... Please, contact developer:
e-mail: makhonin.a.ru@gmail.com''')
