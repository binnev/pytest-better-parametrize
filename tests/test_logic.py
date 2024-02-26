from collections import namedtuple

import pytest


@pytest.mark.parametrize(
    [
        "foo",
        "really_really_long_name",
    ],
    [
        pytest.param(
            "hi",
            69,
            id="first one",
        ),
        pytest.param(
            "it's alive!",
            9000,
            id="second one",
        ),
        pytest.param(
            "we get tab completion!!!!!",
            8999,
            id="will fail",
        ),
    ],
)
def test_vanilla_parametrize(foo: str, really_really_long_name: int):
    assert isinstance(foo, str)
    assert isinstance(really_really_long_name, int)
    assert really_really_long_name < 9001


@pytest.mark.better_parametrize(
    testcase := namedtuple(
        "testcase",
        field_names=[
            "foo",
            "really_really_long_name",
            "id",
            "description",
        ],
    ),
    ignore=["description"],
    testcases=[
        testcase(
            foo="hi",
            really_really_long_name=69,
            id="first one",
            description=(
                "Here we can put a more verbose description of the testcase; "
                "something that would be too long for the `id` field. "
                "Something more like a comment. Except unlike a comment, "
                "it is bound to the testcase by being an argument."
            ),
        ),
        testcase(
            foo="it's alive!",
            really_really_long_name=9000,
            id="second one",
            description="aaiosdjfoiafjaiodfjads ofiaj dsofiajdsfoaidjsf oas",
        ),
        testcase(
            really_really_long_name=8999,
            foo="we get tab completion!!!!!",
            id="will fail",
            description="",
        ),
    ],
)
def test_better_parametrize(foo: str, really_really_long_name: int):
    assert isinstance(foo, str)
    assert isinstance(really_really_long_name, int)
    assert really_really_long_name < 9001


@pytest.mark.better_parametrize(
    testcase := namedtuple("testcase", "foo, bar, baz, id"),
    [
        testcase(foo="foo", bar=69, baz=[1, 2, 3], id="print me"),
        testcase(foo="qux", bar=420, baz=[], id="hello"),
    ],
)
def test_basic_usage(
    foo: str,
    bar: int,
    baz: list,
):
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)


@pytest.mark.better_parametrize(
    testcase := namedtuple("testcase", "foo, bar, baz, id"),
    [
        testcase("foo", bar=69, baz=[1, 2, 3], id="print me"),
        testcase("qux", bar=420, baz=[], id="hello"),
    ],
)
def test_positional_args(
    foo: str,
    bar: int,
    baz: list,
):
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
            id="print me",
            description="some really long stuff here, really verbose",
        ),
        testcase(
            foo="qux",
            bar=420,
            baz=[],
            id="hello",
            description=(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                "sed do eiusmodtempor incididunt ut labore et dolore magna "
                "aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                "ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                "Duis aute irure dolor in reprehenderit in voluptate velit "
                "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
                "occaecat cupidatat non proident, sunt in culpa qui officia "
                "deserunt mollit anim id est laborum"
            ),
        ),
    ],
    ignore=["description"],
)
def test_ignore_fields(
    foo: str,
    bar: int,
    baz: list,
):
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
            description="some really long stuff here, really verbose",
        ),
        testcase(
            foo="qux",
            bar=420,
            baz=[],
            description=(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                "sed do eiusmodtempor incididunt ut labore et dolore magna "
                "aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                "ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                "Duis aute irure dolor in reprehenderit in voluptate velit "
                "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
                "occaecat cupidatat non proident, sunt in culpa qui officia "
                "deserunt mollit anim id est laborum"
            ),
        ),
    ],
    ignore=["description"],
)
def test_just_description_no_id(
    foo: str,
    bar: int,
    baz: list,
):
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)


@pytest.mark.better_parametrize(
    testcase := namedtuple("testcase", "baz, id"),
    [
        testcase(baz=["foo"], id="print me"),
        testcase(baz=[], id="hello"),
    ],
)
@pytest.mark.better_parametrize(
    testcase := namedtuple("testcase", "foo, bar, id"),
    [
        testcase(foo="foo", bar=69, id="print me"),
        testcase(foo="aaaaa", bar=420, id="hello"),
    ],
)
def test_stacked_usage_with_two_ids(
    foo: str,
    bar: int,
    baz: list,
):
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)


@pytest.mark.better_parametrize(
    param := namedtuple("param", "qux"),
    [
        param(qux="quxx"),
        param(qux=""),
    ],
)
@pytest.mark.better_parametrize(
    param := namedtuple("param", "baz"),
    [
        param(baz=["foo"]),
        param(baz=[]),
    ],
)
@pytest.mark.better_parametrize(
    testcase := namedtuple("testcase", "foo, bar, id"),
    [
        testcase(
            id="The order can be reversed",
            foo="sth",
            bar=666,
        )
    ],
)
def test_stacked_usage_with_one_anonymous_param(
    foo: str,
    bar: int,
    baz: list,
    qux: str,
):
    assert isinstance(foo, str)
    assert isinstance(bar, int)
    assert isinstance(baz, list)
    assert isinstance(qux, str)
