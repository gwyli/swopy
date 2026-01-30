# Numberology

A Python library for converting between different numeral systems.

## Overview

Numberology provides a simple and extensible interface to convert numbers between various numeral systems, including Roman numerals and Egyptian hieroglyphic numerals. The library supports bidirectional conversion—you can convert from any supported system to any other.

## Supported Numeral Systems

* [Roman](numberology/systems/roman.py), in the forms
 * Early, supporting integers between 1 and 899
 * Standard, supporting integers between 1 and 3,999
 * Apostrophus, supporting integers between 1 and 100,000
* [Egyptian](umberology/systems/egyptian.py), supporting integers between 1 and 1,000,000/many
* Arabic, supporting integers between `-int(sys.float_info.max)` and `int(sys.float_info.max)`

## Installation

Install the package:

```bash
pip install numberology # or
uv add numberology
```

## Usage

### Basic Conversion

```python
from numberology import Numberology, systems

converter = Numberology()

# Convert integer Roman numeral to Egyptian hieroglyphic
converter.convert('IX', systems.roman.Standard, systems.egyptian.Egyptian)
# '𓏺𓏺𓏺𓏺𓏺𓏺𓏺𓏺𓏺'

# Convert Apostrophus to an Arabic integer
converter.convert('IↃI', systems.roman.Apostrophus, systems.arabic.Arabic)
# 501
```

### Available Systems

```python
from numberology import Numberology, get_all_systems
import pprint
systems = get_all_systems()
pprint.pprint(systems)
#{'arabic.Arabic': <class 'numberology.systems.arabic.Arabic'>,
# 'egyptian.Egyptian': <class 'numberology.systems.egyptian.Egyptian'>,
# 'roman.Apostrophus': <class 'numberology.systems.roman.Apostrophus'>,
# 'roman.Early': <class 'numberology.systems.roman.Early'>,
# 'roman.Standard': <class 'numberology.systems.roman.Standard'>}

converter = Numberology()
converter.convert(42, systems['arabic.Arabic'], systems['roman.Early'])
# 'XLII'

```

### Error Handling

The library validates numbers against the acceptable range for each system:

```python
from numberology import Numberology, systems

converter = Numberology()

# This will raise ValueError (4000 is outside the valid range)
try:
    result = converter.convert(4000, systems.arabic.Arabic, systems.roman.Standard)
except ValueError as e:
    print(f"Conversion failed: {e}")
# Conversion failed: Number must be less than or equal to 3999.
```

## Requirements

- Python 3.12 or higher

## Development

### Dependencies

Development dependencies are managed through `pyproject.toml`:

```bash
# Install development dependencies
sh scripts/startup.sh
```

Dev tools include:
- pytest / pytest-cov: Testing framework
- ruff: Fast Python linter and formatter
- pyright: Static type checker
- deptry: Dependency validation
- hypothesis: Property-based testing
- pre-commit: Git hooks framework
- tox, with tox-uv: Test runner
- uv