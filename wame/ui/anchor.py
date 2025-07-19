from __future__ import annotations

from enum import auto, IntEnum
from wame.vector.xy import IntVector2

__all__ = ("Anchor",)

class Anchor(IntEnum):
    '''Relative position of a UI element from a specific point.'''

    BOTTOM: int = auto()
    '''Position is based on the bottom area of this element.'''

    BOTTOM_LEFT: int = auto()
    '''Position is based on the bottom-left area of this element.'''

    BOTTOM_RIGHT: int = auto()
    '''Position is based on the bottom-right area of this element.'''

    CENTER: int = auto()
    '''Position is based on the center area of this element.'''

    LEFT: int = auto()
    '''Position is based on the left area of this element.'''

    RIGHT: int = auto()
    '''Position is based on the right area of this element.'''

    TOP: int = auto()
    '''Position is based on the top area of this element.'''

    TOP_LEFT: int = auto()
    '''Position is based on the top-left area of this element.'''

    TOP_RIGHT: int = auto()
    '''Position is based on the top-right area of this element.'''

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    @staticmethod
    def calculate_position(position: IntVector2, size: IntVector2, anchor: Anchor) -> IntVector2:
        '''
        Calculate the relative position of an element based on an anchor point.
        
        Parameters
        ----------
        position : IntVector2
            The X, Y relative position.
        size : IntVector2
            The X, Y relative size.
        anchor : Anchor
            The anchor point to calculate to.
        
        Returns
        -------
        IntVector2
            The calculated position relative to the anchor point.
        
        Raises
        ------
        TypeError
            - Parameters `position` and `size` aren't `IntVector2`.
            - Parameter `anchor` isn't an `Anchor`.
        '''

        if not isinstance(position, IntVector2) or not isinstance(size, IntVector2):
            error: str = "Position and size must be `IntVector2`"
            raise TypeError(error)
        
        if not isinstance(anchor, Anchor):
            error: str = "Anchor must be an `Anchor` object"
            raise TypeError(error)

        if anchor == Anchor.TOP_LEFT:
            return IntVector2(
                position.x,
                position.y
            )
        elif anchor == Anchor.TOP:
            return IntVector2(
                position.x - (size.x // 2),
                position.y
            )
        elif anchor == Anchor.TOP_RIGHT:
            return IntVector2(
                position.x - size.x,
                position.y
            )
        elif anchor == Anchor.LEFT:
            return IntVector2(
                position.x,
                position.y - (size.y // 2)
            )
        elif anchor == Anchor.CENTER:
            return IntVector2(
                position.x - (size.x // 2),
                position.y - (size.y // 2)
            )
        elif anchor == Anchor.RIGHT:
            return IntVector2(
                position.x - size.x,
                position.y - (size.y // 2)
            )
        elif anchor == Anchor.BOTTOM_LEFT:
            return IntVector2(
                position.x,
                position.y - size.y
            )
        elif anchor == Anchor.BOTTOM:
            return IntVector2(
                position.x - (size.x // 2),
                position.y - size.y
            )
        elif anchor == Anchor.BOTTOM_RIGHT:
            return IntVector2(
                position.x - size.x,
                position.y - size.y
            )