"""This module demonstrates inheritance, abstract base classes.

Additionally, this module demonstrates an understanding of binary
encoding, and binary arithmetic. This module contains five classes,
two of which is written for this assignment. They are MultiLinkNode and
Neurode, an abstract base class and a child class, respectively.
 """

from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
import random
import copy
import math


class MultiLinkNode(ABC):
    class Side(Enum):
        """Identify the relationships between nodes."""
        UPSTREAM = "UPSTREAM"
        DOWNSTREAM = "DOWNSTREAM"

    def __init__(self):
        """Implement Multilinknode class."""
        self._reporting_nodes = {self.Side.UPSTREAM: 0,
                                 self.Side.DOWNSTREAM: 0}
        self._reference_value = {self.Side.UPSTREAM: 0,
                                 self.Side.DOWNSTREAM: 0}
        self._neighbors = {self.Side.UPSTREAM: [],
                           self.Side.DOWNSTREAM: []}

    def __str__(self):
        upstream_ids = ""
        downstream_ids = ""
        for upstream_neighbors in self._neighbors[MultiLinkNode.Side.UPSTREAM]:
            upstream_ids += f"{id(upstream_neighbors)}, "

        for downstream_neighbors in (
                self._neighbors)[MultiLinkNode.Side.DOWNSTREAM]:
            downstream_ids += f"{id(downstream_neighbors)}, "

        string = (f"Node ID: {id(self)} "
                  f"\n\nUpstream Neighbors' IDs: [{upstream_ids}]"
                  f"\nDownstream Neighbors' IDs: [{downstream_ids}]")
        return string


    @ abstractmethod
    def _process_new_neighbor(self, node: MultiLinkNode, side: Side):
        """Implemented in the Neurode class.

        :param MultiLinkeNode: Neighboring node to be added
        :param Side side: Where node exists relative to self.
        """
        pass

    def reset_neighbors(self, nodes: list, side: MultiLinkNode.Side):
        """Take in a list and side, store references to linked nodes"""

        self._neighbors[side] = []
        copy_of_nodes = copy.copy(nodes)

        if side is MultiLinkNode.Side.UPSTREAM:
            self._neighbors[MultiLinkNode.Side.UPSTREAM] = copy_of_nodes
        elif side is MultiLinkNode.Side.DOWNSTREAM:
            self._neighbors[MultiLinkNode.Side.DOWNSTREAM] = copy_of_nodes
        for node in nodes:
            self._process_new_neighbor(node, side)
        number_of_nodes = len(nodes)
        self._reference_value[side] = (math.pow(2, number_of_nodes) - 1)


class Neurode(MultiLinkNode):
    """Inherit and implement MultiLinkNode."""

    _learning_rate = .05

    @property
    def learning_rate(self):
        """Return the learning rate."""
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, new_learning_rate):
        """Set a new learning rate.

        :param new_learning_rate: int
        """
        try:
            if new_learning_rate >= 0 and new_learning_rate <= 1:
                self._learning_rate = new_learning_rate
            else:
                print("Please enter a number between 0 and 1")
        except ValueError:
            print("Please enter a number")

    def __init__(self):
        """Implement the Neurode class."""
        self._value = 0
        self._weights = {}
        super().__init__()

    @property
    def value(self):
        """Return value."""
        return self._value

    def get_weight(self, node: Neurode):
        """Return weights.

        :param node: Neurode
        """
        return self._weights[node]

    def _process_new_neighbor(self, node: Neurode, side: MultiLinkNode.Side):
        """Add node as a key to weights and generate a random weight.

        :param node: Neurode
        :param side: Side enum
        """
        if side is MultiLinkNode.Side.UPSTREAM:
            self._weights[node] = random.random()

    def _check_in(self, node: Neurode, side: MultiLinkNode.Side):
        """Determine if all nodes have reported.

        Return true if all nodes have reported, false if not.
        :param node: Neurode
        :param side: Side enum
        :return: boolean
        """
        # Below is the corrected version
        index_of_node = self._neighbors[side].index(node)
        self._reporting_nodes[side] =\
            self._reporting_nodes[side] | 1 << index_of_node
        if self._reporting_nodes[side] == self._reference_value[side]:
            self._reporting_nodes[side] = 0
            return True
        else:
            return False

        # Below is the OG version
        # index_of_node = self._neighbors[side].index(node)
        # if side is MultiLinkNode.Side.UPSTREAM:
        #     self._reporting_nodes[MultiLinkNode.Side.UPSTREAM] \
        #         = math.pow(2, index_of_node + 1) - 1
        # elif side is MultiLinkNode.Side.DOWNSTREAM:
        #     self._reporting_nodes[MultiLinkNode.Side.DOWNSTREAM] \
        #         = math.pow(2, index_of_node + 1) - 1

        # if self._reporting_nodes[side] == self._reference_value[side]:
        #     self._reporting_nodes[side] = 0
        #     return True
        # else:
        #     return False
