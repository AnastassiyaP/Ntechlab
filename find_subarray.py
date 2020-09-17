import unittest

UNEXIST_INDEX = -1


class Sequence:
    first_index = UNEXIST_INDEX
    last_index = UNEXIST_INDEX
    sum = 0

    def __init__(self):
        self.reset_indices()

    def reset_indices(self):
        self.first_index = UNEXIST_INDEX
        self.last_index = UNEXIST_INDEX
        self.sum = 0

    def copy(self):
        sequence = type(self)()
        sequence.first_index = self.first_index
        sequence.last_index = self.last_index
        sequence.sum = self.sum
        return sequence

    def __str__(self):
        return f"first_index: {self.first_index}, last_index: {self.last_index}, sum: {self.sum}"


class MaxSequence:
    def __init__(self):
        self.cur_max = Sequence()
        self.positive = Sequence()
        self.negative = Sequence()
        self.max = Sequence()
        self.list = []

    def reset_indices(self):
        for seq in [self.positive, self.negative]:
            seq.reset_indices()

    def set_first_index(self, index):
        self.reset_indices()
        self.max.reset_indices()
        self.positive.first_index = index
        self.max.first_index = index
        self.cur_max.first_index = index

    def set_sum(self):
        if self.max.sum == 0:
            self.max = self.positive.copy()
            self.cur_max = self.positive.copy()
        else:
            # increase max
            if self.max.last_index == self.negative.first_index - 1:
                if self.positive.sum + self.negative.sum > 0:
                    if self.max.sum + self.negative.sum > 0:
                        self.max.sum = self.negative.sum + self.positive.sum + self.max.sum
                        self.max.last_index = self.positive.last_index
                    else:
                        self.max = self.positive.copy()
                else:
                    self.cur_max = self.positive.copy()
                    if self.max.sum + self.negative.sum > 0:
                        self.cur_max.first_index = self.max.first_index
                        self.cur_max.sum = self.max.sum + self.positive.sum + self.negative.sum
            else:
                if self.cur_max.sum + self.negative.sum > 0:
                    self.cur_max.sum = self.cur_max.sum + self.positive.sum + self.negative.sum
                    self.cur_max.last_index = self.positive.last_index
                else:
                    self.cur_max = self.positive.copy()
                if self.cur_max.sum > self.max.sum:
                    self.max = self.cur_max.copy()

                if self.positive.sum > self.max.sum:
                    self.max = self.positive.copy()
        self.reset_indices()


def findMaxSubArray(A):
    sequence = MaxSequence()
    is_curr_positive = None

    for index, elem in enumerate(A):
        if elem >= 0:
            if sequence.max.first_index == UNEXIST_INDEX or sequence.max.sum < 0:
                sequence.set_first_index(index)

            elif sequence.positive.first_index == UNEXIST_INDEX:
                sequence.positive.first_index = index
            is_curr_positive = True
            seq = sequence.positive
        else:
            if is_curr_positive:
                sequence.set_sum()
            if sequence.negative.first_index == UNEXIST_INDEX:
                sequence.negative.first_index = index
            if sequence.max.first_index == UNEXIST_INDEX or sequence.max.sum < elem:
                sequence.max.first_index = index
                sequence.max.last_index = index
                sequence.max.sum = elem

            is_curr_positive = False
            seq = sequence.negative

        seq.sum += elem
        seq.last_index = index

    if is_curr_positive:
        sequence.set_sum()

    return A[sequence.max.first_index: sequence.max.last_index + 1]


class TestFindMaxSubArray(unittest.TestCase):
    def test_find_max_sub_array(self):
        self.assertEqual(findMaxSubArray([1]), [1])
        self.assertEqual(findMaxSubArray([-1]), [-1])
        self.assertEqual(findMaxSubArray([-5, -1, -2]), [-1])
        self.assertEqual(findMaxSubArray([0, 0, 0]), [0, 0, 0])
        self.assertEqual(findMaxSubArray([1, 2, 3]), [1, 2, 3])
        self.assertEqual(findMaxSubArray([0, 1, 2, 0, 3, 0]), [0, 1, 2, 0, 3, 0])
        self.assertEqual(findMaxSubArray([4, -5, 6]), [6])
        self.assertEqual(findMaxSubArray([9, -8, 7, -1, 5]), [9, -8, 7, -1, 5])
        self.assertEqual(findMaxSubArray([-1, -2, 0, 1, 2, 0, 3, 0]), [0, 1, 2, 0, 3, 0])
        self.assertEqual(findMaxSubArray(
            [-1, -2, 0, 1, 2, 0, 3, 0, -1, -2, 5, 2]),
            [0, 1, 2, 0, 3, 0, -1, -2, 5, 2])
        self.assertEqual(findMaxSubArray([5, -4, 3, -2, 5, -1, 0.5]), [5, -4, 3, -2, 5])
        self.assertEqual(findMaxSubArray([2, -1, 3, -2, 1, -1, 5]), [2, -1, 3, -2, 1, -1, 5])
        self.assertEqual(findMaxSubArray([1, -1, 2, 1, 5, -3, 2, -8, 6, -1, 3]), [2, 1, 5])
        self.assertEqual(findMaxSubArray([4, -1, 1, -2, 3, -4, 5]), [4, -1, 1, -2, 3, -4, 5])
        self.assertEqual(findMaxSubArray([-1, 1, -1, 2, -1, 3, -1]), [2, -1, 3])
        self.assertEqual(findMaxSubArray([-1, 1, 2, 3, -1]), [1, 2, 3])
        self.assertEqual(findMaxSubArray([1, 2, 3, -1, -2]), [1, 2, 3])
        self.assertEqual(
            findMaxSubArray([1, 2, 3, 4, 0, -1, 0, -3, 1, -10, 1, 2, 3, -1, 0, -2, 1, -1, 1, 0, 0, 2, 3, -1, -5, 1]),
            [1, 2, 3, 4, 0])
        self.assertEqual(
            findMaxSubArray([1, 2, 3, 4, 0, -1, 0, -3, 1, -10, 1, 2, 3, -1, 0, -2, 1, -1, 1, 0, 0, 2, 3, 2, -1, -5, 1]),
            [1, 2, 3, -1, 0, -2, 1, -1, 1, 0, 0, 2, 3, 2])
        self.assertEqual(findMaxSubArray([5, -4, -2, 10, -9, 8, -7, 6, -5, 4, -3, 6 - 7, 8]),
                         [10, -9, 8, -7, 6, -5, 4, -3, 6 - 7, 8])
