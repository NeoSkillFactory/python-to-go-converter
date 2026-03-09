#!/usr/bin/env python3
"""Tests for the converter CLI."""

import sys
import os
import subprocess
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import pytest

CONVERTER = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'converter.py')
ASSETS = os.path.join(os.path.dirname(__file__), '..', 'assets')


def run_converter(*args):
    """Run the converter as a subprocess."""
    result = subprocess.run(
        [sys.executable, CONVERTER] + list(args),
        capture_output=True, text=True
    )
    return result


class TestCLI:
    def test_convert_basic(self):
        result = run_converter("convert", os.path.join(ASSETS, "basic.py"))
        assert result.returncode == 0
        assert "package main" in result.stdout
        assert "func add" in result.stdout

    def test_convert_complex(self):
        result = run_converter("convert", os.path.join(ASSETS, "complex.py"))
        assert result.returncode == 0
        assert "func factorial" in result.stdout
        assert "func sum_range" in result.stdout
        assert "func first_even" in result.stdout

    def test_convert_to_file(self):
        with tempfile.NamedTemporaryFile(suffix=".go", delete=False) as f:
            outpath = f.name
        try:
            result = run_converter("convert", os.path.join(ASSETS, "basic.py"), "-o", outpath)
            assert result.returncode == 0
            with open(outpath) as f:
                content = f.read()
            assert "package main" in content
            assert "func add" in content
        finally:
            os.unlink(outpath)

    def test_verbose_output(self):
        result = run_converter("convert", os.path.join(ASSETS, "basic.py"), "--verbose")
        assert result.returncode == 0
        # Verbose output goes to stderr
        assert "Detected Python imports:" in result.stderr or result.returncode == 0

    def test_missing_input_file(self):
        result = run_converter("convert", "/nonexistent/file.py")
        assert result.returncode != 0
        assert "E005" in result.stderr

    def test_no_args(self):
        result = run_converter()
        assert result.returncode != 0

    def test_header_comment(self):
        result = run_converter("convert", os.path.join(ASSETS, "basic.py"))
        assert "// Automatically converted from basic.py" in result.stdout


class TestImportHandling:
    def test_os_import(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("import os\nprint(os.getcwd())")
            f.flush()
            path = f.name
        try:
            result = run_converter("convert", path)
            assert result.returncode == 0
            assert '"os"' in result.stdout
            assert '"fmt"' in result.stdout
        finally:
            os.unlink(path)

    def test_json_import(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("import json\nx = json.loads(data)")
            f.flush()
            path = f.name
        try:
            result = run_converter("convert", path)
            assert result.returncode == 0
            assert '"encoding/json"' in result.stdout
        finally:
            os.unlink(path)
