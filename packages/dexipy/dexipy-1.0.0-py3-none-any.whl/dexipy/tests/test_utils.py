# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=invalid-name, line-too-long

import unittest
from dexipy.types import BoundAssoc
from dexipy.utils import rule_values, values_to_str
from dexipy.utils import set_to_distr, distr_to_set
from dexipy.utils import norm_sum, norm_max
from dexipy.utils import cartesian_product, unique_names
from dexipy.utils import name_to_id, names_to_ids
from dexipy.utils import is_in_range
from dexipy.utils import pad_list
from dexipy.utils import lin_map, lin_map_values


class test_test_utils(unittest.TestCase):

    def test_rule_values(self):
        self.assertEqual(rule_values("3"), (3,))
        self.assertEqual(rule_values(":"), (10,))
        self.assertEqual(rule_values("0123:"), (0, 1, 2, 3, 10))
        self.assertEqual(rule_values("0123:", 1), (1, 2, 3, 4, 11))

    def test_values_to_str(self):
        self.assertEqual(values_to_str((3,)), "3")
        self.assertEqual(values_to_str([10]), ":")
        self.assertEqual(values_to_str((0, 1, 2, 3, 10)), "0123:")
        self.assertEqual(values_to_str([1, 2, 3, 4, 11], -1), "0123:")

    def test_set_to_distr(self):
        self.assertEqual(set_to_distr({}), [])
        self.assertEqual(set_to_distr([]), [])
        self.assertEqual(set_to_distr(""), [])
        self.assertEqual(set_to_distr({1, 3, 4}), [0.0, 1.0, 0.0, 1.0, 1.0])
        self.assertEqual(set_to_distr({0, 3, -1, 4}), [1.0, 0.0, 0.0, 1.0, 1.0])
        self.assertEqual(set_to_distr({-1, -2, -4}), [])

    def test_distr_to_set(self):
        with self.assertRaises(TypeError):
            distr_to_set(None)
        self.assertEqual(distr_to_set([0.1]), {0})
        self.assertEqual(distr_to_set([]), set())
        self.assertEqual(distr_to_set([0, 1, 0, 0.5]), {1, 3})
        self.assertEqual(distr_to_set([0, -1, 1, 0]), {2})
        self.assertEqual(distr_to_set([0, -1, 1, 0.5]), {2, 3})
        self.assertEqual(distr_to_set([0, -1, 1, 0.5], eps = 0.5), {2})
        self.assertEqual(distr_to_set([1, 0.1, 0.2, 0.005]), {0, 1, 2, 3})
        self.assertEqual(distr_to_set([1, 0.1, 0.2, 0.005], eps = 0.1), {0, 2})

    def test_norm_sum(self):
        self.assertEqual(norm_sum([]), [])
        self.assertEqual(norm_sum([1]), [1])
        self.assertEqual(norm_sum([0.5]), [1])
        self.assertEqual(norm_sum([0.5], req_sum = 2), [2])
        self.assertEqual(norm_sum([0.5, 1], req_sum = 2), [2/3, 4/3])
        self.assertEqual(norm_sum([0.5, 1], req_sum = 1), [1/3, 2/3])
        self.assertEqual(norm_sum([0.5, 1], req_sum = 0.5), [1/6, 2/6])
        self.assertEqual(norm_sum([0.5, 1], req_sum = 0.0), [0, 0])
        self.assertEqual(norm_sum([0.5, 1], req_sum = -1), [-1/3, -2/3])
        self.assertEqual(norm_sum([0, 0], req_sum = -1), [0, 0])
        self.assertEqual(norm_sum([0, 0], req_sum = 1), [0, 0])

    def test_norm_max(self):
        self.assertEqual(norm_max([]), [])
        self.assertEqual(norm_max([0.5]), [1])
        self.assertEqual(norm_max([0.5], req_max = 2), [2])
        self.assertEqual(norm_max([0.5, 1], req_max = 2), [1, 2])
        self.assertEqual(norm_max([0.5, 1], req_max = 1), [0.5, 1])
        self.assertEqual(norm_max([0.5, 1], req_max = 0.5), [0.25, 0.5])
        self.assertEqual(norm_max([0.5, 1], req_max = 0.0), [0, 0])
        self.assertEqual(norm_max([0.5, 1], req_max = -1), [-0.5, -1.0])
        self.assertEqual(norm_max([0, 0], req_max = -1), [0, 0])
        self.assertEqual(norm_max([0, 0], req_max = 1), [0, 0])

    def test_is_in_range(self):
        self.assertFalse(is_in_range(-1, 0, 2))
        self.assertTrue(is_in_range(1, 0, 2))
        self.assertTrue(is_in_range(0, 0, 2))
        self.assertTrue(is_in_range(2, 0, 2))
        self.assertFalse(is_in_range(-1, 0, 2))
        self.assertTrue(is_in_range(0, 0, 2, la = BoundAssoc.UP, ha = BoundAssoc.DOWN))
        self.assertTrue(is_in_range(0, 0, 2, la = BoundAssoc.UP, ha = BoundAssoc.UP))
        self.assertFalse(is_in_range(0, 0, 2, la = BoundAssoc.DOWN, ha = BoundAssoc.UP))
        self.assertTrue(is_in_range(2, 0, 2, la = BoundAssoc.UP, ha = BoundAssoc.DOWN))
        self.assertFalse(is_in_range(2, 0, 2, la = BoundAssoc.UP, ha = BoundAssoc.UP))
        self.assertFalse(is_in_range(2, 0, 2, la = BoundAssoc.DOWN, ha = BoundAssoc.UP))

    def test_cartesian_product(self):
        dimensions = ({1,2,3}, {4,5})
        self.assertEqual(cartesian_product(*dimensions), [(1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)])
        dimensions = (range(3), range(2,5))
        self.assertEqual(cartesian_product(*dimensions), [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 2), (2, 3), (2, 4)])

    def test_unique_names(self):
        names = ["name", "state", "name", "city", "name", "zip", "zip"]
        self.assertEqual(unique_names(names), ['name', 'state', 'name_1', 'city', 'name_2', 'zip', 'zip_1'])
        names = ["name", "state", "name", "city", "name", "zip", "zip", "name_2"]
        self.assertEqual(unique_names(names), ['name', 'state', 'name_1', 'city', 'name_2', 'zip', 'zip_1', 'name_2_1'])
        self.assertEqual(unique_names(names, start = 1), ['name', 'state', 'name_2', 'city', 'name_3', 'zip', 'zip_2', 'name_2_2'])
        self.assertEqual(unique_names(names, reserved = ["name", "zip"]), ['name_1', 'state', 'name_2', 'city', 'name_3', 'zip_1', 'zip_2', 'name_2_1'])

    def test_name_to_id(self):
        self.assertEqual(name_to_id("abc123"), "abc123")
        self.assertEqual(name_to_id("a b c 12 3"), "a_b_c_12_3")
        self.assertEqual(name_to_id("a b c 12 3", replace = "."), "a.b.c.12.3")
        self.assertEqual(name_to_id("aA%bB#cC*._X "), "aA_bB_cC___X_")

    def test_names_to_ids(self):
        self.assertEqual(names_to_ids([]), [])
        self.assertEqual(names_to_ids(["abc123", "a b c 12 3", "aA%bB#cC*._X "]), ["abc123", "a_b_c_12_3", "aA_bB_cC___X_"])
        self.assertEqual(names_to_ids(["abc123", "a b c 12 3", "aA%bB#cC*._X "], replace = "*"), ["abc123", "a*b*c*12*3", "aA*bB*cC***X*"])

    def test_pad_list(self):
        lst = ["a", "b", "c"]
        self.assertEqual(pad_list(lst, 0, ""), [])
        self.assertEqual(pad_list(lst, 2, ""), ["a", "b"])
        self.assertEqual(pad_list(lst, 3, ""), lst)
        self.assertEqual(pad_list(lst, 4, ""), ["a", "b", "c", ""])
        self.assertEqual(pad_list([], 0, ""), [])
        self.assertEqual(pad_list([], 2, ""), ["", ""])

    def test_lin_map(self):
        self.assertEqual(lin_map(1, 1, 3), 0.0)
        self.assertEqual(lin_map(2, 1, 3), 0.5)
        self.assertEqual(lin_map(3, 1, 3), 1.0)
        self.assertEqual(lin_map(1, 3, 1), 1.0)
        self.assertEqual(lin_map(2, 3, 1), 0.5)
        self.assertEqual(lin_map(3, 3, 1), 0.0)

        self.assertEqual(lin_map(1, 1, 3, 0, 10), 0)
        self.assertEqual(lin_map(2, 1, 3, 0, 10), 5)
        self.assertEqual(lin_map(3, 1, 3, 0, 10), 10)
        self.assertEqual(lin_map(1, 3, 1, 0, 10), 10)
        self.assertEqual(lin_map(2, 3, 1, 0, 10), 5)
        self.assertEqual(lin_map(3, 3, 1, 0, 10), 0)
        with self.assertRaises(ZeroDivisionError):
            lin_map(3, 3, 3)
        self.assertEqual(lin_map(3, 1, 3, 5, 5), 5)

    def test_lin_map_values(self):
        self.assertEqual(lin_map_values([1, 2, 3], 1, 3), [0.0, 0.5, 1.0])
        self.assertEqual(lin_map_values([1, 2, 3], 3, 1), [1.0, 0.5, 0.0])
        self.assertEqual(lin_map_values([1, 2, 3], 1, 3, 0, 10), [0, 5, 10])
        self.assertEqual(lin_map_values([1, 2, 3], 3, 1, 0, 10), [10, 5, 0])
        self.assertEqual(lin_map_values([1, 2, 3], 1, 3, -5, +5), [-5, 0, +5])
        self.assertEqual(lin_map_values([1, 2, 3], 1, 3, +5, -5), [+5, 0, -5])

if __name__ == '__main__':
    unittest.main()
