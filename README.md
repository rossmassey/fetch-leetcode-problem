## Fetch Problem

Python package to get a dictionary with information about a leetcode problem, formatted in `rst`

# Installing
1. Install package with `pip install rossmassey.fetch-leetcode-problem`
2. Use `import fetch_leetcode_problem` or `from fetch_leetcode_problem import ...`

## Documentation

1. `cd docs && make html`

[![Deploy Documentation](https://github.com/rossmassey/fetch-leetcode-problem/actions/workflows/gh-pages.yml/badge.svg)](https://github.com/rossmassey/fetch-leetcode-problem/actions/workflows/gh-pages.yml)

Sphinx documentation is generated from the docstrings

https://rossmassey.github.io/fetch-leetcode-problem/

## Building & Publishing to PyPI

[![Upload Python Package](https://github.com/rossmassey/fetch-leetcode-problem/actions/workflows/python-publish.yml/badge.svg)](https://github.com/rossmassey/fetch-leetcode-problem/actions/workflows/python-publish.yml)

This is done automatically on release tag by GitHub actions

### Manually
Assume `.pypirc` configured in user home directory wih PyPI credentials
```
rm -rf dist
python3 -m build
python3 -m twine upload --repository pypi dist/*
```
