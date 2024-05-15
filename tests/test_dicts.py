# Some of these tests were inspired from the addict package
# https://github.com/mewwts/addict

import json
import copy
import unittest
import pickle
import pytups as pt

TEST_VAL = [1, 2, 3]
TEST_VAL2 = 4
TEST_DICT = {"a": {"b": {"c": TEST_VAL}}}
TEST_DICT_2 = {"a": {"b": {"c": TEST_VAL}}, "b": {("c", "t"): {"d": TEST_VAL2}}}
TEST_DICT_3 = {"ABC": {("a", "b", "c"): TEST_VAL2}}


class DictTest(unittest.TestCase):
    dict_class = pt.SuperDict

    def test_property(self):
        prop = self.dict_class.from_dict(TEST_DICT).get_property("b")
        self.assertDictEqual(prop, {"a": {"c": [1, 2, 3]}})

    def test_dictup(self):
        prop = self.dict_class.from_dict(TEST_DICT).to_dictup()
        self.assertDictEqual(prop, {("a", "b", "c"): TEST_VAL})

    def test_tuplist(self):
        prop = self.dict_class.from_dict(TEST_DICT).to_dictup().to_tuplist()
        self.assertListEqual(
            prop, [("a", "b", "c", 1), ("a", "b", "c", 2), ("a", "b", "c", 3)]
        )

    def test_filter_wrong(self):
        prop = lambda: self.dict_class.from_dict(TEST_DICT).filter(["b"])
        with self.assertRaises(KeyError):
            prop()

    def test_filter_good(self):
        prop = self.dict_class.from_dict(TEST_DICT_2).filter(["b"])
        self.assertDictEqual(prop, {"b": {("c", "t"): {"d": TEST_VAL2}}})

    def test_filter_good_check(self):
        prop = self.dict_class.from_dict(TEST_DICT_2).filter(["b"], check=False)
        self.assertDictEqual(prop, {"b": {("c", "t"): {"d": TEST_VAL2}}})

    def test_to_dictdict(self):
        prop = self.dict_class.from_dict(
            {"b": {("c", "t"): {"d": TEST_VAL2}}}
        ).to_dictdict()
        self.assertDictEqual(prop, {"b": {"c": {"t": {"d": TEST_VAL2}}}})

    def test_to_dictdict2(self):
        prop = self.dict_class.from_dict(TEST_DICT_3).to_dictdict()
        self.assertDictEqual(prop, {"ABC": {"a": {"b": {"c": TEST_VAL2}}}})

    def test_set_one_level_item(self):
        some_dict = {"a": TEST_VAL}
        prop = self.dict_class()
        prop["a"] = TEST_VAL
        self.assertDictEqual(prop, some_dict)

    def test_set_two_level_items(self):
        some_dict = {"a": {"b": TEST_VAL}}
        prop = self.dict_class()
        prop.set_m("a", "b", value=TEST_VAL)
        self.assertDictEqual(prop, some_dict)

    def test_set_three_level_items(self):
        prop = self.dict_class()
        prop.set_m("a", "b", "c", value=TEST_VAL)
        self.assertDictEqual(prop, TEST_DICT)

    def test_set_one_level_property(self):
        prop = self.dict_class()
        prop["a"] = TEST_VAL
        self.assertDictEqual(prop, {"a": TEST_VAL})

    def test_set_two_level_properties(self):
        prop = self.dict_class()
        prop.set_m("a", "b", value=TEST_VAL)
        self.assertDictEqual(prop, {"a": {"b": TEST_VAL}})

    def test_set_existing_key(self):
        prop = self.dict_class()
        prop.set_m("a", "b", "c", "d", value=1)
        self.assertDictEqual(prop, {"a": {"b": {"c": {"d": 1}}}})

    def test_set_three_level_properties(self):
        prop = self.dict_class()
        prop.set_m("a", "b", "c", value=TEST_VAL)
        self.assertDictEqual(prop, TEST_DICT)

    def test_init_with_dict(self):
        self.assertDictEqual(TEST_DICT, self.dict_class(TEST_DICT))

    def test_init_with_kws(self):
        prop = self.dict_class(a=2, b={"a": 2}, c=[{"a": 2}])
        self.assertDictEqual(prop, {"a": 2, "b": {"a": 2}, "c": [{"a": 2}]})

    def test_init_with_tuples(self):
        prop = self.dict_class([(0, 1), (1, 2), (2, 3)])
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_list(self):
        prop = self.dict_class([(0, 1), (1, 2), (2, 3)])
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_generator(self):
        prop = self.dict_class(((i, i + 1) for i in range(3)))
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    # def test_init_with_tuples_and_empty_list(self):
    #     prop = self.dict_class([(0, 1), [], (2, 3)])
    #     self.assertDictEqual(prop, {0: 1, 2: 3})

    def test_init_raises(self):
        def init():
            self.dict_class(5)

        def init2():
            self.dict_class("a")

        self.assertRaises(TypeError, init)
        self.assertRaises(ValueError, init2)

    def test_init_with_empty_stuff(self):
        a = self.dict_class({})
        b = self.dict_class([])
        self.assertDictEqual(a, {})
        self.assertDictEqual(b, {})

    # def test_init_with_list_of_dicts(self):
    #     a = self.dict_class.from_dict({'a': [{'b': 2}]})
    #     self.assertIsInstance(a['a'][0], self.dict_class)
    #     self.assertEqual(a['a'][0]['b'], 2)

    def test_init_with_kwargs(self):
        a = self.dict_class(a="b", c=dict(d="e", f=dict(g="h")))
        a = self.dict_class.from_dict(a)
        self.assertEqual(a["a"], "b")
        self.assertIsInstance(a["c"], self.dict_class)

        self.assertEqual(a.get_m("c", "f", "g"), "h")
        self.assertIsInstance(a["c"]["f"], self.dict_class)

    def test_getitem(self):
        prop = self.dict_class(TEST_DICT)
        self.assertEqual(prop["a"]["b"]["c"], TEST_VAL)

    def test_empty_getitem(self):
        prop = self.dict_class()
        prop.get_m("a", "b", "c")
        self.assertEqual(prop, {})

    def test_getattr(self):
        prop = self.dict_class(TEST_DICT)
        self.assertEqual(prop["a"]["b"]["c"], TEST_VAL)

    def test_isinstance(self):
        self.assertTrue(isinstance(self.dict_class(), dict))

    def test_str(self):
        prop = self.dict_class(TEST_DICT)
        self.assertEqual(str(prop), str(TEST_DICT))

    def test_json(self):
        some_dict = TEST_DICT
        some_json = json.dumps(some_dict)
        prop = self.dict_class()
        prop.set_m("a", "b", "c", value=TEST_VAL)
        prop_json = json.dumps(prop)
        self.assertEqual(some_json, prop_json)

    def test_delitem(self):
        prop = self.dict_class.from_dict({"a": 2})
        del prop["a"]
        self.assertDictEqual(prop, {})

    def test_delitem_nested(self):
        prop = self.dict_class.from_dict(TEST_DICT)
        del prop["a"]["b"]["c"]
        self.assertDictEqual(prop, {"a": {"b": {}}})

    def test_delattr(self):
        prop = self.dict_class.from_dict({"a": 2})
        del prop["a"]
        self.assertDictEqual(prop, {})

    def test_delattr_nested(self):
        prop = self.dict_class.from_dict(TEST_DICT)
        del prop["a"]["b"]["c"]
        self.assertDictEqual(prop, {"a": {"b": {}}})

    def test_delitem_delattr(self):
        prop = self.dict_class.from_dict(TEST_DICT)
        del prop["a"]["b"]
        self.assertDictEqual(prop, {"a": {}})

    def test_tuple_key(self):
        prop = self.dict_class()
        prop[(1, 2)] = 2
        self.assertDictEqual(prop, {(1, 2): 2})
        self.assertEqual(prop[(1, 2)], 2)

    def test_dir(self):
        key = "a"
        prop = self.dict_class({key: 1})
        dir_prop = dir(prop)

        dir_dict = dir(self.dict_class)
        for d in dir_dict:
            self.assertTrue(d in dir_prop, d)

        self.assertTrue("__methods__" not in dir_prop)
        self.assertTrue("__members__" not in dir_prop)

    def test_dir_with_members(self):
        prop = self.dict_class({"__members__": 1})
        dir(prop)
        self.assertTrue("__members__" in prop.keys())

    def test_fill_default(self):
        prop = self.dict_class.from_dict(TEST_DICT)
        prop2 = prop.fill_with_default(["f", "g", "h"])
        prop2_result = {"a": {"b": {"c": [1, 2, 3]}}, "f": 0, "g": 0, "h": 0}
        self.assertEqual(prop2, prop2_result)

    def test_fill_default2(self):
        prop = self.dict_class.from_dict(TEST_DICT)
        prop2 = prop.fill_with_default(("f", "g", "h"), "OK")
        prop2_result = {"a": {"b": {"c": [1, 2, 3]}}, "f": "OK", "g": "OK", "h": "OK"}
        self.assertEqual(prop2, prop2_result)

    # TODO: vapply tests

    def test_sapply(self):
        import operator as op

        prop = self.dict_class.from_dict(TEST_DICT).to_dictup()
        prop2 = (
            self.dict_class.from_dict(TEST_DICT).to_dictup().vapply(lambda v: [4, 5, 6])
        )
        sum_prop = prop.sapply(op.__add__, prop2).to_dictdict()
        result = {"a": {"b": {"c": [1, 2, 3, 4, 5, 6]}}}
        self.assertEqual(sum_prop, result)

    # def test_to_dict(self):
    #     nested = {'a': [{'a': 0}, 2], 'b': {}, 'c': 2}
    #     prop = self.dict_class(nested)
    #     regular = prop.to_dict()
    #     self.assertDictEqual(regular, prop)
    #     self.assertDictEqual(regular, nested)
    #     self.assertNotIsInstance(regular, self.dict_class)
    #
    #     def get_attr():
    #         regular.a = 2
    #     self.assertRaises(AttributeError, get_attr)
    #
    #     def get_attr_deep():
    #         regular['a'][0].a = 1
    #     self.assertRaises(AttributeError, get_attr_deep)

    # def test_to_dict_with_tuple(self):
    #     nested = {'a': ({'a': 0}, {2: 0})}
    #     prop = self.dict_class(nested)
    #     regular = prop.to_dict()
    #     self.assertDictEqual(regular, prop)
    #     self.assertDictEqual(regular, nested)
    #     self.assertIsInstance(regular['a'], tuple)
    #     self.assertNotIsInstance(regular['a'][0], self.dict_class)

    def test_update(self):
        old = self.dict_class()
        old.set_m("child", "a", value="a")
        old.set_m("child", "b", value="b")
        old["foo"] = "c"

        new = self.dict_class()
        new.set_m("child", "b", value="b2")
        new.set_m("child", "c", value="c")
        new.set_m("foo", "bar", value=True)

        old.update(new)

        reference = {"foo": {"bar": True}, "child": {"a": "a", "c": "c", "b": "b2"}}

        self.assertDictEqual(old, reference)

    def test_update_with_lists(self):
        org = self.dict_class()
        org["a"] = [1, 2, {"a": "superman"}]
        someother = self.dict_class()
        someother["b"] = [{"b": 123}]
        org.update(someother)

        correct = {"a": [1, 2, {"a": "superman"}], "b": [{"b": 123}]}

        org.update(someother)
        self.assertDictEqual(org, correct)
        self.assertIsInstance(org["b"][0], dict)

    def test_update_with_kws(self):
        org = self.dict_class(one=1, two=2)
        someother = self.dict_class(one=3)
        someother.update(one=1, two=2)
        self.assertDictEqual(org, someother)

    def test_update_with_args_and_kwargs(self):
        expected = {"a": 1, "b": 2}
        org = self.dict_class()
        org.update({"a": 3, "b": 2}, a=1)
        self.assertDictEqual(org, expected)

    def test_update_with_multiple_args(self):
        def update():
            org.update({"a": 2}, {"a": 1})

        org = self.dict_class()
        self.assertRaises(TypeError, update)

    def test_hook_in_constructor(self):
        a_dict = self.dict_class.from_dict(TEST_DICT)
        self.assertIsInstance(a_dict["a"], self.dict_class)

    def test_copy(self):
        class MyMutableObject(object):
            def __init__(self):
                self.attribute = None

        foo = MyMutableObject()
        foo.attribute = True

        a = self.dict_class()
        a["child"] = self.dict_class()
        a["child"]["immutable"] = 42
        a["child"]["mutable"] = foo

        b = a.copy()

        # immutable object should not change
        b["child"]["immutable"] = 21
        self.assertEqual(a["child"]["immutable"], 21)

        # mutable object should change
        b["child"]["mutable"].attribute = False
        self.assertEqual(
            a["child"]["mutable"].attribute, b["child"]["mutable"].attribute
        )

        # changing child of b should not affect a
        b["child"] = "new stuff"
        self.assertTrue(isinstance(a["child"], self.dict_class))

    def test_deepcopy(self):
        class MyMutableObject(object):
            def __init__(self):
                self.attribute = None

        foo = MyMutableObject()
        foo.attribute = True

        a = self.dict_class()
        a["child"] = self.dict_class()
        a["child"]["immutable"] = 42
        a["child"]["mutable"] = foo

        b = copy.deepcopy(a)

        # immutable object should not change
        b["child"]["immutable"] = 21
        self.assertEqual(a["child"]["immutable"], 42)

        # mutable object should not change
        b["child"]["mutable"].attribute = False
        self.assertTrue(a["child"]["mutable"].attribute)

        # changing child of b should not affect a
        b.child = "new stuff"
        self.assertTrue(isinstance(a["child"], self.dict_class))

    def test_pickle(self):
        a = self.dict_class(TEST_DICT)
        self.assertEqual(a, pickle.loads(pickle.dumps(a)))

    def test_init_from_zip(self):
        keys = ["a"]
        values = [42]
        items = zip(keys, values)
        d = self.dict_class(items)
        self.assertEqual(d["a"], 42)

    def test_iterable1(self):
        no = pt.tools.is_really_iterable("sqdf")
        self.assertEqual(no, False)

    def test_iterable2(self):
        yes = pt.tools.is_really_iterable([1, 3, 5])
        self.assertEqual(yes, True)

    def test_iterable3(self):
        yes = pt.tools.is_really_iterable((1, 9))
        self.assertEqual(yes, True)

    # def test_setdefault_simple(self):
    #     d = self.dict_class()
    #     d.setdefault('a', 2)
    #     self.assertEqual(d['a'], 2)
    #     d.setdefault('a', 3)
    #     self.assertEqual(d['a'], 2)
    #     d.setdefault('c', []).append(2)
    #     self.assertEqual(d['c'], [2])
    #
    # def test_setdefault_nested(self):
    #     d = self.dict_class()
    #     d.one.setdefault('two', [])
    #     self.assertEqual(d.one.two, [])
    #     d.one.setdefault('three', []).append(3)
    #     self.assertEqual(d.one.three, [3])

    def test_copy_shallow(self):
        original = self.dict_class.from_dict(TEST_DICT)
        copy = original.copy_shallow()
        copy["a"] = 1
        self.assertEqual(type(original["a"]), self.dict_class)

    def test_copy_shallow_modify(self):
        original = self.dict_class.from_dict(TEST_DICT).copy_deep()
        copy = original.copy_shallow()
        copy["a"]["b"] = 1
        self.assertEqual(original["a"]["b"], 1)

    def test_copy_deep(self):
        original = self.dict_class.from_dict(TEST_DICT)
        copy = original.copy_deep()
        copy["a"]["b"] = 1
        self.assertEqual(type(original["a"]["b"]), self.dict_class)

    def test_copy_deep2(self):
        original = self.dict_class.from_dict(TEST_DICT)
        copy = original.copy_deep2()
        copy["a"]["b"] = 1
        self.assertEqual(type(original["a"]["b"]), self.dict_class)

    def test_parent_key_item(self):
        a = self.dict_class()
        try:
            a.set_m("keys", "x", value=1)
        except AttributeError as e:
            self.fail(e)
        try:
            a.set_m(1, "x", value=3)
        except Exception as e:
            self.fail(e)
        self.assertEqual(a, {"keys": {"x": 1}, 1: {"x": 3}})

    def test_parent_key_prop(self):
        a = self.dict_class()
        try:
            a.set_m("y", "x", value=1)
        except AttributeError as e:
            self.fail(e)
        self.assertEqual(a, {"y": {"x": 1}})

    def test_add_dicts(self):
        a = self.dict_class({"a": 1})
        b = self.dict_class({"a": 2, "b": 1})
        c = a + b
        self.assertEqual(c, {"a": 3})

    def test_add_int(self):
        a = self.dict_class({"a": 1, "b": 5})
        c = a + 2
        self.assertEqual(c, {"a": 3, "b": 7})

    def test_add_float(self):
        a = self.dict_class({"a": 1, "b": 5})
        c = a + 2.5
        self.assertEqual(c, {"a": 3.5, "b": 7.5})

    def test_subtract_dict(self):
        a = self.dict_class({"a": 1})
        b = self.dict_class({"a": 2})
        c = a - b
        self.assertEqual(c, {"a": -1})

    def test_subtract_int(self):
        a = self.dict_class({"a": 1, "b": 1})
        c = a - 1
        self.assertEqual(c, {"a": 0, "b": 0})

    def test_subtract_float(self):
        a = self.dict_class({"a": 1, "b": 1})
        c = a - 1.5
        self.assertEqual(c, {"a": -0.5, "b": -0.5})

    def test_multiply_dicts(self):
        a = self.dict_class({"a": 1})
        b = self.dict_class({"a": 2})
        c = a * b
        self.assertEqual(c, {"a": 2})

    def test_multiply_int(self):
        a = self.dict_class({"a": 1, "b": -1})
        c = a * 2
        self.assertEqual(c, {"a": 2, "b": -2})

    def test_multiply_float(self):
        a = self.dict_class({"a": 1, "b": 5})
        c = a * 2.5
        self.assertEqual(c, {"a": 2.5, "b": 12.5})

    def test_divide_dicts(self):
        a = self.dict_class({"a": 4})
        b = self.dict_class({"a": 2})
        c = a / b
        self.assertEqual(c, {"a": 2})

    def test_divide_int(self):
        a = self.dict_class({"a": 4, "b": 4})
        c = a / 3
        self.assertEqual(c, {"a": 4 / 3, "b": 4 / 3})

    def test_divide_float(self):
        a = self.dict_class({"a": 4, "b": 6})
        c = a / 3.0
        self.assertEqual(c, {"a": 4 / 3.0, "b": 6 / 3.0})

    def test_integer_div_dicts(self):
        a = self.dict_class({"a": 4})
        b = self.dict_class({"a": 3, "b": 1})
        c = a // b
        self.assertEqual(c, {"a": 1})

    def test_integer_div_int(self):
        a = self.dict_class({"a": 4, "b": 6})
        c = a // 3
        self.assertEqual(c, {"a": 1, "b": 2})

    def test_integer_div_float(self):
        a = self.dict_class({"a": 4, "b": 7})
        c = a // 3.5
        self.assertEqual(c, {"a": 1, "b": 2})

    def test_add_strings(self):
        a = self.dict_class({"a": "a"})
        b = self.dict_class({"a": "b"})
        c = a + b
        self.assertEqual(c, {"a": "ab"})

    def test_add_lists(self):
        a = self.dict_class({"a": [1]})
        b = self.dict_class({"a": [2]})
        c = a + b
        self.assertEqual(c, {"a": [1, 2]})

    def test_add_int_to_list(self):
        a = self.dict_class({"a": [1]})
        lambda_add = lambda a: a + 2
        self.assertRaises(TypeError, lambda_add, a)

    def test_add_int_to_string(self):
        a = self.dict_class({"a": "a"})
        lambda_add = lambda a: a + 2
        self.assertRaises(TypeError, lambda_add, a)

    def test_add_str_to_int(self):
        a = self.dict_class({"a": 2})
        lambda_add = lambda a: a + "2"
        self.assertRaises(TypeError, lambda_add, a)

    def test_multiply_string_into_int(self):
        a = self.dict_class({"a": "a"})
        c = a * 2
        self.assertEqual(c, {"a": "aa"})

    def test_multiply_int_to_string(self):
        a = self.dict_class({"a": 2})
        c = a * "2"
        self.assertEqual(c, {"a": "22"})

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
