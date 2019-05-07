import unittest
import pytups as pt

TEST_TUP = [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3),
            ('r', 'b', 'c', 1), ('r', 'b', 'c', 2), ('r', 'b', 'c', 3)]


class TupTest(unittest.TestCase):
    dict_class = pt.TupList

    def test_filter(self):
        prop = self.dict_class(TEST_TUP)
        result = [('a', 'c'), ('a', 'c'), ('a', 'c'),
                  ('r', 'c'), ('r', 'c'), ('r', 'c')]
        self.assertListEqual(result, prop.filter([0, 2]))

    def test_filter2(self):
        prop = self.dict_class(TEST_TUP)
        result = [1, 2, 3, 1, 2, 3]
        self.assertListEqual(result, prop.filter(3))

    def test_filter_list_f(self):
        prop = self.dict_class(TEST_TUP)
        result = [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3)]
        self.assertListEqual(result, prop.filter_list_f(lambda x: x[0] <= 'a'))

    def test_to_dict(self):
        prop = self.dict_class(TEST_TUP)
        result = {('a', 'b', 'c'): [1, 2, 3], ('r', 'b', 'c'): [1, 2, 3]}
        self.assertDictEqual(result, prop.to_dict(result_col=3))

    def test_to_dict2(self):
        prop = self.dict_class(TEST_TUP).filter([0, 1])
        result = {'a': ['b', 'b', 'b'], 'r': ['b', 'b', 'b']}
        self.assertDictEqual(result, prop.to_dict(result_col=1))

    def test_to_dict_nolist(self):
        prop = self.dict_class(TEST_TUP)
        result = {('a', 'b', 'c'): 3, ('r', 'b', 'c'): 3}
        self.assertDictEqual(result, prop.to_dict(result_col=3, is_list=False))

    def test_unique(self):
        prop = self.dict_class(TEST_TUP).filter([0, 1])
        result = [('a', 'b'), ('r', 'b')]
        self.assertSetEqual(set(result), set(prop.unique('U7,U7')))

    def test_unique_int(self):
        prop = self.dict_class(TEST_TUP).filter(3)
        result = [1, 2, 3]
        self.assertSetEqual(set(result), set(prop.unique('i')))

    def test_unique2(self):
        prop = self.dict_class(TEST_TUP).filter([0, 1])
        result = [('a', 'b'), ('r', 'b')]
        self.assertSetEqual(set(result), set(prop.unique2()))

    def test_start_finish(self):
        prop = self.dict_class(TEST_TUP).filter([0, 3])
        compare_tups = lambda x, y, p: x[0] != y[0] or x[p] -1 != y[p]
        st_fin = prop.to_start_finish(compare_tups=compare_tups, pp=1)
        result = [('a', 1, 3), ('r', 1, 3)]
        self.assertListEqual(result, st_fin)

    def test_to_list(self):
        prop = self.dict_class(TEST_TUP)
        self.assertTrue(type(prop.to_list()) is list)

    def add(self):
        prop = self.dict_class()
        prop.add('b', 't', '3', 5)
        self.assertListEqual([('b', 't', '3', 5)], prop)

    # intersect

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
    # self = TupTest()