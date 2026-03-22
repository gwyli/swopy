# swopy

A library for bidirectional conversion between numeral systems. Supports 46 different systems across all numeral systems available in Unicode.

## Installation

```bash
pip install swopy
# or
uv add swopy
```

swopy has no external dependencies and requires Python 3.13 or higher.

## Quick Start

```python
import swopy
from swopy import systems

# Roman to Egyptian
swopy.swop('IX', systems.roman.Standard, systems.egyptian.Egyptian)
# '𓏺𓏺𓏺𓏺𓏺𓏺𓏺𓏺𓏺'

# Apostrophus to Arabic integer
swopy.swop('IↃI', systems.roman.Apostrophus, systems.arabic.Arabic)
# 501

# Arabic to Kaktovik (base-20)
swopy.swop(42, systems.arabic.Arabic, systems.kaktovik.Kaktovik)
# '𝋂𝋂'
```

## Using `get_all_systems`

```python
import swopy

all_systems = swopy.get_all_systems()
swopy.swop(42, all_systems['arabic.Arabic'], all_systems['roman.Early'])
# 'XLII'
```

## Encoding

Most systems return UTF-8 Unicode by default. Use `encode="ascii"` where supported:

```python
swopy.swop(10, systems.arabic.Arabic, systems.roman.Standard, encode="ascii")
# 'X'  (instead of UTF-8 'Ⅹ')
```

## Error Handling

```python
# Out of range
swopy.swop(4000, systems.arabic.Arabic, systems.roman.Standard)
# ValueError: Number must be less than or equal to 3999.

# Invalid numeral
swopy.swop('IIIII', systems.egyptian.Egyptian, systems.roman.Early)
# ValueError: Invalid Egyptian hieroglyph: I

# Wrong type
swopy.swop(1.2, systems.arabic.Arabic, systems.roman.Early)
# TypeError: 1.2 of type float cannot be represented in Early.
```
