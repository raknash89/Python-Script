import PyPDF2

FILE_PATH = 'D:\gowrishankar.p\Python Script\py_input\Aadhar.pdf'

with open(FILE_PATH, mode='rb') as f:

    reader = PyPDF2.PdfFileReader(f)

    page = reader.getPage(0)

    print(page.extractText())