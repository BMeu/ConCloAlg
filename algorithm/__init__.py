# -*- coding: utf-8 -*-

from node import Node


class Algorithm(object):
    """
        The implementation of the congruence closure algorithm.
    """


    def __init__(self, merge_list = None, inequality_list = None):
        """
            Initialize this class.

            :type merge_list: list[(Node, Node)]
            :type inequality_list: list[(Node, Node)]
        """

        if not merge_list:
            self.merge_list = []
        else:
            self.merge_list = merge_list

        if not inequality_list:
            self.inequality_list = []
        else:
            self.inequality_list = inequality_list


    def merge_nodes(self):
        """
            Merge all nodes in the merge list.
        """

        for mergees in self.merge_list:
            node1, node2 = mergees
            node1.merge(node2)


    def check_satisfiability(self):
        """
            Check the inequality and atom lists for contradictions.

            :rtype: bool
        """

        # Check the inequality list.
        for inequality in self.inequality_list:
            node1, node2 = inequality
            if node1.get_class_representative() == \
               node2.get_class_representative():
                return False

        # TODO: Implement checking atoms for T_cons.

        # No contradictions found.
        return True
