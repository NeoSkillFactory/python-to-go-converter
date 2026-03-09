#!/usr/bin/env python3
"""Tests for go_generator module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import pytest
from ast_parser import parse
from go_generator import GoGenerator


def convert(source, imports=None):
    """Helper to convert Python source to Go code."""
    ir = parse(source)
    gen = GoGenerator(ir, required_imports=imports)
    return gen.generate()


class TestFunctions:
    def test_simple_function(self):
        go = convert("def add(x: int, y: int) -> int:\n    return x + y")
        assert "func add(x int, y int) int {" in go
        assert "return (x + y)" in go

    def test_function_no_return_type(self):
        go = convert("def greet(name: str):\n    print(name)")
        assert "func greet(name string) {" in go
        assert "fmt.Println(name)" in go

    def test_function_no_type_hints(self):
        go = convert("def foo(x, y):\n    return x")
        assert "func foo(x interface{}, y interface{}) {" in go

    def test_empty_function(self):
        go = convert("def empty():\n    pass")
        assert "func empty() {" in go
        assert "// pass" in go


class TestVariables:
    def test_simple_assignment(self):
        go = convert("def f():\n    x = 42")
        assert "x := 42" in go

    def test_string_assignment(self):
        go = convert('def f():\n    name = "Alice"')
        assert 'name := "Alice"' in go

    def test_reassignment(self):
        go = convert("def f():\n    x = 1\n    x = 2")
        assert "x := 1" in go
        assert "x = 2" in go

    def test_augmented_assignment(self):
        go = convert("def f():\n    x = 0\n    x += 1")
        assert "x += 1" in go


class TestControlFlow:
    def test_if_else(self):
        go = convert("def f():\n    if x > 0:\n        pass\n    else:\n        pass")
        assert "if x > 0 {" in go
        assert "} else {" in go

    def test_elif(self):
        source = "def f():\n    if x > 0:\n        pass\n    elif x < 0:\n        pass\n    else:\n        pass"
        go = convert(source)
        assert "} else if x < 0 {" in go

    def test_for_range(self):
        go = convert("def f():\n    for i in range(10):\n        pass")
        assert "for i := 0; i < 10; i += 1 {" in go

    def test_for_range_start_stop(self):
        go = convert("def f():\n    for i in range(2, 10):\n        pass")
        assert "for i := 2; i < 10; i += 1 {" in go

    def test_for_range_step(self):
        go = convert("def f():\n    for i in range(0, 10, 2):\n        pass")
        assert "for i := 0; i < 10; i += 2 {" in go

    def test_for_iterable(self):
        go = convert("def f():\n    for x in items:\n        pass")
        assert "for _, x := range items {" in go

    def test_while_loop(self):
        go = convert("def f():\n    while x > 0:\n        x = x - 1")
        assert "for x > 0 {" in go
        assert "while" not in go

    def test_while_true(self):
        go = convert("def f():\n    while True:\n        break")
        assert "for {" in go
        assert "break" in go

    def test_break_continue(self):
        go = convert("def f():\n    for i in range(10):\n        break\n        continue")
        assert "break" in go
        assert "continue" in go


class TestDataStructures:
    def test_int_list(self):
        go = convert("def f():\n    nums = [1, 2, 3]")
        assert "[]int{1, 2, 3}" in go

    def test_string_list(self):
        go = convert('def f():\n    names = ["a", "b"]')
        assert '[]string{"a", "b"}' in go

    def test_empty_list(self):
        go = convert("def f():\n    items = []")
        assert "[]interface{}{}" in go

    def test_dict(self):
        go = convert('def f():\n    m = {"a": 1, "b": 2}')
        assert "map[string]int" in go

    def test_empty_dict(self):
        go = convert("def f():\n    m = {}")
        assert "map[string]interface{}{}" in go


class TestExpressions:
    def test_print(self):
        go = convert("print('hello')")
        assert 'fmt.Println("hello")' in go
        assert '"fmt"' in go

    def test_len(self):
        go = convert("def f():\n    n = len(items)")
        assert "len(items)" in go

    def test_binary_ops(self):
        go = convert("def f():\n    x = a + b\n    y = a * b\n    z = a % b")
        assert "(a + b)" in go
        assert "(a * b)" in go
        assert "(a % b)" in go

    def test_comparison(self):
        go = convert("def f():\n    x = a > b")
        assert "a > b" in go

    def test_boolean_ops(self):
        go = convert("def f():\n    x = a and b")
        assert "a && b" in go

    def test_unary_minus(self):
        go = convert("def f() -> int:\n    return -1")
        assert "return -1" in go

    def test_string_constant(self):
        go = convert('def f():\n    x = "hello"')
        assert '"hello"' in go

    def test_none_constant(self):
        go = convert("def f():\n    x = None")
        assert "nil" in go

    def test_bool_constants(self):
        go = convert("def f():\n    x = True\n    y = False")
        assert "true" in go
        assert "false" in go

    def test_subscript(self):
        go = convert("def f():\n    x = items[0]")
        assert "items[0]" in go

    def test_attribute_access(self):
        go = convert("def f():\n    x = obj.attr")
        assert "obj.attr" in go


class TestExceptionHandling:
    def test_raise(self):
        go = convert("def f():\n    raise Exception('error')")
        assert 'panic("error")' in go

    def test_raise_no_arg(self):
        go = convert("def f():\n    raise")
        assert 'panic("error")' in go

    def test_assert_with_message(self):
        go = convert('def f():\n    assert x > 0, "must be positive"')
        assert "if !(x > 0) {" in go
        assert 'panic("must be positive")' in go

    def test_assert_no_message(self):
        go = convert("def f():\n    assert x > 0")
        assert 'panic("assertion failed")' in go

    def test_try_except(self):
        go = convert("def f():\n    try:\n        x = 1\n    except:\n        pass")
        assert "// try/except block" in go


class TestClasses:
    def test_simple_class(self):
        source = """
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
"""
        go = convert(source)
        assert "type Point struct {" in go
        assert "func (c *Point) __init__" in go

    def test_class_method(self):
        source = """
class Counter:
    def __init__(self):
        self.count = 0
    def inc(self):
        self.count += 1
"""
        go = convert(source)
        assert "type Counter struct {" in go
        assert "count int" in go
        assert "func (c *Counter) inc() {" in go
        assert "c.count += 1" in go


class TestImports:
    def test_fmt_auto_added(self):
        go = convert("print('hello')")
        assert '"fmt"' in go

    def test_no_unnecessary_imports(self):
        go = convert("x = 42")
        assert "import" not in go

    def test_package_declaration(self):
        go = convert("x = 42")
        assert go.startswith("package main")


class TestUnsupported:
    def test_async_function(self):
        go = convert("async def foo(): pass")
        assert "// Unsupported feature: async function" in go

    def test_with_statement(self):
        go = convert("with open('f') as f:\n    pass")
        assert "// Unsupported feature: with statement" in go

    def test_delete(self):
        go = convert("del x")
        assert "// delete not supported" in go


class TestEdgeCases:
    def test_empty_source(self):
        go = convert("")
        assert "package main" in go

    def test_nested_if(self):
        source = "def f():\n    if a:\n        if b:\n            pass"
        go = convert(source)
        assert go.count("if") == 2

    def test_multiple_functions(self):
        source = "def f():\n    pass\ndef g():\n    pass"
        go = convert(source)
        assert "func f()" in go
        assert "func g()" in go

    def test_recursive_function(self):
        source = "def fact(n: int) -> int:\n    if n <= 1:\n        return 1\n    return n * fact(n - 1)"
        go = convert(source)
        assert "func fact(n int) int {" in go
        assert "fact((n - 1))" in go
