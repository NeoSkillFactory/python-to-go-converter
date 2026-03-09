# python-to-go-converter

![Audit](https://img.shields.io/badge/audit%3A%20PASS-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-orange)

> Automatically converts Python code to optimized Go code for performance-critical applications.

## Features

- Convert Python source files to Go with preserved functionality
- Intelligent Python-to-Go type mapping (int, str, list, dict, classes, etc.)
- Translate common Python standard library imports to Go equivalents
- Generate properly formatted Go code with comments
- Provide detailed error diagnostics for unsupported Python features
- CLI interface for batch conversion and agent integration
- Support for functions, classes, control flow, and basic data structures

## Examples

```bash
# Convert a single file
python-to-go-converter convert examples/basic.py --output output.go

# Convert with diagnostics
python-to-go-converter convert myscript.py --verbose
```

## Quick Start
## Installation

The skill is installed as part of an OpenClaw skill package. Ensure dependencies are met (Python 3.8+, `go` compiler in PATH).

## GitHub

Source code: [github.com/NeoSkillFactory/python-to-go-converter](https://github.com/NeoSkillFactory/python-to-go-converter)

**Price suggestion:** $29 USD

## License

MIT © NeoSkillFactory
