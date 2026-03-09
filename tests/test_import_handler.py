#!/usr/bin/env python3
"""Tests for import_handler module."""

import ast
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import pytest
from import_handler import translate_import, collect_imports_from_ast, get_required_go_imports


class TestTranslateImport:
    def test_os(self):
        assert translate_import("os") == "os"

    def test_json(self):
        assert translate_import("json") == "encoding/json"

    def test_math(self):
        assert translate_import("math") == "math"

    def test_time(self):
        assert translate_import("time") == "time"

    def test_unknown(self):
        assert translate_import("numpy") is None

    def test_os_path(self):
        assert translate_import("os.path") == "path/filepath"


class TestCollectImports:
    def test_simple_import(self):
        tree = ast.parse("import os")
        modules = collect_imports_from_ast(tree)
        assert "os" in modules

    def test_from_import(self):
        tree = ast.parse("from json import loads")
        modules = collect_imports_from_ast(tree)
        assert "json" in modules

    def test_multiple_imports(self):
        tree = ast.parse("import os\nimport math\nimport json")
        modules = collect_imports_from_ast(tree)
        assert modules == {"os", "math", "json"}

    def test_no_imports(self):
        tree = ast.parse("x = 42")
        modules = collect_imports_from_ast(tree)
        assert len(modules) == 0

    def test_dotted_import(self):
        tree = ast.parse("import os.path")
        modules = collect_imports_from_ast(tree)
        assert "os" in modules


class TestGetRequiredGoImports:
    def test_known_modules(self):
        imports = get_required_go_imports({"os", "json"})
        assert "os" in imports
        assert "encoding/json" in imports

    def test_unknown_filtered(self):
        imports = get_required_go_imports({"numpy", "os"})
        assert "os" in imports
        assert len(imports) == 1

    def test_empty(self):
        assert get_required_go_imports(set()) == []
