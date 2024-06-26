"""This module contains the NNData Class.

This module demonstrates an understanding of NumPy Arrays, Deque,
Random, and Specification. The NNData Class contains methods that help
manage testing and training data. Additionally, this module contains
the enums Order and Set.
"""
import math
from enum import Enum
from collections import deque
import numpy as np
import random


class Order(Enum):
    """Implementing the Order Class and defining the Enums."""

    SHUFFLE = 'SHUFFLE'
    STATIC = 'STATIC'


class Set(Enum):
    """Implementing the Set Class and defining the Enums."""

    TRAIN = 'TRAIN'
    TEST = 'TEST'


class NNData:
    """Implementing the NNData Class."""

    @staticmethod
    def percentage_limiter(percentage: float):
        """Take in a percentage value and ensure it is within range.

        Checks the argument and returns 0 if it's less than 0, or 1 if
        the value is greater than 1.

        :param percentage: training percentage
        :return: float
        """
        if percentage < 0:
            return 0
        elif percentage > 1:
            return 1
        else:
            return percentage

    def __init__(self, features=None, labels=None, train_factor=0.9):
        """Create an NNData object.

        :param features: features of one example from data
        :param labels: list of list where one row is one label from data
        :param train_factor: percent of data to be used for training
        """
        if features is None:
            features = []
        if labels is None:
            labels = []

        self._features = None
        self._labels = None
        self._train_factor = NNData.percentage_limiter(train_factor)
        self._train_indices = []
        self._test_indices = []
        self._train_pool = deque()
        self._test_pool = deque()
        self.load_data(features, labels)

    def load_data(self, features=None, labels=None):
        """Assign self._features and self._labels to respective array.

        :param features: features from one example of data
        :param labels: list of list where one row is one label from data
        """
        if features is None or labels is None:
            self._features = None
            self._labels = None
            self.split_set()
            return

        if len(features) != len(labels):
            self._features = None
            self._labels = None
            self.split_set()
            raise ValueError

        try:
            self._features = np.array(features, dtype=float)
            self._labels = np.array(labels, dtype=float)
        except ValueError:
            self._features = None
            self._labels = None
            self.split_set()
            raise ValueError

        self.split_set()

    def split_set(self, new_train_factor=None):
        """Create train_indices and test_indices.

        :param new_train_factor: new percentage for training, float
        between 0 and 1.
        """
        if self._features is None:
            # note to self: if there are no features, there can't be any
            # training indices nor test indices
            self._train_indices = []
            self._test_indices = []
            return

        if new_train_factor is not None:
            self._train_factor = NNData.percentage_limiter(new_train_factor)

        size_of_features = len(self._features)
        number_of_indices = math.floor(size_of_features *
                                       self._train_factor)
        indices = [i for i in range(size_of_features)]
        random.shuffle(indices)

        self._train_indices = indices[:number_of_indices]
        self._test_indices = indices[number_of_indices:]
        return

    def prime_data(self, target_set=None, order=None):
        """Load _train_pool or _test_pool, or both.

        :param target_set: used to determine which pool to load
        :param order: used to either shuffle deque or keep in order
        """
        if target_set is None or target_set == Set.TRAIN:
            # self._train_pool.clear()
            self._train_pool = deque(self._train_indices)
            if order == Order.SHUFFLE:
                random.shuffle(self._train_pool)

        if target_set is None or target_set == Set.TEST:
            # self._test_pool.clear()
            self._test_pool = deque(self._test_indices)

            if order == Order.SHUFFLE:
                random.shuffle(self._test_pool)

    def get_one_item(self, target_set=None):
        """Return one feature/label pair as a tuple.

        :param target_set: determines which pool used to find pair
        :return: tuple
        """
        if target_set is None or target_set == Set.TRAIN:
            if len(self._train_pool) == 0:
                return None
            else:
                index = self._train_pool.popleft()
                return (self._features[index], self._labels[index])

        elif target_set == Set.TEST:
            if len(self._test_pool) == 0:
                return None
            else:
                index = self._test_pool.popleft()
                return (self._features[index], self._labels[index])

    def number_of_samples(self, target_set=None):
        """Determine the number testing or training samples.

        :param target_set: used to return testing or training samples
        :return: int
        """
        if target_set == Set.TEST:
            return len(self._test_indices)
        elif target_set == Set.TRAIN:
            return len(self._train_indices)
        else:
            return len(self._train_indices) + len(self._test_indices)

    def pool_is_empty(self, target_set=None):
        """Check if testing or training pools are empty.

        :param target_set: used to check testing or training pools
        :return: bool
        """
        if target_set == Set.TEST:
            if len(self._test_pool) == 0:
                return True
            else:
                return False

        if target_set is None or target_set == Set.TRAIN:
            if len(self._train_pool) == 0:
                return True
            else:
                return False
