# -*- coding: utf-8 -*-

import sys
from node import Node

class Algorithm(object):
  ''' The implementation of the congruence closure algorithm. '''

  # ____________________________________________________________________________
  def __init__(self, merge_list = [], inequality_list = [], atom_list = [], \
               out = sys.stdout):
    ''' Initialize this class and set the output. '''
    self.out = out
    self.merge_list = merge_list
    self.inequality_list= inequality_list
    self.atom_list = []

  # ____________________________________________________________________________
  def merge_nodes(self):
    ''' Merge all nodes in the merge list. '''
    for tuple in self.merge_list:
      node1, node2 = tuple
      self.merge(node1, node2)

  # ____________________________________________________________________________
  def check_satisfiability(self, indent = ''):
    ''' Check the inequality and atom lists for contradictions. '''

    # Check the inequality list.
    for tuple in self.inequality_list:
      node1, node2 = tuple
      if node1.find_representative() == node2.find_representative():
        self.out.write('{0}FIND({1!s}) = {2!s} = FIND({3!s})\n' \
                       .format(indent, node1, node1.find_representative(),
                               node2))
        return False

      # Fine for now, just print a message
      self.out.write('{0}FIND({1!s}) = {2!s} != FIND({3!s}) = {4!s}\n' \
                     .format(indent, node1, node1.find_representative(),
                             node2, node2.find_representative()))

    # TODO: Implement.
    for tuple in self.atom_list:
      node1, node2 = tuple

    # No contradictions found.
    return True
