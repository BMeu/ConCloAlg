# -*- coding: utf-8 -*-

import unittest
from algorithm.node import Node


class TestNode(unittest.TestCase):
    """
        A collection of tests for the entire Node class.
    """


    def test_init(self):
        node1 = Node('f')
        self.assertEqual(node1.name, 'f')
        self.assertEqual(node1.arguments, [])
        self.assertEqual(node1.find, node1)
        self.assertEqual(node1.parents, set())

        node2 = Node('g', [node1])
        self.assertEqual(node2.name, 'g')
        self.assertEqual(node2.arguments, [node1])
        self.assertEqual(node2.find, node2)
        self.assertEqual(node2.parents, set())
        self.assertEqual(node1.parents, {node2})


    def test_add_single_parent(self):
        node1 = Node('f')
        node2 = Node('g')
        node3 = Node('h')

        self.assertEqual(node1.parents, set())
        self.assertEqual(node2.parents, set())
        self.assertEqual(node3.parents, set())

        node1.add_single_parent(node2)
        self.assertEqual(node1.parents, {node2})

        node1.add_single_parent(node3)
        self.assertEqual(node1.parents, {node2, node3})


    def test_get_class_representative(self):
        node1 = Node('f')
        node2 = Node('f')
        node3 = Node('f')
        node4 = Node('f')

        # Without setting anything else, all nodes are their own
        # representatives.
        self.assertEqual(node1.get_class_representative(), node1)
        self.assertEqual(node2.get_class_representative(), node2)
        self.assertEqual(node3.get_class_representative(), node3)
        self.assertEqual(node4.get_class_representative(), node4)

        node1.find = node2
        self.assertEqual(node1.get_class_representative(), node2)
        self.assertEqual(node2.get_class_representative(), node2)
        self.assertEqual(node3.get_class_representative(), node3)
        self.assertEqual(node4.get_class_representative(), node4)

        node3.find = node4
        self.assertEqual(node1.get_class_representative(), node2)
        self.assertEqual(node2.get_class_representative(), node2)
        self.assertEqual(node3.get_class_representative(), node4)
        self.assertEqual(node4.get_class_representative(), node4)

        node2.find = node3
        self.assertEqual(node1.get_class_representative(), node4)
        self.assertEqual(node2.get_class_representative(), node4)
        self.assertEqual(node3.get_class_representative(), node4)
        self.assertEqual(node4.get_class_representative(), node4)


    def test_get_class_parents(self):
        node1 = Node('f')
        node2 = Node('f', [node1])
        node3 = Node('f')
        node4 = Node('f', [node3])

        # Without setting anything else, there are no parents.
        self.assertEqual(node1.get_class_parents(), {node2})
        self.assertEqual(node2.get_class_parents(), set())
        self.assertEqual(node3.get_class_parents(), {node4})
        self.assertEqual(node4.get_class_parents(), set())

        # Attention: Changing the find value will not change the parents sets!
        node2.find = node1
        node4.find = node3
        self.assertEqual(node1.get_class_parents(), {node2})
        self.assertEqual(node2.get_class_parents(), {node2})
        self.assertEqual(node3.get_class_parents(), {node4})
        self.assertEqual(node4.get_class_parents(), {node4})

        node3.find = node1
        self.assertEqual(node1.get_class_parents(), {node2})
        self.assertEqual(node2.get_class_parents(), {node2})
        self.assertEqual(node3.get_class_parents(), {node2})
        self.assertEqual(node4.get_class_parents(), {node2})


    def test_union(self):
        # Create a few nodes.
        node1 = Node('f')
        node2 = Node('x')
        node3 = Node('f')
        node4 = Node('f')
        node5 = Node('a')
        node1.add_argument(node2)
        node3.add_argument(node1)
        node4.add_argument(node5)

        # Create the union of nodes 1 and 2, 3 and 1, 5 and 3, and 4 and 1.
        node1.union(node2)
        node3.union(node1)
        node5.union(node3)
        node4.union(node1)
        self.assertEqual(node1.parents, set())
        self.assertEqual(node2.parents, {node1, node3, node4})
        self.assertEqual(node3.parents, set())
        self.assertEqual(node4.parents, set())
        self.assertEqual(node5.parents, set())
        self.assertEqual(node1.find, node2)
        self.assertEqual(node2.find, node2)
        self.assertEqual(node3.find, node2)
        self.assertEqual(node4.find, node2)
        self.assertEqual(node5.find, node2)


    def test_merge(self):
        # Create a few nodes.
        node1 = Node('f')
        node2 = Node('x')
        node3 = Node('f')
        node4 = Node('f')
        node5 = Node('a')
        node1.add_argument(node2)
        node3.add_argument(node1)
        node4.add_argument(node5)

        # Merge nodes 1 and 2 and nodes 5 and 3.
        self.assertTrue(node1.merge(node2))
        self.assertTrue(node5.merge(node3))

        # Now node 2 should be the representative.
        self.assertEqual(node1.parents, set())
        self.assertEqual(node1.find, node2)
        self.assertEqual(node2.parents, {node1, node3, node4})
        self.assertEqual(node2.find, node2)
        self.assertEqual(node3.parents, set())
        self.assertEqual(node3.find, node2)
        self.assertEqual(node4.parents, set())
        self.assertEqual(node4.find, node2)
        self.assertEqual(node5.parents, set())
        self.assertEqual(node5.find, node2)

        # Trying to merge nodes 1 and 2 should return false as they are already
        # congruent to each other.
        self.assertFalse(node1.merge(node2))


    def test_equality(self):
        # Create a few nodes.
        node1 = Node('f')
        node2 = Node('f')
        node3 = Node('g')
        node4 = Node('f')
        node4.add_argument(node1)
        node4.add_argument(node3)
        node5 = Node('f')
        node5.add_argument(node1)
        node5.add_argument(node2)

        # Nodes 1 and 2 should be equal to each other.
        self.assertEqual(node1, node2)

        # Nodes 1 and 3 are not equal because their function names differ.
        self.assertNotEqual(node1, node3)

        # Nodes 1 and 4 are not equal because they do not have the same number
        # of arguments.
        self.assertNotEqual(node1, node4)

        # Nodes 4 and 5 are not equal because their arguments are not congruent.
        self.assertNotEqual(node4, node5)


    def test_add_argument(self):
        # A few nodes.
        node1 = Node('f')
        node2 = Node('g')
        node3 = Node('h')

        # The functions have the following forms: g(f, f), h(f)
        node2.add_argument(node1)
        node2.add_argument(node1)
        node3.add_argument(node1)

        # Now node 2 should have an argument list with two elements, both being
        # node 1 and node 3 should have node 1 as its only argument. Node 1
        # should have nodes 2 and 3 as its parents, but both only once.
        self.assertEqual(node1.arguments, [])
        self.assertEqual(node1.parents, {node2, node3})
        self.assertEqual(node2.arguments, [node1, node1])
        self.assertEqual(node2.parents, set())
        self.assertEqual(node3.arguments, [node1])
        self.assertEqual(node3.parents, set())

        # Create a few nodes.
        node1 = Node('f')
        node2 = Node('x')
        node3 = Node('f')
        node4 = Node('f')
        node5 = Node('a')
        node1.add_argument(node2)
        node3.add_argument(node1)
        node4.add_argument(node5)

        self.assertEqual(node1.arguments, [node2])
        self.assertEqual(node2.arguments, [])
        self.assertEqual(node3.arguments, [node1])
        self.assertEqual(node4.arguments, [node5])
        self.assertEqual(node5.arguments, [])
        self.assertEqual(node1.parents, {node3})
        self.assertEqual(node2.parents, {node1})
        self.assertEqual(node3.parents, set())
        self.assertEqual(node4.parents, set())
        self.assertEqual(node5.parents, {node4})
