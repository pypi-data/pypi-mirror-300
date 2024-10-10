import pytest

from .callback import Callback


def test_callback(mocker):
    mock = mocker.Mock()

    def fn(*args, **kwargs):
        mock(*args, **kwargs)

    cb = Callback(fn)
    cb("v1", "v2", kw1="v3")

    mock.assert_called_once_with("v1", "v2", kw1="v3")


def test_non_function_raises():
    with pytest.raises(ValueError):
        Callback("not a function")


def test_handles_system_exit():
    def fn():
        raise SystemExit("This is a system exit")

    cb = Callback(fn)
    cb()  # no error because it's handled.
