from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

import math
import pygame

class Easing:
    '''Animation Easing Functions.'''
    
    @staticmethod
    def BOUNCE_IN(t: float) -> float:
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
    '''Animate Objects Easily.'''

    def __init__(self, scene: 'Scene') -> None:
        '''
        Instantiate this object and hook to a parent `Scene`.
        
        Parameters
        ----------
        scene : Scene
            The parent scene to hook this instance to.
        
        Warning
        -------
        This is an internal instantiation and should not be created elsewhere.
        '''

        self._scene: 'Scene' = scene
        self._scene._events_update.add(self._update)

        # START, END, TARGET, DURATION, STARTED_AT, EASING_FUNC
        self._tween_rects: list[tuple[pygame.Rect, pygame.Rect, pygame.Rect, float, int, Callable[[float], float]]] = []

    def _apply_rect(self, tween_rect:tuple[pygame.Rect, pygame.Rect, pygame.Rect, float, int, Callable[[float], float]]) -> bool:
        start, end, target, duration, started_at, easing_func = tween_rect
        progress = self._calculate_progress(started_at, duration, easing_func)

        target.topleft = (
            round(start.x + (end.x - start.x) * progress),
            round(start.y + (end.y - start.y) * progress)
        )
        target.size = (
            round(start.width + (end.width - start.width) * progress),
            round(start.height + (end.height - start.height) * progress)
        )

        return progress >= 1.0

    @staticmethod
    def _calculate_progress(started_at: int, duration: float, easing_func: Callable[[float], float]) -> float:
        current_time: int = pygame.time.get_ticks()
        elapsed: float = (current_time - started_at) / 1000.0
        
        return easing_func(min(elapsed / duration, 1.0))

    def _update(self) -> None:
        finished: list = []
        new_tween_rects: list[pygame.Rect, pygame.Rect, pygame.Rect, float, int, Callable[[float], float]] = []

        for tween_rect in self._tween_rects:
            if self._apply_rect(tween_rect):
                finished.append(tween_rect[2]) # Finished, return original instance
            else:
                new_tween_rects.append(tween_rect) # Re-cycle back into system to finish
        
        self._tween_rects = new_tween_rects

        for object_ in finished:
            self._scene.on_tweened(object_)

    def rect(self, origin: pygame.Rect, destination: pygame.Rect, duration: float, easing: Callable[[float], float] = Easing.LINEAR) -> None:
        '''
        Tween/Animate an origin `pygame.Rect` to a destination `pygame.Rect` over a period of time.
        
        Parameters
        ----------
        origin : pygame.Rect
            The origin rectangle to tween.
        destination : pygame.Rect
            The destination rectangle to tween the origin to.
        duration : float
            How long this tween/animation should take.
        easing : typing.Callable[[float], float]
            The easing function to use when animating.
        
        Raises
        ------
        TypeError
            - If the provided origin is not a `pygame.Rect`.
            - If the provided destination is not a `pygame.Rect`.
            - If the provided duration is not a `float` or `int`.
        ValueError
            If the provided duration is not greater than `0`.
        '''

        if not isinstance(origin, pygame.Rect):
            error: str = "Parameter `origin` must be a `pygame.Rect`."
            raise TypeError(error)
        
        if not isinstance(destination, pygame.Rect):
            error: str = "Parameter `destination` must be a `pygame.Rect`."
            raise TypeError(error)
        
        if not isinstance(duration, (float, int)):
            error: str = "Parameter `duration` must be a `float` or `int`."
            raise TypeError(error)
        
        if duration <= 0:
            error: str = "Parameter `duration` must be greater than `0`."
            raise ValueError(error)
    
        self._tween_rects.append((origin.copy(), destination, origin, duration, pygame.time.get_ticks(), easing))