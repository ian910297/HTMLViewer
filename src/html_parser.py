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

    def run(self):
        rawdata = self.rawdata
        i = 0
        length = len(rawdata)
        #print("rawdata is", rawdata)
        #print("length is", length)

        while i < length:
            # find first label '<'
            j = rawdata.find('<', i)
            if j < 0: # We cannot find the next label '<'
                break
            
            # store data content to node
            if self.walker_state is not HTMLParserMode.initial:
                node = self.parse_content(i, j)

                if node is not None:
                    self.walker.append_child(node)

            i = self.updatepos(i, j)

            if i == length: break

            startswith = rawdata.startswith # startswith is a method of string
            if startswith('<', i):
                if starttag_open.match(rawdata, i): # < + letter, i.e. <head ...>
                    k, node = self.parse_starttag(i)

                    if self.root is None: # build the dom tree
                        self.root = node
                        self.walker = node
                    else:
                        self.walker.append_child(node)
                        self.walker.children[-1].set_parent(self.walker)
                        self.walker = self.walker.children[-1]
                    
                    self.walker_state = HTMLParserMode.allow_pure_text
                elif startswith('</', i):
                    k = self.parse_endtag(i)

                    if self.walker.parent is not None:
                        self.walker = self.walker.parent
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

        # get tag name
        tag = starttag_get.search(rawdata, i)
        tagname = tag.group()
        i = tag.end()

        # append tag
        self.opentag_stack.append(tagname)
        node = HTMLNode()
        node.name = tagname

        # parse attr
        while True:
            attrname = attrname_get.search(rawdata, i)
            if (attrname is None) or (attrname.start() > endpos):
                break

            i = attrname.end()

            attrvalue = attrvalue_get.search(rawdata, i)
            if (attrvalue is None):
                break
            
            node = self.parse_attr(attrname.group().strip(), attrvalue.group(), node)

            i = attrvalue.end()
        
        return endpos, node

    def parse_attr(self, attrname, attrvalue, node):
        if attrname == 'id':
            node.id = attrvalue
        elif attrname == 'class':
            classes = attrvalue[1: len(attrvalue)-1]
            classes = classes.split(' ')
            node.classes = classes

        return node

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
    
    def parse_content(self, i, j):
        rawdata = self.rawdata
        node = None
        text = rawdata[i:j]

        # another impl but it would remove the trailing space at the begin and the end
        # ' '.join(text.split())
        text = re.sub('\s+', ' ', text)

        if not text.isspace() and len(text) > 0:
            node = HTMLNode(True)
            node.name = text
            node.data = text

        return node
        
        
    def handle_comment(self, comment):
        pass
