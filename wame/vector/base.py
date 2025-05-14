from __future__ import annotations

from numpy.typing import NDArray
from typing import Iterator, Union

import numpy as np

class BaseVector:
    '''
    Base Vector Array.
    
    Warning
    -------
    This is a base vector object that only should be inherited by other vector objects.
    This should never be instantiated for any reason.
    '''

    __slots__ = ("_array",)
    
    def __abs__(self) -> float: return self.magnitude()
    def __array__(self) -> NDArray[Union[np.int32, np.float32]]: return self._array
    def __eq__(self, other: object) -> bool: return isinstance(other, type(self)) and np.array_equal(self._array, other._array)
    def __iter__(self) -> Iterator[Union[int, float]]: return iter(self._array)
    def __ge__(self, other: BaseVector) -> bool: return self.magnitude() >= other.magnitude()
    def __getitem__(self, index: int) -> Union[int, float]: return self._array[index]
    def __gt__(self, other: BaseVector) -> bool: return self.magnitude() > other.magnitude()
    def __le__(self, other: BaseVector) -> bool: return self.magnitude() <= other.magnitude()
    def __lt__(self, other: BaseVector) -> bool: return self.magnitude() < other.magnitude()
    def __radd__(self, other: BaseVector) -> BaseVector: return self + other
    def __repr__(self) -> str: return f"{type(self).__name__}{str(self)}"
    def __rmul__(self, scalar: Union[int, float]) -> BaseVector: return self * scalar

    def magnitude(self) -> float:
        '''
        Calculate the magnitude of this vector.
        
        Returns
        -------
        float
            The magnitude of this vector.
        '''

        return float(np.linalg.norm(self._array))

class BaseVector2(BaseVector):
    '''
    Base 2D Vector Array.
    
    Warning
    -------
    This is a base 2D vector object that only should be inherited by other 2D vector objects.
    This should never be instantiated for any reason.
    '''
    
    def __len__(self) -> int: return 2
    def __hash__(self) -> int: return hash((self._array[0], self._array[1]))
    def __str__(self) -> str: return f"({self._array[0]}, {self._array[1]})"

class BaseVector3(BaseVector):
    '''
    Base 3D Vector Array.
    
    Warning
    -------
    This is a base 3D vector object that only should be inherited by other 3D vector objects.
    This should never be instantiated for any reason.
    '''
    
    def __len__(self) -> int: return 3
    def __hash__(self) -> int: return hash((self._array[0], self._array[1], self._array[2]))
    def __str__(self) -> str: return f"({self._array[0]}, {self._array[1]}, {self._array[2]})"