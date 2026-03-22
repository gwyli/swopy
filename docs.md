# Documentation

## Building locally

Install the docs dependencies and serve:

```bash
uv sync --group docs
uv run zensical serve --open
```

`--open` opens the site in your default browser automatically. While the server is running, the site reloads on any change.

To build static HTML without serving:

```bash
uv run zensical build --clean
```

Output goes to `site/` (gitignored).

## Structure

```
docs/
  index.md         # Home page: installation, quick start, error handling
  systems.md       # Reference table of all 46 supported numeral systems
  api.md           # API reference (auto-generated from docstrings)
zensical.toml      # Zensical configuration
.readthedocs.yml   # ReadTheDocs build configuration
```

## How it works

Docs are built with [Zensical](https://zensical.org/), a static site generator by the creators of Material for MkDocs.

API reference pages use [mkdocstrings](https://mkdocstrings.github.io/) to generate documentation directly from the source docstrings in `swopy/swopy.py` and `swopy/system.py`. Private members (prefixed with `_`) are excluded automatically.

## ReadTheDocs

The `.readthedocs.yml` at the project root configures the ReadTheDocs build. On every push, RTD runs:

```bash
pip install uv
uv sync --group docs
uv run zensical build --clean
cp -r site/. $READTHEDOCS_OUTPUT/html
```

No manual publishing step is needed. Import the repository at [readthedocs.io](https://readthedocs.io) and it will pick up `.readthedocs.yml` automatically.
