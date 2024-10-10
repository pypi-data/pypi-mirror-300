import pytest

from .base_component import BaseComponent
from .value_receiver_base_component import ValueReceiverBaseComponent


def test_is_base_subclass():
    assert issubclass(ValueReceiverBaseComponent, BaseComponent)


def test_is_abstract():
    # pylint:disable=abstract-class-instantiated
    # pylint:disable=abstract-method

    with pytest.raises(TypeError, match="abstract class"):
        ValueReceiverBaseComponent("id")

    class ComponentWithSetValue(ValueReceiverBaseComponent):
        def _set_value(self, value):
            self.value = value

    with pytest.raises(TypeError, match="abstract class"):
        ComponentWithSetValue("id")

    class ComponentWithCallbackArgs(ValueReceiverBaseComponent):
        def _callback_args(self):
            return []

    with pytest.raises(TypeError, match="abstract class"):
        ComponentWithCallbackArgs("id")


class Component(ValueReceiverBaseComponent):
    """Concrete class for testing setting value and making callbacks"""

    def _set_value(self, value):
        self.value = value

    def _callback_args(self):
        return (self.value, self.value * 2)


def test_impl():

    c = Component("id")
    value = 9  # Arbitrary value
    c.receive_value(value)
    assert c.value == value


def test_callbacks(mocker):
    mock1 = mocker.Mock()
    mock2 = mocker.Mock()

    c = Component("id")
    c.add_callback(lambda x, y: mock1(x, y))

    value = 9  # Arbitrary value
    c.receive_value(value)
    mock1.assert_called_once_with(value, value * 2)
    mock1.reset_mock()

    c.add_callback(lambda x, y: mock2(x, y))

    value = 4  # Arbitrary value
    c.receive_value(value)
    mock1.assert_called_once_with(value, value * 2)
    mock2.assert_called_once_with(value, value * 2)


def test_clear_callbacks(mocker):
    mock1 = mocker.Mock()
    mock2 = mocker.Mock()

    c = Component("id")
    c.add_callback(lambda x, y: mock1(x, y))
    c.add_callback(lambda x, y: mock2(x, y))

    value = 9  # Arbitrary value
    c.receive_value(value)
    mock1.assert_called_once_with(value, value * 2)
    mock2.assert_called_once_with(value, value * 2)

    c.clear_callbacks()
    c.receive_value(10)  # Arbitrary value
    mock1.reset_mock()
    mock2.reset_mock()

    mock1.assert_not_called()
    mock2.assert_not_called()
