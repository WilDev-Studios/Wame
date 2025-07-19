import math
import pygame
import typing

class Easing:
    '''Animation Easing Functions.'''

    @staticmethod
    def BOUNCE_IN(t: float) -> float:
        '''Bounce Easing In.'''
        return 1 - Easing.BOUNCE_OUT(1 - t)
    
    @staticmethod
    def BOUNCE_OUT(t: float) -> float:
        '''Bounce Easing In.'''
        
        if t < 1 / 2.75:
            return 7.5625 * t * t
        
        if t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        
        if t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375
    
    @staticmethod
    def BOUNCE_IN_OUT(t: float) -> float:
        '''Bounce Easing In/Out.'''
        return (1 - Easing.BOUNCE_OUT(1 - 2 * t)) / 2 if t < 0.5 else (1 + Easing.BOUNCE_OUT(2 * t - 1)) / 2

    @staticmethod
    def CUBIC_IN(t: float) -> float:
        '''Cubic Easing In.'''
        return t ** 3
    
    @staticmethod
    def CUBIC_OUT(t: float) -> float:
        '''Cubic Easing Out.'''
        return (t - 1) ** 3 + 1
    
    @staticmethod
    def CUBIC_IN_OUT(t: float) -> float:
        '''Cubic Easing In/Out.'''
        return 4 * t ** 3 if t < 0.5 else (t - 1) * (2 * t - 2) ** 2 + 1
    
    @staticmethod
    def LINEAR(t: float) -> float:
        '''Linear Easing.'''
        return t

    @staticmethod
    def QUAD_IN(t: float) -> float:
        '''Quadratic Easing In.'''
        return t * t

    @staticmethod
    def QUAD_OUT(t: float) -> float:
        '''Quadratic Easing Out.'''
        return t * (2 - t)
    
    @staticmethod
    def QUAD_IN_OUT(t : float) -> float:
        '''Quadratic Easing In/Out.'''
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

    @staticmethod
    def QUARTIC_IN(t: float) -> float:
        '''Quartic Easing In.'''
        return t ** 4
    
    @staticmethod
    def QUARTIC_OUT(t: float) -> float:
        '''Quartic Easing Out.'''
        return 1 - (t - 1) ** 4
    
    @staticmethod
    def QUARTIC_IN_OUT(t: float) -> float:
        '''Quartic Easing In/Out.'''
        return 8 * t ** 4 if t < 0.5 else 1 - 8 * (t - 1) ** 4
    
    @staticmethod
    def QUINTIC_IN(t: float) -> float:
        '''Quintic Easing In.'''
        return t ** 5
    
    @staticmethod
    def QUINTIC_OUT(t: float) -> float:
        '''Quintic Easing Out.'''
        return 1 + (t - 1) ** 5
    
    @staticmethod
    def QUINTIC_IN_OUT(t: float) -> float:
        '''Quintic Easing In/Out.'''
        return 16 * t ** 5 if t < 0.5 else 1 + 16 * (t - 1) ** 5
    
    @staticmethod
    def SINE_IN(t: float) -> float:
        '''Sine Easing In.'''
        return 1 - math.cos((t * math.pi) / 2)
    
    @staticmethod
    def SINE_OUT(t: float) -> float:
        '''Sine Easing Out.'''
        return math.sin((t * math.pi) / 2)
    
    @staticmethod
    def SINE_IN_OUT(t: float) -> float:
        '''Sine Easing In/Out.'''
        return -(math.cos(math.pi * t) - 1) / 2

class Tween:
    '''Collection of tween utility methods.'''

    @staticmethod
    def calculate_progress(started_at: int, duration: float, easing: typing.Callable[[float], float]) -> float:
        '''
        Calculate the progress of an ongoing tween, represented as a percentage.
        
        Parameters
        ----------
        started_at : int
            The starting tick provided by `pygame`.
        duration : float
            The desired total time for the tween to take place in seconds.
        easing : typing.Callable[[float], float]
            The desired easing function/method to use - Usually an `Easing` child method.
        
        Returns
        -------
        float
            The percentage progress of this tween.
        '''
        
        current_time: int = pygame.time.get_ticks()
        elapsed: float = (current_time - started_at) / 1000.0

        return min (1.0, max(0.0, easing(min(elapsed / duration, 1.0))))