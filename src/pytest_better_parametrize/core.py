import typing as t
import pytest
from _pytest.mark import ParameterSet

TestCase = t.NamedTuple


def prep_args(
    cls: t.Type[TestCase],
    testcases: t.Sequence[TestCase],
    ignore: t.Sequence[str] = (),
    **kwargs,
) -> pytest.mark.parametrize:
    """
    Wraps pytest.mark.parametrize.
    Unpacks the params into pytest.params with positional arguments.
    """

    # check it's a proper `namedtuple`
    if not hasattr(cls, "_fields"):
        raise ValueError(
            "`cls` must be a namedtuple with a `_fields` attribute"
        )

    ignore: set[str] = {"id"}.union(ignore)

    # remove ignore fields
    fields = tuple(key for key in cls._fields if key not in ignore)
    params = [_to_pytest_param(tc, fields) for tc in testcases]
    return fields, params, kwargs


def _to_pytest_param(
    testcase: TestCase,
    fields: t.Tuple[str, ...],
) -> ParameterSet:
    return pytest.param(
        *(getattr(testcase, key) for key in fields),
        id=_get_id(testcase, fields),
    )


def _get_id(
    testcase: TestCase,
    fields: t.Tuple[str, ...],
) -> str:
    return getattr(
        testcase,
        "id",
        ",".join(f"{key}={getattr(testcase, key)!r}" for key in fields),
    )
