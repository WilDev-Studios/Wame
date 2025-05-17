from __future__ import annotations

from numpy.typing import NDArray
from typing import Iterator, Union

import colorsys
import numpy

__all__ = ("ColorRGB", "ColorRGBA",)

class ColorRGB:
    '''Red, Green, Blue - Color Object.'''

    __slots__ = ("_r", "_g", "_b", "_nr", "_ng", "_nb",)
    _r: int
    _g: int
    _b: int
    _nr: float
    _ng: float
    _nb: float

    def __init__(self, r: int, g: int, b: int) -> None:
        '''
        Create a new RGB color.
        
        Parameters
        ----------
        r : int
            The red color value (`0`-`255`).
        g : int
            The green color value (`0`-`255`).
        b : int
            The blue color value (`0`-`255`).
        
        Raises
        ------
        TypeError
            If `r`, `g`, or `b` are not `int`.
        ValueError
            If `r`, `g`, or `b` are not between `0` and `255`.
        '''

        if not isinstance(r, int) or not isinstance(g, int) or not isinstance(b, int):
            error: str = "R, G, and B values provided must be `int`."
            raise TypeError(error)
        
        if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
            error: str = "R, G, and B values must be between `0` and `255`."
            raise ValueError(error)

        self._r: int = r
        self._g: int = g
        self._b: int = b
        self._nr: float = r / 255
        self._ng: float = g / 255
        self._nb: float = b / 255
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, ColorRGB):
            return (self._r, self._g, self._b) == (other._r, other._g, other._b)
        
        if isinstance(other, (tuple, list, numpy.ndarray)) and len(other) == 3:
            return self._r == other[0] and self._g == other[1] and self._b == other[2]
        
        return False
    
    def __format__(self, spec: str) -> str:
        if spec == "hex":
            return self.hex()
        
        if spec == "hsl":
            return str(self.hsl())
        
        if spec == "hsv":
            return str(self.hsv())
        
        if spec == "int":
            return str(self.int())
        
        if spec == "tuple":
            return str(self.to_tuple())
        
        error: str = f"Unknown format specifier: {spec}"
        raise ValueError(error)

    def __getitem__(self, index: int) -> int:
        if not isinstance(index, int):
            error: str = "Index must be an `int`."
            raise TypeError(error)
        
        if index < 0 or index > 2:
            error: str = "Index must be between `0` and `2`."
            raise ValueError(error)
        
        if index == 0:
            return self._r
        
        if index == 1:
            return self._g
        
        return self._b

    def __hash__(self) -> int: return hash((self._r, self._g, self._b))
    def __iter__(self) -> Iterator[int]: return iter((self._r, self._g, self._b))
    def __len__(self) -> int: return 3
    def __repr__(self) -> str: return f"ColorRGB(r={self._r}, g={self._g}, b={self._b})"

    def __setitem__(self, index: int, value: int) -> None:
        if not isinstance(index, int):
            error: str = "Index must be an `int`."
            raise TypeError(error)
        
        if index < 0 or index > 2:
            error: str = "Index must be between `0` and `2`."
            raise ValueError(error)
        
        if not isinstance(value, int):
            error: str = "Color value must be an `int`."
            raise TypeError(error)
        
        if value < 0 or value > 255:
            error: str = "Color value must be between `0` and `255`."
            raise ValueError(error)
        
        if index == 0:
            self._r = value
            self._nr = value / 255

            return
        
        if index == 1:
            self._g = value
            self._ng = value / 255

            return
        
        self._b = value
        self._nb = value / 255

    def __str__(self) -> str: return f"({self._r}, {self._g}, {self._b})"
    
    @property
    def b(self) -> int:
        '''The blue color value.'''
        return self._b
    
    @b.setter
    def b(self, value: int) -> None:
        if not isinstance(value, int):
            error: str = "Color value must be an `int`."
            raise TypeError(error)
        
        if value < 0 or value > 255:
            error: str = "Color value must be between `0` and `255`."
            raise ValueError(error)
        
        self._b = value
        self._nb = value / 255

    def copy(self) -> ColorRGB:
        '''
        Create a copy of this color.
        
        Returns
        -------
        ColorRGB
            An exact replica of this color.
        '''

        return ColorRGB(self._r, self._g, self._b)

    @classmethod
    def from_iterable(cls, iterable: Union[ColorRGB, tuple[int, int, int], list[int], NDArray[numpy.uint8]]) -> ColorRGB:
        '''
        Create a new RGB color from an iterable object.
        
        Parameters
        ----------
        iterable : ColorRGB | tuple[int, int, int], list[int], NDArray[numpy.uint8]
            The iterable object to create the color from.
        
        Raises
        ------
        TypeError
            If RGB values are not `int`.
        ValueError
            - If provided iterable is not 3 objects in length.
            - If RGB values are not between `0` and `255`.
        '''

        if not hasattr(iterable, "__len__"):
            error: str = "Iterable must support length."
            raise TypeError(error)

        if len(iterable) != 3:
            error: str = "Iterable object must be 3 objects in length."
            raise ValueError(error)

        return cls(*tuple(iterable))

    @property
    def g(self) -> int:
        '''The green color value.'''
        return self._g
    
    @g.setter
    def g(self, value: int) -> None:
        if not isinstance(value, int):
            error: str = "Color value must be an `int`."
            raise TypeError(error)
        
        if value < 0 or value > 255:
            error: str = "Color value must be between `0` and `255`."
            raise ValueError(error)
        
        self._g = value
        self._ng = value / 255
    
    def hex(self) -> str:
        '''Return the hexadecimal representation of this color.'''
        return "#{:02X}{:02X}{:02X}".format(self._r, self._g, self._b)

    def hsl(self) -> tuple[float, float, float]:
        '''Return the HSL representation of this color.'''
        return colorsys.rgb_to_hls(self._nr, self._ng, self._nb)

    def hsv(self) -> tuple[float, float, float]:
        '''Return the HSV representation of this color.'''
        return colorsys.rgb_to_hsv(self._nr, self._ng, self._nb)

    def int(self) -> int:
        '''Return the packed integer representation of this color.'''
        return (self._r << 16) | (self._g << 8) | (self._b)

    @property
    def nb(self) -> float:
        '''The normalized blue color value.'''
        return self._nb
    
    @nb.setter
    def nb(self, value: float) -> None:
        if not isinstance(value, float):
            error: str = "Color value must be a `float`."
            raise TypeError(error)
        
        if value < 0 or value > 1:
            error: str = "Color value must be between `0` and `1`."
            raise ValueError(error)
        
        self._b = int(value * 255)
        self._nb = value

    @property
    def ng(self) -> float:
        '''The normalized green color value.'''
        return self._ng
    
    @ng.setter
    def ng(self, value: float) -> None:
        if not isinstance(value, float):
            error: str = "Color value must be a `float`."
            raise TypeError(error)
        
        if value < 0 or value > 1:
            error: str = "Color value must be between `0` and `1`."
            raise ValueError(error)
        
        self._g = int(value * 255)
        self._ng = value

    def normalized(self) -> tuple[float, float, float]:
        '''
        Return the normalized color values.
        
        Returns
        -------
        tuple[float, float, float]
            The normalized color values.
        '''

        return (self._nr, self._ng, self._nb)

    @property
    def nr(self) -> float:
        '''The normalized red color value.'''
        return self._nr
    
    @nr.setter
    def nr(self, value: float) -> None:
        if not isinstance(value, float):
            error: str = "Color value must be a `float`."
            raise TypeError(error)
        
        if value < 0 or value > 1:
            error: str = "Color value must be between `0` and `1`."
            raise ValueError(error)
        
        self._r = int(value * 255)
        self._nr = value
    
    @property
    def r(self) -> int:
        '''The red color value.'''
        return self._r
    
    @r.setter
    def r(self, value: int) -> None:
        if not isinstance(value, int):
            error: str = "Color value must be an `int`."
            raise TypeError(error)
        
        if value < 0 or value > 255:
            error: str = "Color value must be between `0` and `255`."
            raise ValueError(error)
        
        self._r = value
        self._nr = value / 255
    
    def to_numpy(self) -> NDArray[numpy.uint8]:
        '''
        Return this color as a `NumPy` array.
        
        Returns
        -------
        NDArray[numpy.uint8]
            This color as an array.
        '''

        return numpy.array([self._r, self._g, self._b], numpy.uint8)

    def to_tuple(self) -> tuple[int, int, int]:
        '''
        Return this color as a `tuple`.
        
        Returns
        -------
        tuple[int, int, int]
            This color as a tuple.
        '''

        return (self._r, self._g, self._b)

class ColorRGBA(ColorRGB):
    '''Red, Green, Blue, Alpha - Color Object.'''

    __slots__ = ("_r", "_g", "_b", "_a", "_nr", "_ng", "_nb",)
    _r: int
    _g: int
    _b: int
    _a: float
    _nr: float
    _ng: float
    _nb: float

    def __init__(self, r: int, g: int, b: int, a: float) -> None:
        '''
        Create a new RGBA color.
        
        Parameters
        ----------
        r : int
            The red color value (`0`-`255`).
        g : int
            The green color value (`0`-`255`).
        b : int
            The blue color value (`0`-`255`).
        a : float
            The alpha/transparency value (`0`-`1`).
        
        Raises
        ------
        TypeError
            - If `r`, `g`, or `b` are not `int`.
            - If `a` is not `float` or `int`.
        ValueError
            - If `r`, `g`, or `b` are not between `0` and `255`.
            - If `a` is not between `0` and `1`.
        '''
        
        if not isinstance(a, (float, int)):
            error: str = "`a` value provided must be `float` or `int`."
            raise TypeError(error)
        
        if a < 0 or a > 1:
            error: str = "`a` value must be between `0` and `1`."
            raise ValueError(error)

        super().__init__(r, g, b)

        self._a: float = a
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, ColorRGBA):
            return (self._r, self._g, self._b, self._a) == (other._r, other._g, other._b, other._a)
        
        if isinstance(other, (tuple, list, numpy.ndarray)) and len(other) == 4:
            return self._r == other[0] and self._g == other[1] and self._b == other[2] and self._a == other[3]
        
        return False
    
    def __format__(self, spec: str) -> str:
        if spec == "hex":
            return self.hex()
        
        if spec == "hsla":
            return str(self.hsla())
        
        if spec == "hsva":
            return str(self.hsva())
        
        if spec == "int":
            return str(self.int())
        
        if spec == "tuple":
            return str(self.to_tuple())
        
        error: str = f"Unknown format specifier: {spec}"
        raise ValueError(error)

    def __getitem__(self, index: int) -> Union[int, float]:
        if not isinstance(index, int):
            error: str = "Index must be an `int`."
            raise TypeError(error)
        
        if index < 0 or index > 3:
            error: str = "Index must be between `0` and `3`."
            raise ValueError(error)
        
        if index == 0:
            return self._r
        
        if index == 1:
            return self._g
        
        if index == 2:
            return self._b

        return self._a

    def __hash__(self) -> int: return hash((self._r, self._g, self._b, self._a))
    def __iter__(self) -> Iterator[Union[int, float]]: return iter((self._r, self._g, self._b, self._a))
    def __len__(self) -> int: return 4
    def __repr__(self) -> str: return f"ColorRGBA(r={self._r}, g={self._g}, b={self._b}, a={self._a})"

    def __setitem__(self, index: int, value: Union[int, float]) -> None:
        if not isinstance(index, int):
            error: str = "Index must be an `int`."
            raise TypeError(error)
        
        if index < 0 or index > 3:
            error: str = "Index must be between `0` and `3`."
            raise ValueError(error)
        
        if index != 3:
            if not isinstance(value, int):
                error: str = "Color value must be an `int`."
                raise TypeError(error)
            
            if value < 0 or value > 255:
                error: str = "Color value must be between `0` and `255`."
                raise ValueError(error)
        else:
            if not isinstance(value, (float, int)):
                error: str = "Alpha value must be an `int` or `float`."
                raise TypeError(error)
            
            if value < 0 or value > 1:
                error: str = "Alpha value must be between `0` and `1`."
                raise ValueError(error)
        
        if index == 0:
            self._r = value
            self._nr = value / 255

            return
        
        if index == 1:
            self._g = value
            self._ng = value / 255

            return
        
        if index == 2:
            self._b = value
            self._nb = value / 255

            return
        
        self._a = value

    def __str__(self) -> str: return f"({self._r}, {self._g}, {self._b}, {self._a})"
    
    @property
    def a(self) -> float:
        '''The alpha/transparency value.'''
        return self._a
    
    @a.setter
    def a(self, value: Union[int, float]) -> None:
        if not isinstance(value, (float, int)):
            error: str = "Alpha value must be an `int` or `float`."
            raise TypeError(error)
        
        if value < 0 or value > 1:
            error: str = "Alpha value must be between `0` and `1`."
            raise ValueError(error)
        
        self._a = value

    def copy(self) -> ColorRGBA:
        '''
        Create a copy of this color.
        
        Returns
        -------
        ColorRGBA
            An exact replica of this color.
        '''

        return ColorRGBA(self._r, self._g, self._b, self._a)

    @classmethod
    def from_iterable(cls, iterable: Union[ColorRGBA, tuple[int, int, int, float], list[int, float], NDArray[Union[numpy.uint8, numpy.float16]]]) -> ColorRGBA:
        '''
        Create a new RGBA color from an iterable object.
        
        Parameters
        ----------
        iterable : ColorRGBA | tuple[int, int, int, float], list[int, float], NDArray[numpy.uint8 | numpy.float16]
            The iterable object to create the color from.
        
        Raises
        ------
        TypeError
            - If RGB values are not `int`.
            - If alpha value is not `int` or `float`.
        ValueError
            - If provided iterable is not 3-4 objects in length.
            - If RGB values are not between `0` and `255`.
            - If alpha value is not between `0` and `1`.
        '''

        if not hasattr(iterable, "__len__"):
            error: str = "Iterable must support length."
            raise TypeError(error)

        length: int = len(iterable)

        if length not in [3, 4]:
            error: str = "Iterable object must be 3-4 objects in length."
            raise ValueError(error)
        
        iterable: tuple = tuple(iterable)

        if length == 3:
            iterable = (*iterable, 1.0)

        return cls(*iterable)
    
    def hex(self) -> str:
        '''Return the hexadecimal representation of this color.'''
        return "#{:02X}{:02X}{:02X}{:02X}".format(self._r, self._g, self._b, int(round(self._a * 255)))

    def hsla(self) -> tuple[float, float, float, float]:
        '''Return the HSLA representation of this color.'''
        h, l, s = colorsys.rgb_to_hls(self._nr, self._ng, self._nb)
        return (h, s, l, self._a)

    def hsva(self) -> tuple[float, float, float, float]:
        '''Return the HSV representation of this color.'''
        h, s, v = colorsys.rgb_to_hsv(self._nr, self._ng, self._nb)
        return (h, s, v, self._a)

    def int(self) -> int:
        '''Return the packed integer representation of this color.'''
        return (round(self._a * 255) << 24) | (self._r << 16) | (self._g << 8) | (self._b)

    def normalized(self) -> tuple[float, float, float, float]:
        '''
        Return the normalized color values.
        
        Returns
        -------
        tuple[float, float, float, float]
            The normalized color values.
        '''

        return (self._nr, self._ng, self._nb, self._a)

    def to_numpy(self) -> NDArray[numpy.float16]:
        '''
        Return this color as a `NumPy` array.
        
        Returns
        -------
        NDArray[numpy.float16]
            This color as an array.
        '''

        return numpy.array([self._r, self._g, self._b, self._a], numpy.float16)

    def to_tuple(self) -> tuple[int, int, int, float]:
        '''
        Return this color as a `tuple`.
        
        Returns
        -------
        tuple[int, int, int, float]
            This color as a tuple.
        '''

        return (self._r, self._g, self._b, self._a)