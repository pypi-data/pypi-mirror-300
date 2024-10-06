from __future__ import annotations
from typing import TypeVar, Callable, Any, Generic, Union

OriginalType = TypeVar("OriginalType")
TargetType = TypeVar("TargetType")


class Castable(Generic[TargetType]):
    """This generic type can be used to align static type checking between packages."""

    pass


# For convenience in function signatures
CastableValue = Union[TargetType, Castable[TargetType]]


_CASTS: dict[tuple[type, type], Callable[[Any], Any]] = {}


def add_cast(
    original_class: type[OriginalType],
    target_class: type[TargetType],
    converter: Callable[[OriginalType], TargetType],
) -> None:
    """
    Enable casting from all instances of a class to a target class
    and set the function that does it.

    If a `value` passed to `cast` is an instance of original_class
    and the `target_class` passed to `cast` is the same as this
    `target_class`, then the value will be converted with this
    `converter` function and returned.

    Args:
        original_class:
            Will match a value passed to `cast` if the value is
            an instance of this, or one of its subclasses. If there
            could be multiple matches, the most specific
            `original_class` will be used (precisely, the first match
            in the Method Resolution Order
            https://www.python.org/download/releases/2.3/mro/ ).
        target_class:
            Will match a `target_class` passed to `cast` if it is exactly
            the same class (subclasses are not matched).
        converter:
            If there is a match with `original_class` and `target_class`
            when `cast` is called, this function will be called on
            `value` and the result will be returned.
    """
    classes = (original_class, target_class)
    if classes in _CASTS:
        raise Exception(f"There is already a mapping for the classes {classes}")
    _CASTS[classes] = converter


def cast(value: Any, target_class: type[TargetType]) -> TargetType:
    """
    Convert a value into an equivalent object of a diferent class.

    Args:
        value:
            A value that we want to convert into an equivalentvalue of a
            different type.
        target_type:
            The type that we want our output value to have.

    Returns:
        The result of passing the `value` to the `coverter` function from
        the matching `add_cast` call.
    """
    original_class = value.__class__
    if issubclass(original_class, target_class):
        return value
    for ancestor in original_class.__mro__:
        converter = _CASTS.get((ancestor, target_class))
        if converter is not None:
            return converter(value)
    raise TypeError(f"Not able to cast type {original_class} to {target_class}.")
