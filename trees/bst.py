#!/usr/bin/env python

"""
Simple BST implementation accompanied by GUI generated using DOT

For more info on DOT visit http://www.graphviz.org/

There are sleeps introduced in the code so that you can watch the png
image (in your file manager's preview window) while the script is executin.

"""

__author__ = "Orko Garai (orko.garai@gmail.com)"

from collections import OrderedDict
from subprocess import call
from time import sleep


DOT_HEADER = '''\
graph test_tree {
    bgcolor="#8989ff";

    node[style=filled, fillcolor=white, color=gray, fontcolor="#aa0101aa"];
    edge[color=gray];

'''

class Node(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

    def is_leaf(self):
        return self.left is None and self.right is None

class Dot(object):
    header = DOT_HEADER
    footer = '}\n'

    def __init__(self, dot_file_path):
        self.nodes = OrderedDict()
        self.file_path = dot_file_path
        self.lonely_root = False
        self.blank = 0
        self.write()

    def update_node(self, node):
        dot_str = ''
        for child in [node.left, node.right]:
            if child is None:
                dot_str += self._add_blank(node.val)
            else:
                dot_str += self._add_child(node.val, child.val)
        if node.parent is None:
            dot_str += '    %s[root=true];\n' % node.val
        self.nodes[node] = dot_str
        self.write()

    def remove_node(self, node):
        del self.nodes[node]
        self.write()

    def _add_child(self, parent_val, child_val):
        return '    %s -- %s;\n' % (parent_val, child_val)

    def _add_blank(self, parent_val):
        blank = self._get_next_blank()
        dot_str = '    %s -- %s;\n' % (parent_val, blank)
        dot_str += '    %s[shape=point];\n' % blank
        return dot_str

    def _get_next_blank(self):
        self.blank += 1
        return 'blank%s' % self.blank

    def write(self):
        with open(self.file_path, 'w') as f:
            f.write(Dot.header)
            for dot_str in self.nodes.values():
                f.write(dot_str)
            f.write(Dot.footer)
        call(['dot', '-Tpng', 'bst.dot', '-O'])

class Bst(object):
    dot_file_path = 'bst.dot'
    def __init__(self):
        print 'Initializing new BST'
        sleep(5)
        self.root = None
        self._init_graph()

    def _init_graph(self):
        self.dot = Dot(Bst.dot_file_path)

    def is_empty(self):
        return self.root is None

    def insert(self, val):
        print 'Attempting to insert %s' % val
        sleep(5)
        if self.is_empty():
            self.root = Node(val)
            self.dot.update_node(self.root)
            return True
        node = self.root
        while(node is not None):
            if val == node.val:
                return False
            if val < node.val:
                if node.left is None:
                    node.left = Node(val)
                    node.left.parent = node
                    self.dot.update_node(node)
                    self.dot.update_node(node.left)
                    return True
                else:
                    node = node.left
                    continue
            elif val > node.val:
                if node.right is None:
                    node.right = Node(val)
                    node.right.parent = node
                    self.dot.update_node(node)
                    self.dot.update_node(node.right)
                    return True
                else:
                    node = node.right
                    continue

    def find_node(self, val):
        if self.is_empty():
            return None
        node = self.root
        while(node is not None):
            if val == node.val:
                return node
            if val < node.val:
                node = node.left
                continue
            elif val > node.val:
                node = node.right
                continue
        return None

    def get_values(self, start=None):
        '''
        Get values by iterative inorder tree traversal
        '''
        if start is None:
            start = self.root
        else:
            start = self.find_node(start)
        values = []
        if start is None:
            return values
        temp = start.parent
        start.parent = None
        node = start
        while node is not None:
            if node.left is not None\
                    and node.left.val not in values:
                node = node.left
                continue
            if node.val not in values:
                values.append(node.val)
            if node.right is not None\
                    and node.right.val not in values:
                node = node.right
                continue
            node = node.parent
        start.parent = temp
        return values

    def min_node(self, start=None):
        if start is None:
            start = self.root
        node = start
        if node is None:
            return None
        while True:
            if node.left is None:
                return node
            node = node.left

    def max_node(self, start=None):
        if start is None:
            start = self.root
        node = start
        if node is None:
            return None
        while True:
            if node.right is None:
                return node
            node = node.right

    def delete(self, val):
        print 'Attempting to delete %s' % val
        sleep(5)
        node = self.find_node(val)
        if node is None:
            return False
        if node.is_leaf():
            self._remove_leaf(node)
        elif node.right:
            if node.left is None:
                # Only has one right child and no left child
                if node is self.root:
                    #Convert right child to root
                    self.root = node.right
                    node.right.parent = None
                    self.dot.update_node(node.right)
                else:
                    # Has both left and right children
                    self._replace_child(node.parent, node, node.right)
                    self.dot.update_node(node.parent)
                self.dot.remove_node(node)
            else:
                rmin = self.min_node(start=node.right)
                node.val = rmin.val
                self.dot.update_node(node)
                self.dot.update_node(node.parent)
                self._remove_leaf(rmin)
        else:
            #only has a left child and no right child
            if node is self.root:
                #Convert left child to root
                self.root = node.left
                node.left.parent = None
                self.dot.update_node(node.left)
            else:
                self._replace_child(node.parent, node, node.left)
                self.dot.update_node(node.parent)
            self.dot.remove_node(node)
        return True

    def _replace_child(self, parent, child, new_child):
        if child is child.parent.left:
            child.parent.left = new_child
        else:
            child.parent.right = new_child
        new_child.parent = parent

    def _remove_leaf(self, node):
        if node is self.root:
            self.root = None
            self._init_graph()
            return
        if node is node.parent.left:
            node.parent.left = None
        else:
            node.parent.right = None
        self.dot.update_node(node.parent)
        self.dot.remove_node(node)

def empty_check(b):
    assert b.is_empty()
    assert b.root is None
    assert b.min_node() is None
    assert b.max_node() is None
    assert b.find_node(1) is None  # Check non-existing values cannot be found in empty tree
    assert b.get_values() == []
    assert b.delete(1) is False  # Should not succeed deleting from empty tree

def test_bst():
    '''
    Method that tests the Bst class
    '''
    b = Bst()
    empty_check(b)

    # Creating 1 element tree
    assert b.insert(1) is True
    assert not b.is_empty()
    assert b.root.val == 1
    assert b.root.is_leaf()
    assert b.find_node(1).val == 1
    assert b.min_node().val ==  1
    assert b.max_node().val ==  1
    assert b.get_values() == [1]
    assert b.insert(1) is False  # Check that existing values cannot be inserted
    assert b.find_node(2) is None  # Check non-existing values cannot be found in non-empty tree
    b.delete(1)
    empty_check(b)

    # Removing leaf node
    b = Bst()
    b.insert(5)
    b.insert(2)
    b.insert(-4)
    b.insert(3)
    assert b.root.val == 5
    assert not b.root.is_leaf()
    assert b.root.left.val == 2
    assert not b.root.left.is_leaf()
    assert b.root.left.left.val == -4
    assert b.root.left.left.is_leaf()
    assert b.root.left.right.val == 3
    assert b.root.left.right.is_leaf()
    b.delete(-4)
    assert b.root.val == 5
    assert not b.root.is_leaf()
    assert b.root.left.val == 2
    assert not b.root.left.is_leaf()
    assert b.root.left.left is None
    assert b.root.left.right.val == 3
    assert b.root.left.right.is_leaf()

    # Removing node with 1 child
    b = Bst()
    b.insert(5)
    b.insert(2)
    b.insert(18)
    b.insert(-4)
    b.insert(3)
    b.insert(21)
    b.insert(19)
    b.insert(25)
    assert b.get_values() == [-4, 2, 3, 5, 18, 19, 21, 25]
    assert b.get_values(2) == [-4, 2, 3]  # Check subtree values work
    assert b.min_node().val == -4
    assert b.max_node().val == 25
    assert b.root.val == 5
    assert not b.root.is_leaf()
    assert b.root.left.val == 2
    assert not b.root.left.is_leaf()
    assert b.root.left.left.val == -4
    assert b.root.left.left.is_leaf()
    assert b.root.left.right.val == 3
    assert b.root.left.right.is_leaf()
    assert b.root.right.val == 18
    assert not b.root.right.is_leaf()
    assert b.root.right.left is None
    assert b.root.right.right.val == 21
    assert not b.root.right.right.is_leaf()
    assert b.root.right.right.right.val == 25
    assert b.root.right.right.right.is_leaf()
    assert b.root.right.right.left.val == 19
    assert b.root.right.right.left.is_leaf()
    b.delete(18)
    assert b.get_values() == [-4, 2, 3, 5, 19, 21, 25]
    assert b.min_node().val == -4
    assert b.max_node().val == 25
    assert b.root.val == 5
    assert not b.root.is_leaf()
    assert b.root.left.val == 2
    assert not b.root.left.is_leaf()
    assert b.root.left.left.val == -4
    assert b.root.left.left.is_leaf()
    assert b.root.left.right.val == 3
    assert b.root.left.right.is_leaf()
    assert b.root.right.val == 21
    assert not b.root.right.is_leaf()
    assert b.root.right.right.val == 25
    assert b.root.right.right.is_leaf()
    assert b.root.right.left.val == 19
    assert b.root.right.left.is_leaf()
    # Extended Coverage around deletion of node that has single child
    b.delete(25)
    b.delete(21)
    assert b.root.right.val == 19
    b.delete(19)
    assert b.root.right is None
    b.delete(5)
    b.delete(-4)
    assert b.root.val == 2
    assert b.root.left is None
    assert b.root.right.val == 3
    b.delete(2)
    b.delete(3)
    b.insert(2)
    b.insert(-2)
    b.insert(-4)
    b.delete(-2)

    # Removing node with 2 children
    b = Bst()
    b.insert(5)
    b.insert(2)
    b.insert(12)
    b.insert(-4)
    b.insert(3)
    b.insert(9)
    b.insert(21)
    b.insert(19)
    b.insert(25)
    assert b.get_values() == [-4, 2, 3, 5, 9, 12, 19, 21, 25]
    # Check subtrees work
    assert b.get_values(12) == [9, 12, 19, 21, 25]
    assert b.get_values(9) == [9]
    assert b.min_node().val == -4
    assert b.max_node().val == 25
    assert b.root.val == 5
    assert not b.root.is_leaf()
    assert b.root.left.val == 2
    assert not b.root.left.is_leaf()
    assert b.root.left.left.val == -4
    assert b.root.left.left.is_leaf()
    assert b.root.left.right.val == 3
    assert b.root.left.right.is_leaf()
    assert b.root.right.val == 12
    assert not b.root.right.is_leaf()
    assert b.root.right.left.val == 9
    assert b.root.right.left.is_leaf()
    assert b.root.right.right.val == 21
    assert not b.root.right.right.is_leaf()
    assert b.root.right.right.right.val == 25
    assert b.root.right.right.right.is_leaf()
    assert b.root.right.right.left.val == 19
    assert b.root.right.right.left.is_leaf()
    b.delete(12)
    assert b.get_values() == [-4, 2, 3, 5, 9, 19, 21, 25]
    assert b.min_node().val == -4
    assert b.max_node().val == 25
    assert b.root.val == 5
    assert not b.root.is_leaf()
    assert b.root.left.val == 2
    assert not b.root.left.is_leaf()
    assert b.root.left.left.val == -4
    assert b.root.left.left.is_leaf()
    assert b.root.left.right.val == 3
    assert b.root.left.right.is_leaf()
    assert b.root.right.val == 19
    assert not b.root.right.is_leaf()
    assert b.root.right.left.val == 9
    assert b.root.right.left.is_leaf()
    assert b.root.right.right.val == 21
    assert not b.root.right.right.is_leaf()
    assert b.root.right.right.right.val == 25
    assert b.root.right.right.right.is_leaf()
    assert b.root.right.right.left is None

if __name__ == '__main__':
    test_bst()
