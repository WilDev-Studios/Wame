from __future__ import annotations

from typing import Union

import numpy as np

class FloatVector2:
    '''Vector with 2 Float Values: X and Y'''

    def __init__(self, x:Union[float, int], y:Union[float, int]) -> None:
        '''
        Instantiate a new Vector with float X and Y values
        
        Parameters
        ----------
        x : float
            The X value
        y : float
            The Y value
        
        Raises
        ------
        ValueError
            If any provided arguments are not `float` or `int`
        '''

        if not isinstance(x, (float, int)) or not isinstance(y, (float, int)):
            error:str = "XY values must be `float` or `int`"
            raise ValueError(error)
        
        if isinstance(x, int):
            x = float(x)
        
        if isinstance(y, int):
            y = float(y)

        self.x:float = x
        self.y:float = y
    
    def __add__(self, other:Union[FloatVector2, IntVector2, np.ndarray]) -> FloatVector2:
        if isinstance(other, FloatVector2) or isinstance(other, IntVector2):
            return FloatVector2(self.x + other.x, self.y + other.y)
        
        if isinstance(other, np.ndarray):
            return FloatVector2(self.x + other[0], self.y + other[1])
        
        raise TypeError(f"Unsupported addition with type {type(other)}")
    
    def __eq__(self, other:Union[FloatVector2, IntVector2, np.ndarray]) -> bool:
        if isinstance(other, FloatVector2) or isinstance(other, IntVector2):
            return self.to_tuple() == other.to_tuple()
        
        if isinstance(other, np.ndarray):
            return self.to_tuple() == (other[0], other[1])

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __sub__(self, other:Union[FloatVector2, IntVector2, np.ndarray]) -> FloatVector2:
        if isinstance(other, FloatVector2) or isinstance(other, IntVector2):
            return FloatVector2(self.x - other.x, self.y - other.y)
        
        if isinstance(other, np.ndarray):
            return FloatVector2(self.x - other[0], self.y - other[1])
        
        raise TypeError(f"Unsupported subtraction with type {type(other)}")

    def __repr__(self) -> str:
        return f"X: {self.x}, Y: {self.y}"
    
    @classmethod
    def from_tuple(cls, xy:tuple[Union[float, int], Union[float, int]]) -> FloatVector2:
        '''
        Instantiate a new Vector from a tuple with float X and Y values
        
        Parameters
        ----------
        xy : tuple[float | int, float | int]
            The tuple with the X and Y values
        
        Raises
        ------
        ValueError
            - If the provided items in the tuple are not `float` or `int`
            - If the provided tuple does not contain 2 values
        '''

        if len(xy) != 2:
            error:str = "XY tuple can only contain 2 values"
            raise ValueError(error)
        
        return cls(xy[0], xy[1])
    
    def to_numpy(self) -> np.ndarray[np.int32]:
        '''
        Converts this instance of `FloatVector2` into a numpy array
        
        Returns
        -------
        array : numpy.ndarray[numpy.float32]
            Converted x and Y values
        '''

        return np.array([self.x, self.y], dtype=np.float32)

    def to_tuple(self) -> tuple[float, float]:
        '''
        Converts this instance of `FloatVector2` into a `tuple`
        
        Returns
        -------
        vector : tuple[float, float]
            Converted x and y values
        '''

        return (self.x, self.y)

class IntVector2:
    '''Vector with 2 Integer Values: X and Y'''

    def __init__(self, x:int, y:int) -> None:
        '''
        Instantiate a new Vector with integer X and Y values
        
        Parameters
        ----------
        x : int
            The X value
        y : int
            The Y value
        
        Raises
        ------
        ValueError
            If any provided arguments are not integers
        '''
        
        if not isinstance(x, int):
            error:str = f"Value of X ({x}) is not an integer"
            raise ValueError(error)
    
        if not isinstance(y, int):
            error:str = f"Value of Y ({y}) is not an integer"
            raise ValueError(error)

        self.x:int = x
        self.y:int = y
    
    def __add__(self, other:Union[IntVector2, np.ndarray]) -> IntVector2:
        if isinstance(other, IntVector2):
            return IntVector2(self.x + other.x, self.y + other.y)
        
        if isinstance(other, np.ndarray):
            return IntVector2(self.x + other[0], self.y + other[1])
        
        raise TypeError(f"Unsupported addition with type {type(other)}")
    
    def __eq__(self, other:Union[FloatVector2, IntVector2, np.ndarray]) -> bool:
        if isinstance(other, FloatVector2) or isinstance(other, IntVector2):
            return self.to_tuple() == other.to_tuple()
        
        if isinstance(other, np.ndarray):
            return self.to_tuple() == (other[0], other[1])

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __sub__(self, other:Union[IntVector2, np.ndarray]) -> IntVector2:
        if isinstance(other, IntVector2):
            return IntVector2(self.x - other.x, self.y - other.y)
        
        if isinstance(other, np.ndarray):
            return IntVector2(self.x - other[0], self.y - other[1])
        
        raise TypeError(f"Unsupported subtraction with type {type(other)}")

    def __repr__(self) -> str:
        return f"X: {self.x}, Y: {self.y}"

    @classmethod
    def from_tuple(cls, xy:tuple[int, int]) -> IntVector2:
        '''
        Instantiate a new Vector from a tuple with integer X and Y values
        
        Parameters
        ----------
        xy : tuple[int, int]
            The tuple with the X and Y values
        
        Raises
        ------
        ValueError
            - If the provided items in the tuple are not integers
            - If the provided tuple does not contain 2 values
        '''

        if len(xy) != 2:
            error:str = "XY tuple must contain 2 values"
            raise ValueError(error)
        
        return cls(xy[0], xy[1])
    
    def to_numpy(self) -> np.ndarray[np.int32]:
        '''
        Converts this instance of `IntVector2` into a numpy array
        
        Returns
        -------
        array : numpy.ndarray[numpy.int32]
            Converted x and y values
        '''

        return np.array([self.x, self.y], dtype=np.int32)

    def to_tuple(self) -> tuple[int, int]:
        '''
        Converts this instance of `IntVector2` into a `tuple`
        
        Returns
        -------
        vector : tuple[int, int]
            Converted x and y values
        '''

        return (self.x, self.y)