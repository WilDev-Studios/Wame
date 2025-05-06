from __future__ import annotations

from typing import Union

import numpy as np
import math

class FloatVector3:
    '''Vector with 3 Float Values: X, Y, and Z'''

    def __init__(self, x:float, y:float, z:float) -> None:
        '''
        Instantiate a new Vector with float X, Y, and Z values
        
        Parameters
        ----------
        x : `float`
            The X value
        y : `float`
            The Y value
        z : `float`
            The Z value
        
        Raises
        ------
        `ValueError`
            If any provided arguments are not floats
        '''
        
        if isinstance(x, int):
            x = float(x)
        
        if isinstance(y, int):
            y = float(y)
        
        if isinstance(z, int):
            z = float(z)

        self.x:float = x
        self.y:float = y
        self.z:float = z
    
    def __add__(self, other:Union[FloatVector3, IntVector3, np.ndarray]) -> FloatVector3:
        if isinstance(other, FloatVector3) or isinstance(other, IntVector3):
            return FloatVector3(self.x + other.x, self.y + other.y, self.z + other.z)
        
        if isinstance(other, np.ndarray):
            return FloatVector3(self.x + other[0], self.y + other[1], self.z + other[2])
        
        raise TypeError(f"Unsupported addition with type {type(other)}")
    
    def __eq__(self, other:Union[FloatVector3, IntVector3, np.ndarray]) -> bool:
        if isinstance(other, FloatVector3) or isinstance(other, IntVector3):
            return self.to_tuple() == other.to_tuple()
        
        if isinstance(other, np.ndarray):
            return self.to_tuple() == (other[0], other[1], other[2])

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __sub__(self, other:Union[FloatVector3, IntVector3, np.ndarray]) -> FloatVector3:
        if isinstance(other, FloatVector3) or isinstance(other, IntVector3):
            return FloatVector3(self.x - other.x, self.y - other.y, self.z - other.z)
        
        if isinstance(other, np.ndarray):
            return FloatVector3(self.x - other[0], self.y - other[1], self.z - other[2])
        
        raise TypeError(f"Unsupported subtraction with type {type(other)}")

    def __repr__(self) -> str:
        return f"X: {self.x}, Y: {self.y}, Z: {self.z}"
    
    @classmethod
    def from_tuple(cls, xyz:tuple[float, float, float]) -> FloatVector3:
        '''
        Instantiate a new Vector from a tuple with float X, Y, and Z values
        
        Parameters
        ----------
        xyz : `tuple[float, float, float]`
            The tuple with the X, Y, and Z values
        
        Raises
        ------
        `ValueError`
            If the provided items in the tuple are not floats
        '''
        
        return cls(xyz[0], xyz[1], xyz[2])
    
    def to_numpy(self) -> np.ndarray[np.int32]:
        '''
        Converts this instance of `FloatVector3` into a numpy array
        
        Returns
        -------
        array : `numpy.ndarray[numpy.float32]`
            Converted x, y, and z values
        '''

        return np.array([self.x, self.y, self.z], dtype=np.float32)

    def to_tuple(self) -> tuple[float, float, float]:
        '''
        Converts this instance of `FloatVector3` into a `tuple`
        
        Returns
        -------
        vector : `tuple[float, float, float]`
            Converted x, y, and z values
        '''

        return (self.x, self.y, self.z)

class IntVector3:
    '''Vector with 3 Integer Values: X, Y, and Z'''

    def __init__(self, x:int, y:int, z:int) -> None:
        '''
        Instantiate a new Vector with integer X, Y, and Z values.
        
        Parameters
        ----------
        x : int
            The X value.
        y : int
            The Y value.
        z : int
            The Z value.
        
        Raises
        ------
        ValueError
            If any provided arguments are not integers.
        '''
        
        if not isinstance(x, int):
            error:str = f"Value of X ({x}) is not an integer"
            raise ValueError(error)
    
        if not isinstance(y, int):
            error:str = f"Value of Y ({y}) is not an integer"
            raise ValueError(error)
    
        if not isinstance(z, int):
            error:str = f"Value of Z ({z}) is not an integer"
            raise ValueError(error)

        self.x:int = x
        self.y:int = y
        self.z:int = z
    
    def __add__(self, other:Union[IntVector3, np.ndarray]) -> IntVector3:
        if isinstance(other, IntVector3):
            return IntVector3(self.x + other.x, self.y + other.y, self.z + other.z)
        
        if isinstance(other, np.ndarray):
            return IntVector3(self.x + other[0], self.y + other[1], self.z + other[2])
        
        raise TypeError(f"Unsupported addition with type {type(other)}")

    def __hash__(self) -> int:
        return hash(self.to_tuple())
    
    def __eq__(self, other:Union[FloatVector3, IntVector3, np.ndarray]) -> bool:
        if isinstance(other, FloatVector3) or isinstance(other, IntVector3):
            return self.to_tuple() == other.to_tuple()
        
        if isinstance(other, np.ndarray):
            return self.to_tuple() == (other[0], other[1], other[2])

    def __sub__(self, other:Union[IntVector3, np.ndarray]) -> IntVector3:
        if isinstance(other, IntVector3):
            return IntVector3(self.x - other.x, self.y - other.y, self.z - other.z)
        
        if isinstance(other, np.ndarray):
            return IntVector3(self.x - other[0], self.y - other[1], self.z - other[2])
        
        raise TypeError(f"Unsupported subtraction with type {type(other)}")

    def __repr__(self) -> str:
        return f"X: {self.x}, Y: {self.y}, Z: {self.z}"
    
    def cross(self, vector:Union[IntVector3, 'FloatVector3']) -> Union[IntVector3, 'FloatVector3']:
        '''
        Calculate the cross product of two vectors
        
        Parameters
        ----------
        vector : `wame.IntVector3, wame.FloatVector3`
            The other vector to cross with this vector
        
        Returns
        -------
        cross : `wame.IntVector3, wame.FloatVector3`
            The cross product - Will be `wame.IntVector3` if `vector` is a `wame.IntVector3`, else `wame.FloatVector3`
        '''

        result:tuple[float, int, float, int, float, int] = (
            (self.y * vector.z) - (self.z * vector.y),
            (self.z * vector.x) - (self.x * vector.z),
            (self.x * vector.y) - (self.y * vector.x)
        )

        if isinstance(vector, IntVector3):
            if isinstance(result[0], int) and isinstance(result[1], int) and isinstance(result[2], int):
                return IntVector3.from_tuple(result)
        
        return FloatVector3.from_tuple(result)

    @classmethod
    def from_tuple(cls, xyz:tuple[int, int, int]) -> IntVector3:
        '''
        Instantiate a new Vector from a tuple with integer X, Y, and Z values
        
        Parameters
        ----------
        xyz : `tuple[int, int, int]`
            The tuple with the X, Y, and Z values
        
        Raises
        ------
        `ValueError`
            If the provided items in the tuple are not integers
        '''
        
        return cls(xyz[0], xyz[1], xyz[2])
    
    def normalize(self) -> FloatVector3:
        '''
        Calculate the normal of this vector
        
        Returns
        -------
        vector : `wame.FloatVector3`
            This vector normalized
        '''

        length:float = math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

        if length > 0:
            return FloatVector3(self.x / length, self.y / length, self.z / length)

        return FloatVector3(0.0, 0.0, 0.0)

    def to_numpy(self) -> np.ndarray[np.int32]:
        '''
        Converts this instance of `IntVector3` into a numpy array
        
        Returns
        -------
        array : `numpy.ndarray[numpy.int32]`
            Converted x, y, and z values
        '''

        return np.array([self.x, self.y, self.z], dtype=np.int32)

    def to_tuple(self) -> tuple[int, int, int]:
        '''
        Converts this instance of `IntVector3` into a `tuple`
        
        Returns
        -------
        vector : `tuple[int, int, int]`
            Converted x, y, and z values
        '''

        return (self.x, self.y, self.z)