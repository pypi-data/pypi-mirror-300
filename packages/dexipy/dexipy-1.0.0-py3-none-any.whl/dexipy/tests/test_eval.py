# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=invalid-name, line-too-long

import unittest
from copy import deepcopy
from dexipy.eval import evaluation_order, eval_parameters, EvalMethods
from dexipy.eval import _evaluate_as_set, _evaluate_as_distribution
from dexipy.eval import evaluate
from dexipy.eval import aggregate_alternatives, alternatives_value_ranges
from dexipy.dexi import read_dexi_from_string
from dexipy.tests.testdata import CAR_XML, CAR2_XML, LINKED_XML, CONTINUOUS_OLD_XML, CONTINUOUS_NEW_XML, CONTINUOUS_NEW_NO_ALT_XML, DOZEN_XML

def unchanged_alternative(alt1, alt2, ids = []) -> bool:
    if not (isinstance(alt1, dict) and isinstance(alt2, dict)):
        return False
    for attid in ids:
        if alt1[attid] != alt2[attid]:
            return False
    return True

def unchanged(alts1, alts2, ids = []) -> bool:
    if len(alts1) != len(alts2):
        return False
    # pylint: disable-next=consider-using-enumerate
    for idx in range(len(alts1)):
        alt1 = alts1[idx]
        alt2 = alts2[idx]
        if not unchanged_alternative(alt1, alt2, ids):
            return False
    return True

class Test_test_eval(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.car_dxi = read_dexi_from_string(CAR_XML)
        cls.car2_dxi = read_dexi_from_string(CAR2_XML)
        cls.linked_dxi = read_dexi_from_string(LINKED_XML)
        cls.continuous_old_dxi = read_dexi_from_string(CONTINUOUS_OLD_XML)
        cls.continuous_new_dxi = read_dexi_from_string(CONTINUOUS_NEW_XML)
        cls.continuous_new_no_alt_dxi = read_dexi_from_string(CONTINUOUS_NEW_NO_ALT_XML)
        cls.dozen_dxi = read_dexi_from_string(DOZEN_XML)
        return super().setUpClass()

    def test_evaluation_order_Car(self):
        order = evaluation_order(self.car_dxi.root)
        self.assertEqual(order, ["BUY.PRICE", "MAINT.PRICE", "PRICE", "#PERS", "#DOORS", "LUGGAGE", "COMFORT", "SAFETY", "TECH.CHAR.", "CAR", "CAR_MODEL"])
        order = evaluation_order(self.car_dxi.attrib("PRICE"))
        self.assertEqual(order, ["BUY.PRICE", "MAINT.PRICE", "PRICE"])
        order = evaluation_order(self.car_dxi.root, prune = ["COMFORT"])
        self.assertEqual(order, ["BUY.PRICE", "MAINT.PRICE", "PRICE", "COMFORT", "SAFETY", "TECH.CHAR.", "CAR", "CAR_MODEL"])
        order = evaluation_order(self.car_dxi.root, prune = ["TECH.CHAR.", "PRICE"])
        self.assertEqual(order, ["PRICE", "TECH.CHAR.", "CAR", "CAR_MODEL"])

    def test_evaluation_order_Linked(self):
        order = evaluation_order(self.linked_dxi.root)
        self.assertEqual(order, ['A_2', 'A', 'B_2', 'B', 'MIN', 'A_1', 'B_1', 'MAX', 'MID', 'LinkedBoundsTest', 'root'])
        order = evaluation_order(self.linked_dxi.root, prune = ["MAX"])
        self.assertEqual(order, ['A_2', 'A', 'B_2', 'B', 'MIN', 'MAX', 'MID', 'LinkedBoundsTest', 'root'])

    def test_EvalMethods_Linked(self):
        # pylint: disable-next=protected-access
        self.assertEqual(len(EvalMethods._eval_methods.keys()), 4)
        # pylint: disable-next=protected-access
        self.assertEqual(list(EvalMethods._eval_methods.keys()), ["set", "prob", "fuzzy", "fuzzynorm"])

    def test_evaluate_as_set_Car_CAR(self):
        att = self.car_dxi.attrib("CAR")
        fnc = att.funct

        inps = [0, 0]
        value = _evaluate_as_set(fnc, inps)
        self.assertEqual(value, {0})

        inps = [1, 1]
        value = _evaluate_as_set(fnc, inps)
        self.assertEqual(value, {1})

        inps = [{1,0}, 1]
        value = _evaluate_as_set(fnc, inps)
        self.assertEqual(value, {0, 1})

        inps = [{1,0}, {1,2}]
        value = _evaluate_as_set(fnc, inps)
        self.assertEqual(value, {0, 1, 2})

    def test_evaluate_as_set_Car_SetExpandedCAR(self):
        att = self.car_dxi.attrib("CAR")
        fnc = deepcopy(att.funct)
        fnc.values[(0,0)] = {0, 1}

        inps = [0, 0]
        value = _evaluate_as_set(fnc, inps)
        self.assertEqual(value, {0, 1})

        inps = [1, 1]
        value = _evaluate_as_set(fnc, inps)
        self.assertEqual(value, {1})

        inps = [{2,0}, {3,0}]
        value = _evaluate_as_set(fnc, inps)
        self.assertEqual(value, {0, 1, 3})

    def test_evaluate_as_distribution_prob_Car_CAR(self):
        att = self.car_dxi.attrib("CAR")
        fnc = att.funct
        eval_param = eval_parameters("prob")

        inps = [[1], 0]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        self.assertEqual(value, [1, 0, 0, 0])

        inps = [[1, 0, 1], 0]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        self.assertEqual(value, [2, 0, 0, 0])

        inps = [[0.1, 0.3, 0.6], [0.1, 0.2, 0.3, 0.4]]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        self.assertEqual(value, [0.19, 0.06, 0.21, 0.54])

    def test_evaluate_as_distribution_fuzzy_Car_CAR(self):
        att = self.car_dxi.attrib("CAR")
        fnc = att.funct
        eval_param = eval_parameters("fuzzy")

        inps = [[1], 0]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        self.assertEqual(value, [1, 0, 0, 0])

        inps = [[1, 0, 1], 0]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        self.assertEqual(value, [1, 0, 0, 0])

        inps = [[0.1, 0.3, 0.6], [0.1, 0.2, 0.3, 0.4]]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        self.assertEqual(value, [0.1, 0.2, 0.3, 0.4])

        inps = [[0.2, 0.4, 1], [0.1, 0.5, 0.7, 1]]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        self.assertEqual(value, [0.2, 0.4, 0.5, 1])

    def test_evaluate_as_distribution_prob_Car_SetExpandedCAR(self):
        att = self.car_dxi.attrib("CAR")
        fnc = deepcopy(att.funct)
        fnc.values[(0,0)] = {0, 1}
        fnc.values[(1,0)] = {1, 2}
        eval_param = eval_parameters("prob")

        inps = [[1], 0]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        self.assertEqual(value, [0.5, 0.5, 0, 0])

        inps = [[1, 0, 1], 0]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        self.assertEqual(value, [1.5, 0.5, 0, 0])

        inps = [[0.1, 0.3, 0.6], [0.1, 0.2, 0.3, 0.4]]
        value = _evaluate_as_distribution(fnc, inps, eval_param)
        expect = [0.155, 0.08, 0.225, 0.54]
        self.assertEqual(len(value), len(expect))
        self.assertEqual(sum(value), 1.0)
        for idx, el in enumerate(value):
            self.assertAlmostEqual(el, expect[idx])

    def test_PlainEvaluation_Car(self):
        alts0 = self.car_dxi.alternatives
        alts = deepcopy(alts0)
        for attid in self.car_dxi.aggregate_ids:
            for alt in alts:
                alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alts)
        self.assertTrue(unchanged(alts0, eval_alt, self.car_dxi.non_root_ids))

    def test_PlainPrunedEvaluation_Car(self):
        alts0 = self.car_dxi.alternatives
        alts = deepcopy(alts0)
        for attid in self.car_dxi.aggregate_ids:
            if attid != "PRICE":
                for alt in alts:
                    alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alts, prune = ["PRICE"])
        check = ['CAR', 'PRICE', 'TECH.CHAR.', 'COMFORT', '#PERS', '#DOORS', 'LUGGAGE', 'SAFETY']
        self.assertTrue(unchanged(alts0, eval_alt, check))
        for attid in ['BUY.PRICE','MAINT.PRICE']:
            for alt in eval_alt:
                self.assertEqual(alt[attid], None)

    def test_SetEvaluation_Car(self):
        alt0 = self.car_dxi.alternatives[0]
        alt = self.car_dxi.alternative(alt = alt0, values = {"BUY.PRICE": "*"})
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt)
        check = ['MAINT.PRICE', 'TECH.CHAR.', 'COMFORT', '#PERS', '#DOORS', 'LUGGAGE', 'SAFETY']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["BUY.PRICE"], {0, 1, 2})
        self.assertEqual(eval_alt["PRICE"], {0, 2})
        self.assertEqual(eval_alt["CAR"], {0, 3})

        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = "*")
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt)
        check = ['PRICE', 'BUY.PRICE', 'MAINT.PRICE', 'COMFORT', '#PERS', '#DOORS', 'LUGGAGE']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["TECH.CHAR."], {0, 2, 3})
        self.assertEqual(eval_alt["CAR"], {0, 2, 3})

        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = {1, 2})
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt)
        check = ["PRICE", "BUY.PRICE", "MAINT.PRICE", "COMFORT", "#PERS", "#DOORS", "LUGGAGE"]
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["SAFETY"], {1, 2})
        self.assertEqual(eval_alt["TECH.CHAR."], {2, 3})
        self.assertEqual(eval_alt["CAR"], {2, 3})

    def test_ProbEvaluation_Car(self):
        alt0 = self.car_dxi.alternatives[0]
        alt = self.car_dxi.alternative(alt = alt0, values = {"BUY.PRICE": "*"})
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt, method = "prob")
        check = ['MAINT.PRICE', '#PERS', '#DOORS', 'LUGGAGE', 'SAFETY']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["BUY.PRICE"], {0, 1, 2})
        self.assertEqual(eval_alt["TECH.CHAR."], 3)
        self.assertEqual(eval_alt["COMFORT"], 2)
        self.assertEqual(eval_alt["PRICE"], [1/3, 0, 2/3])
        self.assertEqual(eval_alt["CAR"], [1/3, 0, 0, 2/3])

        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = "*")
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt, method = "prob")
        check = ['BUY.PRICE', 'MAINT.PRICE', '#PERS', '#DOORS', 'LUGGAGE']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["SAFETY"], {0, 1, 2})
        self.assertEqual(eval_alt["COMFORT"], 2)
        self.assertEqual(eval_alt["TECH.CHAR."], [1/3, 0, 1/3, 1/3])
        self.assertEqual(eval_alt["CAR"], [1/3, 0, 1/3, 1/3])

        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = {1, 2})
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt, method = "prob")
        check = ['BUY.PRICE', 'MAINT.PRICE', '#PERS', '#DOORS', 'LUGGAGE']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["SAFETY"], {1, 2})
        self.assertEqual(eval_alt["COMFORT"], 2)
        self.assertEqual(eval_alt["TECH.CHAR."], [0, 0, 1/2, 1/2])
        self.assertEqual(eval_alt["CAR"], [0, 0, 1/2, 1/2])

    def test_FuzzyEvaluation_Car(self):
        alt0 = self.car_dxi.alternatives[0]
        alt = self.car_dxi.alternative(alt = alt0, values = {"BUY.PRICE": "*"})
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt, method = "fuzzy")
        check = ['MAINT.PRICE', '#PERS', '#DOORS', 'LUGGAGE', 'SAFETY']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["BUY.PRICE"], {0, 1, 2})
        self.assertEqual(eval_alt["TECH.CHAR."], 3)
        self.assertEqual(eval_alt["COMFORT"], 2)
        self.assertEqual(eval_alt["PRICE"], {0, 2})
        self.assertEqual(eval_alt["CAR"], {0, 3})

        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = "*")
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt, method = "fuzzy")
        check = ['BUY.PRICE', 'MAINT.PRICE', '#PERS', '#DOORS', 'LUGGAGE']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["SAFETY"], {0, 1, 2})
        self.assertEqual(eval_alt["COMFORT"], 2)
        self.assertEqual(eval_alt["TECH.CHAR."], {0, 2, 3})
        self.assertEqual(eval_alt["CAR"], {0, 2, 3})

        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = {1, 2})
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt, method = "fuzzy")
        check = ['BUY.PRICE', 'MAINT.PRICE', '#PERS', '#DOORS', 'LUGGAGE']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["SAFETY"], {1, 2})
        self.assertEqual(eval_alt["COMFORT"], 2)
        self.assertEqual(eval_alt["TECH.CHAR."], {2, 3})
        self.assertEqual(eval_alt["CAR"], {2, 3})

        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = [0, 0.2, 0.5])
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt, method = "fuzzy")
        check = ['BUY.PRICE', 'MAINT.PRICE', '#PERS', '#DOORS', 'LUGGAGE']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["SAFETY"], [0, 0.2, 0.5])
        self.assertEqual(eval_alt["COMFORT"], 2)
        self.assertEqual(eval_alt["TECH.CHAR."], [0, 0, 0.2, 0.5])
        self.assertEqual(eval_alt["CAR"], [0, 0, 0.2, 0.5])

    def test_FuzzyNormEvaluation_Car(self):
        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = [0, 0.2, 0.5])
        for attid in self.car_dxi.aggregate_ids:
            alt[attid] = None
        eval_alt = evaluate(self.car_dxi, alt, method = "fuzzynorm")
        check = ['BUY.PRICE', 'MAINT.PRICE', '#PERS', '#DOORS', 'LUGGAGE']
        self.assertTrue(unchanged_alternative(alt0, eval_alt, check))
        self.assertEqual(eval_alt["SAFETY"], [0, 0.4, 1])
        self.assertEqual(eval_alt["COMFORT"], 2)
        self.assertEqual(eval_alt["TECH.CHAR."], [0, 0, 0.4, 1])
        self.assertEqual(eval_alt["CAR"], [0, 0, 0.4, 1])

    def test_PlainEvaluation_Linked(self):
        model = self.linked_dxi
        alts0 = model.alternatives
        alts = deepcopy(alts0)
        for attid in model.aggregate_ids:
            for alt in alts:
                alt[attid] = None
        eval_alt = evaluate(model, alts)
        self.assertTrue(unchanged(alts0, eval_alt, model.non_root_ids))

    def test_PlainEvaluation_ContinuousNew(self):
        model = self.continuous_new_dxi
        alts0 = model.alternatives
        alts = deepcopy(alts0)
        for attid in model.aggregate_ids:
            for alt in alts:
                alt[attid] = None
        eval_alt = evaluate(model, alts)
        self.assertEqual(eval_alt[0], {'name': 'Null/Null', 'OneLevel': None, 'X1': None, 'N1': None, 'X2': None, 'N2': None})
        self.assertEqual(eval_alt[1], {'name': 'Null/All', 'OneLevel': None, 'X1': None, 'N1': None, 'X2': None, 'N2': None})
        self.assertEqual(eval_alt[2], {'name': 'Test1', 'OneLevel': 0, 'X1': 0, 'N1': -2.0, 'X2': 0, 'N2': -2.0})
        self.assertEqual(eval_alt[3], {'name': 'Test2', 'OneLevel': {0, 1}, 'X1': 0, 'N1': -2.0, 'X2': 1, 'N2': 0.0})
        self.assertEqual(eval_alt[4], {'name': 'Test3', 'OneLevel': 2, 'X1': 0, 'N1': -2.0, 'X2': 2, 'N2': 2.0})
        self.assertEqual(eval_alt[5], {'name': 'Test4', 'OneLevel': {1, 2}, 'X1': 1, 'N1': 2.0, 'X2': 0, 'N2': -2.0})
        self.assertEqual(eval_alt[6], {'name': 'Test5', 'OneLevel': 2, 'X1': 1, 'N1': 2.0, 'X2': 1, 'N2': 0.0})
        self.assertEqual(eval_alt[7], {'name': 'Test6', 'OneLevel': 2, 'X1': 1, 'N1': 2.0, 'X2': 2, 'N2': 2.0})
        self.assertEqual(eval_alt[8], {'name': 'Test7', 'OneLevel': {0, 1}, 'X1': 0, 'N1': 0.0, 'X2': 1, 'N2': 0.0})

    def test_PlainEvaluation_Dozen(self):
        model = self.linked_dxi
        alts0 = model.alternatives
        alts = deepcopy(alts0)
        for attid in model.aggregate_ids:
            for alt in alts:
                alt[attid] = None
        eval_alt = evaluate(model, alts)
        self.assertTrue(unchanged(alts0, eval_alt, model.non_root_ids))

    def test_aggregate_value(self):
        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = [0, 0.2, 0.5], LUGGAGE = {0, 1})
        eval_alt = evaluate(self.car_dxi, alt, method = "prob")
        # pylint: disable-next=unbalanced-tuple-unpacking
        [aggreg] = aggregate_alternatives(self.car_dxi, eval_alt, aggregate = "min")
        self.assertEqual(aggreg["SAFETY"], 1)
        self.assertEqual(aggreg["LUGGAGE"], 0)
        self.assertEqual(aggreg["CAR"], 0)
        # pylint: disable-next=unbalanced-tuple-unpacking
        [aggreg] = aggregate_alternatives(self.car_dxi, eval_alt, aggregate = "max")
        self.assertEqual(aggreg["SAFETY"], 2)
        self.assertEqual(aggreg["LUGGAGE"], 1)
        self.assertEqual(aggreg["CAR"], 3)
        # pylint: disable-next=unbalanced-tuple-unpacking
        [aggreg] = aggregate_alternatives(self.car_dxi, eval_alt, aggregate = "mean")
        self.assertEqual(aggreg["SAFETY"], (0.2 + 2 * 0.5) / (0.2 + 0.5))
        self.assertEqual(aggreg["LUGGAGE"], 0.5)
        car_eval = eval_alt["CAR"]
        self.assertEqual(aggreg["CAR"], sum(i * car_eval[i] for i in range(len(car_eval))) / sum(car_eval))

    def test_alternatives_value_ranges(self):
        alt0 = self.car_dxi.alternatives[1]
        alt = self.car_dxi.alternative(alt = alt0, SAFETY = [0, 0.2, 0.5], LUGGAGE = {0, 1})
        eval_alt = evaluate(self.car_dxi, [alt0, alt], method = "prob")
        aggreg = aggregate_alternatives(self.car_dxi, eval_alt, aggregate = "mean")
        ranges = alternatives_value_ranges(aggreg, self.car_dxi.att_ids)
        keys = list(ranges.keys())
        self.assertEqual(keys, ['CAR', 'PRICE', 'BUY.PRICE', 'MAINT.PRICE', 'TECH.CHAR.', 'COMFORT', '#PERS', '#DOORS', 'LUGGAGE', 'SAFETY'])
        self.assertEqual(ranges["LUGGAGE"], (0.5, 2))
        self.assertEqual(ranges["COMFORT"], (1, 2))
        self.assertEqual(ranges["PRICE"], (1, 1))

if __name__ == '__main__':
    unittest.main()
