import copy
import math
from abc import ABC, abstractmethod


class RMSE(ABC):
    """Root-mean-squared-error calculator."""
    def __init__(self):
        """Initialize the RMSE class."""
        self._expected_list = []
        self._predicted_list = []

    def __add__(self, other):
        """Add a new entry of expected, predicted values.
        
        :param tuple other: Tuple of two tuples with 
            (expected, predicted)
        :returns RMSE: new error object with parameter 'other' 
            incorporated.
        """
        new_obj = copy.deepcopy(self)
        new_obj._expected_list.append(other[0])
        new_obj._predicted_list.append(other[1])
        return new_obj

    def __iadd__(self, other):
        """Add a new entry of expected, predicted values.

        :param tuple other: Tuple of two tuples with 
            (expected, predicted)
        :returns RMSE: modified error object with parameter 'other' 
            incorporated.
        """
        self._expected_list.append(other[0])
        self._predicted_list.append(other[1])
        return self

    def reset(self):
        """Reset error object."""
        self._expected_list = []
        self._predicted_list = []

    @property
    def error(self):
        """Calculate and return RMSE.
        
        :returns float: RMSE
        """
        if len(self._expected_list) == 0:
            return 0
        sum_of_squares = 0
        for item in zip(self._expected_list, self._predicted_list):
            sum_of_squares += self.distance(item[0], item[1])**2
        return math.sqrt(sum_of_squares / len(self._expected_list))

    @staticmethod
    @abstractmethod
    def distance(vector_one, vector_two):
        """Calculate distance of two vectors.
        
        :param tuple vector_one: Vector of floats
        :param tuple vector_two: Vector of floats
        :returns float: distance between vector_one and vector_two
        """
        pass


class Euclidean(RMSE):

    @staticmethod
    def distance(vector_one, vector_two):
        """Calculate distance of two vectors using Euclidean distance.

        :param tuple vector_one: Vector of floats
        :param tuple vector_two: Vector of floats
        :returns float: Euclidean distance between vector_one and 
            vector_two
        """
        squared_diffs = [(a-b)**2 for a, b in zip(vector_one, vector_two)]
        sum_of_squares = sum(squared_diffs)
        return math.sqrt(sum_of_squares)


class Taxicab(RMSE):
    @staticmethod
    def distance(vector_one, vector_two):
        """Calculate distance of two vectors using Euclidean distance.

        :param tuple vector_one: Vector of floats
        :param tuple vector_two: Vector of floats
        :returns float: Taxicab distance between vector_one and 
            vector_two
        """
        abs_diffs = [abs(a-b) for a, b in zip(vector_one, vector_two)]
        return sum(abs_diffs)
