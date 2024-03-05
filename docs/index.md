# pytest-better-parametrize

Better description of parametrized test cases.

## Installation

`pytest-better-parametrize` is available on pip:

```shell
pip install pytest-better-parametrize
```

## Example

For those eager to get started, here is a minimal example test. For a full guide, please see the [Features](features.md) page.

```python
import pytest
from collections import namedtuple


@pytest.mark.better_parametrize(
    param := namedtuple("param", "foo, bar"),  
    [ 
        param(foo=True, bar=True),
        param(foo=True, bar=False),
        param(foo=False, bar=True),
        param(foo=False, bar=False),
    ],
)
def test_something(foo: bool, bar: bool) -> None:
    assert isinstance(foo, bool)
    assert isinstance(bar, bool)
```

This test produces the following output:

```
============================= test session starts ==============================
collecting ... collected 4 items

test_something[foo=False,bar=False] PASSED                 [ 25%]
test_something[foo=False,bar=True] PASSED                  [ 50%]
test_something[foo=True,bar=False] PASSED                  [ 75%]
test_something[foo=True,bar=True] PASSED                   [100%]

============================== 4 passed in 0.02s ===============================
```
