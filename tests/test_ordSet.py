import unittest
import pytups as pt

TEST_TUP = [
    ("a", "b", "c", 1),
    ("a", "b", "c", 2),
    ("a", "b", "c", 3),
    ("r", "b", "c", 1),
    ("r", "b", "c", 2),
    ("r", "b", "c", 3),
]
TEST_DATES = ["2019-0" + str(i) for i in range(1, 10)]


class OrdSetTest(unittest.TestCase):
    list_class = pt.OrderSet

    def setUp(self):
        self.prop1 = self.list_class(TEST_TUP)
        self.dates1 = self.list_class(TEST_DATES)
        self.refDates1 = list(TEST_DATES)

    def tearDown(self):
        pass

    def test_select(self):
        self.assertEqual(self.prop1[1], ("a", "b", "c", 2))

    def test_missing_value(self):
        _func = lambda: self.dates1.ord("2018-01")
        self.assertRaises(pt.MissingValue, _func)

    def test_wrong_list(self):
        _func = lambda: self.list_class([[]])
        self.assertRaises(TypeError, _func)

    def test_select_ord(self):
        self.assertEqual(self.prop1.ord(("r", "b", "c", 3)), 5)

    def test_select_range(self):
        first_two = self.prop1[:2]
        self.assertListEqual([("a", "b", "c", 1), ("a", "b", "c", 2)], first_two)

    def test_dates1(self):
        self.assertEqual(self.dates1[0], "2019-01")

    def test_dates_next(self):
        self.assertEqual(self.dates1.next("2019-02"), "2019-03")

    def test_dates_prev(self):
        self.assertEqual(self.dates1.prev("2019-02"), "2019-01")

    def test_dates_next_mult(self):
        self.assertEqual(self.dates1.next("2019-06", 3), "2019-09")

    def test_edit(self):
        prev_len = len(self.dates1)
        new_value = "2019-00"
        self.dates1[0] = new_value
        new_len = len(self.dates1)
        self.assertEqual(self.dates1[0], new_value)
        self.assertEqual(new_len, prev_len)
        self.refDates1[0] = new_value
        self.assertListEqual(self.refDates1, self.dates1._pos)

    def test_append(self):
        prev_len = len(self.dates1)
        new_value = "2019-10"
        self.dates1.append(new_value)
        new_len = len(self.dates1)
        self.assertEqual(self.dates1[-1], new_value)
        self.assertEqual(prev_len + 1, new_len)
        self.refDates1.append(new_value)
        self.assertListEqual(self.refDates1, self.dates1._pos)

    def test_pop(self):
        self.refDates1.pop()
        self.dates1.pop()
        self.assertListEqual(self.refDates1, self.dates1._pos)

    def test_del(self):
        del self.refDates1[3]
        del self.dates1[3]
        self.assertListEqual(self.refDates1, self.dates1._pos)

    def test_dist(self):
        self.assertEqual(self.dates1.dist("2019-01", "2019-09"), 8)


if __name__ == "__main__":
    unittest.main()
    self = OrdSetTest()
    self.setUp()
