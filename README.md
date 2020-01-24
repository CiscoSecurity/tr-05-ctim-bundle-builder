[![Travis CI Build Status](https://travis-ci.com/CiscoSecurity/tr-05-ctim-bundle-builder.svg)](https://travis-ci.com/CiscoSecurity/tr-05-ctim-bundle-builder)
[![PyPi Version](https://img.shields.io/pypi/v/bundlebuilder.svg)](https://pypi.python.org/pypi/bundlebuilder)
[![Python Versions](https://img.shields.io/pypi/pyversions/bundlebuilder.svg)](https://pypi.python.org/pypi/bundlebuilder)

# Bundle Builder

Bundle Builder (or BB for short) is a tool for manipulating CTIM entities and
packaging them into so-called bundles.

Features (more details later):
- Support for sessions per each particular use of BB.
- Validation of fields for CTIM entities according to the
[latest schemas](https://github.com/threatgrid/ctim/tree/master/doc/structures).
- Generation of transient IDs and external IDs (XIDs) according to the
[best practices](https://github.com/threatgrid/ctim/blob/master/doc/tutorials/modeling-threat-intel-ctim.md#1113-best-practices-for-external-ids).

## Installation

* Local

```bash
pip install -U .
pip show bundlebuilder
```

* GitHub

```bash
pip install -U git+https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder.git[@branch_name_or_release_version]
pip show bundlebuilder
```

* PyPi

```bash
pip install -U bundlebuilder[==release_version]
pip show bundlebuilder
```

## Usage

TBD...
