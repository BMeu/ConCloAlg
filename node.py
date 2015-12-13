# -*- coding: utf-8 -*-

# ______________________________________________________________________________
class Node(object):
  ''' This class represents a node of a DAG for the DAG based decision procedure
      for T_E formulas. '''

  # ____________________________________________________________________________
  def __init__(self, id, fn):
    ''' Initialize the node. '''
    self.id = id          # Int
    self.fn = fn          # String
    self.args = []        # List
    self.find = self      # Node
    self.ccpar = set()    # Set

  # ____________________________________________________________________________
  def add_argument(self, argument):
    ''' Add a node as this node's arguments and add this node to the argument's
        set of parents. '''
    self.args.append(argument)
    argument.ccpar.add(self)

  # ____________________________________________________________________________
  def find_representative(self):
    ''' Return the representative of a node's equivalence class. '''

    # If a node's ID is the same as its find value, it is the representative.
    if self == self.find:
      return self
    else:
      return (self.find).find_representative()

  # ____________________________________________________________________________
  def get_ccpar(self):
    ''' Return the parents of all nodes in this congruence class. '''
    return (self.find_representative()).ccpar

  # ____________________________________________________________________________
  def __str__(self):
    return str(self.id)
