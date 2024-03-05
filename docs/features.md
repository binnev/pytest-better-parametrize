# Features

`pytest.mark.parametrize` is great. It's one of my favourite pytest features. It allows us to easily DRY up test code. However, it does have a few limitations. We'll walk through those limitations (and the solutions offered by `pytest-better-parametrize`) here.

## Keyword arguments

It is not possible to pass keyword arguments to `pytest.param`. This can make tests difficult to read if they have many params and many fields. Consider the following example:

```python
import pytest


@pytest.mark.parametrize(
    "email, logged_in, is_superuser, is_staff, expected",
    [
        pytest.param(
            "someone@mycompany.com",
            True,
            False,
            False,
            False,
            id="Logged in but not superuser or staff",
        ),
        pytest.param(
            "someone@mycompany.com",
            True,
            True,
            False,
            False,
            id="Logged and superuser, but not staff",
        ),
        pytest.param(
            "someone@mycompany.com",
            True,
            True,
            True,
            True,
            id="Logged and superuser and staff",
        ),
        pytest.param(
            "someone@example.com",
            True,
            True,
            True,  # <-----------------------------------
            False,
            id="Wrong email type",
        ),
    ],
)
def test_parametrize__vanilla(
    email: str,
    logged_in: bool,
    is_superuser: bool,
    is_staff: bool,
    expected: bool,
):
    ...  # test body goes here

```

That `True` value the arrow is pointing at -- can you tell at a glance which field it is? Did you need to scroll back up to the fields definition at the top?

Let's rewrite the same test using `pytest-better-parametrize`:

```python
import pytest
from collections import namedtuple


@pytest.mark.better_parametrize(
    param := namedtuple(
        "param",
        "email, logged_in, is_superuser, is_staff, expected, id",
    ),
    [
        param(
            id="Logged in but not superuser or staff",
            email="someone@mycompany.com",
            logged_in=True,
            is_superuser=False,
            is_staff=False,
            expected=False,
        ),
        param(
            id="Logged and superuser, but not staff",
            email="someone@mycompany.com",
            logged_in=True,
            is_superuser=True,
            is_staff=False,
            expected=False,
        ),
        param(
            id="Logged and superuser and staff",
            email="someone@mycompany.com",
            logged_in=True,
            is_superuser=True,
            is_staff=True,
            expected=True,
        ),
        param(
            id="Wrong email type",
            email="someone@example.com",
            logged_in=True,
            is_superuser=True,
            is_staff=True,  # <-----------------------------------
            expected=False,
        ),
    ],
)
def test_parametrize__better(
    email: str,
    logged_in: bool,
    is_superuser: bool,
    is_staff: bool,
    expected: bool,
):
    ...  
```

Now it's immediately clear that the arrow is pointing at `is_staff`. Having access to keyword arguments makes tests easier to read, and easier to write (because it's harder to make a mistake).

## Better output formatting

Pytest's default ids for multiple parameters can become a little hard to read. Consider the following test with 2 parameters:

```python
@pytest.mark.parametrize("full_moon", [True, False])
@pytest.mark.parametrize("weekend", [True, False])
def test_stacking__vanilla(
    weekend: int,
    full_moon: bool,
):
    ...
```

It produces the following output:

```
============================= test session starts ==============================
collecting ... collected 4 items

test_stacking__vanilla[True-True] 
test_stacking__vanilla[True-False] 
test_stacking__vanilla[False-True] 
test_stacking__vanilla[False-False] 

============================== 4 passed in 0.03s ===============================

```

The bare `True-False` display is not very helpful, especially as the number of parameters increases.

`pytest-better-parametrize` includes the parameter name in auto-generated ids, so the test output is more informative.

```python
@pytest.mark.better_parametrize(
    full_moon := namedtuple("param", "full_moon"),
    [
        full_moon(True),
        full_moon(False),
    ],
)
@pytest.mark.better_parametrize(
    weekend := namedtuple("param", "weekend"),
    [
        weekend(True),
        weekend(False),
    ],
)
def test_stacking__better(
    weekend: int,
    full_moon: bool,
):
    ...
```

This test generates the following output, where it is clear at a glance which parameter has which value.

```
============================= test session starts ==============================
collecting ... collected 4 items

test_stacking__better[weekend=True-full_moon=True] PASSED  [ 25%]
test_stacking__better[weekend=True-full_moon=False] PASSED [ 50%]
test_stacking__better[weekend=False-full_moon=True] PASSED [ 75%]
test_stacking__better[weekend=False-full_moon=False] PASSED [100%]

============================== 4 passed in 0.05s ===============================

```

## Annotation fields

Sometimes we may want to describe a specific test case and the motivation behind it. In pytest, we can place a long comment or make a long `id`:

```python
@pytest.mark.parametrize(
    "foo, bar, baz",
    [
        # Really long comment describing this test case... lorem ipsum dolor
        # sit amet, consectetur adipiscing elit, sed do eiusmodtempor
        # incididunt ut labore et dolore magna aliqua.
        pytest.param(
            "foo",
            69,
            [1, 2, 3],
            id="Short id for display purposes",
        ),
        pytest.param(
            "qux",
            420,
            [],
            id=(
                "Really long id describing this test case... lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit, sed do "
                "eiusmodtempor incididunt ut labore et dolore magna aliqua. "
            ),
        ),
    ],
)
def test_long_descriptions__vanilla(
    foo: str,
    bar: int,
    baz: list,
):
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)

```

The comment is not part of the testcase, so it is not always clear to which testcase it refers. Also, linters can sometimes move comments around in unintuitive ways, which may break the association between the comment and the testcase.

The long id results in unhelpful testcase display, because pytest uses the whole thing:

```
=========================== test session starts ============================
collecting ... collected 2 items

test_long_descriptions__vanilla[Short id for display purposes] PASSED [ 50%]
test_long_descriptions__vanilla[Really long id describing this test case... lorem ipsum dolor sit amet, consectetur adipiscing elit...

============================ 2 passed in 0.03s =============================
```

`pytest-better-parametrize` allows you to pass a list of fields to ignore -- these can then be used for additional annotations that you don't want to include in the test or the output:

```python
@pytest.mark.better_parametrize(
    testcase := namedtuple("testcase", "foo, bar, baz, id, description"),
    [
        testcase(
            foo="foo",
            bar=69,
            baz=[1, 2, 3],
            id="Short id number 1",
            description=(
                "Really long description of this test case... lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit, sed do "
                "eiusmodtempor incididunt ut labore et dolore magna aliqua. "
            ),
        ),
        testcase(
            foo="qux",
            bar=420,
            baz=[],
            id="Short id number 2",
            description=(
                "Really long id describing this test case... lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit, sed do "
                "eiusmodtempor incididunt ut labore et dolore magna aliqua. "
            ),
        ),
    ],
    ignore=["description"],
)
def test_long_descriptions__better(
    foo: str,
    bar: int,
    baz: list,
):
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)
```

The output of this test looks like this:

```
=========================== test session starts ============================
collecting ... collected 2 items

test_long_descriptions__better[Short id number 1] PASSED   [ 50%]
test_long_descriptions__better[Short id number 2] PASSED   [100%]

============================ 2 passed in 0.03s =============================
```