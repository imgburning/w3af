'''
pdf.py

Copyright 2006 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
import StringIO
# Added this try/except to fix a bug in debian/ubuntu.
try:
    import extlib.pyPdf.pyPdf as pyPdf
except:
    import pyPdf

from plugins.grep.password_profiling_plugins.base_plugin import BasePwdProfilingPlugin
from core.data.getResponseType import isPDF


class pdf(BasePwdProfilingPlugin):
    '''
    This plugin creates a map of possible passwords by reading pdf documents.

    @author: Andres Riancho (andres.riancho@gmail.com)
    '''

    def __init__(self):
        BasePwdProfilingPlugin.__init__(self)

    def _get_pdf_content(self, document_str):
        '''
        Iterate through all PDF pages and extract text
        
        @return: The page content
        '''
        content = ''

        document_io = StringIO.StringIO(document_str)
        pdf = pyPdf.PdfFileReader(document_io)

        for i in range(0, pdf.getNumPages()):
            content += pdf.getPage(i).extractText() + '\n'
        
        content = " ".join(content.replace(u'\xa0', u' ').strip().split())
        return content.split()

    def get_words(self, response):
        '''
        Get words from the pdf document.

        @param response: In most common cases, an html. Could be almost
                         anything, if we are lucky, it's a PDF file.
        @return: A map of strings:repetitions.
        '''
        res = None
        words = []

        if isPDF(response.get_headers()):
            try:
                words = self._get_pdf_content(response.get_body())
            except:
                return None
            else:
                res = {}
                for w in words:
                    if w in res:
                        res[w] += 1
                    else:
                        res[w] = 1

        return res
