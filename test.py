#!/home/bastian/.venv/cga/bin/python
# -*- coding: utf-8 -*-

# ______________________________________________________________________________
# Create a coverage report if this script is executed directly.
if __name__ == '__main__':
  from coverage import coverage
  cov = coverage(branch=True, omit=['.cga/*', 'test.py'])
  cov.start()

# ______________________________________________________________________________
import os
import unittest
from StringIO import StringIO
from node import Node
from algorithm import Algorithm

# ______________________________________________________________________________
class TestNode(unittest.TestCase):
  ''' A collection of tests for the entire Node class. '''

  # ____________________________________________________________________________
  def test_init(self):
    ''' Test the constructor. All class members should be set correctly. '''

    # The parameters should be set correctly.
    node = Node(10, 'f')
    self.assertEqual(node.id, 10)
    self.assertEqual(node.fn, 'f')

    # The node should have no arguments and parents and its find value should
    # point to itself.
    self.assertEqual(node.args, [])
    self.assertEqual(node.find, node)
    self.assertEqual(node.ccpar, set())

  # ____________________________________________________________________________
  def test_add_argument(self):
    ''' Test the add_argument method. '''

    # A few nodes.
    node1 = Node(1, 'f')
    node2 = Node(2, 'g')
    node3 = Node(3, 'h')

    # The functions have the following forms: g(f, f), h(f)
    node2.add_argument(node1)
    node2.add_argument(node1)
    node3.add_argument(node1)

    # Now node 2 should have an argument list with two elements, both being
    # node 1 and node 3 should have node 1 as its only argument. Node 1 should
    # have nodes 2 and 3 as its parents, but both only once.
    self.assertEqual(node1.args, [])
    self.assertEqual(node1.ccpar, set([node2, node3]))
    self.assertEqual(node2.args, [node1, node1])
    self.assertEqual(node2.ccpar, set())
    self.assertEqual(node3.args, [node1])
    self.assertEqual(node3.ccpar, set())

    # Create a few nodes.
    node1 = Node(1, 'f')
    node2 = Node(2, 'x')
    node3 = Node(3, 'f')
    node4 = Node(4, 'f')
    node5 = Node(5, 'a')
    node1.add_argument(node2)
    node3.add_argument(node1)
    node4.add_argument(node5)

    self.assertEqual(node1.args, [node2])
    self.assertEqual(node2.args, [])
    self.assertEqual(node3.args, [node1])
    self.assertEqual(node4.args, [node5])
    self.assertEqual(node5.args, [])
    self.assertEqual(node1.ccpar, set([node3]))
    self.assertEqual(node2.ccpar, set([node1]))
    self.assertEqual(node3.ccpar, set())
    self.assertEqual(node4.ccpar, set())
    self.assertEqual(node5.ccpar, set([node4]))

  # ____________________________________________________________________________
  def test_find_representative(self):
    ''' Test the find_representative function. '''

    # Create three nodes. Node 1 points to node 2 which points to node 3.
    # 1 -> 2 -> 3
    node1 = Node(10, 'f')
    node2 = Node(11, 'g')
    node3 = Node(12, 'h')
    node1.find = node2
    node2.find = node3

    # All representatives should be node 3.
    self.assertEqual(node1.find_representative(), node3)
    self.assertEqual(node2.find_representative(), node3)
    self.assertEqual(node3.find_representative(), node3)

  # ____________________________________________________________________________
  def test_get_ccpar(self):
    ''' Test the get_ccpar function. '''

    # Create a few nodes. Node 2 will be the parent of node 1 and node 4 the
    # parent of node 3.
    node1 = Node(10, 'f')
    node2 = Node(11, 'g')
    node3 = Node(20, 'h')
    node4 = Node(21, 'i')
    node1.ccpar = set([node2])
    node2.args = [node1]
    node3.ccpar = set([node4])
    node4.args = [node3]

    # The ccpar values of nodes 2 and 4 should be empty, the one's of nodes 1
    # and 3 should contain their respective parents.
    self.assertEqual(node1.get_ccpar(), set([node2]))
    self.assertEqual(node2.get_ccpar(), set())
    self.assertEqual(node3.get_ccpar(), set([node4]))
    self.assertEqual(node4.get_ccpar(), set())

  # ____________________________________________________________________________
  def test_str(self):
    ''' Test the str function. '''

    # Create a node.
    node = Node(42, 'f')

    # The string representation should be the node's ID as a string.
    self.assertEqual(str(node), '42')

# ______________________________________________________________________________
class TestAlgorithm(unittest.TestCase):
  ''' A collection of tests for the entire Algorithm class. '''

  # ____________________________________________________________________________
  def test_union(self):
    ''' Test the union function. '''
    alg = Algorithm([], [], [], StringIO())

    # Create a few nodes.
    node1 = Node(1, 'f')
    node2 = Node(2, 'x')
    node3 = Node(3, 'f')
    node4 = Node(4, 'f')
    node5 = Node(5, 'a')
    node1.add_argument(node2)
    node3.add_argument(node1)
    node4.add_argument(node5)

    # Create the union of nodes 1 and 2, 3 and 1, 5 and 3, and 4 and 1.
    alg.union(node1, node2)
    alg.union(node3, node1)
    alg.union(node5, node3)
    alg.union(node4, node1)
    self.assertEqual(node1.ccpar, set())
    self.assertEqual(node2.ccpar, set([node1, node3, node4]))
    self.assertEqual(node3.ccpar, set())
    self.assertEqual(node4.ccpar, set())
    self.assertEqual(node5.ccpar, set())
    self.assertEqual(node1.find, node2)
    self.assertEqual(node2.find, node2)
    self.assertEqual(node3.find, node2)
    self.assertEqual(node4.find, node2)
    self.assertEqual(node5.find, node2)

  # ____________________________________________________________________________
  def test_is_congruent(self):
    ''' Test the is_congruent function. '''
    alg = Algorithm([], [], [], StringIO())

    # Create a few nodes.
    node1 = Node(10, 'f')
    node2 = Node(11, 'f')
    node3 = Node(20, 'g')
    node4 = Node(30, 'f')
    node4.args = [node1, node3]
    node3.ccpar = set([node4])
    node5 = Node(40, 'f')
    node5.args = [node1, node2]
    node2.ccpar = set([node5])
    node1.ccpar = set([node4, node5])

    # Nodes 1 and 2 should be congruent to each other.
    self.assertTrue(alg.is_congruent(node1, node2))

    # Nodes 1 and 3 are not congruent because their function names differ.
    self.assertFalse(alg.is_congruent(node1, node3))

    # Nodes 1 and 4 are not congruent because they do not have the same number
    # of arguments.
    self.assertFalse(alg.is_congruent(node1, node4))

    # Nodes 4 and 5 are not congruent because their arguments are not congruent.
    self.assertFalse(alg.is_congruent(node4, node5))

  # ____________________________________________________________________________
  def test_merge(self):
    ''' Test the merge function. '''
    alg = Algorithm([], [], [], StringIO())

    # Create a few nodes.
    node1 = Node(1, 'f')
    node2 = Node(2, 'x')
    node3 = Node(3, 'f')
    node4 = Node(4, 'f')
    node5 = Node(5, 'a')
    node1.args = [node2]
    node2.ccpar = set([node1])
    node3.args = [node1]
    node1.ccpar = set([node3])
    node4.args = [node5]
    node5.ccpar = set([node4])

    # Merge nodes 1 and 2 and nodes 5 and 3.
    self.assertTrue(alg.merge(node1, node2))
    self.assertTrue(alg.merge(node5, node3))

    # Now node 2 should be the representative.
    self.assertEqual(node1.ccpar, set())
    self.assertEqual(node1.find_representative(), node2)
    self.assertEqual(node2.ccpar, set([node1, node3, node4]))
    self.assertEqual(node2.find_representative(), node2)
    self.assertEqual(node3.ccpar, set())
    self.assertEqual(node3.find_representative(), node2)
    self.assertEqual(node4.ccpar, set())
    self.assertEqual(node4.find_representative(), node2)
    self.assertEqual(node5.ccpar, set())
    self.assertEqual(node5.find_representative(), node2)

    # Trying to merge nodes 1 and 2 should return false as they are already
    # congruent to each other.
    self.assertFalse(alg.merge(node1, node2))

# ______________________________________________________________________________
# If this script is called directly, execute the tests.
if __name__ == '__main__':
  # Catch and pass all exceptions or the coverage report cannot be created.
  try:
    unittest.main()
  except:
    pass

  # Stop recording the coverage report, print and save it as HTML.
  cov.stop()
  cov.save()
  basedir = os.path.abspath(os.path.dirname(__file__))
  report_path = 'tmp/coverage'
  print('\n\nCoverage Report:\n')
  cov.report()
  print('HTML version: ' + os.path.join(basedir, report_path + '/index.html'))
  cov.html_report(directory=report_path)
  cov.erase()
