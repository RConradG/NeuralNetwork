class DLLNode:
    """Node class for a DoublyLinkedList - not designed for
    general clients, so no accessors or exception raising."""

    def __init__(self, data: object):
        """Initialize DLL Node.

        :param object data: Data of any type.
        """
        self.prev = None
        self.next = None
        self.data = data


class DoublyLinkedList:
    """Control class for DoublyLinkedList."""

    def __init__(self):
        """Initialize DoublyLinkedList."""
        self._head = None
        self._tail = None
        self._curr = None

    def move_forward(self):
        """Move the current pointer forward through the list.

        :raises IndexError: if list is empty or current node is head.
        """
        if not self._curr or not self._curr.next:
            raise IndexError
        self._curr = self._curr.next

    def move_backward(self):
        """Move the current pointer backward through the list.

        :raises IndexError: if list is empty or current node is head.
        """
        if not self._curr or not self._curr.prev:
            raise IndexError
        self._curr = self._curr.prev

    def add_to_head(self, data: object):
        """Add a new node containing data to the head of the list.

        :param object data: Data of any type."""
        new_node = DLLNode(data)
        new_node.next = self._head
        if self._head:
            self._head.prev = new_node
        self._head = new_node
        if self._tail is None:
            self._tail = new_node
        self.reset_to_head()

    def remove_from_head(self) -> object:
        """Remove the head node from the list, returning data.

        :return object: Data contained in the removed node.
        :raises IndexError: if there is no data in the list."""
        if not self._head:
            raise IndexError
        return_val = self._head.data
        self._head = self._head.next
        if self._head:
            self._head.prev = None
        else:
            self._tail = None
        self.reset_to_head()
        return return_val

    def add_after_current(self, data):
        """Add a new node containing data after the current node.

        :param object data: Data of any type.
        :raises IndexError: if there is no data in the list."""
        if not self._curr:
            raise IndexError
        new_node = DLLNode(data)
        new_node.prev = self._curr
        new_node.next = self._curr.next
        if self._curr.next:
            self._curr.next.prev = new_node
        self._curr.next = new_node
        if self._tail == self._curr:
            self._tail = new_node

    def remove_after_current(self):
        """Remove the node afgter the current node, returning data.

        :return object: Data contained in the removed node.
        :raises IndexError: If list is empty or current node is tail.
        """
        if not self._curr or self._curr is self._tail:
            raise IndexError
        return_value = self._curr.next.data
        if self._curr.next is self._tail:
            self._tail = self._curr
            self._curr.next = None
        else:
            self._curr.next = self._curr.next.next
            self._curr.next.prev = self._curr
        return return_value

    def reset_to_head(self):
        """Reset current pointer to head."""
        self._curr = self._head

    def reset_to_tail(self):
        """Reset current pointer to tail."""
        self._curr = self._tail

    @property
    def curr_data(self) -> object:
        """Return data contained in the current node.

        :return object: Data contained in the current node."""
        if not self._curr:
            raise IndexError
        return self._curr.data

    def find(self, data: object) -> object:
        """Find and return an item in the list.

        :param object data: Key to search for.
        :return object: Full data payload of found node.
        :raises IndexError: if no matching data is found.
        """
        temp_curr = self._head
        while temp_curr:
            if temp_curr.data == data:
                return temp_curr.data
            temp_curr = temp_curr.next
        raise IndexError

    def remove(self, data):
        """Find and remove an item in the list.

        :param object data: Key to search for.
        :return object: Full data payload of removed node.
        :raises IndexError: if no matching data is found.
        """
        if not self._curr:
            raise IndexError
        if self._head.data == data:
            return self.remove_from_head()
        temp_curr = self._head
        while temp_curr.next:
            if temp_curr.next.data == data:
                return_value = temp_curr.next.data
                temp_curr.next = temp_curr.next.next
                if temp_curr.next is None:
                    self._tail = temp_curr
                else:
                    temp_curr.next.prev = temp_curr
                return return_value
            temp_curr = temp_curr.next
        raise IndexError