# Core Data Utility

[![test](https://github.com/korawica/ddeutil/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/korawica/ddeutil/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/ddeutils/ddeutil/graph/badge.svg?token=G3XGBSRKA6)](https://codecov.io/gh/ddeutils/ddeutil)
[![pypi version](https://img.shields.io/pypi/v/ddeutil)](https://pypi.org/project/ddeutil/)
[![python support version](https://img.shields.io/pypi/pyversions/ddeutil)](https://pypi.org/project/ddeutil/)
[![size](https://img.shields.io/github/languages/code-size/korawica/ddeutil)](https://github.com/korawica/ddeutil)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![type check: mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

The **Core Data utility** package implements the data utility functions and objects
that was created on sub-package namespace, `ddeutil`, design for independent
installation.

I make this package able to extend with any sub-extension with this namespace.
So, this namespace able to scale-out the requirement with folder level design.
You can add any custom features and import it by `import ddeutil.{extension}`.

> [!NOTE]
> This package provide the base utility functions and objects for any sub-namespace
> package.

## :round_pushpin: Installation

```shell
pip install -U ddeutil
```

**Python version supported**:

| Python Version | Installation                        | Support Fixed Bug  |
|----------------|-------------------------------------|--------------------|
| `>=3.9,<3.14`  | `pip install -U ddeutil`            | :heavy_check_mark: |

> [!NOTE]
> If you want to install all optional dependencies for this package, you can use
> `pip install -U ddeutil[all]`. I will install `ujson`, `python-dateutil`, and `psutil`
> packages for some functions in this project such as `hash.checksum`, 
> `dtutils.next_date_with_freq`, and `MonitorThread`.

## :dart: Features

This core data package will implement all of utility functions and objects that
does not re-create again because it is basic code but has a lot of using require.

| Module         | Name                | Type           | Description                                                                                                   | Remark |
|----------------|---------------------|----------------|---------------------------------------------------------------------------------------------------------------|--------|
| base           | `isinstance_check`  | function       |                                                                                                               |        |
|                | `import_string`     | function       |                                                                                                               |        |
|                | `lazy`              | function       |                                                                                                               |        |
|                | `round_up`          | function       |                                                                                                               |        |
|                | `remove_pad`        | function       |                                                                                                               |        |
|                | `first`             | function       |                                                                                                               |        |
|                | `onlyone`           | function       |                                                                                                               |        |
|                | `hasdot`            | function       |                                                                                                               |        |
|                | `getdot`            | function       |                                                                                                               |        |
|                | `setdot`            | function       |                                                                                                               |        |
|                | `filter_dict`       | function       |                                                                                                               |        |
|                | `random_str`        | function       |                                                                                                               |        |
|                | `coalesce`          | function       |                                                                                                               |        |
| base.cache     | `memorize`          | function       | Return a cachable function that keep all arguments and pass to string type for keeping it in the caching key. |        |
|                | `property_memorize` | function       |                                                                                                               |        |
|                | `clear_cache`       | function       |                                                                                                               |        |
| base.checker   | `can_int`           | function       |                                                                                                               |        |
|                | `is_int`            | function       |                                                                                                               |        |
| base.convert   | `must_bool`         | function       |                                                                                                               |        |
|                | `must_list`         | function       |                                                                                                               |        |
|                | `str2any`           | function       |                                                                                                               |        |
|                | `str2args`          | function       |                                                                                                               |        |
|                | `str2bool`          | function       |                                                                                                               |        |
|                | `str2dict`          | function       |                                                                                                               |        |
|                | `str2int_float`     | function       |                                                                                                               |        |
|                | `str2list`          | function       |                                                                                                               |        |
| base.hash      | `checksum`          | function       |                                                                                                               |        |
|                | `freeze`            | function       |                                                                                                               |        |
|                | `freeze_args`       | function       |                                                                                                               |        |
|                | `hash_all`          | function       |                                                                                                               |        |
|                | `hash_pwd`          | function       |                                                                                                               |        |
|                | `hash_str`          | function       |                                                                                                               |        |
|                | `same_pwd`          | function       |                                                                                                               |        |
|                | `tokenize`          | function       |                                                                                                               |        |
| base.merge     | `merge_dict`        | function       |                                                                                                               |        |
|                | `merge_dict_value`  | function       |                                                                                                               |        |
|                | `merge_dict_values` | function       |                                                                                                               |        |
|                | `merge_list`        | function       |                                                                                                               |        |
|                | `merge_values`      | function       |                                                                                                               |        |
|                | `zip_equal`         | function       |                                                                                                               |        |
| base.sorting   | `ordered`           | function       |                                                                                                               |        |
|                | `sort_priority`     | function       |                                                                                                               |        |
| base.splitter  | `isplit`            | function       |                                                                                                               |        |
|                | `must_rsplit`       | function       |                                                                                                               |        |
|                | `must_split`        | function       |                                                                                                               |        |
| decorator      | `deepcopy`          | decorator      |                                                                                                               |        |
|                | `deepcopy_args`     | decorator func |                                                                                                               |        |
|                | `timing`            | decorator func |                                                                                                               |        |
|                | `timing_open`       | decorator func |                                                                                                               |        |
|                | `debug`             | decorator func |                                                                                                               |        |
|                | `retry`             | decorator func |                                                                                                               |        |
|                | `profile`           | decorator func | Profile the current memory and cpu usage while wrapped function running.                                      |        |
| dtutils        | `replace_date`      | function       |                                                                                                               |        |
|                | `next_date`         | function       |                                                                                                               |        |
|                | `closest_quarter`   | function       |                                                                                                               |        |
|                | `last_dom`          | function       |                                                                                                               |        |
|                | `last_doq`          | function       |                                                                                                               |        |
|                | `next_date_freq`    | function       |                                                                                                               |        |
|                | `calc_data_freq`    | function       |                                                                                                               |        |
| threader       | `ThreadWithControl` | object         | Threading object that can control maximum background agent and result after complete.                         |        |
|                | `MonitorThread`     | object         | Monitoring threading object that log the current memory and cpu usage.                                        |        |

## :beers: Usages

I will show some usage example of function in this package. If you want to use
complex or adjust some parameter, please see doc-string or real source code
(I think it do not complex and you can see how that function work).

### OnlyOne

```python
from ddeutil.core import onlyone

assert 'a' == onlyone(['a', 'b'], ['a', 'b', 'c'])
assert 'c' == onlyone(('a', 'b'), ['c', 'e', 'f'])
assert onlyone(['a', 'b'], ['c', 'e', 'f'], default=False) is None
```

### Instance Check

```python
from ddeutil.core import isinstance_check
from typing import Union, Optional

assert isinstance_check("s", str)
assert isinstance_check(["s"], list[str])
assert isinstance_check(("s", "t"), tuple[str, ...])
assert not isinstance_check(("s", "t"), tuple[str])
assert isinstance_check({"s": 1, "d": "r"}, dict[str, Union[int, str]])
assert isinstance_check("s", Optional[str])
assert isinstance_check(1, Optional[Union[str, int]])
assert not isinstance_check("s", list[str])
```
