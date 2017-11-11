#Program uses PDF Miner to extract text from UN Session Reports

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


#File locations
f53 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/NoProcessing/NoVotingNoSponsorshipData/53.pdf'
f54 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/NoProcessing/Scanned/54.pdf' #scanned pdf, can not parse
f55 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/NoProcessing/Scanned/55.pdf' #scanned pdf, can not parse
f56 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/NoProcessing/Scanned/56.pdf' #scanned pdf, can not parse
f57 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/57.pdf'
f58 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/58.pdf'
f59 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/59.pdf'
f60 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/60.pdf'
f61 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/61.pdf'
f62 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/62.pdf'
f63 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/63.pdf'
f64 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/64.pdf'
f65 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/65.pdf'
f66 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/66.pdf'
f67 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/67.pdf'
f68 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/68.pdf'
f69 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/69.pdf'
f70 = '/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextPDFs/70.pdf'

#Location of Output File
OUTPUT_FILE = '' #Fill in with location of output text file
o = open(OUTPUT_FILE, 'w')
o.write(convert_pdf_to_txt(f69))
o.close()