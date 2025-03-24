import unittest
import pytups as pt
import os

TEST_TUP = [
    ("a", "b", "c", 1),
    ("a", "b", "c", 2),
    ("a", "b", "c", 3),
    ("r", "b", "c", 1),
    ("r", "b", "c", 2),
    ("r", "b", "c", 3),
]

TEST_DICT = [
    {1: "a", 2: "b", 3: "c", 4: 1},
    {1: "a", 2: "b", 3: "c", 4: 2},
    {1: "a", 2: "b", 3: "c", 4: 3},
    {1: "r", 2: "b", 3: "c", 4: 1},
    {1: "r", 2: "b", 3: "c", 4: 2},
    {1: "r", 2: "b", 3: "c", 4: 3},
]


class TupTest(unittest.TestCase):
    tuplist_class = pt.TupList

    def setUp(self):
        self.prop1 = self.tuplist_class(TEST_TUP)
        self.prop2 = self.tuplist_class(TEST_DICT)
        self.tmpcsv = "tmp.csv"
        try:
            os.remove(self.tmpcsv)
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove(self.tmpcsv)
        except FileNotFoundError:
            pass

    def test_filter(self):
        result = [
            ("a", "c"),
            ("a", "c"),
            ("a", "c"),
            ("r", "c"),
            ("r", "c"),
            ("r", "c"),
        ]
        self.assertListEqual(result, self.prop1.take([0, 2]))

    def test_filter2(self):
        result = [1, 2, 3, 1, 2, 3]
        self.assertListEqual(result, self.prop1.take(3))

    def test_filter_order(self):
        result = [(1, "a"), (2, "a"), (3, "a"), (1, "r"), (2, "r"), (3, "r")]
        self.assertListEqual(result, self.prop1.take([3, 0]))

    def test_filter_list_f(self):
        result = [("a", "b", "c", 1), ("a", "b", "c", 2), ("a", "b", "c", 3)]
        self.assertListEqual(result, self.prop1.vfilter(lambda x: x[0] <= "a"))

    def test_to_dict(self):
        result = {("a", "b", "c"): [1, 2, 3], ("r", "b", "c"): [1, 2, 3]}
        self.assertDictEqual(result, self.prop1.to_dict(result_col=3))

    def test_to_dict2(self):
        prop = self.prop1.take([0, 1])
        result = {"a": ["b", "b", "b"], "r": ["b", "b", "b"]}
        self.assertDictEqual(result, prop.to_dict(result_col=1))

    def test_to_dict_negative_col(self):
        prop = self.prop1.take([0, 1])
        result = {"a": ["b", "b", "b"], "r": ["b", "b", "b"]}
        self.assertDictEqual(result, prop.to_dict(result_col=-1))

    def test_to_dict_nolist(self):
        result = {("a", "b", "c"): 3, ("r", "b", "c"): 3}
        self.assertDictEqual(result, self.prop1.to_dict(result_col=3, is_list=False))

    def test_unique(self):
        prop = self.prop1.take([0, 1])
        result = [("a", "b"), ("r", "b")]
        self.assertSetEqual(set(result), set(prop.unique(dtype="U7,U7")))

    def test_unique_int(self):
        prop = self.prop1.take(3)
        result = [1, 2, 3]
        self.assertSetEqual(set(result), set(prop.unique(dtype="i")))

    def test_unique2(self):
        prop = self.prop1.take([0, 1])
        result = [("a", "b"), ("r", "b")]
        self.assertSetEqual(set(result), set(prop.unique2()))

    def test_start_finish(self):
        prop = self.prop1.take([0, 3])
        compare_tups = lambda x, y, p: x[0] != y[0] or x[p] - 1 != y[p]
        st_fin = prop.to_start_finish(compare_tups=compare_tups, pp=1)
        result = [("a", 1, 3), ("r", 1, 3)]
        self.assertListEqual(result, st_fin)

    def test_to_list(self):
        self.assertTrue(type(self.prop1.to_list()) is list)

    def test_vapply(self):
        result = ["a", "a", "a", "r", "r", "r"]
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
        result = ["0a", "1a", "2a", "3r", "4r", "5r"]
        prop = self.prop1.kvapply(lambda k, v: str(k) + v[0])
        self.assertListEqual(prop, result)

    def test_add(self):
        prop = self.tuplist_class()
        prop.add("b", "t", "3", 5)
        self.assertListEqual([("b", "t", "3", 5)], prop)

    def test_add_operator(self):
        prop = self.tuplist_class
        result = self.prop1 + self.prop1
        result1 = [
            ("a", "b", "c", 1),
            ("a", "b", "c", 2),
            ("a", "b", "c", 3),
            ("r", "b", "c", 1),
            ("r", "b", "c", 2),
            ("r", "b", "c", 3),
            ("a", "b", "c", 1),
            ("a", "b", "c", 2),
            ("a", "b", "c", 3),
            ("r", "b", "c", 1),
            ("r", "b", "c", 2),
            ("r", "b", "c", 3),
        ]
        self.assertIsInstance(result, prop)
        self.assertListEqual(result, result1)

    def test_get(self):
        prop = self.prop1
        self.assertEqual(prop[0], ("a", "b", "c", 1))

    def test_get2(self):
        prop = self.prop1
        prop2 = prop[:2]
        self.assertIsInstance(prop2, pt.TupList)
        self.assertEqual(prop2, [("a", "b", "c", 1), ("a", "b", "c", 2)])

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
        other = [("a", "b", "c", 1), ("a", "b", "c", 2), ("a", "b", "c", 45)]
        result = {("a", "b", "c", 1), ("a", "b", "c", 2)}
        self.assertSetEqual(prop.intersect(other).to_set(), result)

    def test_write(self):
        self.prop1.to_csv(self.tmpcsv)
        content = read_and_delete(self.tmpcsv)
        result = "a,b,c,1\na,b,c,2\na,b,c,3\nr,b,c,1\nr,b,c,2\nr,b,c,3\n"
        self.assertEqual(result, content)

    def test_write_dict(self):
        self.prop2.to_csv(self.tmpcsv)
        content = read_and_delete(self.tmpcsv)
        result = "1,2,3,4\na,b,c,1\na,b,c,2\na,b,c,3\nr,b,c,1\nr,b,c,2\nr,b,c,3\n"
        self.assertEqual(result, content)

    def test_write_dict_header(self):
        self.prop2.to_csv(self.tmpcsv, [a for a in range(1, 5)])
        content = read_and_delete(self.tmpcsv)
        result = "1,2,3,4\na,b,c,1\na,b,c,2\na,b,c,3\nr,b,c,1\nr,b,c,2\nr,b,c,3\n"
        self.assertEqual(result, content)

    def test_write_header(self):
        self.prop1.to_csv(self.tmpcsv, header=["A", "B", "C", "D"])
        content = read_and_delete(self.tmpcsv)
        result = "A,B,C,D\na,b,c,1\na,b,c,2\na,b,c,3\nr,b,c,1\nr,b,c,2\nr,b,c,3\n"
        self.assertEqual(result, content)

    def test_write_bad_header(self):
        to_error = lambda: self.prop1.to_csv(self.tmpcsv, header=["A", "B", "D"])
        self.assertRaises(ValueError, to_error)

    def test_write_bad_header_dict(self):
        to_error = lambda: self.prop2.to_csv(self.tmpcsv, header=["A", "B", "C", "D"])
        self.assertRaises(KeyError, to_error)

    def test_read(self):
        with open(self.tmpcsv, "w") as file:
            file.write("a,b,c,1\na,b,c,2\na,b,c,3\nr,b,c,1\nr,b,c,2\nr,b,c,3\n")

        def fmt(_tup):
            _tup[3] = int(_tup[3])
            return tuple(_tup)

        a = self.tuplist_class.from_csv(self.tmpcsv, func=fmt)
        self.assertEqual(a, self.prop1)

    def test_to_dictlist(self):
        self.assertEqual(self.prop1.to_dictlist([1, 2, 3, 4]), self.prop2)

    def test_to_dict_for_dictlist_0(self):
        # Should raise error if indices is missing and the object is a list of dict.
        self.assertRaises(ValueError, self.prop2.to_dict, result_col=1, is_list=False)
        self.assertRaises(ValueError, self.prop2.to_dict, result_col=1, is_list=True)

    def test_to_dict_for_dictlist_1(self):
        # Should work if result_col=None and indices is a single value
        # result1 = {d[2]: d for d in self.prop2}
        result1 = {"b": {1: "r", 2: "b", 3: "c", 4: 3}}
        self.assertDictEqual(
            self.prop2.to_dict(result_col=None, indices=2, is_list=False), result1
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=None, indices=[2], is_list=False), result1
        )

    def test_to_dict_for_dictlist_2(self):
        # Should work if result_col=None and indices has multiples values
        # result2 = {(d[1], d[2]):d for d in self.prop2}
        result2 = {
            ("a", "b"): {1: "a", 2: "b", 3: "c", 4: 3},
            ("r", "b"): {1: "r", 2: "b", 3: "c", 4: 3},
        }
        self.assertDictEqual(
            self.prop2.to_dict(result_col=None, indices=[1, 2], is_list=False), result2
        )

    def test_to_dict_for_dictlist_3(self):
        # Should work if indices and result_col are given as list or scalar.
        # TODO: a test with a string should be added
        # result3 = {d[1]:d[2] for d in self.prop2}
        result3 = {"a": "b", "r": "b"}
        self.assertDictEqual(
            self.prop2.to_dict(result_col=2, indices=1, is_list=False), result3
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=[2], indices=[1], is_list=False), result3
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=[2], indices=1, is_list=False), result3
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=2, indices=[1], is_list=False), result3
        )

    def test_to_dict_for_dictlist_4(self):
        # Should work with multiple values in result_col and indices (list or tuple)
        # result4 = {(d[1], d[2]):(d[3],d[4]) for d in self.prop2}
        result4 = {("a", "b"): ("c", 3), ("r", "b"): ("c", 3)}
        self.assertDictEqual(
            self.prop2.to_dict(result_col=[3, 4], indices=[1, 2], is_list=False),
            result4,
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=(3, 4), indices=(1, 2), is_list=False),
            result4,
        )

    def test_to_dict_for_dictlist_5(self):
        # Should work with is_list=True if result_col=None and indices is a single value
        result5 = {
            "a": [
                {1: "a", 2: "b", 3: "c", 4: 1},
                {1: "a", 2: "b", 3: "c", 4: 2},
                {1: "a", 2: "b", 3: "c", 4: 3},
            ],
            "r": [
                {1: "r", 2: "b", 3: "c", 4: 1},
                {1: "r", 2: "b", 3: "c", 4: 2},
                {1: "r", 2: "b", 3: "c", 4: 3},
            ],
        }
        self.assertDictEqual(
            self.prop2.to_dict(result_col=None, indices=1, is_list=True), result5
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=None, indices=[1], is_list=True), result5
        )

    def test_to_dict_for_dictlist_6(self):
        # Should work with is_list=True if result_col=None and indices has multiples values
        result6 = {
            ("a", "b"): [
                {1: "a", 2: "b", 3: "c", 4: 1},
                {1: "a", 2: "b", 3: "c", 4: 2},
                {1: "a", 2: "b", 3: "c", 4: 3},
            ],
            ("r", "b"): [
                {1: "r", 2: "b", 3: "c", 4: 1},
                {1: "r", 2: "b", 3: "c", 4: 2},
                {1: "r", 2: "b", 3: "c", 4: 3},
            ],
        }
        self.assertDictEqual(
            self.prop2.to_dict(result_col=None, indices=[1, 2], is_list=True), result6
        )

    def test_to_dict_for_dictlist_7(self):
        # Should work with is_list=True if indices and result_col are given as list or scalar.
        result7 = {"a": ["b", "b", "b"], "r": ["b", "b", "b"]}
        self.assertDictEqual(
            self.prop2.to_dict(result_col=2, indices=1, is_list=True), result7
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=[2], indices=1, is_list=True), result7
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=2, indices=[1], is_list=True), result7
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=[2], indices=[1], is_list=True), result7
        )

    def test_to_dict_for_dictlist_8(self):
        # Should work with is_list=True and with multiple values in result_col and indices (list or tuple)
        result8 = {
            ("a", "b"): [("c", 1), ("c", 2), ("c", 3)],
            ("r", "b"): [("c", 1), ("c", 2), ("c", 3)],
        }
        self.assertDictEqual(
            self.prop2.to_dict(result_col=[3, 4], indices=[1, 2], is_list=True), result8
        )
        self.assertDictEqual(
            self.prop2.to_dict(result_col=(3, 4), indices=(1, 2), is_list=True), result8
        )

    def test_copy_shallow(self):
        original = self.prop1.copy_deep()
        copy = original.copy_shallow()
        copy[0] = 1
        self.assertEqual(type(original[0]), tuple)

    def test_copy_shallow_modify(self):
        original = self.prop2.copy_deep()
        copy = original.copy_shallow()
        copy[0][1] = 1
        self.assertEqual(original[0][1], 1)

    def test_copy_deep(self):
        original = self.prop2.copy_deep()
        copy = original.copy_deep()
        copy[0][1] = 1
        self.assertEqual(original[0][1], "a")

    def test_chain(self):
        some_test = self.tuplist_class([[{"a": 1}], [{"b": 2, "c": 4}]])
        self.assertEqual(some_test.chain(), [{"a": 1}, {"b": 2, "c": 4}])

    def test_vapply_col(self):
        result = self.prop1.vapply_col(0, lambda v: v[1] + v[2])
        result_good = [
            ("bc", "b", "c", 1),
            ("bc", "b", "c", 2),
            ("bc", "b", "c", 3),
            ("bc", "b", "c", 1),
            ("bc", "b", "c", 2),
            ("bc", "b", "c", 3),
        ]
        self.assertEqual(result, result_good)

    def test_vapply_col_new(self):
        result = self.prop1.vapply_col(None, lambda v: v[1] + v[2])
        result_good = [
            ("a", "b", "c", 1, "bc"),
            ("a", "b", "c", 2, "bc"),
            ("a", "b", "c", 3, "bc"),
            ("r", "b", "c", 1, "bc"),
            ("r", "b", "c", 2, "bc"),
            ("r", "b", "c", 3, "bc"),
        ]
        self.assertEqual(result, result_good)

    def test_vapply_col_last(self):
        result = self.prop1.vapply_col(-1, lambda v: v[1] + v[2])
        result_good = [
            ("a", "b", "c", "bc"),
            ("a", "b", "c", "bc"),
            ("a", "b", "c", "bc"),
            ("r", "b", "c", "bc"),
            ("r", "b", "c", "bc"),
            ("r", "b", "c", "bc"),
        ]
        self.assertEqual(result, result_good)

    def test_vapply_col_dict(self):
        a = self.prop2.copy_deep()
        result = a.vapply_col(5, lambda v: v[1] + v[2] + str(v[4]))
        result_good = [
            {1: "a", 2: "b", 3: "c", 4: 1, 5: "ab1"},
            {1: "a", 2: "b", 3: "c", 4: 2, 5: "ab2"},
            {1: "a", 2: "b", 3: "c", 4: 3, 5: "ab3"},
            {1: "r", 2: "b", 3: "c", 4: 1, 5: "rb1"},
            {1: "r", 2: "b", 3: "c", 4: 2, 5: "rb2"},
            {1: "r", 2: "b", 3: "c", 4: 3, 5: "rb3"},
        ]
        self.assertEqual(result, result_good)


def read_and_delete(_filename):
    with open(_filename, "r") as file:
        content = file.read()
    try:
        os.remove(_filename)
    except FileNotFoundError:
        pass
    return content


if __name__ == "__main__":
    unittest.main()
    # self = TupTest()
    # self.setUp()
