from .core import _prep_args


def pytest_configure(config):
    """
    This registers the `pytest-better-parametrize` marker with pytest. It is
    the programmatic equivalent of writing

        ```
        markers =
            better_parametrize
        ```

    in your pytest.ini file.
    """
    config.addinivalue_line("markers", "better_parametrize")


def pytest_generate_tests(metafunc) -> None:
    """
    Pytest looks for functions with this name, and calls them during test
    generation. This allows us to detect the `better_paramterize` marker,
    convert its input into vanilla pytest.params, and pipe those into
    pytest's own parametrize logic.

    :param metafunc: a wrapper around the test function, which has access to
        the markers that decorate it
    :return: None
    """

    for marker in metafunc.definition.own_markers:
        if marker.name == "better_parametrize":
            argnames, argvalues, kwargs = _prep_args(
                *marker.args,
                **marker.kwargs,
            )
            metafunc.parametrize(argnames, argvalues, **kwargs)
