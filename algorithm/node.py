# -*- coding: utf-8 -*-


class Node(object):
    """
        This class represents a node of a DAG for the DAG based decision
        procedure for T_E formulas.
    """

    # Each node object will have a unique ID. The value will be incremented
    # by the
    # constructor to keep the ID unique.
    __last_ID = 0


    def __init__(self, name, arguments = None):
        """
            Initialize the node.

            :type arguments: list[Node]
        """

        Node.__last_ID += 1

        self._id = Node.__last_ID  # Int
        self._fn = name  # String
        self._find = self  # Node
        self._ccpar = set()  # Set

        if arguments is None:  # List
            self._args = []
        else:
            self._args = arguments

        # Set this node as the parent for all arguments.
        for argument in self._args:
            argument.add_single_parent(self)


    @property
    def name(self):
        """
            :rtype: str
        """

        return self._fn


    @property
    def arguments(self):
        """
            :rtype: list[Node]
        """

        return self._args


    @property
    def find(self):
        """
            :rtype: Node
        """

        return self._find


    @find.setter
    def find(self, value):
        """
            :type value: Node
        """

        self._find = value


    @property
    def parents(self):
        """
            :rtype: set(Node)
        """
        return self._ccpar


    @parents.setter
    def parents(self, value):
        """
            :type value: set(Node)
        """
        self._ccpar = value


    def add_single_parent(self, parent):
        """
            Add a node to the list of parents.

            :type parent: Node
        """

        self._ccpar.add(parent)


    def get_class_representative(self):
        """
            Return the representative of this node's equivalence class.

            :rtype: Node
        """

        if self._find == self:
            return self

        return self._find.get_class_representative()


    def get_class_parents(self):
        """
            Return all parents of all nodes in this node's equivalence class.

            :rtype: set(Node)
        """

        return self._find.get_class_representative().parents


    def union(self, other):
        """
            Create the union of this node and another node.

            :type other: Node
        """

        # Get the representatives of both nodes.
        rep1 = self.get_class_representative()
        rep2 = other.get_class_representative()

        # Create the actual union on the representatives.
        rep1.find = rep2.find
        rep2.parents = rep1.parents | rep2.parents
        rep1.parents = set()


    def merge(self, other):
        """
            Merge the two given nodes.

            :type other: Node
        """

        # The two nodes must not already be congruent to each other.
        if self.get_class_representative() == other.get_class_representative():
            return False

        # Save the parents temporarily because they will be overwritten
        # before the
        # current values will be used.
        parents1 = self.parents
        parents2 = other.parents

        self.union(other)

        # Merge all possible parent combinations.
        parents = [(p1, p2) for p1 in parents1 for p2 in parents2]
        for parent_tuple in parents:
            p1, p2 = parent_tuple

            # If the two nodes have the same representative, continue with
            # the next
            # tuple.
            if p1.get_class_representative() == p2.get_class_representative():
                continue

            # If both nodes are congruent, merge them.
            if p1 == p2:
                p1.merge(p2)

        return True


    def __eq__(self, other):
        """
            Return True if two nodes are equal to each other. They are
            considered equal if their function names match, they have the
            same number of arguments and each argument in one node is equal
            to its corresponding argument in the other node.

            :type other: Node
            :rtype: bool
        """

        # The function names must match.
        if self.name != other.name:
            return False

        # The number of arguments must match.
        if len(self.arguments) != len(other.arguments):
            return False

        # All arguments of the first node must be congruent to their
        # corresponding
        # arguments in the second node.
        number_of_arguments = len(self.arguments)
        for n in range(0, number_of_arguments):
            arg1 = self.arguments[n]
            arg2 = other.arguments[n]

            if arg1.get_class_representative() != \
                    arg2.get_class_representative():
                return False

        return True


    def __ne__(self, other):
        """
            Return False if two nodes are equal to each other.

            :type other: Node
            :rtype: bool
        """
        return not self.__eq__(other)


    def add_argument(self, argument):
        """
            Add a node as this node's arguments and add this node to the
            argument's set of parents.

            :type argument: Node
        """
        self.arguments.append(argument)
        argument.parents.add(self)


    def __repr__(self):
        """
            :rtype: str
        """
        return '{0!s}:{1}'.format(self._id, self._fn)
