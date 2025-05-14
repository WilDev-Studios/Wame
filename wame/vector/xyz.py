from __future__ import annotations

from numpy.typing import NDArray
from typing import Union
from wame.vector.base import BaseVector3

import numpy as np

class FloatVector3(BaseVector3):
    '''3D Float Vector Array.'''

    _array: NDArray[np.float32]

    def __init__(self, x: float, y: float, z: float) -> None:
        '''
        Create a new 3D, `float`-based vector array.
        
        Parameters
        ----------
        x : float
            Coordinate on the X-axis.
        y : float
            Coordinate on the Y-axis.
        z : float
            Coordinate on the Z-axis.
        '''

        self._array:NDArray[np.float32] = np.array([x, y, z], np.float32)

    def __add__(self, other: FloatVector3) -> FloatVector3:
        if isinstance(other, FloatVector3):
            return FloatVector3.from_iterable(self._array + other._array)
        
        error:str = f"Unsupported operand type(s) for +: `FloatVector3` and `{type(other).__name__}`"
        raise TypeError(error)

    def __floordiv__(self, scalar: Union[int, float]) -> FloatVector3:
        if scalar == 0:
            error:str = "Cannot divide by zero"
            raise ZeroDivisionError(error)
        
        if isinstance(scalar, (int, float)):
            return FloatVector3.from_iterable(self._array // scalar)
        
        error:str = "Can only divide `FloatVector3` by an `int` or `float`"
        raise TypeError(error)

    def __mul__(self, scalar: float) -> FloatVector3:
        if isinstance(scalar, (float, int)):
            return FloatVector3.from_iterable(self._array * scalar)
        
        error:str = "Can only multiply `FloatVector3` by a `float` or `int`"
        raise TypeError(error)

    def __neg__(self) -> FloatVector3:
        return FloatVector3.from_iterable(-self._array)

    def __rsub__(self, other: FloatVector3) -> FloatVector3:
        if isinstance(other, FloatVector3):
            return FloatVector3.from_iterable(other._array - self._array)
        
        error:str = f"Unsupported operand type(s) for -: `{type(other).__name__}` and `FloatVector3`"
        raise TypeError(error)

    def __setitem__(self, index: int, value:float) -> None:
        if index not in (0, 1, 2):
            error:str = "Index out of bounds for FloatVector3: valid indices are 0, 1, and 2"
            raise IndexError(error)
        
        self._array[index] = float(value)

    def __sub__(self, other: FloatVector3) -> FloatVector3:
        if isinstance(other, FloatVector3):
            return FloatVector3.from_iterable(self._array - other._array)
        
        error:str = f"Unsupported operand type(s) for -: `FloatVector2` and `{type(other).__name__}`"
        raise TypeError(error)

    def __truediv__(self, scalar: Union[int, float]) -> FloatVector3:
        if scalar == 0:
            error:str = "Cannot divide by zero"
            raise ZeroDivisionError(error)
        
        if isinstance(scalar, (int, float)):
            return FloatVector3.from_iterable(self._array / scalar)
    
        error:str = "Can only divide `FloatVector3` by an `int` or `float`"
        raise TypeError(error)

    def copy(self) -> FloatVector3:
        '''
        Copy this vector into another instance of the same vector.
        
        Returns
        -------
        FloatVector3
            This vector as another instance.
        '''

        return FloatVector3(self._array[0], self._array[1], self._array[2])

    def cross(self, other: FloatVector3) -> FloatVector3:
        '''
        Calculate the cross product of this vector with another.
        
        Parameters
        ----------
        other : FloatVector3
            The other vector cross with.
        
        Returns
        -------
        FloatVector3
            The resulting cross product vector.
        '''

        if not isinstance(other, FloatVector3):
            error:str = f"Expected `FloatVector3`, got `{type(other).__name__}`"
            raise TypeError(error)
        
        return FloatVector3.from_iterable(np.cross(self._array, other._array))

    def dot(self, other: FloatVector3) -> float:
        '''
        Calculate the dot product of this vector with another.
        
        Parameters
        ----------
        other : FloatVector3
            The other vector to calculate the dot product with.
        
        Returns
        -------
        float
            The dot product of these two vectors.
        '''
        
        return float(np.dot(self._array, other._array))

    @classmethod
    def from_iterable(cls, iterable: Union[FloatVector3, IntVector3, np.ndarray[np.float32], tuple[Union[int, float], Union[int, float], Union[int, float]], list[Union[int, float]]]) -> FloatVector3:
        '''
        Create a new 3D, `float`-based vector array from an iterable with 3 `float` or `int` values.
        
        Parameters
        ----------
        iterable : FloatVector3 | IntVector3 | numpy.ndarray[numpy.int32] | tuple[int | float, int | float, int | float] | list[int | float]
            The iterable with 3 `float` or `int` values.
        
        Returns
        -------
        FloatVector3
            The new 3D, `float`-based vector array.
        
        Raises
        ------
        ValueError
            If the provided iterable contains more or less than 3 values
        '''

        items: tuple[float, float, float] = tuple(iterable)

        if len(items) != 3:
            error:str = "Iterable provided must only contain 3 values"
            raise ValueError(error)

        x, y, z = items        
        return cls(x, y, z)

    def normalize(self) -> FloatVector3:
        '''
        Normalize this vector.
        
        Returns
        -------
        FloatVector3
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
        numpy.ndarray[numpy.float32]
            This vector as an instance of a `NumPy` array.

        Warning
        -------
        If you return the array itself, any changes to that array will change this vector object.
        '''

        return self._array.copy() if copy else self._array
    
    def to_tuple(self) -> tuple[float, float, float]:
        '''
        Return this vector as a tuple.
        
        Returns
        -------
        tuple[float, float, float]
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
    
    @property
    def z(self) -> float:
        '''Coordinate on the Z-axis.'''
        return self._array[2]
    
    @z.setter
    def z(self, value: float) -> None:
        self._array[2] = float(value)

class IntVector3(BaseVector3):
    '''3D Integer Vector Array.'''

    _array: NDArray[np.int32]

    def __init__(self, x: int, y: int, z: int) -> None:
        '''
        Create a new 3D, `int`-based vector array.
        
        Parameters
        ----------
        x : int
            Coordinate on the X-axis.
        y : int
            Coordinate on the Y-axis.
        z : int
            Coordinate on the Z-axis.
        '''

        self._array:NDArray[np.int32] = np.array([x, y, z], np.int32)

    def __add__(self, other: IntVector3) -> IntVector3:
        if isinstance(other, IntVector3):
            return IntVector3.from_iterable(self._array + other._array)
        
        error:str = f"Unsupported operand type(s) for +: `IntVector3` and `{type(other).__name__}`"
        raise TypeError(error)

    def __floordiv__(self, scalar: float) -> IntVector3:
        if scalar == 0:
            error:str = "Cannot divide by zero"
            raise ZeroDivisionError(error)
        
        if isinstance(scalar, (int, float)):
            return IntVector3.from_iterable(self._array // scalar)
        
        error:str = "Can only floor divide `IntVector3` by an `int` or `float`"
        raise TypeError(error)

    def __mul__(self, scalar: int) -> IntVector3:
        if isinstance(scalar, int):
            return IntVector3.from_iterable(self._array * scalar)
        
        error:str = "Can only multiply `IntVector2` by an `int`"
        raise TypeError(error)

    def __neg__(self) -> IntVector3:
        return IntVector3.from_iterable(-self._array)

    def __rsub__(self, other: IntVector3) -> IntVector3:
        if isinstance(other, IntVector3):
            return IntVector3.from_iterable(other._array - self._array)
        
        error:str = f"Unsupported operand type(s) for -: `{type(other).__name__}` and `IntVector3`"
        raise TypeError(error)

    def __setitem__(self, index: int, value:int) -> None:
        if index not in (0, 1, 2):
            error:str = "Index out of bounds for IntVector3: valid indices are 0, 1, and 2"
            raise IndexError(error)
        
        self._array[index] = int(value)

    def __sub__(self, other: IntVector3) -> IntVector3:
        if isinstance(other, IntVector3):
            return IntVector3.from_iterable(self._array - other._array)
        
        error:str = f"Unsupported operand type(s) for -: `IntVector3` and `{type(other).__name__}`"
        raise TypeError(error)

    def __truediv__(self, scalar: float) -> FloatVector3:
        if scalar == 0:
            error:str = "Cannot divide by zero"
            raise ZeroDivisionError(error)
        
        if isinstance(scalar, (int, float)):
            return FloatVector3.from_iterable(self._array / scalar)
    
        error:str = "Can only divide `IntVector3` by an `int` or `float`"
        raise TypeError(error)

    def copy(self) -> IntVector3:
        '''
        Copy this vector into another instance of the same vector.
        
        Returns
        -------
        IntVector3
            This vector as another instance.
        '''

        return IntVector3(self._array[0], self._array[1], self._array[2])

    def cross(self, other: IntVector3) -> IntVector3:
        '''
        Calculate the cross product of this vector with another.
        
        Parameters
        ----------
        other : IntVector3
            The other vector cross with.
        
        Returns
        -------
        IntVector3
            The resulting cross product vector.
        '''

        if not isinstance(other, IntVector3):
            error:str = f"Expected `IntVector3`, got `{type(other).__name__}`"
            raise TypeError(error)
        
        return IntVector3.from_iterable(np.cross(self._array, other._array))

    def dot(self, other: IntVector3) -> float:
        '''
        Calculate the dot product of this vector with another.
        
        Parameters
        ----------
        other : IntVector3
            The other vector to calculate the dot product with.
        
        Returns
        -------
        float
            The dot product of these two vectors.
        '''
        
        return float(np.dot(self._array, other._array))

    @classmethod
    def from_iterable(cls, iterable: Union[IntVector3, np.ndarray[np.int32], tuple[int, int, int], list[int]]) -> IntVector3:
        '''
        Create a new 3D, `int`-based vector array from an iterable with 3 `int` values.
        
        Parameters
        ----------
        iterable : IntVector3 | numpy.ndarray[numpy.int32] | tuple[int, int, int] | list[int]
            The iterable with 3 `int` values.
        
        Returns
        -------
        IntVector3
            The new 3D, `int`-based vector array.
        
        Raises
        ------
        ValueError
            If the provided iterable contains more or less than 3 values
        '''

        items: tuple[int, int, int] = tuple(iterable)

        if len(items) != 3:
            error:str = "Iterable provided must only contain 3 values"
            raise ValueError(error)

        x, y, z = items
        return cls(x, y, z)

    def normalize(self) -> FloatVector3:
        '''
        Normalize this vector.
        
        Returns
        -------
        FloatVector3
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
    
    def to_tuple(self) -> tuple[int, int, int]:
        '''
        Return this vector as a tuple.
        
        Returns
        -------
        tuple[int, int, int]
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
    
    @property
    def z(self) -> int:
        '''Coordinate on the Z-axis.'''
        return self._array[2]
    
    @z.setter
    def z(self, value: int) -> None:
        self._array[2] = int(value)