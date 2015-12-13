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

  # ____________________________________________________________________________
  def union(self, node1, node2, indent = ''):
    ''' Create the union of this node and another node. '''

    # Print a message which nodes are being used.
    self.out.write('{0}UNION({1!s},{2!s}):\n'.format(indent, node1, node2))
    indent += '  '

    # Get the representatives of both nodes.
    rep1 = node1.find_representative()
    rep2 = node2.find_representative()
    self.out.write('{0}n1 <- FIND({1!s}) = {2!s}\n'.format(indent, node1, rep1))
    self.out.write('{0}n2 <- FIND({1!s}) = {2!s}\n'.format(indent, node2, rep2))

    # Create the actual union.
    rep1.find = rep2.find
    tmp = rep1.ccpar | rep2.ccpar
    self.out.write('{0}n1.find <- n2.find = {1!s}\n'.format(indent, rep2.find))
    self.out.write(('{0}n2.ccpar <- n1.ccpar U n2.ccpar = ' \
                    + '{{{1}}} U {{{2}}} = {{{3}}}\n') \
                    .format(indent, ', '.join(str(p) for p in rep1.ccpar), \
                            ', '.join(str(p) for p in rep2.ccpar), \
                            ', '.join(str(p) for p in tmp)))
    self.out.write('{0}n1.ccpar = {{}}\n'.format(indent))
    rep2.ccpar = tmp
    rep1.ccpar = set()

    # End the method.
    indent = indent[:-2]
    self.out.write('{0}DONE\n'.format(indent))

  # ____________________________________________________________________________
  def is_congruent(self, node1, node2, indent = ''):
    ''' Return true if the given nodes are congruent to each other. '''

    self.out.write('{0}CONGRUENT({1!s},{2!s}): '.format(indent, node1, node2))
    indent += '  '

    # The function names must match.
    if node1.fn != node2.fn:
      self.out.write('FALSE\n')
      self.out.write('{0}{1!s}.fn = {2} != {3!s}.fn = {4}\n' \
                     .format(indent, node1, node1.fn, node2, node2.fn))
      return False

    # The number of arguments must match.
    if len(node1.args) != len(node2.args):
      self.out.write('FALSE\n')
      self.out.write('{0}|{1!s}.args| = {2} != |{3!s}.args| = {4}\n' \
                     .format(indent, node2, len(node1.args), node2, \
                             len(node2.args)))
      return False

    # All arguments of the first node must be congruent to their corresponding
    # arguments in the second node.
    number_of_arguments = len(node1.args)
    for n in range(0, number_of_arguments):
      arg1 = node1.args[n]
      arg2 = node2.args[n]
      if arg1.find_representative() != arg2.find_representative():
        self.out.write('FALSE\n')
        self.out.write(('{0}FIND({1!s}.args[{2}]) = {3!s} ' \
                        + '!= FIND({4!s}.args[{5}]) = {6!s}\n') \
                       .format(indent, node1, n, arg1.find_representative(), \
                               node2, n, arg2.find_representative()))
        return False

    # All criteria are okay.
    self.out.write('TRUE\n')
    return True

  # ____________________________________________________________________________
  def merge(self, node1, node2, indent = ''):
    ''' Merge the two given nodes. '''

    # self.out.write(a message which nodes are being merged.
    if indent == '':
      self.out.write('\n')
    self.out.write('{0}MERGE({1!s},{2!s}):\n'.format(indent, node1, node2))
    indent += '  '

    # The two nodes must not already be congruent to each other.
    if node1.find_representative() == node2.find_representative():
      self.out.write('{0}FIND({1!s}) = {2} = FIND({3!s})\n' \
                     .format(indent, node1, node1.find_representative(), node2))
      indent = indent[:-2]
      self.out.write('{0}DONE\n'.format(indent))
      return False

    # Save the parents temporarily.
    parents1 = node1.get_ccpar()
    parents2 = node2.get_ccpar()
    self.out.write('{0}P{1!s} <- {{{2}}}\n'.format(indent, node1, \
                                                   ', '.join(str(p) for p in parents1)))
    self.out.write('{0}P{1!s} <- {{{2}}}\n'.format(indent, node2, \
                                                   ', '.join(str(p) for p in parents2)))

    # Create the union of both nodes.
    self.union(node1, node2, indent)

    # Create the cartesian cross product of parents.
    parents = [(p1, p2) for p1 in parents1 for p2 in parents2]
    self.out.write('{0}P{1} x P{2} = {{{3}}} U {{{4}}} = {{{5}}}:\n' \
                   .format(indent, node1, node2, \
                           ', '.join(str(p) for p in parents1), \
                           ', '.join(str(p) for p in parents2), \
                           ', '.join('({0})'.format(', '.join(str(p) for p in t)) for t in parents)))
    indent += '  '

    # For all elements in the parents list, merge them.
    for tuple in parents:
      p1, p2 = tuple

      # If the two nodes have the same representative, continue with the next
      # tuple.
      if p1.find_representative() == p2.find_representative():
        self.out.write('{0}FIND({1!s}) = {2} = FIND({3!s})\n' \
                       .format(indent, p1, p1.find_representative(), p2))
        continue

      # If both nodes are congruent, merge them.
      if self.is_congruent(p1, p2, indent):
        self.merge(p1, p2, indent)

    # Everything went well.
    indent = indent[:-4]
    self.out.write('{0}DONE\n'.format(indent))
    return True
