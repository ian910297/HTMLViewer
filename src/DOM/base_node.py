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
    nodes = []
    attrs = []
    __is_leaf = False

    def AppendNode(self, node):
        self.nodes.append(node)
