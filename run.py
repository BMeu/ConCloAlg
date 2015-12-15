#!/home/bastian/.venv/cga/bin/python
# -*- coding: utf-8 -*-

# If called directly execute the algorithm for an example.
if __name__ == '__main__':
  from algorithm.node import Node
  from algorithm import Algorithm

  # Print message.
  print 'Initializing...'


  '''
  # f(g(x)) == g(f(x)) && f(g(f(y))) == x && f(y) == x && g(f(x)) != x

  # Create the nodes.
  node1 = Node(1, 'f')
  node2 = Node(2, 'g')
  node3 = Node(3, 'x')
  node4 = Node(4, 'f')
  node5 = Node(5, 'g')
  node6 = Node(6, 'f')
  node7 = Node(7, 'y')
  node8 = Node(8, 'g')
  node9 = Node(9, 'f')

  # Set the nodes' arguments.
  node1.add_argument(node2)
  node2.add_argument(node3)
  node4.add_argument(node5)
  node5.add_argument(node6)
  node6.add_argument(node7)
  node8.add_argument(node9)
  node9.add_argument(node3)

  # Create the lists to check.
  merge_list = [
    (node1, node8),
    (node4, node3),
    (node6, node3)
  ]
  inequality_list = [
    (node8, node3)
  ]
  atom_list = []

  # Create the nodes.
  node1 = Node(1, 'y')
  node2 = Node(2, 'cons')
  node3 = Node(3, 'cdr')
  node4 = Node(4, 'x')
  node5 = Node(5, 'car')
  node6 = Node(6, 'cons')
  node7 = Node(7, 'car')
  node8 = Node(8, 'cdr')
  node9 = Node(9, 'car')
  node10 = Node(10, 'cdr')
  node11 = Node(11, 'car')
  node12 = Node(12, 'cdr')

  # Set the nodes' arguments.
  node2.add_argument(node3)
  node2.add_argument(node5)
  node3.add_argument(node4)
  node5.add_argument(node4)
  node6.add_argument(node7)
  node6.add_argument(node8)
  node7.add_argument(node1)
  node8.add_argument(node1)
  node9.add_argument(node6)
  node10.add_argument(node6)
  node11.add_argument(node2)
  node12.add_argument(node2)

  # Set the node's find values.
  node9.find = node7
  node10.find = node8
  node11.find = node3
  node12.find = node5

  # Create the lists to check.
  merge_list = [
    (node1, node2),
    (node4, node6)
  ]
  inequality_list = [
    (node3, node5)
  ]
  atom_list = []
  '''

  # Create the nodes.
  node1 = Node(1, 'x')
  node2 = Node(2, 'cons')
  node3 = Node(3, 'x1')
  node4 = Node(4, 'x2')
  node5 = Node(5, 'y')
  node6 = Node(6, 'cons')
  node7 = Node(7, 'cdr')
  node8 = Node(8, 'car')
  node9 = Node(9, 'z')
  node10 = Node(10, 'cons')
  node11 = Node(11, 'cdr')
  node12 = Node(12, 'car')
  node13 = Node(13, 'car')
  node14 = Node(14, 'cdr')
  node15 = Node(15, 'car')
  node16 = Node(16, 'cdr')
  node17 = Node(17, 'car')
  node18 = Node(18, 'cdr')

  # Set the nodes' arguments.
  node2.add_argument(node3)
  node2.add_argument(node4)
  node3.add_argument(node4)
  node6.add_argument(node7)
  node6.add_argument(node8)
  node7.add_argument(node1)
  node8.add_argument(node1)
  node10.add_argument(node11)
  node10.add_argument(node12)
  node11.add_argument(node5)
  node12.add_argument(node5)
  node13.add_argument(node6)
  node14.add_argument(node6)
  node15.add_argument(node2)
  node16.add_argument(node2)
  node17.add_argument(node10)
  node18.add_argument(node10)

  # Set the node's find values.
  node13.find = node7
  node14.find = node8
  node15.find = node3
  node16.find = node4
  node17.find = node11
  node18.find = node12

  # Create the lists to check.
  merge_list = [
    (node1, node2),
    (node5, node6),
    (node9, node10)
  ]
  inequality_list = [
    (node9, node1)
  ]
  atom_list = []

  # Print message.
  print '  ... Done'
  print ''
  print 'Merging...'
  print '####################'

  # Execute the merges.
  alg = Algorithm(merge_list, inequality_list, atom_list)
  alg.merge_nodes()

  # Print message.
  print '####################'
  print '  ... Done'
  print ''
  print 'Checking satisfiabilty...'

  # Check for satisfiability.
  satisfiable = alg.check_satisfiability('  ')

  # Print message.
  if satisfiable:
    print '    => Satisfiable'
  else:
    print '    => Unsatisfiable'
