from __future__ import annotations

from typing import NoReturn

class ColorRGB:
    '''RGB Color Object'''

    def __init__(self, r:int, g:int, b:int) -> None:
        '''
        Create a RGB color
        
        Parameters
        ----------
        r : int
            The R (red) value (0-255)
        g : int
            The G (green) value (0-255)
        b : int
            The B (blue) value (0-255)
        
        Raises
        ------
        TypeError
            If any color value is not an integer
        ValueError
            If any color value is less than `0` or more than `255`
        '''

        def color_not_int(color:str) -> NoReturn:
            error:str = f"RGB color value {color} must be an integer"
            raise TypeError(error)
    
        def color_invalid_range(color:str, value:int) -> NoReturn:
            error:str = f"RGB color value {color} value must be between 0-255, not {value}"
            raise ValueError(error)

        if not isinstance(r, int):
            color_not_int('R')
        
        if not isinstance(g, int):
            color_not_int('G')
        
        if not isinstance(b, int):
            color_not_int('B')
        
        if r > 255 or r < 0:
            color_invalid_range('R', r)
        
        if g > 255 or g < 0:
            color_invalid_range('G', g)
        
        if b > 255 or b < 0:
            color_invalid_range('B', b)

        self.r:int = r
        self.g:int = g
        self.b:int = b

        self.nr:float = r / 255
        self.ng:float = g / 255
        self.nb:float = b / 255

    def __str__(self) -> str:
        return f"R: {self.r}, G: {self.g}, B: {self.b}"

    @classmethod
    def from_tuple(cls, rgb:tuple[int, int, int]) -> ColorRGB:
        '''
        Create a RGB color from a tuple
        
        Parameters
        ----------
        rgb : tuple[int, int, int]
            The R, G, and B values
        
        Returns
        -------
        color : wame.color.rgb.ColorRGB
            New `ColorRGB` object from the tuple
        
        Raises
        ------
        TypeError
            If the provided `rgb` object is not a tuple
        ValueError
            If there's not 3 values within the provided tuple
        '''

        if not isinstance(rgb, tuple):
            error: str = "RGB object must be a tuple"
            raise TypeError(error)

        if len(rgb) != 3:
            error:str = "RGB tuple must contain 3 values"
            raise ValueError(error)

        return cls(rgb[0], rgb[1], rgb[2])
    
    def normalized(self) -> tuple[float, float, float]:
        '''
        Normalize this color into RGB values `0-1`, not `0-255`
        
        Returns
        -------
        rgb : tuple[float, float, float]
            The normalized RGB values
        '''

        return (self.nr, self.ng, self.nb)

    def to_tuple(self) -> tuple[int, int, int]:
        '''
        Convert this object to a tuple
        
        Returns
        -------
        color : tuple[int, int, int]
            The R, G, and B values in a tuple
        '''

        return (self.r, self.g, self.b)

class ColorRGBA(ColorRGB):
    '''RGBA Color Object'''

    def __init__(self, r:int, g:int, b:int, a:float) -> None:
        '''
        Create a RGB color
        
        Parameters
        ----------
        r : int
            The R (red) value (0-255)
        g : int
            The G (green) value (0-255)
        b : int
            The B (blue) value (0-255)
        a : int
            The A (alpha) value (0-1)
        
        Raises
        ------
        TypeError
            If the provided `a` argument is not an `int` or `float`
        ValueError
            If the provided `a` argument is not between `0` and `1`
        '''

        super().__init__(r, g, b)
        
        if not isinstance(a, (int, float)):
            error: str = f"RGBA color value A must be either an integer or float"
            raise TypeError(error)

        if a > 1 or a < 0:
            error:str = f"RGBA color value A value must be between 0-1, not {a}"
            raise ValueError(error)

        self.a:float = a
    
    def __str__(self) -> str:
        return f"R: {self.r}, G: {self.g}, B: {self.b}, A: {self.a}"

    @classmethod
    def from_tuple(cls, rgba:tuple[int, int, int, float]) -> ColorRGBA:
        '''
        Create a RGBA color from a tuple
        
        Parameters
        ----------
        rgba : tuple[int, int, int, float]
            The R, G, B, and (optionally) A values
        
        Returns
        -------
        color : wame.color.rgb.ColorRGBA
            New `ColorRGBA` object from the tuple - If `A` is omitted, default is `1.0`
        
        Raises
        ------
        TypeError
            If the provided `rgba` object isn't a `tuple`
        ValueError
            If the provided `tuple` doesn't contain 3-4 characters (RGB or RGBA)
        '''

        if not isinstance(rgba, tuple):
            error: str = "RGBA object must be a tuple"
            raise TypeError(error)

        if len(rgba) not in [3, 4]:
            error:str = "RGBA object must contain 3-4 values only"
            raise ValueError(error)

        try:
            return ColorRGBA(rgba[0], rgba[1], rgba[2], rgba[3])
        except IndexError:
            return ColorRGBA(rgba[0], rgba[1], rgba[2], 1.0)

    def normalized(self) -> tuple[float, float, float, float]:
        '''
        Normalize this color into RGBA values `0-1`, not `0-255`
        
        Returns
        -------
        rgba : tuple[float, float, float, float]
            The normalized RGBA values
        '''

        return (self.nr, self.ng, self.nb, self.a)

    def to_tuple(self) -> tuple[int, int, int, float]:
        '''
        Convert this object to a tuple
        
        Returns
        -------
        color : tuple[int, int, int, float]
            The R, G, B, and A values in a tuple
        '''

        return (self.r, self.g, self.b, self.a)