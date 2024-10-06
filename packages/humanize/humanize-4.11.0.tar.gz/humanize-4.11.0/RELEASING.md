# Release Checklist

- [ ] Get `main` to the appropriate code release state.
      [GitHub Actions](https://github.com/python-humanize/humanize/actions) should be
      running cleanly for all merges to `main`.
      [![GitHub Actions status](https://github.com/python-humanize/humanize/workflows/Test/badge.svg)](https://github.com/python-humanize/humanize/actions)

* [ ] Start from a freshly cloned repo:

```bash
cd /tmp
rm -rf humanize
git clone https://github.com/python-humanize/humanize
cd humanize
# Generate translation binaries
scripts/generate-translation-binaries.sh
```

- [ ] (Optional) Create a distribution and release on **TestPyPI**:

```bash
pip install -U pip build keyring twine
rm -rf build dist
python -m build
twine check --strict dist/* && twine upload --repository testpypi dist/*
```

- [ ] (Optional) Check **test** installation:

```bash
pip3 uninstall -y humanize
pip3 install -U -i https://test.pypi.org/simple/ humanize --pre
python3 -c "import humanize; print(humanize.__version__)"
```

- [ ] Tag with the version number:

```bash
git tag -a 2.1.0 -m "Release 2.1.0"
```

- [ ] Create a distribution and release on **live PyPI**:

```bash
pip install -U pip build keyring twine
rm -rf build dist
python -m build
twine check --strict dist/* && twine upload --repository pypi dist/*
```

- [ ] Check installation:

```bash
pip uninstall -y humanize
pip install -U humanize
python3 -c "import humanize; print(humanize.__version__)"
```

- [ ] Push tag:

```bash
git push --tags
```

- [ ] Edit release draft, adjust text if needed:
      https://github.com/python-humanize/humanize/releases

- [ ] Check next tag is correct, amend if needed

- [ ] Publish release
