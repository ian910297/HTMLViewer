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

class HTMLParser:
    def __init__(self):
        self.source = None
        self.root = None
        self.state = HTMLParserMode.initial
    
    def LoadRawText(self, raw_text):
        self.source = raw_text

    def LoadFile(self, filepath):
        with open(filepath, 'r') as src:
            self.source = src.read()

    def Parse(self):
        self.root = HTMLNode()
        
        buffer_stack = []
        text = self.source
        html_label_regex = r"<[a-zA-Z]+>"
        buffer_stack.append(re.split(html_label_regex, text))
        

        print(self.state)
        #for i in range(len(buffer_stack[0])):
        #    print(buffer_stack[0][i])
        #print(buffer_stack)
