"""BaseComponentValueSetter class module."""

from abc import abstractmethod

from zmc.utils.callback import Callback

from .base_component import BaseComponent


__all__ = ["ValueReceiverBaseComponent"]


class ValueReceiverBaseComponent(BaseComponent):
    """Base class for any component that can set a value.

    Any concrete subclass must implement _set_value(self, value).
    """

    def __init__(self, component_id):
        super().__init__(component_id)
        self._callbacks = []

    def add_callback(self, func):
        """Adds a callback function that will be called when value is received.

        Callbacks will be called in the order that they are added.

        Raises:
            ValueError: If the param passed in is not a function.
        """
        # TODO: add type checking (at least number of args? no kwargs only?)
        self._callbacks.append(Callback(func))

    def clear_callbacks(self):
        """Clears all callbacks from the component."""
        self._callbacks = []

    @abstractmethod
    def _set_value(self, value):
        """Store the value pass in for future access."""

    @abstractmethod
    def _callback_args(self):
        """Args to be passed into the callbacks as: *args

        These should be the values of the component in whatever form makes the
        most sense.

        Returns:
            Iterable of args that will be unpacked and passed into the callbacks
        """

    def receive_value(self, value):
        """Receive the value sent from the Mission Control app.

        First sets the value on the component. Once that is done, calls any
        callback functions that have been added.

        Args:
            value: component value that has been received.
        """
        self._set_value(value)
        for fn in self._callbacks:
            fn(*self._callback_args())
