#!/usr/bin/env python3
"""Tests for ast_parser module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import pytest
from ast_parser import parse


class TestParseBasic:
    def test_simple_function(self):
        ir = parse("def foo(): pass")
        assert len(ir) == 1
        assert ir[0]['type'] == 'function'
        assert ir[0]['name'] == 'foo'

    def test_function_with_args(self):
        ir = parse("def add(x: int, y: int) -> int:\n    return x + y")
        func = ir[0]
        assert func['type'] == 'function'
        assert len(func['args']) == 2
        assert func['args'][0]['name'] == 'x'
        assert func['args'][0]['type'] == {'type': 'name', 'id': 'int'}
        assert func['returns'] == {'type': 'name', 'id': 'int'}

    def test_assignment(self):
        ir = parse("x = 42")
        assert ir[0]['type'] == 'assign'
        assert ir[0]['targets'][0] == {'type': 'name', 'id': 'x'}
        assert ir[0]['value'] == {'type': 'constant', 'value': 42}

    def test_aug_assignment(self):
        ir = parse("x += 1")
        assert ir[0]['type'] == 'aug_assign'
        assert ir[0]['op'] == 'Add'

    def test_if_statement(self):
        ir = parse("if x > 0:\n    pass")
        assert ir[0]['type'] == 'if'
        assert ir[0]['test']['type'] == 'compare'

    def test_for_loop(self):
        ir = parse("for i in range(10):\n    pass")
        stmt = ir[0]
        assert stmt['type'] == 'for'
        assert stmt['target'] == {'type': 'name', 'id': 'i'}

    def test_while_loop(self):
        ir = parse("while True:\n    break")
        stmt = ir[0]
        assert stmt['type'] == 'while'
        assert stmt['test'] == {'type': 'constant', 'value': True}
        assert stmt['body'][0]['type'] == 'break'

    def test_return(self):
        ir = parse("def f():\n    return 42")
        body = ir[0]['body']
        assert body[0]['type'] == 'return'
        assert body[0]['value'] == {'type': 'constant', 'value': 42}

    def test_pass(self):
        ir = parse("pass")
        assert ir[0]['type'] == 'pass'

    def test_break_continue(self):
        ir = parse("for i in x:\n    break\n    continue")
        body = ir[0]['body']
        assert body[0]['type'] == 'break'
        assert body[1]['type'] == 'continue'

    def test_class_def(self):
        ir = parse("class Foo:\n    pass")
        assert ir[0]['type'] == 'class'
        assert ir[0]['name'] == 'Foo'

    def test_raise(self):
        ir = parse("raise Exception('msg')")
        assert ir[0]['type'] == 'raise'
        assert ir[0]['exc']['type'] == 'call'

    def test_assert(self):
        ir = parse('assert x > 0, "must be positive"')
        stmt = ir[0]
        assert stmt['type'] == 'assert'
        assert stmt['msg'] == {'type': 'constant', 'value': 'must be positive'}

    def test_try_except(self):
        ir = parse("try:\n    pass\nexcept:\n    pass")
        assert ir[0]['type'] == 'try'

    def test_unsupported_async(self):
        ir = parse("async def foo(): pass")
        assert ir[0]['type'] == 'unsupported'
        assert ir[0]['feature'] == 'async function'

    def test_unsupported_with(self):
        ir = parse("with open('f') as f:\n    pass")
        assert ir[0]['type'] == 'unsupported'

    def test_list_comprehension(self):
        ir = parse("x = [i for i in range(10)]")
        # The value should be unsupported
        assert ir[0]['value']['type'] == 'unsupported'

    def test_delete(self):
        ir = parse("del x")
        assert ir[0]['type'] == 'delete'


class TestParseExpressions:
    def test_constant_int(self):
        ir = parse("x = 42")
        assert ir[0]['value'] == {'type': 'constant', 'value': 42}

    def test_constant_string(self):
        ir = parse("x = 'hello'")
        assert ir[0]['value'] == {'type': 'constant', 'value': 'hello'}

    def test_constant_bool(self):
        ir = parse("x = True")
        assert ir[0]['value'] == {'type': 'constant', 'value': True}

    def test_constant_none(self):
        ir = parse("x = None")
        assert ir[0]['value'] == {'type': 'constant', 'value': None}

    def test_binop(self):
        ir = parse("x = a + b")
        val = ir[0]['value']
        assert val['type'] == 'binop'
        assert val['op'] == 'Add'

    def test_compare(self):
        ir = parse("x = a > b")
        val = ir[0]['value']
        assert val['type'] == 'compare'
        assert val['ops'] == ['Gt']

    def test_boolop(self):
        ir = parse("x = a and b")
        val = ir[0]['value']
        assert val['type'] == 'boolop'
        assert val['op'] == 'And'

    def test_unaryop(self):
        ir = parse("x = -1")
        val = ir[0]['value']
        assert val['type'] == 'unaryop'
        assert val['op'] == 'USub'

    def test_call(self):
        ir = parse("print('hello')")
        val = ir[0]['value']
        assert val['type'] == 'call'
        assert val['func'] == {'type': 'name', 'id': 'print'}

    def test_attribute(self):
        ir = parse("x = obj.attr")
        val = ir[0]['value']
        assert val['type'] == 'attribute'
        assert val['attr'] == 'attr'

    def test_list(self):
        ir = parse("x = [1, 2, 3]")
        val = ir[0]['value']
        assert val['type'] == 'list'
        assert len(val['elts']) == 3

    def test_dict(self):
        ir = parse('x = {"a": 1}')
        val = ir[0]['value']
        assert val['type'] == 'dict'

    def test_subscript(self):
        ir = parse("x = a[0]")
        val = ir[0]['value']
        assert val['type'] == 'subscript'

    def test_lambda(self):
        ir = parse("x = lambda a: a + 1")
        val = ir[0]['value']
        assert val['type'] == 'lambda'

    def test_syntax_error(self):
        with pytest.raises(ValueError, match="Syntax error"):
            parse("def (broken")
