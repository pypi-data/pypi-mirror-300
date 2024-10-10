from .base_component import BaseComponent
from .single_value_component import SingleValueComponent
from .value_receiver_base_component import ValueReceiverBaseComponent


def test_is_base_subclass():
    assert issubclass(SingleValueComponent, BaseComponent)
    assert issubclass(SingleValueComponent, ValueReceiverBaseComponent)


def test_default_value():
    val = 4  # Arbitrary value
    c1 = SingleValueComponent("id", val)

    assert c1.value == val


def test_set_value():
    c1 = SingleValueComponent("id", 5)
    val = 9  # Arbitrary value
    c1.receive_value({"value": val})

    assert c1.value == val


def test_callback(mocker):
    mock = mocker.Mock()

    c1 = SingleValueComponent("id", 5)
    c1.add_callback(lambda v: mock(v))
    val = 9  # Arbitrary value
    c1.receive_value({"value": val})
    mock.assert_called_once_with(val)
