"""
Name:       HTML Parser
Purpose:    A simple HTML Parser. It doesn't meet the w3c standard just a toy.
Author:     Chung-Yi, Chi
Created:    2018/11/13
Updated:    2018/11/13
"""

from enum import Enum
import re

from dom.html_node import HTMLNode


class HTMLParserMode(Enum):
    initial = 1
    before_html = 2
    in_head = 3
    in_body = 4

"""  regular expression rule
copy part of code from https://github.com/python/cpython/blob/3.7/Lib/html/parser.py

'^':    matches the start of the string
'\s':   [ \r\t\n\f] space character 
        I don't know the meaning of '\f'
'&':    the whole matched string
'\x00': 
"""

starttag_open = re.compile('<[a-zA-Z]')
tagfind_tolerant = re.compile(r'([a-zA-Z][^\t\n\r\f />\x00]*)(?:\s|/(?!>))*')
attrfind_tolerant = re.compile(
    r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*'
    r'(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*')
locatestarttagend_tolerant = re.compile(r"""
  <[a-zA-Z][^\t\n\r\f />\x00]*       # tag name
  (?:[\s/]*                          # optional whitespace before attribute name
    (?:(?<=['"\s/])[^\s/>][^\s/=>]*  # attribute name
      (?:\s*=+\s*                    # value indicator
        (?:'[^']*'                   # LITA-enclosed value
          |"[^"]*"                   # LIT-enclosed value
          |(?!['"])[^>\s]*           # bare value
         )
         (?:\s*,)*                   # possibly followed by a comma
       )?(?:\s|/(?!>))*
     )*
   )?
  \s*                                # trailing whitespace
""", re.VERBOSE)
endtag = re.compile('>')
commentclose = re.compile(r'--\s*>')

class BaseParser:
    def reset(self):
        self.lineno = 1 # line number
        self.offset = 0 # data offset
    
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
    

class HTMLParser(BaseParser):
    def __init__(self):
        self.rawdata = ''
        self.root = HTMLNode()
        self.state = HTMLParserMode.initial
        self.cdata_elem = None # style, script
        self.reset()

    def load_text(self, data):
        self.rawdata = self.rawdata + data

    def load_file(self, filepath):
        with open(filepath, 'r') as src:
            self.rawdata = self.rawdata + src.read()
    
    def run(self):
        rawdata = self.rawdata
        i = 0
        length = len(rawdata)
        print("rawdata is", rawdata)
        print("length is", length)

        while i < length:
            # find first label '<'
            j = rawdata.find('<', i)
            if j < 0: # We cannot find the next label '<'
                break
            i = self.updatepos(i, j)

            if i == length: break

            print("i is", i)
            print(rawdata[i:i+4])
            startswith = rawdata.startswith # startswith is a method of string
            if startswith('<', i):
                if starttag_open.match(rawdata, i): # < + letter, i.e. <head ...>
                    k = self.parse_starttag(i)
                elif startswith('<!--', i):
                    k = self.parse_comment(i)
                else:
                    break
                
                if k < 0:
                    print('syntax error')
            
            i = self.updatepos(i, k)
        # end while
        self.rawdata = rawdata[i:]
    
    def parse_starttag(self, i):
        # get the end position of the start tag
        self.__starttag_txt = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]
        
        # parse the content
        attrs = []
        match = tagfind_tolerant.match(rawdata, i+1)
        assert match, 'unexpected call to parse_starttag()'
        
        print(match)
        k = match.end()
        self.lasttag = tag = match.group(1).lower()
        print(endpos, k, self.lasttag)

        return endpos

    def check_for_whole_start_tag(self, i, report=1):
        rawdata = self.rawdata
        m = locatestarttagend_tolerant.match(rawdata, i)
        if m:
            j = m.end()
            next = rawdata[j:j+1]
            if next == ">":
                return j + 1
            if next == "/":
                if rawdata.startswith("/>", j):
                    return j + 2
                if rawdata.startswith("/", j): # buffer boundary
                    return -1
                # else bogus input
                if j > i:
                    return j
                else:
                    return i + 1
            if next == "": # end of input
                return -1
            if next in ("abcdefghijklmnopqrstuvwxyz=/"
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                # end of input in or before attribute value, or we have the
                # '/' from a '/>' ending
                return -1
            if j > i:
                return j
            else:
                return i + 1
        raise AssertionError("we should not get here!")

    def parse_endtag(self):
        pass

    def parse_comment(self, i, report=1):
        print('parse comment')
        raw_data = self.rawdata
        match = commentclose.search(raw_data, i+4)

        if not match:
            return -1
        if report:
            j = match.start()
            self.handle_comment(raw_data[i+4: j])
        
        return match.end()
        
    def handle_comment(self, comment):
        pass
