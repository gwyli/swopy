# Swopy

A library for biredirectional conversion between numeral systems (e.g. Egyptian, Roman, Arabic etc.).

## Overview

Swopy provides a simple and extensible interface to convert numbers between various numeral systems.
Swopy supports bidirectional conversion — you can convert from any supported system to any other.

## Supported Numeral Systems

* [Arabic](https://github.com/gwyli/swopy/blob/main/swopy/systems/arabic.py), supporting integers, floats and fractions between `-math.inf` and `math.inf`
* [Egyptian](https://github.com/gwyli/swopy/blob/main/swopy/systems/egyptian.py), supporting integers between 1 and 1,000,000/many
* [Etruscan](https://github.com/gwyli/swopy/blob/main/swopy/systems/etruscan.py), supporting integers between 1 and 300
* [Roman](https://github.com/gwyli/swopy/blob/main/swopy/systems/roman.py), in the forms:
   * Early, supporting integers between 1 and 899
   * Standard, supporting integers and base-12 fractions between 1/12 and 3,999
   * Apostrophus, supporting integers between 1 and 100,000

## Installation

Install the package:

```bash
pip install swopy # or
uv add swopy
```

## Usage

### Basic Conversion

```python
import swopy
from swopy import systems

# Convert integer Roman numeral to Egyptian hieroglyphic
swopy.swop('IX', systems.roman.Standard, systems.egyptian.Egyptian)
# '𓏺𓏺𓏺𓏺𓏺𓏺𓏺𓏺𓏺'

# Convert Apostrophus to an Arabic integer
swopy.swop('IↃI', systems.roman.Apostrophus, systems.arabic.Arabic)
# 501
```

### Available Systems

```python
import swopy
import pprint
systems = swopy.get_all_systems()
pprint.pprint(systems)

# {'arabic.Arabic': <class 'swopy.systems.arabic.Arabic'>,
# 'egyptian.Egyptian': <class 'swopy.systems.egyptian.Egyptian'>,
# 'etruscan.Etruscan': <class 'swopy.systems.etruscan.Etruscan'>,
#  'roman.Apostrophus': <class 'swopy.systems.roman.Apostrophus'>,
#  'roman.Early': <class 'swopy.systems.roman.Early'>,
#  'roman.Standard': <class 'swopy.systems.roman.Standard'>}

swopy.swop(42, systems['arabic.Arabic'], systems['roman.Early'])
# 'XLII'

```

### Error Handling

Swopy will raise a `ValueError` if there is a number is not representable in a numeral system

```python
import swopy
from swopy import systems

swopy.swop(4000, systems.arabic.Arabic, systems.roman.Standard)
# ValueError: Number must be less than or equal to 3999.

systems.roman.Early.to_numeral(900)
# ValueError: Number must be less than or equal to 899.
```

or if a numeral is invalid

```python
import swopy
from swopy import systems

swopy.swop('IIIII', systems.egyptian.Egyptian, systems.roman.Early)
# ValueError: Invalid Egyptian hieroglyph: I

systems.roman.Apostrophus.from_numeral('P')
# ValueError: Invalid Apostrophus characters at position 0
```

and will raise a `TypeError` if a numeral is not representable in a system.

```python
import swopy
from swopy import systems

swopy.swop(1.2, systems.arabic.Arabic, systems.roman.Early)
# TypeError: 1.2 of type float cannot be represented in Early.

swopy.swop('I', systems.arabic.Arabic, systems.roman.Early)
# TypeError: I of type str cannot be represented in Arabic.

systems.egyptian.Egyptian.to_numeral(10.1)
# TypeError: 10.1 of type float cannot be represented in Egyptian.
```

## Requirements

Swopy only relies on the standard library and needs Python 3.13 or higher. Swopy is currently tested on the latest versions of Windows, MacOS and Ubuntu for Python versions 3.13, 3.14.0, 3.14.3, and 3.15.

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