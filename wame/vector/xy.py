from __future__ import annotations

from numpy.typing import NDArray
from typing import Union
from wame.vector.base import BaseVector2

import numpy as np

class FloatVector2(BaseVector2):
    '''2D Float Vector Array.'''

    __slots__ = ("_array",)
    _array: NDArray[np.float32]

    def __init__(self, x: float, y: float) -> None:
        '''
        Create a new 2D, `float`-based vector array.
        
        Parameters
        ----------
        x : float
            Coordinate on the X-axis.
        y : float
            Coordinate on the Y-axis.
        '''

        self._array:NDArray[np.float32] = np.array([x, y], np.float32)

    def __add__(self, other: FloatVector2) -> FloatVector2:
        if isinstance(other, FloatVector2):
            return FloatVector2.from_iterable(self._array + other._array)
        
        error:str = f"Unsupported operand type(s) for +: `FloatVector2` and `{type(other).__name__}`"
        raise TypeError(error)

    def __floordiv__(self, scalar: Union[int, float]) -> FloatVector2:
        if scalar == 0:
            error:str = "Cannot divide by zero"
            raise ZeroDivisionError(error)
        
        if isinstance(scalar, (int, float)):
            return FloatVector2.from_iterable(self._array // scalar)
        
        error:str = "Can only divide `FloatVector2` by an `int` or `float`"
        raise TypeError(error)

    def __mul__(self, scalar: float) -> FloatVector2:
        if isinstance(scalar, (float, int)):
            return FloatVector2.from_iterable(self._array * scalar)
        
        error:str = "Can only multiply `FloatVector2` by a `float` or `int`"
        raise TypeError(error)

    def __neg__(self) -> FloatVector2:
        return FloatVector2.from_iterable(-self._array)

    def __rsub__(self, other: FloatVector2) -> FloatVector2:
        if isinstance(other, FloatVector2):
            return FloatVector2.from_iterable(other._array - self._array)
        
        error:str = f"Unsupported operand type(s) for -: `{type(other).__name__}` and `FloatVector2`"
        raise TypeError(error)

    def __setitem__(self, index: int, value:float) -> None:
        if index not in (0, 1):
            error:str = "Index out of bounds for FloatVector2: valid indices are 0 and 1"
            raise IndexError(error)
        
        self._array[index] = float(value)

    def __sub__(self, other: FloatVector2) -> FloatVector2:
        if isinstance(other, FloatVector2):
            return FloatVector2.from_iterable(self._array - other._array)
        
        error:str = f"Unsupported operand type(s) for -: `FloatVector2` and `{type(other).__name__}`"
        raise TypeError(error)

    def __truediv__(self, scalar: Union[int, float]) -> FloatVector2:
        if scalar == 0:
            error:str = "Cannot divide by zero"
            raise ZeroDivisionError(error)
        
        if isinstance(scalar, (int, float)):
            return FloatVector2.from_iterable(self._array / scalar)
    
        error:str = "Can only divide `FloatVector2` by an `int` or `float`"
        raise TypeError(error)

    def copy(self) -> FloatVector2:
        '''
        Copy this vector into another instance of the same vector.
        
        Returns
        -------
        FloatVector2
            This vector as another instance.
        '''

        return FloatVector2(self._array[0], self._array[1])

    def dot(self, other: FloatVector2) -> float:
        '''
        Calculate the dot product of this vector with another.
        
        Parameters
        ----------
        other : FloatVector2
            The other vector to calculate the dot product with.
        
        Returns
        -------
        float
            The dot product of these two vectors.
        '''

        return float(np.dot(self._array, other._array))

    @classmethod
    def from_iterable(cls, iterable: Union[FloatVector2, IntVector2, np.ndarray[np.float32], tuple[Union[int, float], Union[int, float]], list[Union[int, float]]]) -> FloatVector2:
        '''
        Create a new 2D, `float`-based vector array from an iterable with 2 `float` or `int` values.
        
        Parameters
        ----------
        iterable : FloatVector2 | IntVector2 | numpy.ndarray[numpy.int32] | tuple[int | float, int | float] | list[int | float]
            The iterable with 3 `float` or `int` values.
        
        Returns
        -------
        FloatVector2
            The new 2D, `float`-based vector array.
        
        Raises
        ------
        ValueError
            If the provided iterable contains more or less than 2 values
        '''

        items: tuple[int, int] = tuple(iterable)

        if len(items) != 2:
            error:str = "Iterable provided must only contain 2 values"
            raise ValueError(error)

        x, y = items        
        return cls(x, y)

    def normalize(self) -> FloatVector2:
        '''
        Normalize this vector.
        
        Returns
        -------
        FloatVector2
            The normalized vector.
        
        Raises
        ------
        ZeroDivisionError
            If the magnitude of this vector is 0
        '''

        mag: float = self.magnitude()

        if mag == 0:
            error:str = "Cannot normalize a zero-length vector."
            raise ZeroDivisionError(error)
        
        return self / mag

    def to_numpy(self, copy: bool = True) -> NDArray[np.float32]:
        '''
        Return this vector as an instance of a `NumPy` array.

        Parameters
        ----------
        copy : bool
            If this method should return a copy of the internal `NumPy` array or the array itself

        Returns
        -------
        numpy.ndarray[numpy.int32]
            This vector as an instance of a `NumPy` array.

        Warning
        -------
        If you return the array itself, any changes to that array will change this vector object.
        '''

        return self._array.copy() if copy else self._array
    
    def to_tuple(self) -> tuple[int, int]:
        '''
        Return this vector as a tuple.
        
        Returns
        -------
        tuple[int, int]
            This vector as a tuple.
        '''

        return tuple(self._array)

    @property
    def x(self) -> float:
        '''Coordinate on the X-axis.'''
        return self._array[0]

    @x.setter
    def x(self, value: float) -> None:
        self._array[0] = float(value)

    @property
    def y(self) -> float:
        '''Coordinate on the Y-axis.'''
        return self._array[1]
    
    @y.setter
    def y(self, value: float) -> None:
        self._array[1] = float(value)

class IntVector2(BaseVector2):
    '''2D Integer Vector Array.'''

    __slots__ = ("_array",)
    _array: NDArray[np.int32]

    def __init__(self, x: int, y: int) -> None:
        '''
        Create a new 2D, `int`-based vector array.
        
        Parameters
        ----------
        x : int
            Coordinate on the X-axis.
        y : int
            Coordinate on the Y-axis.
        '''

        self._array:NDArray[np.int32] = np.array([x, y], np.int32)

    def __add__(self, other: IntVector2) -> IntVector2:
        if isinstance(other, IntVector2):
            return IntVector2.from_iterable(self._array + other._array)
        
        error:str = f"Unsupported operand type(s) for +: `IntVector2` and `{type(other).__name__}`"
        raise TypeError(error)

    def __floordiv__(self, scalar: float) -> IntVector2:
        if scalar == 0:
            error:str = "Cannot divide by zero"
            raise ZeroDivisionError(error)
        
        if isinstance(scalar, (int, float)):
            return IntVector2.from_iterable(self._array // scalar)
        
        error:str = "Can only floor divide `IntVector2` by an `int` or `float`"
        raise TypeError(error)

    def __mul__(self, scalar: int) -> IntVector2:
        if isinstance(scalar, int):
            return IntVector2.from_iterable(self._array * scalar)
        
        error:str = "Can only multiply `IntVector2` by an `int`"
        raise TypeError(error)

    def __neg__(self) -> IntVector2:
        return IntVector2.from_iterable(-self._array)

    def __rsub__(self, other: IntVector2) -> IntVector2:
        if isinstance(other, IntVector2):
            return IntVector2.from_iterable(other._array - self._array)
        
        error:str = f"Unsupported operand type(s) for -: `{type(other).__name__}` and `IntVector2`"
        raise TypeError(error)

    def __setitem__(self, index: int, value:int) -> None:
        if index not in (0, 1):
            error:str = "Index out of bounds for IntVector2: valid indices are 0 and 1"
            raise IndexError(error)
        
        self._array[index] = int(value)

    def __sub__(self, other: IntVector2) -> IntVector2:
        if isinstance(other, IntVector2):
            return IntVector2.from_iterable(self._array - other._array)
        
        error:str = f"Unsupported operand type(s) for -: `IntVector2` and `{type(other).__name__}`"
        raise TypeError(error)

    def __truediv__(self, scalar: float) -> FloatVector2:
        '''
        Warning
        -------
        Truly dividing an `int`-based vector may provide `int` or `float`-based values. This arithmetic method returns a `FloatVector2`
        '''
        
        if scalar == 0:
            error:str = "Cannot divide by zero"
            raise ZeroDivisionError(error)
        
        if isinstance(scalar, (int, float)):
            return FloatVector2.from_iterable(self._array / scalar)
    
        error:str = "Can only divide `IntVector2` by an `int` or `float`"
        raise TypeError(error)

    def copy(self) -> IntVector2:
        '''
        Copy this vector into another instance of the same vector.
        
        Returns
        -------
        IntVector2
            This vector as another instance.
        '''

        return IntVector2(self._array[0], self._array[1])

    def dot(self, other: IntVector2) -> float:
        '''
        Calculate the dot product of this vector with another.
        
        Parameters
        ----------
        other : IntVector2
            The other vector to calculate the dot product with.
        
        Returns
        -------
        float
            The dot product of these two vectors.
        '''

        return float(np.dot(self._array, other._array))

    @classmethod
    def from_iterable(cls, iterable: Union[IntVector2, np.ndarray[np.int32], tuple[int, int], list[int]]) -> IntVector2:
        '''
        Create a new 2D, `int`-based vector array from an iterable with 2 `int` values.
        
        Parameters
        ----------
        iterable : IntVector2 | numpy.ndarray[numpy.int32] | tuple[int, int] | list[int]
            The iterable with 2 `int` values.
        
        Returns
        -------
        IntVector2
            The new 2D, `int`-based vector array.
        
        Raises
        ------
        ValueError
            If the provided iterable contains more or less than 2 values
        '''

        items: tuple[int, int] = tuple(iterable)

        if len(items) != 2:
            error:str = "Iterable provided must only contain 2 values"
            raise ValueError(error)

        x, y = items        
        return cls(x, y)

    def normalize(self) -> FloatVector2:
        '''
        Normalize this vector.
        
        Returns
        -------
        FloatVector2
            The normalized vector.
        
        Raises
        ------
        ZeroDivisionError
            If the magnitude of this vector is 0
        '''

        mag: float = self.magnitude()

        if mag == 0:
            error:str = "Cannot normalize a zero-length vector."
            raise ZeroDivisionError(error)
        
        return self / mag

    def to_numpy(self, copy: bool = True) -> NDArray[np.int32]:
        '''
        Return this vector as an instance of a `NumPy` array.

        Parameters
        ----------
        copy : bool
            If this method should return a copy of the internal `NumPy` array or the array itself

        Returns
        -------
        numpy.ndarray[numpy.int32]
            This vector as an instance of a `NumPy` array.

        Warning
        -------
        If you return the array itself, any changes to that array will change this vector object.
        '''

        return self._array.copy() if copy else self._array
    
    def to_tuple(self) -> tuple[int, int]:
        '''
        Return this vector as a tuple.
        
        Returns
        -------
        tuple[int, int]
            This vector as a tuple.
        '''

        return tuple(self._array)

    @property
    def x(self) -> int:
        '''Coordinate on the X-axis.'''
        return self._array[0]

    @x.setter
    def x(self, value: int) -> None:
        self._array[0] = int(value)

    @property
    def y(self) -> int:
        '''Coordinate on the Y-axis.'''
        return self._array[1]
    
    @y.setter
    def y(self, value: int) -> None:
        self._array[1] = int(value)