# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=invalid-name, line-too-long

import unittest
from dexipy.parse import _dexi_bool, _dexi_vector, _dexi_value, _dexi_option_value


class test_test_parse(unittest.TestCase):

    def test__dexi_bool(self):
        self.assertFalse(_dexi_bool(None))
        self.assertFalse(_dexi_bool(""))
        self.assertFalse(_dexi_bool([]))
        self.assertFalse(_dexi_bool(0))
        self.assertFalse(_dexi_bool(1))
        self.assertFalse(_dexi_bool("F"))
        self.assertFalse(_dexi_bool("tru"))
        self.assertTrue(_dexi_bool("true"))
        self.assertTrue(_dexi_bool("TRUE"))
        self.assertTrue(_dexi_bool("True"))
        self.assertTrue(_dexi_bool("t"))
        self.assertTrue(_dexi_bool("T"))
        self.assertTrue(_dexi_bool("1"))

    def test_dexi_vector(self):
        with self.assertRaises(AttributeError):
            _dexi_vector(None)
        with self.assertRaises(AttributeError):
            _dexi_vector([])
        with self.assertRaises(AttributeError):
            _dexi_vector(1)
        with self.assertRaises(AttributeError):
            _dexi_vector([1])
        with self.assertRaises(AttributeError):
            _dexi_vector([1, 2])
        with self.assertRaises(AttributeError):
            _dexi_vector(["1", "2"])
        with self.assertRaises(ValueError):
            _dexi_vector("a")
        with self.assertRaises(ValueError):
            _dexi_vector("1.1;5.5;-7.7xs")
        with self.assertRaises(ValueError):
            _dexi_vector("")
        self.assertEqual(_dexi_vector("1"), [1])
        self.assertEqual(_dexi_vector("1.1"), [1.1])
        self.assertEqual(_dexi_vector("1;2"), [1, 2])
        vec = _dexi_vector("1;5;-7")
        self.assertEqual(vec, [1, 5, -7])
        self.assertTrue(isinstance(vec[0], int))
        vec = _dexi_vector("1.1;5;-7.2")
        self.assertEqual(vec, [1.1, 5, -7.2])
        self.assertTrue(isinstance(vec[0], float))
        self.assertFalse(isinstance(vec[0], int))
        self.assertTrue(isinstance(vec[1], int))

    def test_dexi_value(self):
        with self.assertRaises(AttributeError):
            _dexi_value([])
        self.assertIsNone(_dexi_value(None))
        self.assertIsNone(_dexi_value(""))
        self.assertIsNone(_dexi_value("Undefined"))
        self.assertEqual(_dexi_value("*"), "*")
        self.assertEqual(_dexi_value("1"), 1)
        self.assertEqual(_dexi_value("1", 1), 2)
        self.assertEqual(_dexi_value("1:3"), {1, 2, 3})
        self.assertEqual(_dexi_value("1:3", 2), {3, 4, 5})
        self.assertEqual(_dexi_value("<1.1>"), [1.1])
        self.assertEqual(_dexi_value("<1.1;2.2>"), [1.1, 2.2])
        self.assertEqual(_dexi_value("{1;2}"), {1, 2})
        self.assertEqual(_dexi_value("{1;2}", add = 1), {2, 3})
        self.assertEqual(_dexi_value("{1; 5; -7}"), {1, 5, -7})
        self.assertEqual(_dexi_value("{1; 5; -7}", 2), {3, 7, -5})
        self.assertEqual(_dexi_value("<1.1; 5.5; -7.7>", 2), [1.1, 5.5, -7.7])

    def test_dexi_option_value(self):
        with self.assertRaises(AttributeError):
            _dexi_option_value([])
        self.assertIsNone(_dexi_option_value(None))
        self.assertIsNone(_dexi_option_value("Undefined"))
        self.assertEqual(_dexi_option_value(""), "*")
        self.assertEqual(_dexi_option_value("*"), "*")
        self.assertEqual(_dexi_option_value("1"), 1)
        self.assertEqual(_dexi_option_value("12"), {1, 2})
        self.assertEqual(_dexi_option_value("13334"), {1, 3, 4})

if __name__ == '__main__':
    unittest.main()
