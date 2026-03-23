# Plans

Future plans for swopy

## Systems

Currently swopy supports numeral systems that are not equivalent to Hindu-Arabic numerals in any script. It is assumed that a future feature to allow translations via the locale is the best implementation to include them.

### Add

The following systems need to be added

- Old Persian: https://www.unicode.org/charts/PDF/U103A0.pdf
- Chorasmian: https://www.unicode.org/charts/PDF/U10FB0.pdf
- Rumi: https://www.unicode.org/charts/PDF/U10E60.pdf
- Merotic Cursive: https://www.unicode.org/charts/PDF/U109A0.pdf
- Old Hungrian: https://www.unicode.org/charts/PDF/U10C80.pdf
- Vinculum form of Roman numerals: There is no specific Viniculum Unicode block, however, they're possible to construct with the combining characters U+0305 (◌̅) and U+033F (◌̿)

### Investigate

The following systems should be investigated to see whether they fit the criteria for inclusion

- Myanmar Extended C: https://www.unicode.org/charts/PDF/U116D0.pdf
- Nushu: https://en.wikipedia.org/wiki/N%C3%BCshu
- Kaithi: https://www.unicode.org/charts/PDF/U11080.pdf
- Sharada: https://www.unicode.org/charts/PDF/U11180.pdf
- Tulu-Tigalari: https://en.wikipedia.org/wiki/Tulu-Tigalari_(Unicode_block) (Sanskrit must have had numbers)
- Pahawh Hmong: https://www.unicode.org/charts/PDF/U16B00.pdf
- Mende Kikakui: https://www.unicode.org/charts/PDF/U1E800.pdf

### Hindu-Arabic representations

The following Unicode blocks are assumed to be a direct translation of Hindhu-Arabic numerals into the script. These are all from the Unicode [Supplementary Multilingual Plane](https://en.wikipedia.org/wiki/Plane_(Unicode)#Supplementary_Multilingual_Plane). It is assumed that all scripts in the [Basic Multilingual Plane](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane) are direct translations of Hindu-Arabic numerals - this assumption needs to be verified.

- Osmanya: https://www.unicode.org/charts/PDF/U10480.pdf
- Hanifi Rohingya: https://www.unicode.org/charts/PDF/U10D00.pdf
- Garay: https://www.unicode.org/charts/PDF/U10D40.pdf
- Sora Sompeng: https://www.unicode.org/charts/PDF/U110D0.pdf
- Chakma: https://www.unicode.org/charts/PDF/U110D0.pdf
- Khudawadi: https://www.unicode.org/charts/PDF/U112B0.pdf
- Newa: https://www.unicode.org/charts/PDF/U11400.pdf
- Modi: https://www.unicode.org/charts/PDF/U11600.pdf
- Takri: https://www.unicode.org/charts/PDF/U11680.pdf
- Warang Citi: https://www.unicode.org/charts/PDF/U118A0.pdf
- Sunuwar: https://www.unicode.org/charts/PDF/U11BC0.pdf
- Masaram Gondi: https://www.unicode.org/charts/PDF/U11D00.pdf
- Gunjala Gondi: https://www.unicode.org/charts/PDF/U11D60.pdf
- Tolong siki: https://www.unicode.org/charts/PDF/U11DB0.pdf
- Kawi: https://www.unicode.org/charts/PDF/U11F00.pdf
- Gurung Khema: https://www.unicode.org/charts/PDF/U11F00.pdf
- Mro: https://www.unicode.org/charts/PDF/U16A40.pdf
- Tangsa: https://www.unicode.org/charts/PDF/U16A70.pdf
- Kirit rai: https://www.unicode.org/charts/PDF/U16D40.pdf
- Nyiakeng puachue Hmong: https://www.unicode.org/charts/PDF/U16D40.pdf
- Wancho: https://www.unicode.org/charts/PDF/U1E2C0.pdf
- Nag Mundari: https://www.unicode.org/charts/PDF/U1E2C0.pdf
- Adlam: https://www.unicode.org/charts/PDF/U1E900.pdf

The following systems are assumed to be based on Hindu-Arabic numerals but are no longer in use and thus might not be translatable by any future locale-based feature.

- Tirhuta: https://www.unicode.org/charts/PDF/U11480.pdf
- Dives Akuru: https://www.unicode.org/charts/PDF/U11900.pdf
- Ol Onal: https://www.unicode.org/charts/PDF/U1E2C0.pdf

### Conlangs

The [ConScript Unicode Registry](https://www.evertype.com/standards/csur/) and the [Under-ConScript Unicode Registry](https://www.kreativekorp.com/ucsur/) coordinate the use of the Unicode Private Use Area to to include conlangs in Unicode, assuming the user has installed a compatible font. Most numbers in conlangs are direct translations of Hindu-Arabic numerals and thus would normally be excluded, however, they are highly unlikely to ever be availble in any future local-based feature for translation and so are eligible.

The Under-ConScript Unicode Registry is a the superset register. Conlangs will be placed in `swopy/systems/conlangs/` in a file <conlang-name>.py with the class name `Conlang`. `conlangs/__init__.py` will import the class and make the class public in `__all__` meaning that conlangs are separated, but can be accessed in swopy via `systems.conlangs.ConlangClass`.

Process: iterate through the (U)CSUR Allocations table on https://www.kreativekorp.com/ucsur/. Read the PDF. If it does not contain numerals ignore it. If it does contain numerals follow the instructions for adding a conlang. I've added __init__.py.


## Testing

- Create a "round-the-world" test that loops through ever number that's valid in every system (currently integers 1-99) and tests that the original number gets returned once it's been translated through every system in sequence.