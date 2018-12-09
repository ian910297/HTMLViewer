"""
Name:       Base Parser
Purpose:    A base class for parser
Author:     Chung-Yi, Chi
Created:    2018/11/16
"""

class BaseParser:
    def reset(self):
        self.lineno = 1 # line number
        self.offset = 0 # data offset
    
    def load_text(self, data):
        self.rawdata = self.rawdata + data

    def load_file(self, filepath):
        with open(filepath, 'r') as src:
            self.rawdata = self.rawdata + src.read()
    
    def getpos(self):
        return self.lineno, self.offset

    def updatepos(self, i, j):
        rawdata = self.rawdata
        nlines = rawdata.count("\n", i, j)

        if nlines:
            self.lineno = self.lineno + nlines
            pos = rawdata.rindex("\n", i, j)
            self.offset = j - (pos+1)
        else:
            self.offset = self.offset + j - 1
        
        return j