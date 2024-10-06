# Pewter

Pewter is a simple library for type casting / type coercion.
Its purpose is to let users avoid boilerplate type conversion code.

## Installation

Install Pewter using [pip](https://pip.pypa.io/):

```commandline
pip install pewter
```

## Usage example

This example will use a simple user-defined class:

```python
from dataclasses import dataclass

@dataclass
class LipschitzQuaternion:
    x: int
    i: int
    j: int
    k: int
```

Before Pewter can convert objects to different classes, it needs to be told how to.
To do this use the `add_cast` function.
In this example we tell Pewter our class can be used as an `int` if its attributes `i`, `j`, `k` are all zero:

```python
from pewter import add_cast

def quaternion_to_int(value: LipschitzQuaternion) -> int:
    if value.i != 0 or value.j != 0 or value.k != 0:
        raise ValueError()
    return value.x

add_cast(LipschitzQuaternion, int, quaternion_to_int)
```

Now converting is easy:

```python
from pewter import cast

quarternion = LipschitzQuaternion(3, 0, 0, 0)
# Result is 3
cast(quarternion, int)
# Result is 5
cast(5, int)
```

## Advanced usage ###

### Type checkng

For parameters which support many castable classes, the type signature with MyPy can get awkward.
Pewter can simplify this by using generic types:

Without generic types:

```python
from typing import Union
from pewter import add_cast, cast

class LikeThree:
    pass

class LikeFour:
    pass

add_cast(LikeThree, int, lambda value: 3)
add_cast(LikeFour, int, lambda value: 4)

def triple(value: Union[int, LikeThree, LikeFour]) -> int:
    return cast(value, int) * 3
```

With generic types:

```python
from pewter import Castable, CastableValue, add_cast, cast

class LikeThree(Castable[int]):
    pass

class LikeFour(Castable[int]):
    pass

add_cast(LikeThree, int, lambda value: 3)
add_cast(LikeFour, int, lambda value: 4)

def triple(value: CastableValue[int]) -> int:
    return cast(value, int) * 3
```

### Subclasses and inheritance

Pewter supports inheritance for the `original_class`, but not for the `target_class`.
To find the appropriate converter method, Pewter looks for a suitable `add_cast` call.
The `value` passed to `cast` must be an instance of the `original_class` in `add_cast` (respecting inheritance).
The `target_class` in `cast` and `add_cast` must match exactly (not using inheritance).

There may be more than one `(original_class, target_class)` pair that matches for a `cast` call.
This can happen when casts have been defined with `add_cast` for origin classes where one is a subclass of another.
In this case, the `origin_class` that is the nearest ancestor of the class of the `value` will be used.
Precisely, the first match in the `value` [Method Resolution Order](https://www.python.org/download/releases/2.3/mro/) will be used.

## Rationale

Type conversion using a constructor is a common and effective idiom in Python.
For example the `int` constructor: `int("2")`.
A problem can arise when it is not possible to modify the constructor to allow a new type, such as when the class is defined in a different project.
Pewter provides functionality similar to `to_str`, but it can be used for any class.

Pewter supports inheritance in the `original_class`, but not in the `target_class` for efficiency and simplicity.
Pewter is intended to reduce boilerplate when passing values, which is why it can accept subclasses in the `original_class`.
The caller does not need to know that Pewter is being used.
The method using `cast` is always aware of Pewter, and can make sure to choose the precise class it wants.
If appropriate casts are available, but do not give the exact class desired, the method can implement a conversion, which would not require code changes for any number of supported castable classes.
