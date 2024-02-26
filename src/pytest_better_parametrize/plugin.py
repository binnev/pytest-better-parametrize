from .core import prep_args


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line(
        "markers", "better_parametrize(cls, values): takes some arguments"
    )


def pytest_generate_tests(metafunc):
    """
    :param metafunc:
    :return:
    """

    for marker in metafunc.definition.own_markers:
        if marker.name == "better_parametrize":
            argnames, argvalues, kwargs = prep_args(
                *marker.args,
                **marker.kwargs,
            )
            metafunc.parametrize(argnames, argvalues, **kwargs)
