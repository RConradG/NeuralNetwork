"""This module extends the DoublyLinkedList class.

This class will manage the input, hidden, and output layers of a neural
network. Additionally, this module will demonstrate an understanding of
Doubly Linked Lists, Inheritance, and dependency injection.
"""

from __future__ import annotations
from DoublyLinkedList import DoublyLinkedList
import Neurode


class LayerList(DoublyLinkedList):
    """Implement the LayerList class."""
    def __init__(self, inputs: int, outputs: int,
                 neurode_type: type(Neurode)):
        """Create a LayerList.

        :param inputs: indicates the number of input neurodes to create
        :param outputs: indicates the number of output neurodes
        to create
        :param neurode_type: indicates the type of neurode to create
        """
        super().__init__()
        self._input_neurodes = [neurode_type() for _ in range(inputs)]
        self._output_neurodes = [neurode_type() for _ in range(outputs)]
        self._neurode_type = neurode_type
        self.link_layers(self._input_neurodes, self._output_neurodes)
        self.add_to_head(self._input_neurodes)
        self.add_after_current(self._output_neurodes)

    # Helper method
    def link_layers(self, input_neurodes, output_neurodes):
        """Link up the neurodes in neighboring layers.

        :param input_neurodes:  a list of neurodes or child classes
        :param output_neurodes: a list of neurodes or child classes
        """
        for neurode in input_neurodes:
            neurode.reset_neighbors(output_neurodes,
                                    Neurode.Neurode.Side.DOWNSTREAM)

        for neurode in output_neurodes:
            neurode.reset_neighbors(input_neurodes,
                                    Neurode.Neurode.Side.UPSTREAM)

    def add_layer(self, num_nodes: int):
        """Add a hidden layer of neurodes after the current layer.

        :param num_nodes: number of nodes to create
        """
        if self.curr_data is self._output_neurodes:
            raise IndexError
        else:
            hidden_nodes = [self._neurode_type() for _ in range(num_nodes)]
            self.link_layers(self.curr_data, hidden_nodes)
            self.link_layers(hidden_nodes, self._curr.next.data)
            self.add_after_current(hidden_nodes)

    def remove_layer(self):
        """Remove the layer after the current layer."""
        if self._curr.next.data is self._output_neurodes:
            raise IndexError
        else:
            self.remove(self._curr.next.data)
            self.link_layers(self.curr_data, self._curr.next.data)

    @property
    def input_nodes(self):
        """Return the input nodes."""
        return self._input_neurodes

    @property
    def output_nodes(self):
        """Return the output nodes."""
        return self._output_neurodes
