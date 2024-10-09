# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=invalid-name, line-too-long

import unittest
from dexipy.dexi import DexiDiscreteScale, DexiAttribute
from dexipy.charts import _get_text_size, _expand_value_to_points

class test_test_parse(unittest.TestCase):

    def test_get_text_size(self):
        size = _get_text_size("M")
        self.assertGreater(size.width, 0)
        self.assertGreater(size.height, 0)
        size24 = _get_text_size("M", font_size = 24)
        self.assertGreater(size24.width, 0)
        self.assertGreater(size24.height, 0)
        self.assertGreater(size24.width, size.width)
        self.assertGreater(size24.height, size.height)

    def test_expand_value_to_points(self):
        att = DexiAttribute("name", "descr")
        scl = DexiDiscreteScale(["low", "med", "high"])
        att.scale = scl
        x = _expand_value_to_points(1, att)
        self.assertEqual(x, ([1], [1.0], ['k']))
        x = _expand_value_to_points((0, 1), att)
        self.assertEqual(x, ([0, 1], [1.0, 1.0], ['r', 'k']))
        x = _expand_value_to_points({1, 2}, att)
        self.assertEqual(x, ([1, 2], [1.0, 1.0], ['k', 'g']))
        x = _expand_value_to_points([0, 0.7, 0.3], att)
        self.assertEqual(x, ([1, 2], [0.7, 0.3], ['k', 'g']))
        x = _expand_value_to_points([0, 0.7, 0.3], att, ('c', 'd', 'f'))
        self.assertEqual(x, ([1, 2], [0.7, 0.3], ['d', 'f']))

if __name__ == '__main__':
    unittest.main()
