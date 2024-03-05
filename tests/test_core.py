from collections import namedtuple

import pytest

from src.pytest_better_parametrize.core import better_parametrize, _prep_args


def _grant_access(
    email: str,
    logged_in: bool,
    is_superuser: bool,
    is_staff: bool,
):
    """
    This is just a dummy function for illustration purposes.
    """
    return (
        email.endswith("@mycompany.com")
        and logged_in
        and is_superuser
        and is_staff
    )


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
            True,
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
    """
    This is a demonstration of a parametrized test using pytest's own
    pytest.mark.parametrize.

    Can you easily tell what the third `True` represents in the last param?
    Did you need to scroll back up to the parameter list to check?
    """
    result = _grant_access(email, logged_in, is_superuser, is_staff)
    assert result == expected


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
            is_staff=True,
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
    """
    This is the same test rewritten with better_parametrize.

    Now you can easily tell what the third `True` in the last param
    represents. It's `is_staff` -- the keyword argument tells us so.

    Also, because we've used kwargs, we can position the `id` field at the
    top, so that each testcase starts with a description, rather than having
    the description at the bottom.
    """
    result = _grant_access(email, logged_in, is_superuser, is_staff)
    assert result == expected


@pytest.mark.parametrize("full_moon", [True, False])
@pytest.mark.parametrize("weekend", [True, False])
def test_stacking__vanilla(
    weekend: int,
    full_moon: bool,
):
    """
    Pytest's parametrize can be stacked to produce combinations of all the
    inputs. Pytest's output for this test looks like this:

    =========================== test session starts ============================
    collecting ... collected 4 items

    test_stacking__vanilla[True-True] PASSED [ 25%]
    test_stacking__vanilla[True-False] PASSED [ 50%]
    test_stacking__vanilla[False-True] PASSED [ 75%]
    test_stacking__vanilla[False-False] PASSED [100%]

    ============================ 4 passed in 0.03s =============================

    That "True-True" label is not very informative if we don't have the
    context. If this test fails, can we easily tell which combination of
    parameters is failing?
    """
    assert isinstance(weekend, int)
    assert isinstance(full_moon, bool)

    def _pad(message: str):
        return message.center(30, "=")

    assert _pad("hello") == "============hello============="


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
    weekend: bool,
    full_moon: bool,
):
    """
    This is the same test rewritten with better_parametrize.

    Note that we can bind our namedtuple to whatever name we like. This is
    particularly handy for single-value parameters, for which the full
    keyword argument syntax would be a little verbose. Instead of:

        @pytest.mark.better_parametrize(
            param := namedtuple("param", "weekend"),
            [
                param(weekend=True),
                param(weekend=False),
            ],
        )

    we can simply write:

        @pytest.mark.better_parametrize(
            weekend := namedtuple("param", "weekend"),
            [
                weekend(True),
                weekend(False),
            ],
        )

    Another thing to note is that if you do not define an `id` field,
    better_parametrize will generate an id for each parameter, showing the
    keyword values. Pytest's output for this test looks like this:

    =========================== test session starts ============================
    collecting ... collected 4 items

    test_stacking__better[weekend=True-full_moon=True]
    test_stacking__better[weekend=True-full_moon=False]
    test_stacking__better[weekend=False-full_moon=True]
    test_stacking__better[weekend=False-full_moon=False]

    ============================ 4 passed in 0.05s =============================

    Now the parameters are labelled by default, which makes it much easier to
    tell which combination of parameters causes a failure.
    """
    assert isinstance(weekend, int)
    assert isinstance(full_moon, bool)

    def _pad(message: str):
        return message.center(30, "=")

    assert _pad("hello") == "============hello============="


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
    """
    Sometimes we may want to describe a specific test case and the motivation
    behind it. In pytest, we can place a long comment or make a long `id`.

    The comment is not part of the testcase, so it is not always clear to
    which testcase it refers. Also, linters can sometimes move comments
    around in unintuitive ways, which may break the association between the
    comment and the testcase.

    The long id results in unhelpful testcase display, because pytest uses
    the whole thing:

    =========================== test session starts ============================
    collecting ... collected 2 items

    test_long_descriptions__vanilla[Short id for display purposes] PASSED [ 50%]
    test_long_descriptions__vanilla[Really long id describing this test case... lorem ipsum dolor sit amet, consectetur adipiscing elit...

    ============================ 2 passed in 0.03s =============================
    """
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)


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
    """
    better_parametrize's solution to this is the `ignore` argument, which you
    can use to ignore certain fields. These fields are not passed to the test
    function or to pytest. You are then free to use these fields to add
    descriptions or other annotations to your testcases.

    The output of this test looks like this:

    =========================== test session starts ============================
    collecting ... collected 2 items

    test_long_descriptions__better[Short id number 1] PASSED   [ 50%]
    test_long_descriptions__better[Short id number 2] PASSED   [100%]

    ============================ 2 passed in 0.03s =============================
    """
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)


@pytest.mark.better_parametrize(
    testcase := namedtuple("testcase", "foo, bar, baz, description"),
    [
        testcase(
            foo="foo",
            bar=69,
            baz=[1, 2, 3],
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
            description=(
                "Really long id describing this test case... lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit, sed do "
                "eiusmodtempor incididunt ut labore et dolore magna aliqua. "
            ),
        ),
    ],
    ignore=["description"],
)
def test_long_descriptions__no_id(
    foo: str,
    bar: int,
    baz: list,
):
    """
    This test is just to illustrate that if we don't pass `id`, the ignored
    fields are not included in the id generation either.

    The output of this test looks like this:

    =========================== test session starts ============================
    collecting ... collected 2 items

    test_long_descriptions__no_id[foo='foo',bar=69,baz=[1, 2, 3]] PASSED [ 50%]
    test_long_descriptions__no_id[foo='qux',bar=420,baz=[]] PASSED [100%]

    ============================ 2 passed in 0.03s =============================
    """
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)


@better_parametrize(
    testcase := namedtuple("testcase", "foo, bar, baz, description"),
    [
        testcase(
            foo="foo",
            bar=69,
            baz=[1, 2, 3],
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
            description=(
                "Really long id describing this test case... lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit, sed do "
                "eiusmodtempor incididunt ut labore et dolore magna aliqua. "
            ),
        ),
    ],
    ignore=["description"],
)
def test_use_decorator_directly(
    foo: str,
    bar: int,
    baz: list,
):
    """
    This test is just to illustrate that if we don't pass `id`, the ignored
    fields are not included in the id generation either.

    The output of this test looks like this:

    =========================== test session starts ============================
    collecting ... collected 2 items

    test_long_descriptions__no_id[foo='foo',bar=69,baz=[1, 2, 3]] PASSED [ 50%]
    test_long_descriptions__no_id[foo='qux',bar=420,baz=[]] PASSED [100%]

    ============================ 2 passed in 0.03s =============================
    """
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)


def test__prep_args_checks_for_namedtuple():
    with pytest.raises(ValueError) as e:
        _prep_args(
            tuple,  # has no `_fields` attr, so will fail
            [],
        )

    assert (
        str(e.value) == "`cls` must be a namedtuple with a `_fields` attribute"
    )
