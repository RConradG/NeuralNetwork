"""This module creates the FFNeurode class that will perform
calculations once all upstream neurodes contain information. It will
then push that information forward and wait until all upstream nodes
have information and repeat the above process."""


from __future__ import annotations
from Neurode import Neurode
import math

class FFNeurode(Neurode):

    def __init__(self):
        """Implement the FFNeurode class."""
        super().__init__()

    @staticmethod
    def _sigmoid(value: float):
        """Take in a float value and calculate the sigmoid value.

        :param value: a float value used to calculate the sigmoid value
        :param return: a float that is the calculated sigmoid value
        """
        sigmoid_value = math.exp(value) / (math.exp(value) + 1)
        return sigmoid_value

    def _calculate_value(self):
        """Calculate the weighted sum of the upstream node's values.

        Pass sum to the _sigmoid method and store the value in
        self._value.
        """
        sum_of_upstream_values = 0
        for node in self._neighbors[self.Side.UPSTREAM]:
            value = node.value
            weight = self.get_weight(node)
            sum_of_upstream_values += value * weight

        self._value = FFNeurode._sigmoid(sum_of_upstream_values)

    def _fire_downstream(self):
        """Call data_ready_upstream on each downeighbor."""

        for node in self._neighbors[self.Side.DOWNSTREAM]:
            node.data_ready_upstream(self)

    def data_ready_upstream(self, node: Neurode):
        """Check in the node.

        If all upstream nodes have data, collect the data, call
        self.calculate_value() then self._fire_downstream().
        :param node: Neurode
        """
        if self._check_in(node, Neurode.Side.UPSTREAM) is True:
            self._calculate_value()
            self._fire_downstream()

    def set_input(self, input_value: float):
        """Set the value of an input layer neurode.

        Assign the input_value to self._value. Call data_ready_upstream
        on all downstream neighbors while passing self as an argument.
        :param input_value: float
        """
        self._value = input_value
        for node in self._neighbors[self.Side.DOWNSTREAM]:
            node.data_ready_upstream(self)
