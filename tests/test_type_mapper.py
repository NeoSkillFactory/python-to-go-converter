#!/usr/bin/env python3
"""Tests for type_mapper module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import pytest
from type_mapper import map_python_type_to_go, operator_to_go, builtin_to_go


class TestTypeMapping:
    def test_int(self):
        assert map_python_type_to_go("int") == "int"

    def test_float(self):
        assert map_python_type_to_go("float") == "float64"

    def test_str(self):
        assert map_python_type_to_go("str") == "string"

    def test_bool(self):
        assert map_python_type_to_go("bool") == "bool"

    def test_list(self):
        assert map_python_type_to_go("list") == "[]interface{}"

    def test_dict(self):
        assert map_python_type_to_go("dict") == "map[string]interface{}"

    def test_none(self):
        assert map_python_type_to_go("None") == "nil"

    def test_bytes(self):
        assert map_python_type_to_go("bytes") == "[]byte"

    def test_unknown_type(self):
        assert map_python_type_to_go("SomeClass") == "interface{}"


class TestOperatorMapping:
    def test_add(self):
        assert operator_to_go("Add") == "+"

    def test_sub(self):
        assert operator_to_go("Sub") == "-"

    def test_mult(self):
        assert operator_to_go("Mult") == "*"

    def test_div(self):
        assert operator_to_go("Div") == "/"

    def test_mod(self):
        assert operator_to_go("Mod") == "%"

    def test_eq(self):
        assert operator_to_go("Eq") == "=="

    def test_not_eq(self):
        assert operator_to_go("NotEq") == "!="

    def test_lt(self):
        assert operator_to_go("Lt") == "<"

    def test_and(self):
        assert operator_to_go("And") == "&&"

    def test_or(self):
        assert operator_to_go("Or") == "||"

    def test_not(self):
        assert operator_to_go("Not") == "!"

    def test_usub(self):
        assert operator_to_go("USub") == "-"

    def test_uadd(self):
        assert operator_to_go("UAdd") == "+"

    def test_unknown_operator(self):
        assert operator_to_go("Unknown") == "Unknown"


class TestBuiltinMapping:
    def test_print(self):
        assert builtin_to_go("print") == "fmt.Println"

    def test_len(self):
        assert builtin_to_go("len") == "len"

    def test_range(self):
        assert builtin_to_go("range") == "range"

    def test_unknown(self):
        assert builtin_to_go("unknown") is None
