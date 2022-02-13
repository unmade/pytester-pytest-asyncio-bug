# `Event loop is closed` when using `pytester` and async fixture finalization

This repo contains a minimal reproducible example of a bug with an async
`autouse=True` fixture finalization when using `pytester` plugin.

Basically, this async fixture added as a finalizer to a non-async test.

The bug only appears when using [pytester](https://docs.pytest.org/en/7.0.x/how-to/writing_plugins.html#testing-plugins).

## Steps to reproduce the bug

To reproduce a bug as is:

```bash
tox -e py3-bug
```

Actual result:

```bash
ERROR tests/test_fixtures.py::test_fixture_setup - RuntimeError: Event loop is closed
```

Expected result: no error at all, finalizer should not run in the regular test.

## Workaround #1

Prior `pytest-asyncio<0.17` you could redefine the `event_loop` fixture without
closing the loop on finalization.

```bash
tox -e py3-workaround_1
```

## Workaround #2

In the `pytest-asyncio>=0.17` the workaround #1 no longer works. However,
you can redefine the fixture with async finalization

```bash
tox -e py3-workaround_2
