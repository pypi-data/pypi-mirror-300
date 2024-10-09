# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=invalid-name, line-too-long

import unittest
import math
from dexipy.utils import BoundAssoc
from dexipy.types import DexiOrder, DexiQuality
from dexipy.dexi import DexiScale, DexiContinuousScale, DexiDiscreteScale
from dexipy.dexi import DexiTabularFunction, DexiDiscretizeFunction
from dexipy.dexi import DexiAttribute, DexiModel
from dexipy.dexi import att_names, scale_value, bounded_scale_value, value_text, subtree_order
from dexipy.dexi import alternative
from dexipy.dexi import read_dexi_from_string
from dexipy.dexi import dexi_value_qualities, dexi_value_has_quality, dexi_value_has_bad, dexi_value_has_none, dexi_value_has_good
from dexipy.dexi import compare_values_on_scale
from dexipy.tests.testdata import CAR_XML, CAR2_XML, LINKED_XML
#from dexipy.tests.testdata import CONTINUOUS_OLD_XML, CONTINUOUS_NEW_XML, CONTINUOUS_NEW_NO_ALT_XML, DOZEN_XML

class Test_test_dexi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.car_dxi = read_dexi_from_string(CAR_XML)
        cls.car2_dxi = read_dexi_from_string(CAR2_XML)
        cls.linked_dxi = read_dexi_from_string(LINKED_XML)
        #cls.continuous_old_dxi = read_dexi_from_string(CONTINUOUS_OLD_XML)
        #cls.continuous_new_dxi = read_dexi_from_string(CONTINUOUS_NEW_XML)
        #cls.continuous_new_no_alt_dxi = read_dexi_from_string(CONTINUOUS_NEW_NO_ALT_XML)
        #cls.dozen_dxi = read_dexi_from_string(DOZEN_XML)
        return super().setUpClass()

    def test_DexiScale_equal_scales(self):
        sc = DexiContinuousScale()
        sd1 = DexiDiscreteScale(["a", "b"])
        sd2 = DexiDiscreteScale(["a", "b"], order = DexiOrder.DESCENDING)
        self.assertTrue(DexiScale.equal_scales(None, None))
        self.assertFalse(DexiScale.equal_scales(sc, None))
        self.assertFalse(DexiScale.equal_scales(None, sd1))
        self.assertTrue(DexiScale.equal_scales(sc, sc))
        self.assertFalse(DexiScale.equal_scales(sc, sd1))
        self.assertFalse(DexiScale.equal_scales(sd1, sd2))

    def test_DexiContinuousScale(self):
        s = DexiContinuousScale()
        self.assertTrue(isinstance(s, DexiScale))
        self.assertTrue(isinstance(s, DexiContinuousScale))
        self.assertEqual(s.order, DexiOrder.ASCENDING)
        self.assertEqual(s.scale_str(), "-inf:inf (+)")
        self.assertTrue(s.is_continuous())
        self.assertFalse(s.is_discrete())
        self.assertTrue(s.equal(s))
        self.assertFalse(s.equal(None))
        self.assertFalse(s.equal(3))
        self.assertEqual(s.value_quality(0), DexiQuality.NONE)
        self.assertEqual(s.full_range(), None)
        z = DexiContinuousScale(order = DexiOrder.NONE)
        self.assertEqual(z.order, DexiOrder.NONE)
        self.assertFalse(s.equal(z))
        self.assertFalse(z.equal(s))
        self.assertEqual(z.scale_str(), "-inf:inf (*)")
        self.assertTrue(s.is_continuous())
        self.assertFalse(s.is_discrete())
        z = DexiContinuousScale(lpoint = -1, hpoint = 1)
        self.assertEqual(z.order, DexiOrder.ASCENDING)
        self.assertEqual(z.lpoint, -1)
        self.assertEqual(z.hpoint, 1)
        self.assertFalse(s.equal(z))
        self.assertFalse(z.equal(s))
        self.assertEqual(z.scale_str(), "-1:1 (+)")
        self.assertTrue(z.is_continuous())
        self.assertFalse(z.is_discrete())
        self.assertEqual(z.value_quality(-1.1), DexiQuality.BAD)
        self.assertEqual(z.value_quality(-1), DexiQuality.NONE)
        self.assertEqual(z.value_quality(-0.9), DexiQuality.NONE)
        self.assertEqual(z.value_quality(0), DexiQuality.NONE)
        self.assertEqual(z.value_quality(0.9), DexiQuality.NONE)
        self.assertEqual(z.value_quality(1), DexiQuality.NONE)
        self.assertEqual(z.value_quality(1.1), DexiQuality.GOOD)

    def test_DexiDiscreteScale_default_quality(self):
        for n in range(5):
            self.assertEqual(DexiDiscreteScale.default_quality(DexiOrder.NONE, n), [DexiQuality.NONE] * n)
        for n in range(2):
            self.assertEqual(DexiDiscreteScale.default_quality(DexiOrder.ASCENDING, n), [DexiQuality.NONE] * n)
            self.assertEqual(DexiDiscreteScale.default_quality(DexiOrder.DESCENDING, n), [DexiQuality.NONE] * n)
        for n in range(2, 5):
            self.assertEqual(DexiDiscreteScale.default_quality(DexiOrder.ASCENDING, n),
                              [DexiQuality.BAD] + [DexiQuality.NONE] * (n-2) + [DexiQuality.GOOD])
            self.assertEqual(DexiDiscreteScale.default_quality(DexiOrder.DESCENDING, n),
                              [DexiQuality.GOOD] + [DexiQuality.NONE] * (n-2) + [DexiQuality.BAD])

    def test_DexiDiscreteScale(self):
        s = DexiDiscreteScale([])
        self.assertTrue(isinstance(s, DexiScale))
        self.assertTrue(isinstance(s, DexiDiscreteScale))
        self.assertFalse(isinstance(s, DexiContinuousScale))
        self.assertEqual(s.order, DexiOrder.ASCENDING)
        self.assertEqual(s.values, [])
        self.assertEqual(s.descriptions, [])
        self.assertEqual(s.quality, [])
        self.assertEqual(s.nvals, 0)
        self.assertEqual(s.count(), 0)
        self.assertEqual(s.scale_str(), " (+)")
        self.assertFalse(s.is_continuous())
        self.assertTrue(s.is_discrete())
        self.assertTrue(s.equal(s))
        self.assertFalse(s.equal(None))
        self.assertFalse(s.equal(3))
        with self.assertRaises(ValueError):
            s.value_index("whatever")
        self.assertEqual(s.value_index_or_none("whatever"), None)
        self.assertEqual(s.value_quality(0), None)
        self.assertEqual(s.full_range(), set())

        s = DexiDiscreteScale(["low", "med", "high"])
        self.assertTrue(isinstance(s, DexiScale))
        self.assertTrue(isinstance(s, DexiDiscreteScale))
        self.assertFalse(isinstance(s, DexiContinuousScale))
        self.assertEqual(s.order, DexiOrder.ASCENDING)
        self.assertEqual(s.values, ["low", "med", "high"])
        self.assertEqual(s.descriptions, ["", "", ""])
        self.assertEqual(s.quality, [DexiQuality.BAD, DexiQuality.NONE, DexiQuality.GOOD])
        self.assertEqual(s.nvals, 3)
        self.assertEqual(s.count(), 3)
        self.assertEqual(s.scale_str(), "low; med; high (+)")
        self.assertFalse(s.is_continuous())
        self.assertTrue(s.is_discrete())
        self.assertTrue(s.equal(s))
        self.assertFalse(s.equal(None))
        self.assertFalse(s.equal(3))
        self.assertEqual(s.value_index("med"), 1)
        with self.assertRaises(ValueError):
            s.value_index("medx")
        self.assertEqual(s.value_index_or_none("medx"), None)
        for n in range(s.count()):
            self.assertEqual(s.value_quality(n), s.quality[n])
        self.assertEqual(s.value_quality("low"), DexiQuality.BAD)
        self.assertEqual(s.value_quality("med"), DexiQuality.NONE)
        self.assertEqual(s.value_quality("high"), DexiQuality.GOOD)
        self.assertEqual(s.value_quality("highx"), None)
        self.assertEqual(s.value_quality(3), None)
        self.assertEqual(s.full_range(), {0, 1, 2})

    def test_dexi_value_qualities(self):
        scl = DexiDiscreteScale(["L", "M", "H"], order = DexiOrder.ASCENDING)
        self.assertEqual(dexi_value_qualities(None, scl), None)
        self.assertEqual(dexi_value_qualities(0, scl), [DexiQuality.BAD])
        self.assertEqual(dexi_value_qualities(1, scl), [DexiQuality.NONE])
        self.assertEqual(dexi_value_qualities(2, scl), [DexiQuality.GOOD])
        self.assertEqual(dexi_value_qualities((2, 1, 0), scl), [DexiQuality.BAD, DexiQuality.NONE, DexiQuality.GOOD])
        self.assertEqual(dexi_value_qualities({2, 1, 0}, scl), [DexiQuality.BAD, DexiQuality.NONE, DexiQuality.GOOD])
        self.assertEqual(dexi_value_qualities([2, 1, 0], scl), [DexiQuality.BAD, DexiQuality.NONE])
        self.assertEqual(dexi_value_qualities({0: 0.5, 2: 1.0}, scl), [DexiQuality.BAD, DexiQuality.GOOD])
        self.assertTrue(dexi_value_has_quality(0, scl, DexiQuality.BAD))
        self.assertFalse(dexi_value_has_quality(0, scl, DexiQuality.GOOD))
        self.assertFalse(dexi_value_has_quality(1, scl, DexiQuality.BAD))
        self.assertTrue(dexi_value_has_quality(2, scl, DexiQuality.GOOD))
        self.assertTrue(dexi_value_has_bad(0, scl))
        self.assertFalse(dexi_value_has_good(0, scl))
        self.assertFalse(dexi_value_has_bad(1, scl))
        self.assertTrue(dexi_value_has_good(2, scl))
        self.assertFalse(dexi_value_has_none(0, scl))
        self.assertTrue(dexi_value_has_none(1, scl))
        self.assertFalse(dexi_value_has_none(2, scl))
        self.assertTrue(scl.has_quality((0,1), DexiQuality.BAD))
        self.assertTrue(scl.has_quality((0,1), DexiQuality.NONE))
        self.assertFalse(scl.has_quality((0,1), DexiQuality.GOOD))
        self.assertTrue(scl.has_bad((0,1)))
        self.assertTrue(scl.has_none((0,1)))
        self.assertFalse(scl.has_good((0,1)))
        self.assertFalse(scl.has_bad((1,2)))
        self.assertTrue(scl.has_none((1,2)))
        self.assertTrue(scl.has_good((1,2)))

    def test_compare_values_on_scale(self):
        self.assertEqual(compare_values_on_scale(1, 1, None), None)
        self.assertEqual(compare_values_on_scale(1, 2, None), None)
        self.assertEqual(compare_values_on_scale(1, 1, None, force = True), 0)
        self.assertEqual(compare_values_on_scale(1, 2, None, force = True), -1)
        self.assertEqual(compare_values_on_scale(2, 1, None, force = True), +1)

        scl = DexiDiscreteScale(["L", "M", "H"], order = DexiOrder.ASCENDING)
        self.assertEqual(compare_values_on_scale(1, 1, scl), 0)
        self.assertEqual(compare_values_on_scale(1, 2, scl), -1)
        self.assertEqual(compare_values_on_scale(3, 2, scl), +1)
        self.assertEqual(compare_values_on_scale(1, 1, scl, force = True), 0)
        self.assertEqual(compare_values_on_scale(1, 2, scl, force = True), -1)
        self.assertEqual(compare_values_on_scale(2, 1, scl, force = True), +1)

        scl = DexiDiscreteScale(["L", "M", "H"], order = DexiOrder.DESCENDING)
        self.assertEqual(compare_values_on_scale(1, 1, scl), 0)
        self.assertEqual(compare_values_on_scale(1, 2, scl), +1)
        self.assertEqual(compare_values_on_scale(3, 2, scl), -1)
        self.assertEqual(compare_values_on_scale(1, 1, scl, force = True), 0)
        self.assertEqual(compare_values_on_scale(1, 2, scl, force = True), +1)
        self.assertEqual(compare_values_on_scale(2, 1, scl, force = True), -1)

        scl = DexiDiscreteScale(["L", "M", "H"], order = DexiOrder.NONE)
        self.assertEqual(compare_values_on_scale(1, 1, scl), 0)
        self.assertEqual(compare_values_on_scale(1, 2, scl), None)
        self.assertEqual(compare_values_on_scale(3, 2, scl), None)
        self.assertEqual(compare_values_on_scale(1, 1, scl, force = True), 0)
        self.assertEqual(compare_values_on_scale(1, 2, scl, force = True), None)
        self.assertEqual(compare_values_on_scale(2, 1, scl, force = True), None)

    def test_DexiTabularFunction_no_attribute(self):
        with self.assertRaises(ValueError):
            f = DexiTabularFunction()
        with self.assertRaises(ValueError):
            f = DexiTabularFunction(None, None)
        with self.assertRaises(ValueError):
            f = DexiTabularFunction(dim = [1, 1.1])

        # auto values
        f = DexiTabularFunction(dim = [2, 3])
        self.assertIsNone(f.attribute)
        self.assertEqual(f.dim, (2, 3, ))
        self.assertEqual(f.nargs(), 2)
        self.assertEqual(f.nvals(), 6)
        self.assertEqual(f.funct_str(), "6 2x3")
        self.assertEqual(len(f.values), 6)
        self.assertTrue(all(val is None for i, val in f.values.items()))

        # from values
        f = DexiTabularFunction(dim = [2, 3], values = [1, 2, 3, 4, {5,6}])
        self.assertIsNone(f.attribute)
        self.assertEqual(f.dim, (2, 3, ))
        self.assertEqual(f.nargs(), 2)
        self.assertEqual(f.nvals(), 6)
        self.assertEqual(f.funct_str(), "6 2x3")
        self.assertEqual(len(f.values), 6)
        vv = f.value_vector()
        self.assertEqual(len(vv), 6)
        for i in range(4):
            self.assertEqual(vv[i], i + 1)
        self.assertEqual(vv[4], {5, 6})
        self.assertEqual(vv[-1], None)
        self.assertEqual(f.evaluate([0, 0]), 1)
        self.assertEqual(f.evaluate([1, 2]), None)
        self.assertEqual(f.evaluate([2, 2]), None)
        self.assertEqual(f.value([0, 0]), 1)
        self.assertEqual(f.value([1, 2]), None)
        with self.assertRaises(KeyError):
            f.value([2, 2])

        # from low
        f = DexiTabularFunction(dim = [2, 3], low = "012345")
        self.assertIsNone(f.attribute)
        self.assertEqual(f.dim, (2, 3, ))
        self.assertEqual(f.nargs(), 2)
        self.assertEqual(f.nvals(), 6)
        self.assertEqual(f.funct_str(), "6 2x3")
        self.assertEqual(len(f.values), 6)
        vv = f.value_vector()
        self.assertEqual(len(vv), 6)
        for i in range(6):
            self.assertEqual(vv[i], i)
        self.assertEqual(f.evaluate([0, 0]), 0)
        self.assertEqual(f.evaluate([1, 2]), 5)
        self.assertEqual(f.evaluate([2, 2]), None)
        self.assertEqual(f.value([0, 0]), 0)
        self.assertEqual(f.value([1, 2]), 5)
        with self.assertRaises(KeyError):
            f.value([2, 2])

        # from low/high
        f = DexiTabularFunction(dim = [2, 3], low = "012345", high = "123456")
        self.assertIsNone(f.attribute)
        self.assertEqual(f.dim, (2, 3, ))
        self.assertEqual(f.nargs(), 2)
        self.assertEqual(f.nvals(), 6)
        self.assertEqual(f.funct_str(), "6 2x3")
        self.assertEqual(len(f.values), 6)
        vv = f.value_vector()
        self.assertEqual(len(vv), 6)
        for i in range(6):
            self.assertEqual(vv[i], {i, i + 1})
        self.assertEqual(f.evaluate([0, 0]), {0, 1})
        self.assertEqual(f.evaluate([1, 2]), {5, 6})
        self.assertEqual(f.evaluate([2, 2]), None)
        self.assertEqual(f.value([0, 0]), {0, 1})
        self.assertEqual(f.value([1, 2]), {5, 6})
        with self.assertRaises(KeyError):
            f.value([2, 2])

    def test_DexiDiscretizeFunction_no_attribute(self):

        # auto values
        f = DexiDiscretizeFunction()
        self.assertIsNone(f.attribute)
        self.assertEqual(f.nargs(), 1)
        self.assertEqual(f.nvals(), 1)
        self.assertEqual(f.funct_str(), "None")
        self.assertEqual(len(f.values), 1)
        self.assertEqual(len(f.bounds), 0)
        self.assertEqual(len(f.assoc), 0)
        self.assertEqual(f.values, [None])
        self.assertEqual(f.value(0), None)
        self.assertEqual(f.value(math.inf), None)

        # two bounds
        f = DexiDiscretizeFunction(bounds = [-1, 1], values = [-5, 0, 5])
        self.assertIsNone(f.attribute)
        self.assertEqual(f.nargs(), 1)
        self.assertEqual(f.nvals(), 3)
        self.assertEqual(f.funct_str(), "-5 <-1] 0 <1] 5")
        self.assertEqual(len(f.values), 3)
        self.assertEqual(len(f.bounds), 2)
        self.assertEqual(len(f.assoc), 2)
        self.assertEqual(f.values, [-5, 0, 5])
        self.assertEqual(f.bounds, [-1, 1])
        self.assertEqual(f.assoc, [BoundAssoc.DOWN] * 2)
        for val in [-math.inf, -2, -1, -0.9, 0, 0.9, 1, 1.1, math.inf]:
            self.assertEqual(f.value(val), f.values[0] if val <= f.bounds[0] else f.values[1] if val <= f.bounds[1] else f.values[2])

    def test_DexiAttribute_simple(self):
        a = DexiAttribute("name", "descr")
        self.assertEqual(a.name, "name")
        self.assertEqual(a.description, "descr")
        self.assertEqual(a.id, "name")
        self.assertIsNone(a.link)
        self.assertIsNone(a.parent)
        self.assertIsNone(a.scale)
        self.assertIsNone(a.funct)
        self.assertEqual(a.inputs, [])
        self.assertEqual(a.ninp(), 0)
        self.assertEqual(a.count(), 0)
        self.assertEqual(a.dim(), [])
        self.assertIsNone(a.model())

    def test_DexiAttribute_complex(self):
        ai = DexiAttribute("inp", "idescr")
        ao = DexiAttribute("out", "odescr")
        a = DexiAttribute("name", "descr", inputs = [ai, ai], parent = ao, link = ai)
        self.assertEqual(a.name, "name")
        self.assertEqual(a.description, "descr")
        self.assertEqual(a.id, "name")
        self.assertEqual(a.parent, ao)
        self.assertEqual(a.link, ai)
        self.assertEqual(a.inputs, [ai, ai])
        self.assertIsNone(a.scale)
        self.assertIsNone(a.funct)
        self.assertEqual(a.ninp(), 2)
        self.assertEqual(a.count(), 2)
        self.assertEqual(a.dim(), [None, None])
        self.assertIsNone(a.model())

    def test_DexiAttribute_methods(self):
        ai1 = DexiAttribute("inp1", "idescr1")
        ai2 = DexiAttribute("inp2", "idescr2")
        ai3 = DexiAttribute("inp3", "idescr3")
        ap = DexiAttribute("parent", "pdescr")
        al = DexiAttribute("link", "ldescr")
        a = DexiAttribute("name", "descr", inputs = [ai1, ai2, ai3], parent = ap, link = al)
        ai1.parent = a
        ai2.parent = a
        ai3.parent = a
        ap.inputs = [a]

        self.assertEqual(a.name, "name")
        self.assertEqual(a.description, "descr")
        self.assertEqual(a.id, "name")
        self.assertEqual(a.parent, ap)
        self.assertEqual(a.link, al)
        self.assertIsNone(a.scale)
        self.assertIsNone(a.funct)

        self.assertEqual(a.inputs, [ai1, ai2, ai3])
        self.assertEqual(a.ninp(), 3)
        self.assertEqual(a.count(), 3)
        self.assertEqual(a.dim(), [None, None, None])
        self.assertIsNone(a.model())

        self.assertIsNone(ap.parent)
        self.assertEqual(ap.inputs, [a])
        self.assertEqual(ap.inputs, [a])
        self.assertEqual(ap.ninp(), 1)
        self.assertEqual(ap.count(), 1)
        self.assertEqual(ap.dim(), [None])
        self.assertIsNone(ap.model())

        self.assertTrue(ai1.is_basic())
        self.assertFalse(ai1.is_aggregate())
        self.assertFalse(ai1.is_link())
        self.assertEqual(ai1.parent, a)

        self.assertFalse(a.is_basic())
        self.assertTrue(a.is_aggregate())
        self.assertTrue(a.is_link())

        self.assertFalse(ap.is_basic())
        self.assertTrue(ap.is_aggregate())
        self.assertFalse(ap.is_link())

        self.assertTrue(al.is_basic())
        self.assertFalse(al.is_aggregate())
        self.assertFalse(al.is_link())

        self.assertEqual(ap.level(), 0)
        self.assertEqual(a.level(), 1)
        self.assertEqual(ai2.level(), 2)

        self.assertTrue(a.affects(ap))
        self.assertFalse(a.affects(ai2))
        self.assertFalse(a.affects(al))

        self.assertTrue(ai3.affects(a))
        self.assertTrue(ai3.affects(ap))
        self.assertFalse(ai3.affects(al))

        self.assertEqual(a.inp_index(ai1), 0)
        self.assertEqual(a.inp_index(ai2), 1)
        self.assertEqual(a.inp_index(ai3), 2)
        self.assertEqual(a.inp_index(ap), None)
        self.assertEqual(ap.inp_index(a), 0)
        self.assertEqual(ap.inp_index(ai1), None)

    def test_DexiAttribute_scale_methods(self):
        att = DexiAttribute("att", "descr")

        self.assertFalse(att.has_order(DexiOrder.ASCENDING))
        self.assertFalse(att.has_order(DexiOrder.DESCENDING))
        self.assertFalse(att.has_order(DexiOrder.NONE))
        self.assertFalse(att.is_ordered())
        self.assertFalse(att.is_ascending())
        self.assertFalse(att.is_descending())

        scl = DexiContinuousScale()
        att.scale = scl
        self.assertTrue(att.has_order(DexiOrder.ASCENDING))
        self.assertFalse(att.has_order(DexiOrder.DESCENDING))
        self.assertFalse(att.has_order(DexiOrder.NONE))
        self.assertTrue(att.is_ordered())
        self.assertTrue(att.is_ascending())
        self.assertFalse(att.is_descending())

        scl.order = DexiOrder.DESCENDING
        self.assertFalse(att.has_order(DexiOrder.ASCENDING))
        self.assertTrue(att.has_order(DexiOrder.DESCENDING))
        self.assertFalse(att.has_order(DexiOrder.NONE))
        self.assertTrue(att.is_ordered())
        self.assertFalse(att.is_ascending())
        self.assertTrue(att.is_descending())

        scl.order = DexiOrder.NONE
        self.assertFalse(att.has_order(DexiOrder.ASCENDING))
        self.assertFalse(att.has_order(DexiOrder.DESCENDING))
        self.assertTrue(att.has_order(DexiOrder.NONE))
        self.assertFalse(att.is_ordered())
        self.assertFalse(att.is_ascending())
        self.assertFalse(att.is_descending())

    def test_DexiAttribute_methods_with_model(self):
        ai1 = DexiAttribute("inp1", "idescr1")
        ai2 = DexiAttribute("inp2", "idescr2")
        ai3 = DexiAttribute("inp3", "idescr3")
        ap = DexiAttribute("parent", "pdescr")
        a = DexiAttribute("name", "descr", inputs = [ai1, ai2, ai3], parent = ap)
        ai1.parent = a
        ai2.parent = a
        ai3.parent = a
        ap.inputs = [a]

        m = DexiModel("model", root = ap)
        ap.parent = m

        self.assertEqual(ap.model(), m)
        self.assertEqual(a.model(), m)
        self.assertEqual(ai1.model(), m)

        self.assertEqual(ap.tree_indent(), "")
        self.assertEqual(a.tree_indent(), "+")
        self.assertEqual(ai1.tree_indent(), " *")
        self.assertEqual(ai2.tree_indent(), " *")
        self.assertEqual(ai3.tree_indent(), " +")

    def test_att_names(self):
        ai1 = DexiAttribute("inp1", "idescr1")
        ai2 = DexiAttribute("inp2", "idescr2")
        ai3 = DexiAttribute("inp3", "idescr3")
        ap = DexiAttribute("parent", "pdescr")
        a = DexiAttribute("name", "descr", id = "name_id", inputs = [ai1, ai2, ai3], parent = ap)
        ai1.parent = a
        ai2.parent = a
        ai3.parent = a
        ap.inputs = [a]

        with self.assertRaises(TypeError):
            att_names(None)
        self.assertEqual(att_names([]), [])
        self.assertEqual(att_names([None]), [None])
        self.assertEqual(att_names([ai1]), ["inp1"])
        self.assertEqual(att_names((ai1, ai2, ai3,)), ["inp1", "inp2", "inp3"])
        self.assertEqual(att_names([a]), ["name_id"])
        self.assertEqual(att_names([a], use_id = False), ["name"])

    def test_subtree_order_Car(self):
        for links in [False, True]:
            order = subtree_order(self.car_dxi.root, links = links)
            self.assertEqual(order,['CAR_MODEL', 'CAR', 'PRICE', 'BUY.PRICE', 'MAINT.PRICE', 'TECH.CHAR.', 'COMFORT', '#PERS', '#DOORS', 'LUGGAGE', 'SAFETY'])
            order = subtree_order(self.car_dxi.attrib("PRICE"), links = links)
            self.assertEqual(order, ['PRICE', 'BUY.PRICE', 'MAINT.PRICE'])
            order = subtree_order(self.car_dxi.root, prune = ["COMFORT"], links = links)
            self.assertEqual(order, ['CAR_MODEL', 'CAR', 'PRICE', 'BUY.PRICE', 'MAINT.PRICE', 'TECH.CHAR.', 'COMFORT', 'SAFETY'])
            order = subtree_order(self.car_dxi.root, prune = ["TECH.CHAR.", "PRICE"], links = links)
            self.assertEqual(order, ['CAR_MODEL', 'CAR', 'PRICE', 'TECH.CHAR.'])
            order = subtree_order(self.car_dxi.attrib("COMFORT"), prune = ["LUGGAGE"], links = links)
            self.assertEqual(order, ["COMFORT", "#PERS", "#DOORS", "LUGGAGE"])

    def test_subtree_order_Linked(self):
        order = subtree_order(self.linked_dxi.root, links = False)
        self.assertEqual(order, ['root', 'LinkedBoundsTest', 'MIN', 'MAX', 'MID', 'A_2', 'B_2'])
        order = subtree_order(self.linked_dxi.root, links = True)
        self.assertEqual(order, ['root', 'LinkedBoundsTest', 'MIN', 'A', 'B', 'MAX', 'A_1', 'B_1', 'MID', 'A_2', 'B_2'])
        order = subtree_order(self.linked_dxi.root, prune = ["MAX"], links = False)
        self.assertEqual(order, ['root', 'LinkedBoundsTest', 'MIN', 'MAX', 'MID', 'A_2', 'B_2'])
        order = subtree_order(self.linked_dxi.root, prune = ["MAX"], links = True)
        self.assertEqual(order, ['root', 'LinkedBoundsTest', 'MIN', 'A', 'B', 'MAX', 'MID', 'A_2', 'B_2'])

    def test_models_setup(self):
        self.assertIsNotNone(self.car_dxi)
        self.assertTrue(isinstance(self.car_dxi, DexiModel))
        self.assertIsNotNone(self.car2_dxi)
        self.assertTrue(isinstance(self.car2_dxi, DexiModel))
        self.assertIsNotNone(self.linked_dxi)
        self.assertTrue(isinstance(self.linked_dxi, DexiModel))
        #self.assertIsNotNone(self.continuous_old_dxi)
        #self.assertTrue(isinstance(self.continuous_old_dxi, DexiModel))
        #self.assertIsNotNone(self.continuous_new_dxi)
        #self.assertTrue(isinstance(self.continuous_new_dxi, DexiModel))
        #self.assertIsNotNone(self.continuous_new_no_alt_dxi)
        #self.assertTrue(isinstance(self.continuous_new_no_alt_dxi, DexiModel))
        #self.assertIsNotNone(self.dozen_dxi)
        #self.assertTrue(isinstance(self.dozen_dxi, DexiModel))

    def test_DexiModel_Car2(self):
        m = self.car2_dxi
        self.assertEqual(m.name, "DEXi Model")
        self.assertEqual(m.description, "")
        self.assertFalse(m.linking)
        self.assertEqual(att_names([m.root]), ["root"])
        self.assertEqual(m.att_index("PRICE"), 2)
        self.assertEqual(m.att_index("PRICE", use_id = False), 2)
        self.assertEqual(m.att_indices("PRICE"), [2, 12])
        self.assertTrue(m.attrib("PRICE") is m.attributes[2])
        self.assertEqual(m.att_index("PRICELESS"), None)
        found = m.find_attributes([1, 2, None, "PRICE", -1, "PRICELESS"])
        self.assertEqual(att_names(found), ["CAR", "PRICE", None, "PRICE", m.att_ids[-1], None])
        self.assertEqual(m.deindex_alternative({1: 1, 2: 2, "TC": 3}), {"CAR": 1, "PRICE": 2, "TC": 3})

    def test_DexiModel_Linked(self):
        m = self.linked_dxi
        self.assertEqual(m.name, "DEXi Model")
        self.assertEqual(m.description, "")
        self.assertTrue(m.linking)
        self.assertEqual(att_names([m.root]), ["root"])
        self.assertEqual(m.att_index("A"), 3)
        self.assertEqual(m.att_indices("A"), [3, 6, 9])
        self.assertTrue(m.attrib("A") is m.attributes[3])
        self.assertEqual(m.att_index("-A"), None)
        self.assertTrue(m.attrib("A").link is m.attrib("A_2"))
        self.assertTrue(m.attrib("A_1").link is m.attrib("A_2"))

        a = m.attrib("MAX")
        self.assertFalse(a is None)
        self.assertFalse(a.scale is None)
        self.assertFalse(a.funct is None)

        a = m.attrib("A")
        self.assertFalse(a is None)
        self.assertFalse(a.scale is None)
        self.assertTrue(a.funct is None)

        a = m.attrib("~A")
        self.assertTrue(a is None)

        a = m.find_attributes(["MAX", "MIN"])
        self.assertEqual(len(a), 2)
        self.assertEqual(a[0].id, "MAX")
        self.assertEqual(a[1].id, "MIN")

        a = m.find_attributes(["A", "undef"])
        self.assertEqual(len(a), 2)
        self.assertEqual(a[0].id, "A")
        self.assertEqual(a[1], None)

    def test_scale_value_continuous(self):
        scl = DexiContinuousScale()
        with self.assertRaises(ValueError):
            scale_value(1, None)
        with self.assertRaises(ValueError):
            scale_value(1, 2)
        with self.assertRaises(AssertionError):
            scale_value(scl, scl)
        with self.assertRaises(AssertionError):
            scale_value("a", scl)
        with self.assertRaises(AssertionError):
            scale_value([1], scl)
        with self.assertRaises(AssertionError):
            scale_value((1,), scl)
        with self.assertRaises(AssertionError):
            self.assertEqual(scale_value("1.1", scl), 1.1)
        self.assertEqual(scale_value(None, scl), None)
        self.assertEqual(scale_value(1, scl), 1)
        self.assertEqual(scale_value(1.1, scl), 1.1)

    def test_DexiModel_alternative(self):
        m = self.car_dxi
        alt = m.alternative()
        self.assertEqual(alt,
            {"CAR": None, "PRICE": None, "BUY.PRICE": None, "MAINT.PRICE": None, "TECH.CHAR.": None, "COMFORT": None, "#PERS": None, "#DOORS": None, "LUGGAGE": None, "SAFETY": None})
        alt = m.alternative(default = 0)
        self.assertEqual(alt,
            {"CAR": 0, "PRICE": 0, "BUY.PRICE": 0, "MAINT.PRICE": 0, "TECH.CHAR.": 0, "COMFORT": 0, "#PERS": 0, "#DOORS": 0, "LUGGAGE": 0, "SAFETY": 0})
        alt = m.alternative(name = "MyCar", default = 0, values = {"PRICE": 1, "Something": "*"})
        self.assertEqual(alt,
            {"name": "MyCar", "Something": "*", "CAR": 0, "PRICE": 1, "BUY.PRICE": 0, "MAINT.PRICE": 0, "TECH.CHAR.": 0, "COMFORT": 0, "#PERS": 0, "#DOORS": 0, "LUGGAGE": 0, "SAFETY": 0})
        alt = m.alternative(name = "MyCar", default = 0, values = {"PRICE": 1, "Something": "*"}, CAR = 11, COMFORT = [])
        self.assertEqual(alt,
            {"name": "MyCar", "Something": "*", "CAR": 11, "PRICE": 1, "BUY.PRICE": 0, "MAINT.PRICE": 0, "TECH.CHAR.": 0, "COMFORT": [], "#PERS": 0, "#DOORS": 0, "LUGGAGE": 0, "SAFETY": 0})
        alt = m.alternative(basic = True)
        self.assertEqual(alt,
            {'BUY.PRICE': None, 'MAINT.PRICE': None, '#PERS': None, '#DOORS': None, 'LUGGAGE': None, 'SAFETY': None})
        alt = m.alternative(aggregate = True)
        self.assertEqual(alt,
            {"CAR": None, "PRICE": None, "TECH.CHAR.": None, "COMFORT": None})
        alt = m.alternative(default = 0, basic = True, aggregate = True)
        self.assertEqual(alt,
            {"CAR": 0, "PRICE": 0, "BUY.PRICE": 0, "MAINT.PRICE": 0, "TECH.CHAR.": 0, "COMFORT": 0, "#PERS": 0, "#DOORS": 0, "LUGGAGE": 0, "SAFETY": 0})
        alt = m.alternative(default = 0, sel_att = ["BLA", 3, "BLE"], BLE = "ble")
        self.assertEqual(alt, {"BLA": 0, "BLE": "ble", 3: 0})

    def test_scale_value_discrete(self):
        scl = DexiDiscreteScale(values = ["low", "med", "high"])
        with self.assertRaises(ValueError):
            scale_value(1, None)
        with self.assertRaises(ValueError):
            scale_value(1, 2)
        with self.assertRaises(ValueError):
            scale_value(scl, scl)
        with self.assertRaises(ValueError):
            scale_value(1.1, scl)
        with self.assertRaises(ValueError):
            scale_value("1.1", scl)
        with self.assertRaises(ValueError):
            scale_value("a", scl)
        with self.assertRaises(ValueError):
            scale_value({"lo", "high"}, scl)
        with self.assertRaises(ValueError):
            scale_value("Low", scl)
        with self.assertRaises(ValueError):
            scale_value(["low", 1], scl)
        with self.assertRaises(ValueError):
            scale_value({"lo": 3, 2: 4}, scl)

        self.assertEqual(scale_value(None, scl), None)
        self.assertEqual(scale_value(1, scl), 1)
        self.assertEqual(scale_value("*", scl), {0, 1, 2})
        self.assertEqual(scale_value("Undefined", scl), None)
        self.assertEqual(scale_value("low", scl), 0)
        self.assertEqual(scale_value("high", scl), 2)
        self.assertEqual(scale_value({1, 2}, scl), {1, 2})
        self.assertEqual(scale_value((1, 2,), scl), {1, 2})
        self.assertEqual(scale_value({"low", 2}, scl), {0, 2})
        self.assertEqual(scale_value(("low", 2,), scl), {0, 2})
        self.assertEqual(scale_value([1, 2, 0, 3], scl), [1, 2, 0, 3])
        self.assertEqual(scale_value([1.1, 2, 3.3], scl), [1.1, 2, 3.3])
        self.assertEqual(scale_value({1: 3, 2: 4}, scl), [0, 3, 4])
        self.assertEqual(scale_value({"low": 2, "high": 4}, scl), [2, 0, 4])

    def test_bounded_scale_value_continuous(self):
        scl = DexiContinuousScale()
        with self.assertRaises(ValueError):
            bounded_scale_value(1, None)
        with self.assertRaises(ValueError):
            bounded_scale_value(1, 2)
        with self.assertRaises(AssertionError):
            bounded_scale_value(scl, scl)
        with self.assertRaises(AssertionError):
            bounded_scale_value("a", scl)
        with self.assertRaises(AssertionError):
            bounded_scale_value([1], scl)
        with self.assertRaises(AssertionError):
            bounded_scale_value((1,), scl)
        with self.assertRaises(AssertionError):
            bounded_scale_value("1.1", scl)
        self.assertEqual(bounded_scale_value(None, scl), None)
        self.assertEqual(bounded_scale_value(1, scl), 1)
        self.assertEqual(bounded_scale_value(1.1, scl), 1.1)

    def test_bounded_scale_value_discrete(self):
        scl = DexiDiscreteScale(values = ["low", "med", "high"])
        with self.assertRaises(ValueError):
            bounded_scale_value(1, None)
            bounded_scale_value(1, 2)
            bounded_scale_value(scl, scl)
            bounded_scale_value(1.1, scl)
            bounded_scale_value("1.1", scl)
            bounded_scale_value("a", scl)
            bounded_scale_value({"lo", "high"}, scl)
            bounded_scale_value("Low", scl)
            bounded_scale_value(["low", 1], scl)
            bounded_scale_value({"lo": 3, 2: 4}, scl)

        self.assertEqual(bounded_scale_value(None, scl), None)
        self.assertEqual(bounded_scale_value(1, scl), 1)
        self.assertEqual(bounded_scale_value(-1, scl), 0)
        self.assertEqual(bounded_scale_value(0, scl), 0)
        self.assertEqual(bounded_scale_value(1, scl), 1)
        self.assertEqual(bounded_scale_value(2, scl), 2)
        self.assertEqual(bounded_scale_value(3, scl), 2)
        self.assertEqual(bounded_scale_value("*", scl), {0, 1, 2})
        self.assertEqual(bounded_scale_value("Undefined", scl), None)
        self.assertEqual(bounded_scale_value("low", scl), 0)
        self.assertEqual(bounded_scale_value("high", scl), 2)
        self.assertEqual(bounded_scale_value({1, 2}, scl), {1, 2})
        self.assertEqual(bounded_scale_value((1, 2,), scl), {1, 2})
        self.assertEqual(bounded_scale_value({1, 2, 3}, scl), {1, 2})
        self.assertEqual(bounded_scale_value((1, 2, 5,), scl), {1, 2})
        self.assertEqual(bounded_scale_value({"low", 2, 6}, scl), {0, 2})
        self.assertEqual(bounded_scale_value(("low", 2, 7,), scl), {0, 2})
        self.assertEqual(bounded_scale_value([1, 2, 0, 3], scl), [1, 2, 0])
        self.assertEqual(bounded_scale_value([1.1, 2, 3.3], scl), [1.1, 2, 3.3])
        self.assertEqual(bounded_scale_value({1: 3, 2: 4}, scl), [0, 3, 4])
        self.assertEqual(bounded_scale_value({"low": 2, "high": 4}, scl), [2, 0, 4])
        self.assertEqual(bounded_scale_value({1: 3, 2: 4, 3: 5}, scl), [0, 3, 4])
        self.assertEqual(bounded_scale_value({"low": 2, "high": 4, 6: 7}, scl), [2, 0, 4])

    def test_value_text_continuous(self):
        scl = DexiContinuousScale()
        self.assertEqual(value_text(None, scl), str(None))
        self.assertEqual(value_text(None, scl, none = "x"), "x")
        self.assertEqual(value_text(1, None, none = "x"), "x")
        with self.assertRaises(AssertionError):
            value_text("something", scl)
            value_text([], scl)
        self.assertEqual(value_text(1, scl), "1")
        self.assertEqual(value_text(1.1, scl), "1.1")
        self.assertEqual(value_text(1.1, scl, decimals = 3), "1.1")
        self.assertEqual(value_text(1/3, scl), str(1/3))
        self.assertEqual(value_text(1/3, scl, decimals = 3), "0.333")
        self.assertEqual(value_text(2/3, scl, decimals = 3), "0.667")

    def test_value_text_discrete(self):
        scl = DexiDiscreteScale(values = ["low", "med", "high"])
        self.assertEqual(value_text(None, scl), str(None))
        self.assertEqual(value_text(None, scl, none = "x"), "x")
        self.assertEqual(value_text(1, None, none = "x"), "x")
        self.assertEqual(value_text("something", scl), "something")
        self.assertEqual(value_text("", scl), "")
        self.assertEqual(value_text(0, scl), "low")
        self.assertEqual(value_text(2, scl), "high")
        self.assertEqual(value_text(-1, scl), "high")
        self.assertEqual(value_text({0, 2}, scl), "('low', 'high')")
        self.assertEqual(value_text((0, 2,), scl), "('low', 'high')")
        self.assertEqual(value_text((0, 0, 2, 2,), scl), "('low', 'high')")
        self.assertEqual(value_text({0, "high"}, scl), "('low', 'high')")
        self.assertEqual(value_text({0, "else"}, scl), "('low', 'else')")

        self.assertEqual(value_text([], scl, use_dict = False), "[]")
        self.assertEqual(value_text([1, 5, 5.5], scl, use_dict = False), "[1, 5, 5.5]")
        self.assertEqual(value_text([1, 5, 5.5], scl, decimals = 2, use_dict = False), "[1, 5, 5.5]")
        self.assertEqual(value_text([1, 5, 5.567], scl, decimals = 2, use_dict = False), "[1, 5, 5.57]")

        self.assertEqual(value_text([], scl), "{}")
        self.assertEqual(value_text([1, 5, 5.5], scl), str({"low": 1, "med": 5, "high": 5.5}))
        self.assertEqual(value_text([1, 5, 5.5], scl, decimals = 2), str({"low": 1, "med": 5, "high": 5.5}))
        self.assertEqual(value_text([1, 5, 5.567], scl, decimals = 2), str({"low": 1, "med": 5, "high": 5.57}))

        self.assertEqual(value_text({0: 3, "med": 4, 2: 5}, scl), "{'low': 3, 'med': 4, 'high': 5}")
        self.assertEqual(value_text({0: 1/3, "med": 2/3, 2: 1/6}, scl, decimals = 2), "{'low': 0.33, 'med': 0.67, 'high': 0.17}")
        with self.assertRaises(IndexError):
            value_text({0, 3}, scl)
            value_text(4, scl)
            value_text({1: 1, 3:3}, scl)

    def test_alternative(self):
        self.assertEqual(alternative(), {})
        self.assertEqual(alternative(name = "new"), {"name": "new"})
        self.assertEqual(alternative(name = "new", description = "descr"), {"name": "new", "description": "descr"})
        self.assertEqual(alternative(name = "new", description = "descr", CAR = 3), {"name": "new", "description": "descr", "CAR": 3})
        alt = alternative(name = "new", description = "descr", values = {1:1, 2:2}, CAR = 3)
        self.assertEqual(alt, {"name": "new", "description": "descr", 1:1, 2:2, "CAR": 3})
        with self.assertRaises(ValueError):
            alternative(name = "new", description = "descr", values = 1, CAR = 3)
        alt2 = alternative(alt = alt)
        self.assertEqual(alt, alt2)
        alt2 = alternative(alt = alt2, name = "alt2")
        self.assertEqual(alt2, {"name": "alt2", "description": "descr", 1:1, 2:2, "CAR": 3})

if __name__ == '__main__':
    unittest.main()
