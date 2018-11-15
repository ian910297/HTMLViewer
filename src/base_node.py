"""
Name:       BaseNode
Purpose:    A base interface
Author:     Chung-Yi, Chi
Created:    2018/11/12
Updated:    2018/11/12
"""

class BaseNode:
    name = None
    data = None
    parent = None
    attrs = []
    children = []
    __is_leaf = False

    def append_child(self, child):
        self.children.append(child)
        self.children[-1].parent = self
