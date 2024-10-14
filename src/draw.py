from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from OpenGL.GL import *

import pygame
import wame

def setup_2D_projection(scene:'Scene') -> None:
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, scene.engine.screen.get_width(), scene.engine.screen.get_height(), 0, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def setup_3D_projection() -> None:
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

def draw_line(scene:'Scene', surface:pygame.Surface, color:wame.IntVector3, start:wame.IntVector2, end:wame.IntVector2) -> None:
    '''
    Draws a line from `start` to `end`
    
    Note
    ----
    Automatically uses the antialiasing settings set in the engine at runtime.
    Also draws correctly no matter if using the `OPENGL` or `PYGAME` renderers.
    
    Parameters
    ----------
    scene : `wame.Scene`
        The parent scene to access engine settings and information
    surface : `pygame.Surface`
        The surface that will be drawn on (usually the screen)
    color : `wame.IntVector3`
        The RGB color values to make the line
    start : `wame.IntVector2`
        The X, Y coordinate to start the line from
    end : `wame.IntVector2`
        The X, Y coordinate to end the line at
    '''

    if not isinstance(color, wame.IntVector3):
        color = wame.IntVector3.from_tuple(color)
    
    if not isinstance(start, wame.IntVector2):
        start = wame.IntVector2.from_tuple(start)

    if not isinstance(end, wame.IntVector2):
        end = wame.IntVector2.from_tuple(end)

    def draw_normal() -> None:
        if scene.engine._renderer == wame.Renderer.PYGAME:
            pygame.draw.line(surface, color.to_tuple(), start.to_tuple(), end.to_tuple())
        else:
            setup_2D_projection(scene)

            glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT | GL_LINE_BIT)

            glDisable(GL_LINE_SMOOTH)
            glBegin(GL_LINES)
            glColor3f(color.x / 255.0, color.y / 255.0, color.z / 255.0)
            glVertex2f(start.x, start.y)
            glVertex2f(end.x, end.y)
            glEnd()

            glPopAttrib()

            setup_3D_projection()

    if start.y == end.y or start.x == end.x:
        draw_normal()
    else:
        if scene.engine.settings.antialiasing:
            if scene.engine._renderer == wame.Renderer.PYGAME:
                pygame.draw.aaline(surface, color.to_tuple(), start.to_tuple(), end.to_tuple())
            else:
                setup_2D_projection(scene)

                glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT | GL_LINE_BIT)

                glEnable(GL_LINE_SMOOTH)
                glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
                glColor3f(color.x / 255, color.y / 255, color.z / 255)
                glBegin(GL_LINES)
                glVertex2f(start.x, start.y)
                glVertex2f(end.x, end.y)
                glEnd()

                glPopAttrib()

                setup_3D_projection()
        else:
            draw_normal()

def draw_rect(scene:'Scene', surface:pygame.Surface, color:wame.IntVector3, rect:pygame.Rect) -> None:
    '''
    Draws a rectangle
    
    Note
    ----
    Automatically uses the antialiasing settings set in the engine at runtime.
    Also draws correctly no matter if using the `OPENGL` or `PYGAME` renderers.
    
    Parameters
    ----------
    scene : `wame.Scene`
        The parent scene to access engine settings and information
    surface : `pygame.Surface`
        The surface that will be drawn on (usually the screen)
    color : `wame.IntVector3`
        The RGB color values to make the rectangle
    rect : `pygame.Rect`
        The position and size values of the rectangle
    '''

    if not isinstance(color, wame.IntVector3):
        color = wame.IntVector3.from_tuple(color)
    
    if not isinstance(rect, pygame.Rect):
        raise ValueError("\"rect\" parameter must be of type `pygame.Rect`")
    
    def draw_normal() -> None:
        if scene.engine._renderer == wame.Renderer.PYGAME:
            pygame.draw.rect(surface, color.to_tuple(), rect)
        else:
            setup_2D_projection(scene)

            glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT | GL_LINE_BIT)

            glDisable(GL_LINE_SMOOTH)
            glColor3f(color.x / 255.0, color.y / 255.0, color.z / 255.0)

            glBegin(GL_QUADS)
            glVertex2f(rect.x, rect.y)
            glVertex2f(rect.x + rect.width, rect.y)
            glVertex2f(rect.x + rect.width, rect.y + rect.height)
            glVertex2f(rect.x, rect.y + rect.height)
            glEnd()

            glPopAttrib()

            setup_3D_projection()
    
    if scene.engine.settings.antialiasing:
        if scene.engine._renderer == wame.Renderer.PYGAME:
            pygame.draw.rect(surface, color.to_tuple(), rect)
        else:
            setup_2D_projection(scene)

            glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT | GL_LINE_BIT)

            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            glColor3f(color.x / 255, color.y / 255, color.z / 255)

            glBegin(GL_QUADS)
            glVertex2f(rect.x, rect.y)
            glVertex2f(rect.x + rect.width, rect.y)
            glVertex2f(rect.x + rect.width, rect.y + rect.height)
            glVertex2f(rect.x, rect.y + rect.height)
            glEnd()

            glPopAttrib()

            setup_3D_projection()
    else:
        draw_normal()