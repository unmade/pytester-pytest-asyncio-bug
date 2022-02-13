from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import pytest_asyncio
from packaging import version

if TYPE_CHECKING:
    from pytest import Pytester


if version.parse(pytest_asyncio.__version__) < version.parse("0.17.0"):
    addopts = ""
    skip_workaround_1 = False
else:
    addopts = "--asyncio-mode=auto"
    skip_workaround_1 = True


def test_fixture_setup(pytester: Pytester):
    pytester.makeconftest("""
        pytest_plugins = ["tests.conftest"]
    """)

    pytester.makepyfile("""
        def test_setup():
            assert True
    """)

    result = pytester.runpytest(addopts)
    result.assert_outcomes(passed=1)


@pytest.mark.workaround_1
@pytest.mark.skipif(skip_workaround_1, reason="works only with pytest-asyncio<0.17.0")
def test_workaround_1(pytester: Pytester):
    pytester.makeconftest("""
        pytest_plugins = ["tests.conftest"]
    """)

    pytester.makepyfile("""
        import asyncio

        import pytest

        @pytest.fixture
        def event_loop():
            # don't close the loop since it will be managed by parent test
            loop = asyncio.get_event_loop_policy().get_event_loop()
            yield loop

        def test_setup():
            assert True
    """)

    result = pytester.runpytest(addopts)
    result.assert_outcomes(passed=1)


@pytest.mark.workaround_1
@pytest.mark.workaround_2
def test_workaround_2(pytester: Pytester):
    pytester.makeconftest("""
        pytest_plugins = ["tests.conftest"]
    """)

    pytester.makepyfile("""
        import pytest

        @pytest.fixture(autouse=True)
        def teardown():
            return

        def test_setup():
            assert True
    """)

    result = pytester.runpytest(addopts)
    result.assert_outcomes(passed=1)
