from wame import IntVector2
from wame.error import *

class Area:
    '''Relative Area for Alignment and Positioning'''

    CENTER:int = 0
    '''Center of the object'''

    CENTER_LEFT:int = 1
    '''Center left of the object'''

    CENTER_RIGHT:int = 2
    '''Center right of the object'''
    
    BOTTOM_CENTER:int = 3
    '''Bottom center of the object'''

    BOTTOM_LEFT:int = 4
    '''Bottom left of the object'''
    
    BOTTOM_RIGHT:int = 5
    '''Bottom right of the object'''
    
    TOP_CENTER:int = 6
    '''Top center of the object'''

    TOP_LEFT:int = 7
    '''Top left of the object'''
    
    TOP_RIGHT:int = 8
    '''Top right of the object'''

    def calculate_position(position:IntVector2, area:'Area', size:IntVector2=None) -> IntVector2:
        '''
        Calculate the proper position of an object
        
        Note
        ----
        Use this to place objects on top of a specific coordinate at a designated location on the object
        
        Parameters
        ----------
        position : `wame.IntVector2`
            The X, Y position to place the specific location of the object at
        area : `wame.Area`
            The specific location of the object to place at the position
        size : `wame.IntVector2`
            The width and height of the object - Optional, default `None` - **Required** if `area` is any value other than `Area.TOP_LEFT`
        '''

        if area != Area.TOP_LEFT and size is None:
            error:str = f"The `size` argument must be passed if `area` is any other value than `TOP_LEFT`"
            raise MissingArgumentException(error)

        match area:
            case Area.CENTER:
                return IntVector2(position.x - (size.x // 2), position.y - (size.y // 2))
            case Area.CENTER_LEFT:
                return IntVector2(position.x, position.y - (size.y // 2))
            case Area.CENTER_RIGHT:
                return IntVector2(position.x - size.x, position.y - (size.y // 2))
            case Area.BOTTOM_CENTER:
                return IntVector2(position.x - (size.x // 2), position.y - size.y)
            case Area.BOTTOM_LEFT:
                return IntVector2(position.x, position.y - size.y)
            case Area.BOTTOM_RIGHT:
                return IntVector2(position.x - size.x, position.y - size.y)
            case Area.TOP_CENTER:
                return IntVector2(position.x - (size.x // 2), position.y)
            case Area.TOP_LEFT:
                return IntVector2(position.x, position.y)
            case Area.TOP_RIGHT:
                return IntVector2(position.x - size.x, position.y)