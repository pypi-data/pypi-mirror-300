"""SingleTextComponent class module."""

from .core import SingleValueComponent


__all__ = ["TextInput", "FilepathInput"]


class SingleTextComponent(SingleValueComponent):
    """Text receiver class which contains a single value."""

    def __init__(self, component_id):
        super().__init__(component_id, "")


class TextInput(SingleTextComponent):
    """Text class, representing a freeform or dropdown text component.

    The class has a single value that can be accessed as an attribute:
    `text_input.value`.

    Callbacks will be called with the value as the first and only parameter.
    """


class FilepathInput(SingleTextComponent):
    """Filepath class, representing a file path choosen from the app.

    The class has a single value that can be accessed as an attribute:
    `filepath.value`.
    """
