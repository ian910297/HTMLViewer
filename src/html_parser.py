"""
Name:       HTML Parser
Purpose:    A simple HTML Parser. It doesn't meet the w3c standard just a toy.
Author:     Chung-Yi, Chi
Created:    2018/11/13
Updated:    2018/11/13
"""

from enum import Enum
import re

from base_parser import BaseParser
from html_node import HTMLNode

class HTMLParserMode(Enum):
    initial = 1
    strip_space = 2
    allow_pure_text = 3 # in text tag
    

""" 
copy part of code from https://github.com/python/cpython/blob/3.7/Lib/html/parser.py
the standar is too complex to learn, so I write a simple regular rule.
the following is some knowledge about regular expression
you can pratice regular expresiion on https://regex101.com/

'^':    matches the start of the string
'$':    matches the end of the string
'&':    the whole matched string
[^abc]: a character except a, b, c
'\s':   [ \r\t\n\f] space character 
        I don't know the meaning of '\f'
'\w':   [a-zA-Z0-9_]
'\W':   [^a-zA-Z0-9_]
'\x00': a kind of space character
'?:':   text: "Chung-Yi, Chi"  pattern: "Chung-Yi, (?:Chi)"   Ans: "Chung-Yi, Chi"
'?=':   text: "Chung-Yi, Chi"  pattern: "Chung-Yi, (?=Chi)"   Ans: "Chung-Yi, "
'?!':   text: "Chung-Yi, Wu"   pattern: "Chung-Yi, (?!Chi)"   Ans: "Chung-Yi, "
'?<=':  text: "Chung-Yi, Chi"  pattern: "(?<=Chung-Yi, )Chi"  Ans: "Chi"
"""

starttag_open = re.compile(r'<[a-zA-Z]')
starttag_get = re.compile(r'(?<=<)[a-zA-Z]+')
starttag_open_close = re.compile(r"""
    <[a-zA-Z]+                  # tag name
    (\s*                        # optional whitespace before attribute name
        ([a-zA-Z\-]+=           # attr name
            (?:                 # attr value                 
             '[^']*'            # use [^'] to allow any character except '
            |"[^"]*"
            )
        )
        (?=\s*)*
    )*
    \s*                         # trailing whitespace
    >                           # close tag
""", re.VERBOSE)
attrname_get = re.compile(r'\s*[a-zA-Z\-]*(?==)')
attrvalue_get = re.compile(r"""
    (?:                         # attr value                 
     '[^']*'                    # use [^'] to allow any character except '
    |"[^"]*"
    )
""", re.VERBOSE)
endtag_get = re.compile(r'(?<=</)[a-zA-Z]+')
endtag_close = re.compile(r'(?<=</)[a-zA-Z]+\s*>')
commentclose = re.compile(r'--\s*>')

class HTMLParser(BaseParser):
    def __init__(self):
        self.rawdata = ''
        self.root = None
        self.walker = None
        self.walker_state = HTMLParserMode.initial
        self.opentag_stack = []
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
        #print("rawdata is", rawdata)
        #print("length is", length)

        while i < length:
            # find first label '<'
            print("opentag_stack:", self.opentag_stack)
            j = rawdata.find('<', i)
            if j < 0: # We cannot find the next label '<'
                break
            i = self.updatepos(i, j)

            if i == length: break

            startswith = rawdata.startswith # startswith is a method of string
            if startswith('<', i):
                if starttag_open.match(rawdata, i): # < + letter, i.e. <head ...>
                    k, node = self.parse_starttag(i)

                    if self.root is None: # set the root
                        self.root = node
                        self.walker = node
                    
                    self.walker = node
                        
                elif startswith('</', i):
                    k = self.parse_endtag(i)
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
        rawdata = self.rawdata

        # get the end position of the start tag
        end = starttag_open_close.match(rawdata, i)
        endpos = end.end()
        if endpos < 0:
            return endpos
        
        print("content:", rawdata[i:endpos])
        print("i:", i, "endpos:", endpos)

        # get tag name
        tag = starttag_get.search(rawdata, i)
        tagname = tag.group()
        i = tag.end()
        print("i:", i, "endpos:", endpos)

        # append tag
        self.opentag_stack.append(tagname)
        node = HTMLNode()
        node.tagname = tagname

        # parse attr
        while True:
            attrname = attrname_get.search(rawdata, i)
            if (attrname is None) or (attrname.start() > endpos):
                break
            print("attrname:", attrname.group())
            
            i = attrname.end()

            attrvalue = attrvalue_get.search(rawdata, i)
            if (attrvalue is None):
                break
            print("attrvalue:", attrvalue.group())

            i = attrvalue.end()
        
        return endpos, node

    def parse_endtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i+2] == "</", "unexpected call to parse_endtag"
        
        # get the end position of the end tag
        end = endtag_close.search(rawdata, i)
        endpos = end.end()

        tag = endtag_get.search(rawdata, i)
        tagname = tag.group().strip()
        if self.opentag_stack[-1] == tagname:
            self.opentag_stack.pop()
        else:
            print('tag match error')
        
        return endpos
        

    def parse_comment(self, i, report=1):
        rawdata = self.rawdata
        match = commentclose.search(rawdata, i+4)

        if not match:
            return -1
        if report:
            j = match.start()
            self.handle_comment(rawdata[i+4: j])
        
        return match.end()
        
    def handle_comment(self, comment):
        pass
