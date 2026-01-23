# Numberology

A Python library for converting numbers between different numeral systems.

## Overview

Numberology provides a simple and extensible interface to convert numbers between various historical numeral systems, including Roman numerals and Egyptian hieroglyphic numerals. The library supports bidirectional conversion—you can convert from any supported system to any other.

## Features

- **Multiple numeral systems**: Roman, Egyptian, and Latin
- **Bidirectional conversion**: Convert from any system to any other
- **Type flexibility**: Accepts both string and integer representations
- **Validation**: Built-in range validation for each system
- **Fully typed**: Complete type hints for better IDE support
- **Tested**: Comprehensive test coverage with pytest

## Supported Numeral Systems

### Roman Numerals
- **Range**: 1 - 3,999
- **Symbols**: I, V, X, L, C, D, M
- **Features**: Supports subtractive notation (e.g., IV = 4, IX = 9, XL = 40)
- **Examples**: 
  - `I` = 1
  - `IV` = 4
  - `XLII` = 42
  - `MCMXCIV` = 1994

### Egyptian Hieroglyphic Numerals
- **Range**: 1 - 9,999,999
- **Base**: Base-10 system with individual hieroglyph symbols
- **Symbols**: Unique Unicode characters for 1, 10, 100, 1,000, 10,000, 100,000, and 1,000,000

### Latin Numerals
- Placeholder implementation for Latin numeral system support

## Installation

Install the package using pip:

```bash
pip install numberology
```

## Usage

### Basic Conversion

```python
from numberology import Numberology, System

converter = Numberology()

# Convert integer Roman numeral to Egyptian hieroglyphic
result = converter.convert(42, System.ROMAN, System.EGYPTIAN)

# Convert Roman numeral string to integer
result = converter.convert("XLII", System.ROMAN, System.EGYPTIAN)
```

### Available Systems

```python
from numberology import System

# Supported numeral systems
System.ROMAN      # Roman numerals (I, V, X, L, C, D, M)
System.EGYPTIAN   # Egyptian hieroglyphic numerals
System.LATIN      # Latin numerals
```

### Error Handling

The library validates numbers against the acceptable range for each system:

```python
from numberology import Numberology, System

converter = Numberology()

# This will raise ValueError (4000 is outside the valid range)
try:
    result = converter.convert(4000, System.ROMAN, System.EGYPTIAN)
except ValueError as e:
    print(f"Conversion failed: {e}")
```

## Requirements

- Python 3.14 or higher
- pydantic (optional, for advanced features)

## Development

### Dependencies

Development dependencies are managed through `pyproject.toml`:

```bash
# Install development dependencies
pip install -e ".[dev]"
```

Dev tools include:
- pytest / pytest-cov: Testing framework
- ruff: Fast Python linter and formatter
- pyright: Static type checker
- deptry: Dependency validation
- hypothesis: Property-based testing
- pre-commit: Git hooks framework