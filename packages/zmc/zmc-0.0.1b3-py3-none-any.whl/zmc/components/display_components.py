"""Graph class module."""

from .core import DataSenderBaseComponent


__all__ = ["BooleanDisplay", "NumericDisplay", "TextDisplay"]


class DisplayBaseComponent(DataSenderBaseComponent):
    """Base display component class."""

    def __init__(self, component_id, default_value):
        super().__init__(component_id)
        self._value = default_value

    @property
    def data(self):
        return {"value": self._value}

    @property
    def value(self):
        """Current value of the component."""
        return self._value

    def set_value(self, value):
        """Send value to app."""
        self._value = value
        self._send_data()


class BooleanDisplay(DisplayBaseComponent):
    """Boolean display component class."""

    def __init__(self, component_id):
        super().__init__(component_id, False)


class NumericDisplay(DisplayBaseComponent):
    """Numeric display component class."""

    def __init__(self, component_id):
        super().__init__(component_id, 0)


class TextDisplay(DisplayBaseComponent):
    """Text display component class."""

    def __init__(self, component_id):
        super().__init__(component_id, "")
