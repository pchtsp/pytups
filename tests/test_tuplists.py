import unittest
import pytups as pt

TEST_TUP = [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3),
            ('r', 'b', 'c', 1), ('r', 'b', 'c', 2), ('r', 'b', 'c', 3)]


class TupTest(unittest.TestCase):
    tuplist_class = pt.TupList

    def test_filter(self):
        result = [('a', 'c'), ('a', 'c'), ('a', 'c'),
                  ('r', 'c'), ('r', 'c'), ('r', 'c')]
        self.assertListEqual(result, self.prop1.take([0, 2]))

    def test_filter2(self):
        result = [1, 2, 3, 1, 2, 3]
        self.assertListEqual(result, self.prop1.take(3))

    def test_filter_order(self):
        result = [(1, 'a'), (2, 'a'), (3, 'a'), (1, 'r'), (2, 'r'), (3, 'r')]
        self.assertListEqual(result, self.prop1.take([3, 0]))

    def test_filter_list_f(self):
        result = [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3)]
        self.assertListEqual(result, self.prop1.vfilter(lambda x: x[0] <= 'a'))

    def test_to_dict(self):
        result = {('a', 'b', 'c'): [1, 2, 3], ('r', 'b', 'c'): [1, 2, 3]}
        self.assertDictEqual(result, self.prop1.to_dict(result_col=3))

    def test_to_dict2(self):
        prop = self.prop1.take([0, 1])
        result = {'a': ['b', 'b', 'b'], 'r': ['b', 'b', 'b']}
        self.assertDictEqual(result, prop.to_dict(result_col=1))

    def test_to_dict_nolist(self):
        result = {('a', 'b', 'c'): 3, ('r', 'b', 'c'): 3}
        self.assertDictEqual(result, self.prop1.to_dict(result_col=3, is_list=False))

    def test_unique(self):
        prop = self.prop1.take([0, 1])
        result = [('a', 'b'), ('r', 'b')]
        self.assertSetEqual(set(result), set(prop.unique(dtype='U7,U7')))

    def test_unique_int(self):
        prop = self.prop1.take(3)
        result = [1, 2, 3]
        self.assertSetEqual(set(result), set(prop.unique(dtype='i')))

    def test_unique2(self):
        prop = self.prop1.take([0, 1])
        result = [('a', 'b'), ('r', 'b')]
        self.assertSetEqual(set(result), set(prop.unique2()))

    def test_start_finish(self):
        prop = self.prop1.take([0, 3])
        compare_tups = lambda x, y, p: x[0] != y[0] or x[p] -1 != y[p]
        st_fin = prop.to_start_finish(compare_tups=compare_tups, pp=1)
        result = [('a', 1, 3), ('r', 1, 3)]
        self.assertListEqual(result, st_fin)

    def test_to_list(self):
        self.assertTrue(type(self.prop1.to_list()) is list)

    def test_vapply(self):
        result = ['a', 'a', 'a', 'r', 'r', 'r']
        self.assertListEqual(self.prop1.vapply(lambda v: v[0]), result)

    def test_vapply2(self):
        result = [1 for r in enumerate(self.prop1)]
        self.assertListEqual(self.prop1.vapply(lambda v: 1), result)

    def test_slicing(self):
        result = list(self.prop1)
        self.assertListEqual(result[:-1], self.prop1[:-1])

    def test_slicing2(self):
        result = list(self.prop1)
        self.assertListEqual(result[1:], self.prop1[1:])

    def test_get_elem(self):
        result = list(self.prop1)
        self.assertEqual(result[1], self.prop1[1])

    def test_kvapply(self):
        result = ['0a', '1a', '2a', '3r', '4r', '5r']
        prop = self.prop1.kvapply(lambda k, v: str(k) + v[0])
        self.assertListEqual(prop, result)

    def test_add(self):
        prop = self.tuplist_class()
        prop.add('b', 't', '3', 5)
        self.assertListEqual([('b', 't', '3', 5)], prop)

    def test_add_operator(self):
        prop = self.tuplist_class
        result = self.prop1 + self.prop1
        result1 = \
        [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3),
         ('r', 'b', 'c', 1), ('r', 'b', 'c', 2), ('r', 'b', 'c', 3),
         ('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3),
         ('r', 'b', 'c', 1), ('r', 'b', 'c', 2), ('r', 'b', 'c', 3)
         ]
        self.assertIsInstance(result, prop)
        self.assertListEqual(result, result1)

    def test_get(self):
        prop = self.prop1
        self.assertEqual(prop[0], ('a', 'b', 'c', 1))

    def test_get2(self):
        prop = self.prop1
        prop2 = prop[:2]
        self.assertIsInstance(prop2, pt.TupList)
        self.assertEqual(prop2, [('a', 'b', 'c', 1), ('a', 'b', 'c', 2)])

    def test_get3(self):
        prop = self.prop1
        prop2 = prop[:-2]
        self.assertIsInstance(prop2, pt.TupList)

    def test_get4(self):
        prop = self.prop1
        prop2 = prop[1:-1]
        self.assertIsInstance(prop2, pt.TupList)

    def test_intersect(self):
        prop = self.prop1
        other = [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 45)]
        result = {('a', 'b', 'c', 1), ('a', 'b', 'c', 2)}
        self.assertSetEqual(prop.intersect(other).to_set(), result)

    def setUp(self):
        self.prop1 = self.tuplist_class(TEST_TUP)
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
    # self = TupTest()
    # self.setUp()