from __future__ import annotations

from typing import Union
from wame.color.rgb import ColorRGB, ColorRGBA
from wame.vector import IntVector2
from wame.interval import Interval
from wame.settings import Settings
from wame.pipeline import Pipeline
from wame.scene import Scene

import ast
import importlib
import json
import os
import pygame
import time

pygame.init()
pygame.font.init()
pygame.joystick.init()

class Engine:
    '''Game Engine'''
    
    _previously_instantiated:bool = False

    def __init__(self, name:str, pipeline:Pipeline, *, size:IntVector2=IntVector2(0, 0), display:int=0, icon:pygame.Surface=None, settings_persistent:bool=True) -> None:
        '''
        Instantiates a game engine that handles all backend code for running games.
        
        Parameters
        ----------
        name : str
            The name of the engine window.
        pipeline : wame.pipeline.Pipeline
            The pipeline library the engine should use.
        size : wame.vector.xy.IntVector2
            The X and Y sizes for the game window.
        display : int
            The index of the display/monitor for the rendering screen.
        icon : pygame.Surface
            The image/surface of the game window icon.
        settings_persistent : bool
            If the engine should read and write the internal `wame.settings.Settings` object persistently, otherwise persistency will be controlled by the developer.
        
        Raises
        ------
        RuntimeError
            - If more than one instance of `wame.engine.Engine` is created during runtime.
            - If an unsupported `wame.pipeline.Pipeline` is set as the pipeline.
        '''

        if Engine._previously_instantiated:
            error: str = "Only one instance of `wame.engine.Engine` is supported during runtime."
            raise RuntimeError(error)
        
        Engine._previously_instantiated = True

        self._name:str = name

        self._screen:pygame.Surface = None
        self._clock:pygame.time.Clock = pygame.time.Clock()
        self._deltaTime:float = 0.001
        self._running:bool = False

        if settings_persistent:
            if not os.path.exists("settings.json"):
                with open("settings.json", 'w') as file:
                    file.write("{}")
        
        self.settings:Settings = None
        '''The settings that the engine renders/runs the game with'''
        self._settings_persistent:bool = settings_persistent

        if self._settings_persistent:
            with open("settings.json") as file:
                self.settings = Settings(json.load(file), self)
        else:
            self.settings = Settings({}, self)

        self._scene:Scene = None
        self._scenes:dict[str, Scene] = {}

        self._set_fps:int = self.settings.max_fps
        self._background_color:ColorRGBA = ColorRGBA(0, 0, 0, 1.0)

        self._size:IntVector2 = size

        self._mouse_visibility:bool = True
        self._mouse_grabbed:bool = False
        
        self._pipeline:Pipeline = pipeline

        if pipeline not in [Pipeline.PYGAME, Pipeline.OPENGL]:
            error:str = "Sorry, the requested pipeline is not supported."
            raise RuntimeError(error)
        
        self._display:int = display
        self.set_pipeline(pipeline)

        if icon:
            pygame.display.set_icon(icon)

        pygame.display.set_caption(self._name)

        pygame.mouse.set_visible(self._mouse_visibility)
        pygame.event.set_grab(self._mouse_grabbed)

        self._fixed_update_interval:float = Interval.HZ_60.value
        self._fixed_update_accumulator:float = 0.0
        self._fixed_update_last:float = 0.0

        self._game_loop_enabled: bool = True
        self._poll_game_loop: bool = False

    def _cleanup(self) -> None:
        if self._settings_persistent:
            with open("settings.json", 'w') as file:
                json.dump(self.settings.export(), file, indent=4)

    def _mainloop(self) -> None:
        if not self.scene:
            error:str = "A starting scene must be defined before the engine can start. Register a scene with any engine.register_scene ... and set the scene using engine.set_scene()"
            raise RuntimeError(error)

        self._running = True

        while self._running:
            if self._game_loop_enabled:
                self._scene._check_events()
                self._scene._check_keys()
                self._scene._update()

                now:float = time.perf_counter()
                frame_time:float = now - self._fixed_update_last
                self._fixed_update_last = now
                self._fixed_update_accumulator += frame_time

                while self._fixed_update_accumulator >= self._fixed_update_interval:
                    self._scene._fixed_update()
                    self._fixed_update_accumulator -= self._fixed_update_interval

                self._scene._render()
            else:
                self._scene._check_events()
                self._scene._check_keys()

                if not self._poll_game_loop:
                    pygame.time.wait(5)
                    continue

                self._poll_game_loop = False

                self._scene._update()
                self._scene._render()

        self._scene._cleanup()
        self._cleanup()

    @property
    def background_color(self) -> ColorRGBA:
        '''The background/screen color of the engine.'''

        return self._background_color

    @property
    def delta_time(self) -> float:
        '''Time since the last frame was rendered.'''

        return self._deltaTime

    @property
    def fps(self) -> float:
        '''Frames per second of the engine.'''

        return self._clock.get_fps()

    @property
    def mouse_locked(self) -> bool:
        '''If the mouse is locked to the engine window.'''

        return self._mouse_grabbed

    @property
    def mouse_visible(self) -> bool:
        '''If the mouse is visible.'''

        return self._mouse_visibility

    @property
    def pipeline(self) -> Pipeline:
        '''The current pipeline of the engine.'''

        return self._pipeline

    def quit(self) -> None:
        '''
        Stops the engine and cleans up.
        '''
        
        self._running = False

    def register_scene(self, name:str, scene:Scene, overwrite:bool=False) -> None:
        '''
        Register a scene to the engine.
        
        Parameters
        ----------
        name : str
            The unique name used to lookup and manipulate this scene.
        scene : wame.scene.Scene
            The scene to register.
        overwrite : bool
            If the unique name is already used, overwrite it, else throw an error.
        
        Raises
        ------
        RuntimeError
            If the unique name already exists and overwriting is not enabled.
        TypeError
            - If the provided name is not a `str`.
            - If the provided overwrite is not a `bool`.
        '''
        
        if not isinstance(name, str):
            error: str = "Parameter `name` must be a `str`."
            raise TypeError(error)
        
        if not isinstance(overwrite, bool):
            error: str = "Parameter `overwrite` must be a `bool`."
            raise TypeError(error)

        if not overwrite and name in self._scenes:
            error:str = f"Scene name \"{name}\" already in use"
            raise RuntimeError(error)

        self._scenes[name] = scene

    def register_scenes(self, scenes:dict[str, Scene], overwrite:bool=False) -> None:
        '''
        Register a set of scenes to the engine.
        
        Parameters
        ----------
        scenes : dict[str, wame.scene.Scene]
            The name-scene pairs to register.
        overwrite : bool
            If any unique name is already used, overwrite it, else throw an error.
        
        Raises
        ------
        RuntimeError
            If any unique name already exists and overwriting is not enabled.
        TypeError
            - If the provided scenes mapping is not a `dict`.
            - If the provided overwrite is not a `bool`.
        '''

        if not isinstance(scenes, dict):
            error: str = "Parameter `scenes` must be a `dict`."
            raise TypeError(error)
        
        if not isinstance(overwrite, bool):
            error: str = "Parameter `overwrite` must be a `bool`."
            raise TypeError(error)

        for name, scene in scenes.items():
            self.register_scene(name, scene, overwrite)
    
    def register_scenes_from_folder(self, folder:str, overwrite:bool=False) -> None:
        '''
        Register all Scene objects within all files in a folder to the engine.
        
        Parameters
        ----------
        folder : str
            The folder to register scenes from.
        overwrite : bool
            If any unique name is already used, overwrite it, else throw an error.
        
        Raises
        ------
        RuntimeError
            - If the folder path provided does not exist or if the folder path does not direct to a folder.
            - If any unique name already exists and overwriting is not enabled.
        TypeError
            - If the provided folder is not a `str`.
            - If the provided overwrite is not a `bool`.

        Tip
        ---
        If you plan on bundling this game into an executable file:
        Continue to use this method, but also include the raw scene program files in the folder provided as well as the .exe file OR
        manually register each scene.
        This is because to bundle Python into executable files, there must be a direct reference to dependencies. Hotloading scenes has no direct reference.

        Note
        ----
        Folder must be in the same directory as your project.
        The engine will only walk through the files in this folder, not any subdirectories.
        All unique scene names will be generated from the Scene subclass names themselves:
        ```python
        class MyScene(wame.Scene):
            ...
        ```
        Will generate unique name "My" and can be used to set the scene later on.

        ```python
        class MainMenuScene(wame.Scene):
            ...
        ```
        Will generate unique name "MainMenu" and can be used to set the scene later on.

        And so forth...
        '''
        
        if not isinstance(folder, str):
            error: str = "Parameter `folder` must be a `str`."
            raise TypeError(error)
        
        if not isinstance(overwrite, bool):
            error: str = "Parameter `overwrite` must be a `bool`."
            raise TypeError(error)

        if not os.path.exists(folder):
            error:str = f"Folder \"{folder}\" could not be found."
            raise RuntimeError(error)
        
        if not os.path.isdir(folder):
            error:str = f"Item with name \"{folder}\" is not a folder/directory."
            raise RuntimeError(error)
        
        for filename in os.listdir(folder):
            if not filename.endswith(".py"):
                continue

            with open(f"{folder}/{filename}") as file:
                contents:str = file.read()
            
            tree:ast.Module = ast.parse(contents)
            classes:list[ast.ClassDef] = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

            for fileClass in classes:
                endIndex:int = fileClass.name.find("Scene")

                if endIndex < 0:
                    continue

                sceneName:str = fileClass.name[0:endIndex]
                
                module = importlib.import_module(f"{folder}.{filename[:-3]}")
                sceneObject:Scene = getattr(module, fileClass.name)

                self.register_scene(sceneName, sceneObject, overwrite)

    @property
    def running(self) -> bool:
        '''If the engine is still running the game loop.'''

        return self._running

    @property
    def scene(self) -> Scene:
        '''The currently active scene - `None` if not running.'''

        return self._scene
    
    @property
    def scenes(self) -> dict[str, Scene]:
        '''The `ID: Scene` mapping of all registered scenes.'''

        return self._scenes
    
    @property
    def screen(self) -> pygame.Surface:
        '''The screen/window the `Engine` is handling.'''

        return self._screen

    def set_background(self, color:ColorRGBA=ColorRGBA(0, 0, 0, 1.0)) -> None:
        '''
        Set the background color of the engine rendering scene
        
        Parameters
        ----------
        color : wame.color.rgb.ColorRGBA
            The background color to apply to all scenes.
        
        Raises
        ------
        TypeError
            If the provided color is not an RGB/A-supported type (like `tuple` or `ColorRGB/A`).
        '''

        if not isinstance(color, (ColorRGB, tuple)):
            error: str = "Parameter `color` must be an instance of `ColorRGB~` or a `tuple`."
            raise TypeError(error)

        if isinstance(color, tuple):
            color = ColorRGBA.from_tuple(color)

        self._background_color = color
 
    def set_game_loop_enabled(self, enabled: bool) -> None:
        '''
        Set the engine to continuously run the game loop or poll it manually using `.step_game_loop`.
        
        Parameters
        ----------
        enabled : bool
            If the game loop should continuously run.
        
        Raises
        ------
        TypeError
            If the provided value is not a `bool`.
        
        Warning
        -------
        If disabled, this will disable the fixed update functionality of the `Engine` and `Scene` objects.
        '''

        if not isinstance(enabled, bool):
            error: str = "Parameter `enabled` must be a `bool`."
            raise TypeError(error)

        self._game_loop_enabled = enabled

    def set_mouse_visible(self, state:bool=True) -> None:
        '''
        Set if the mouse should be visible or hidden.
        
        Parameters
        ----------
        state : bool
            If the mouse should be visible or hidden.

        Raises
        ------
        TypeError
            If the provided state is not a `bool`.
        '''

        if not isinstance(state, bool):
            error: str = "Parameter `state` must be a `bool`."
            raise TypeError(error)

        self._mouse_visibility = state
        pygame.mouse.set_visible(state)

    def set_mouse_locked(self, state:bool=False) -> None:
        '''
        Set if the mouse should be immovable.
        
        Parameters
        ----------
        state : bool
            If the mouse should be locked or not.

        Raises
        ------
        TypeError
            If the provided state is not a `bool`.
        '''

        if not isinstance(state, bool):
            error: str = "Parameter `state` must be a `bool`."
            raise TypeError(error)

        self._mouse_grabbed = state
        pygame.event.set_grab(state)

    def set_pipeline(self, pipeline:Pipeline) -> None:
        '''
        Set the rendering pipeline that the engine should use.
        
        Parameters
        ----------
        pipeline : wame.Pipeline
            The rendering pipeline to switch to.
        
        Raises
        ------
        RuntimeError
            If the pipeline tries to switch during runtime.
        TypeError
            If the provided pipeline isn't a `Pipeline` object.
        '''

        if not isinstance(pipeline, Pipeline):
            error: str = "Parameter `pipeline` must be a `Pipeline` object."
            raise TypeError(error)

        if self._scene and self._scene._first_elapsed:
            error:str = "Switching the rendering pipeline during the game loop is not supported"
            raise RuntimeError(error)

        self._pipeline = pipeline

        if pipeline == Pipeline.PYGAME:
            self._screen = pygame.display.set_mode(self._size.to_tuple(), pygame.HWSURFACE | pygame.DOUBLEBUF, display=self._display, vsync=self.settings.vsync)
        else:
            self._screen = pygame.display.set_mode(self._size.to_tuple(), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL, display=self._display, vsync=self.settings.vsync)

    def set_scene(self, name: str, *args) -> None:
        '''
        Switch the engine to another scene and clean up the previous (if any).
        
        Parameters
        ----------
        name : str
            The unique name of the scene to switch to (must be previously registered).
        args : Any
            Any data you wish to pass to the scene instance.
        
        Raises
        ------
        RuntimeError
            - If a scene with the name doesn't exist.
            - If the desired scene is already set as the active scene.
        TypeError
            If the provided name is not a `str`.
        '''
        
        if not isinstance(name, str):
            error: str = "Parameter `name` must be a `str`."
            raise TypeError(error)

        if name not in self.scenes:
            error:str = f"Scene with name \"{name}\" was not registered/found"
            raise RuntimeError(error)
        
        if isinstance(self.scene, self.scenes[name]):
            error:str = f"Scene with name \"{name}\" is already set as the active scene"
            raise RuntimeError(error)
        
        if self.scene is not None:
            self.scene._cleanup()
            del self.scene

        self._scene = self._scenes[name](self, *args)
        self._scene._first()

        self._fixed_update_accumulator = 0.0
        self._fixed_update_last = time.perf_counter()

    def set_update_interval(self, interval:Union[Interval, float]) -> None:
        '''
        Set the amount of time (in seconds) that has to elapse before a fixed update call to a `Scene` is called.
        
        Parameters
        ----------
        interval : Interval | float
            The amount of seconds to elapse for each fixed update call.
        
        Raises
        ------
        RuntimeError
            If trying to switch interval timing during the game loop.
        TypeError
            If the interval provided is not an `Interval` or `float`.
        '''

        if not isinstance(interval, (Interval, float)):
            error: str = "Parameter `interval` must be an `Interval` object or `float`."
            raise TypeError(error)

        if self.scene and self.scene._first_elapsed:
            error:str = "Switching update intervals during the game loop is not supported"
            raise RuntimeError(error)

        self._fixed_update_interval = interval.value

    def start(self) -> None:
        '''
        Starts the engine.

        Warning
        -------
        This is a blocking call. No code below will execute until the engine has stopped running.

        Raises
        ------
        RuntimeError
            If the engine is started without a scene registered and set.
        '''
        
        self._mainloop()
    
    def step_game_loop(self) -> None:
        '''Poll the game loop to run a cycle (update/render) - Only use when game loop is disabled with `.set_game_loop_enabled(False)`.'''

        self._poll_game_loop = True