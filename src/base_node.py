"""
Name:       BaseNode
Purpose:    A base interface
Author:     Chung-Yi, Chi
Created:    2018/11/12
Updated:    2018/11/12
"""

class BaseNode:
    def __init__(self, is_leaf=False):
        self.name = None
        self.data = None
        self.parent = None
        self.attrs = []
        self.children = []
        self.is_leaf = is_leaf # means only text data exist

    def append_child(self, child):
        self.children.append(child)
        self.children[-1].parent = self
