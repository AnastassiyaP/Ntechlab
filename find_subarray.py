import unittest

UNEXIST_INDEX = -1

class Sequence:
    def __init__(self):
        self.reset_inices()

    def reset_inices(self):
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
        # self.curr = Sequence()
        self.positive = Sequence()
        # self.second_positive_sequence = Sequence()
        self.negative = Sequence()
        self.max = Sequence()
        self.list =[]

    def reset_indices(self):
        for seq in [self.positive, self.negative]:#, self.curr]:
            seq.reset_inices()

    def set_first_index(self, index):
        self.positive.first_index = index
        self.max.first_index = index
        # self.curr.first_index = index

    def set_sum(self):
        if self.max.sum == 0:
            self.max = self.positive.copy()
        else:
            # increase max
            print(f"set sum max {self.max}, pos {self.positive},neg {self.negative}")
            if self.max.last_index == self.negative.first_index - 1:
                print(f"combine {self.max}, {self.positive}, {self.negative}")
                combined_sum = self.negative.sum + self.positive.sum
                if combined_sum >= 0:
                    self.max.sum += combined_sum
                    self.max.last_index = self.positive.last_index
                else:
                    if len(self.list) == 0:
                        self.list.append(self.max.copy())
                    self.list.append(self.negative.copy())
                    self.list.append(self.positive.copy())

            else:
                if len (self.list) == 0:
                    self.list.append(self.max.copy())
                self.list.append(self.negative.copy())
                self.list.append(self.positive.copy())

        if self.positive.sum > self.max.sum:
            self.max = self.positive.copy()
        self.reset_indices()


def findMaxSubArray(A):
    sequence = MaxSequence()
    is_curr_positive = None

    max_negative = None

    for index, elem in enumerate(A):
        if elem >= 0:
            seq = sequence.positive
            if sequence.max.first_index == UNEXIST_INDEX:
                sequence.set_first_index(index)

            elif sequence.positive.first_index == UNEXIST_INDEX:
                sequence.positive.first_index = index
            is_curr_positive = True
        else:

            if is_curr_positive:
                sequence.set_sum()
            else:
                sequence.negative.first_index = index
            is_curr_positive = False
            seq = sequence.negative

        seq.sum += elem
        seq.last_index = index
    if is_curr_positive:
        sequence.set_sum()

    if sequence.list:
        max_elem = sequence.list[0].copy()
        # cur_sum = max_sum.sum
        cur_elem = None

        for elem in sequence.list:
            if cur_elem:
                cur_elem.sum += elem.sum
                cur_elem.last_index = elem.last_index
                if cur_elem.sum > max_elem.sum:
                    max_elem = cur_elem.copy()

                if cur_elem.sum < 0:
                    cur_elem = None

            elif elem.sum > 0:
                cur_elem = elem.copy()
                if cur_elem.sum > max_elem.sum:
                    max_elem = cur_elem.copy()
        return max_elem.sum#, sequence
    else:
        return sequence.max.sum#, sequence


class TestFindMaxSubArray(unittest.TestCase):
    def test_find_max_sub_array(self):
        self.assertEqual(findMaxSubArray([1,2,3]),6)
        self.assertEqual(findMaxSubArray([0,1,2,0,3,0]),6)
        self.assertEqual(findMaxSubArray([-1,-2,0,1,2,0,3,0]),6)
        self.assertEqual(findMaxSubArray([5,-4,3,-2,5,-1,0.5]),7)
        self.assertEqual(findMaxSubArray([2, -1, 3,-2,1,-1,5]),7)
        self.assertEqual(findMaxSubArray([1,-1,2,1,5,-3,2,-8,6,-1,3]), 8)
        self.assertEqual(findMaxSubArray([1]),1)
        self.assertEqual(findMaxSubArray([0,0,0]),0)
        self.assertEqual(findMaxSubArray([4,-1,1,-2,3,-4,5]), 6)
        self.assertEqual(findMaxSubArray([-1, 1,-1,2,-1,3, -1]), 4)
        self.assertEqual(findMaxSubArray([-1, 1,2,3, -1]), 6)
        self.assertEqual(findMaxSubArray([1,2,3, -1, -2]), 6)
        self.assertEqual(findMaxSubArray([1,2,3,4,0,-1,0,-3,1,-10, 1,2,3,-1,0,-2,1,-1,1,0,0,2,3,-1,-5,1 ]), 10)
        self.assertEqual(findMaxSubArray([1,2,3,4,0,-1,0,-3,1,-10, 1,2,3,-1,0,-2,1,-1,1,0,0,2,3,2,-1,-5,1 ]), 11)
        self.assertEqual(findMaxSubArray([-5,-1,-2]),-1)
        self.assertEqual(findMaxSubArray([-1]),-1)
