"""
Name:       HTMLNode
Purpose:    A structure store the parse result
Author:     Chung-Yi, Chi
Created:    2018/11/13
Updated:    2018/11/13
"""

from base_node import BaseNode

class HTMLNode(BaseNode):
    def vardump(self):
        print(self.name)
        for i in range(len(self.children)):
            self.children[i].vardump()

    def selector(self):
        print('selector')