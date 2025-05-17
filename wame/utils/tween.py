from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from dataclasses import dataclass
from wame.color.rgb import ColorRGB, ColorRGBA

import math
import pygame

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

@dataclass(frozen=True, slots=True)
class TweenRect:
    start: pygame.Rect
    end: pygame.Rect
    target: pygame.Rect
    duration: float
    started_at: int
    easing: Callable[[float], float]

@dataclass(frozen=True, slots=True)
class TweenRGB:
    start: ColorRGB
    end: ColorRGB
    target: ColorRGB
    duration: float
    started_at: int
    easing: Callable[[float], float]

@dataclass(frozen=True, slots=True)
class TweenRGBA:
    start: ColorRGBA
    end: ColorRGBA
    target: ColorRGBA
    duration: float
    started_at: int
    easing: Callable[[float], float]

class Tween:
    '''Animate Objects Easily.'''

    __slots__ = ("_scene", "_tween_rects", "_tween_rgbs", "_tween_rgbas",)

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

        self._tween_rects: list[TweenRect] = []
        self._tween_rgbs:  list[TweenRGB] =  []
        self._tween_rgbas: list[TweenRGBA] = []

    def _apply_rect(self, tween_rect: TweenRect) -> bool:
        progress = self._calculate_progress(tween_rect.started_at, tween_rect.duration, tween_rect.easing)
        start, end, target = tween_rect.start, tween_rect.end, tween_rect.target
        r: Callable[[float], int] = round

        target.topleft = (
            r(start.x + (end.x - start.x) * progress),
            r(start.y + (end.y - start.y) * progress)
        )
        target.size = (
            r(start.width + (end.width - start.width) * progress),
            r(start.height + (end.height - start.height) * progress)
        )

        return progress >= 1.0
    
    def _apply_rgb(self, tween_rgb: TweenRGB) -> bool:
        progress: float = self._calculate_progress(tween_rgb.started_at, tween_rgb.duration, tween_rgb.easing)
        start, end, target = tween_rgb.start, tween_rgb.end, tween_rgb.target
        r: Callable[[float], int] = round

        target.r = r(start.r + (end.r - start.r) * progress)
        target.g = r(start.g + (end.g - start.g) * progress)
        target.b = r(start.b + (end.b - start.b) * progress)

        return progress >= 1.0

    def _apply_rgba(self, tween_rgba: TweenRGBA) -> bool:
        progress: float = self._calculate_progress(tween_rgba.started_at, tween_rgba.duration, tween_rgba.easing)
        start, end, target = tween_rgba.start, tween_rgba.end, tween_rgba.target
        r: Callable[[float], int] = round

        target.r = r(start.r + (end.r - start.r) * progress)
        target.g = r(start.g + (end.g - start.g) * progress)
        target.b = r(start.b + (end.b - start.b) * progress)
        target.a = tween_rgba.start.a + (tween_rgba.end.a - tween_rgba.start.a) * progress

        return progress >= 1.0

    @staticmethod
    def _calculate_progress(started_at: int, duration: float, easing_func: Callable[[float], float]) -> float:
        current_time: int = pygame.time.get_ticks()
        elapsed: float = (current_time - started_at) / 1000.0
        
        return min(1.0, max(0.0, easing_func(min(elapsed / duration, 1.0))))

    def _update(self) -> None:
        rects, rgbs, rgbas = self._tween_rects, self._tween_rgbs, self._tween_rgbas
        i = j = k = 0

        for tween in rects:
            if self._apply_rect(tween):
                self._scene.on_tweened(tween.target)
            else:
                rects[i] = tween
                i += 1
        del rects[i:]

        for tween in rgbs:
            if self._apply_rgb(tween):
                self._scene.on_tweened(tween.target)
            else:
                rgbs[j] = tween
                j += 1
        del rgbs[j:]

        for tween in rgbas:
            if self._apply_rgba(tween):
                self._scene.on_tweened(tween.target)
            else:
                rgbas[k] = tween
                k += 1
        del rgbas[k:]

    def color_rgb(self, original: ColorRGB, final: ColorRGB, duration: float, easing: Callable[[float], float]=Easing.LINEAR) -> None:
        '''
        Tween/Animate an original `ColorRGB` to a final `ColorRGB` over a period of time.
        
        Parameters
        ----------
        original : ColorRGB
            The original color to tween.
        final : ColorRGB
            The final color to tween the original to.
        duration : float
            How long this tween/animation should take in seconds.
        easing : typing.Callable[[float], float]
            The easing function to use when animating.
        
        Raises
        ------
        TypeError
            - If the provided original is not a `ColorRGB`.
            - If the provided final is not a `ColorRGB`.
            - If the provided duration is not a `float` or `int`.
        ValueError
            If the provided duration is not greater than `0`.
        '''

        if not type(original) is ColorRGB:
            error: str = "Parameter `original` must be a `ColorRGB`."
            raise TypeError(error)
        
        if not type(final) is ColorRGB:
            error: str = "Parameter `final` must be a `ColorRGB`."
            raise TypeError(error)
        
        if not isinstance(duration, (float, int)):
            error: str = "Parameter `duration` must be a `float` or `int`."
            raise TypeError(error)
        
        if duration <= 0:
            error: str = "Parameter `duration` must be greater than `0`."
            raise ValueError(error)
        
        self._tween_rgbs.append(TweenRGB(original.copy(), final, original, duration, pygame.time.get_ticks(), easing))

    def color_rgba(self, original: ColorRGBA, final: ColorRGBA, duration: float, easing: Callable[[float], float]=Easing.LINEAR) -> None:
        '''
        Tween/Animate an original `ColorRGBA` to a final `ColorRGBA` over a period of time.
        
        Parameters
        ----------
        original : ColorRGBA
            The original color to tween.
        final : ColorRGBA
            The final color to tween the original to.
        duration : float
            How long this tween/animation should take in seconds.
        easing : typing.Callable[[float], float]
            The easing function to use when animating.
        
        Raises
        ------
        TypeError
            - If the provided original is not a `ColorRGBA`.
            - If the provided final is not a `ColorRGBA`.
            - If the provided duration is not a `float` or `int`.
        ValueError
            If the provided duration is not greater than `0`.
        '''

        if not type(original) is ColorRGBA:
            error: str = "Parameter `original` must be a `ColorRGBA`."
            raise TypeError(error)
        
        if not type(final) is ColorRGBA:
            error: str = "Parameter `final` must be a `ColorRGBA`."
            raise TypeError(error)
        
        if not isinstance(duration, (float, int)):
            error: str = "Parameter `duration` must be a `float` or `int`."
            raise TypeError(error)
        
        if duration <= 0:
            error: str = "Parameter `duration` must be greater than `0`."
            raise ValueError(error)
        
        self._tween_rgbs.append(TweenRGBA(original.copy(), final, original, duration, pygame.time.get_ticks(), easing))

    def rect(self, original: pygame.Rect, destination: pygame.Rect, duration: float, easing: Callable[[float], float]=Easing.LINEAR) -> None:
        '''
        Tween/Animate an original `pygame.Rect` to a destination `pygame.Rect` over a period of time.
        
        Parameters
        ----------
        original : pygame.Rect
            The original rectangle to tween.
        destination : pygame.Rect
            The destination rectangle to tween the original to.
        duration : float
            How long this tween/animation should take in seconds.
        easing : typing.Callable[[float], float]
            The easing function to use when animating.
        
        Raises
        ------
        TypeError
            - If the provided original is not a `pygame.Rect`.
            - If the provided destination is not a `pygame.Rect`.
            - If the provided duration is not a `float` or `int`.
        ValueError
            If the provided duration is not greater than `0`.
        '''

        if not isinstance(original, pygame.Rect):
            error: str = "Parameter `original` must be a `pygame.Rect`."
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
    
        self._tween_rects.append(TweenRect(original.copy(), destination, original, duration, pygame.time.get_ticks(), easing))