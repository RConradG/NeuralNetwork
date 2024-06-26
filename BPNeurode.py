"""This module demonstrates and understanding of several concepts.
This module applies the concepts multiple inheritance, method
resolution order, back propagation, and the sigmoid derivative.
"""

from Neurode import Neurode


class BPNeurode(Neurode):

    def __init__(self):
        """Implement the BPNeurode class."""

        self._delta = 0
        super().__init__()

    @property
    def delta(self):
        """Return delta."""
        return self._delta

    @staticmethod
    def _sigmoid_derivative(value: float):
        """Calculate the sigmoid derivative.

        Take in the value of the neurode. Multiply the value of the
        neurode by one minus the value of the neurode.

        :param value: a float representing the value of the neurode
        :return: a float that represents the sigmoid derivative
        """
        sigmoid_derivative = value * (1 - value)
        return sigmoid_derivative

    def _calculate_delta(self, expected_value: float = None):
        """Calculate the delta of this neurode.

        :param expected_value:
        """
        if not self._neighbors[self.Side.DOWNSTREAM]:
            self._delta = ((expected_value - self._value) *
                           self._sigmoid_derivative(self._value))
        else:
            weighted_sum = 0
            for node in self._neighbors[self.Side.DOWNSTREAM]:
                downstream_delta = node.delta
                weight = node.get_weight(self)
                weighted_sum += downstream_delta * weight
                self._delta = (weighted_sum *
                               self._sigmoid_derivative(self.value))

    def data_ready_downstream(self, node: Neurode):
        """Check in the node.

        If all downstream nodes have data, collect the data, call
        self._calculate_delta(), self._fire_downstream(), and
        self._update_weights().

        :param node: Neurode
        """
        if self._check_in(node, self.Side.DOWNSTREAM) is True:
            self._calculate_delta()
            self._fire_upstream()
            self._update_weights()

    def set_expected(self, expected_value: float):
        """Directly set the expected value of an output layer neurode.

        Call self._calculate_delta and pass in the expected value.
        :param expected_value: user value
        """
        self._calculate_delta(expected_value)
        self._fire_upstream()

    def adjust_weights(self, node: Neurode, adjustment: float):
        """Change the upstream node weight.

        :param node: Neurode
        :param adjustment: the value to adjust the weight by adjustment
        """
        self._weights[node] += adjustment

    def _update_weights(self):
        """Calculate the weight adjustment."""
        for node in self._neighbors[self.Side.DOWNSTREAM]:
            adjustment = node.learning_rate * node.delta * self.value
            node.adjust_weights(self, adjustment)

    def _fire_upstream(self):
        """Call data_ready_downstream for each Upstream neighbor"""
        for node in self._neighbors[self.Side.UPSTREAM]:
            node.data_ready_downstream(self)
