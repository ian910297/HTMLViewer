"""
Name:       HTMLNode
Purpose:    A structure store the parse result
Author:     Chung-Yi, Chi
Created:    2018/11/13
Updated:    2018/11/13
"""

class HTMLNode():
    def __init__(self, is_leaf=False):
        # attributes
        self.name = None
        self.data = None
        self.attrs = []

        # tree
        self.children = []
        self.parent = None
        self.is_leaf = is_leaf # means only text data exist

    def append_child(self, child):
        self.children.append(child)
    
    def set_parent(self, parent):
        self.parent = parent
    
    def vardump(self):
        print('tagname:', self.name)
        for i in range(len(self.children)):
            self.children[i].vardump()
        print('data:', self.data)
        