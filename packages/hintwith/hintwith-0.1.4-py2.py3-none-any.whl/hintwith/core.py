"""
Contains the core of hintwith: hintwith(), hintwithmethod(), etc.

NOTE: this module is private. All functions and objects are available in the main
`hintwith` namespace - use that instead.

"""

from typing import Any, Callable, Literal, TypeVar, overload

from typing_extensions import Concatenate, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")

__all__ = ["hintwith", "hintwithmethod"]


@overload
def hintwith(
    __exist: Callable[P, Any], __hint_returntype: Literal[False] = False
) -> Callable[[Callable[..., T]], Callable[P, T]]: ...


@overload
def hintwith(
    __exist: Callable[P, T], __hint_returntype: Literal[True] = True
) -> Callable[[Callable], Callable[P, T]]: ...


def hintwith(__exist: Callable, __hint_returntype: bool = False) -> Callable:
    """
    This decorator does literally NOTHING to the decorated function except
    type-hinting its with the annotations of another existing function.
    Nothing inside the decorated function (including attributes like `__doc__`
    and `__annotations__`) are modified, but the type hints may SEEM to be
    changed in language tools like Pylance.

    Parameters
    ----------
    __exist : Callable
        An existing function object.

    __hint_returntype : bool, optional
        Determines whether to use the return type of the original function
        (or use the decorated function's return type itself), by default
        False.

    Returns
    -------
    Callable
        A decorator which returns the input itself.

    """

    def decorator(a):
        return a  # See? We do nothing to the function

    return decorator


@overload
def hintwithmethod(
    __exist: Callable[Concatenate[Any, P], Any],
    __hint_returntype: Literal[False] = False,
) -> Callable[[Callable[..., T]], Callable[P, T]]: ...


@overload
def hintwithmethod(
    __exist: Callable[Concatenate[Any, P], T], __hint_returntype: Literal[True] = True
) -> Callable[[Callable], Callable[P, T]]: ...


def hintwithmethod(__exist: Callable, __hint_returntype: bool = False) -> Callable:
    """
    Behaves like `hintwith()` except that the existing function whose
    annotations are used is a method rather than a direct callable.

    Parameters
    ----------
    __exist : Callable
        An existing method object.

    __hint_returntype : bool, optional
        Determines whether to use the return type of the original method
        (or use the decorated function's return type itself), by default
        False.


    Returns
    -------
    Callable
        A decorator which returns the input itself.

    """

    def decorator(a):
        return a  # See? We do nothing to the function

    return decorator
