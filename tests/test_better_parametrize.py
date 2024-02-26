def test_stuff(pytester):
    pytester.makepyfile(
        """
        from collections import namedtuple

        import pytest

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
        """
    )
    result = pytester.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_basic_usage*PASSED*",
        ]
    )

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0
