from __future__ import annotations

from wame.color.rgb import ColorRGBA
from wame.vector import IntVector2
from wame.settings import Settings
from wame.pipeline import Pipeline
from wame.scene import Scene

import importlib
import pygame
import json
import ast
import os

pygame.init()
pygame.font.init()

class Engine:
    '''Game Engine'''
    
    _previously_instantiated:bool = False

    def __init__(self, name:str, pipeline:Pipeline, *, size:IntVector2=IntVector2(0, 0), display:int=0, icon_filepath:str=None) -> None:
        '''
        Instantiates a game engine that handles all backend code for running games
        
        Parameters
        ----------
        name : `str`
            The name of the engine window
        pipeline : `wame.Pipeline`
            The pipeline library the engine should use
        size : `wame.vector.IntVector2`
            The X and Y sizes for the game window
        display : `int`
            The index of the display/monitor for the rendering screen
        icon_filepath : `str`
            The filepath of the game window icon
        '''

        if Engine._previously_instantiated:
            error:str = "Only one instance of `wame.engine.Engine` is supported during runtime"
            raise RuntimeError(error)
        
        Engine._previously_instantiated = True

        self._name:str = name

        self.screen:pygame.Surface = None
        '''The screen that the engine is rendering to'''
        self._clock:pygame.time.Clock = pygame.time.Clock()
        self._deltaTime:float = 0.001
        self._running:bool = False

        if not os.path.exists("settings.json"):
            with open("settings.json", 'w') as file:
                file.write("{}")
        
        with open("settings.json") as file:
            self.settings:Settings = Settings(json.load(file), self)
            '''The settings that the engine renders/runs the game with'''

        self.scene:Scene = None
        '''The scene that is currently active - `None` if no scene is running'''
        self.scenes:dict[str, Scene] = {}
        '''The key-value pairs of scenes and their names (name: scene)'''

        self._set_fps:int = self.settings.max_fps
        self._background_color:ColorRGBA = ColorRGBA(0, 0, 0, 1.0)

        self._size:IntVector2 = size

        self._mouse_visibility:bool = True
        self._mouse_grabbed:bool = False
        
        self._pipeline:Pipeline = pipeline

        if pipeline not in [Pipeline.PYGAME, Pipeline.OPENGL]:
            error:str = "Sorry, the requested pipeline is not supported"
            raise RuntimeError(error)
        
        self._display:int = display
        self.set_pipeline(pipeline)

        if icon_filepath:
            pygame.display.set_icon(pygame.image.load(icon_filepath.replace('\\', '/')))

        pygame.display.set_caption(self._name)

        pygame.mouse.set_visible(self._mouse_visibility)
        pygame.event.set_grab(self._mouse_grabbed)

    def _cleanup(self) -> None:
        with open("settings.json", 'w') as file:
            json.dump(self.settings.export(), file, indent=4)

    def _mainloop(self) -> None:
        if not self.scene:
            error:str = "A starting scene must be defined before the engine can start. Register a scene with any engine.register_scene ... and set the scene using engine.set_scene()"
            raise RuntimeError(error)

        self._running = True

        while self._running:
            self.scene._check_events()
            self.scene._check_keys()
            self.scene._update()

            self.scene._render()
        
        self.scene._cleanup()
        self._cleanup()

    @property
    def background_color(self) -> ColorRGBA:
        '''The background/screen color of the engine'''

        return self._background_color

    @property
    def delta_time(self) -> float:
        '''Time since the last frame was rendered'''

        return self._deltaTime

    @property
    def fps(self) -> float:
        '''Frames per second of the engine'''

        return self._clock.get_fps()

    @property
    def mouse_locked(self) -> bool:
        '''If the mouse is locked to the engine window'''

        return self._mouse_grabbed

    @property
    def mouse_visible(self) -> bool:
        '''If the mouse is visible'''

        return self._mouse_visibility

    @property
    def pipeline(self) -> Pipeline:
        '''The current pipeline of the engine'''

        return self._pipeline

    def quit(self) -> None:
        '''
        Stops the engine and cleans up
        '''
        
        self._running = False

    def register_scene(self, name:str, scene:Scene, overwrite:bool=False) -> None:
        '''
        Register a scene to the engine
        
        Parameters
        ----------
        name : `str`
            The unique name used to lookup and manipulate this scene
        scene : `wame.Scene`
            The scene to register
        overwrite : `bool`
            If the unique name is already used, overwrite it, else throw an error - Default `False`
        
        Raises
        ------
        `wame.UniqueNameAlreadyExists`
            If the unique name already exists and overwriting is not enabled
        '''
        
        if not overwrite:
            if name in self.scenes:
                error:str = f"Scene name \"{name}\" already in use"
                raise RuntimeError(error)

        self.scenes[name] = scene

    def register_scenes(self, scenes:dict[str, Scene], overwrite:bool=False) -> None:
        '''
        Register a set of scenes to the engine
        
        Parameters
        ----------
        scenes : `dict[str, wame.Scene]`
            The name-scene pairs to register
        overwrite : `bool`
            If any unique name is already used, overwrite it, else throw an error - Default `False`
        
        Raises
        ------
        `wame.UniqueNameAlreadyExists`
            If any unique name already exists and overwriting is not enabled
        '''

        for name, scene in scenes.items():
            self.register_scene(name, scene, overwrite)
    
    def register_scenes_from_folder(self, folder:str, overwrite:bool=False) -> None:
        '''
        Register all Scene objects within all files in a folder to the engine
        
        Warning
        -------
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
        Will generate unique name "My" and can be used to set the scene later on

        ```python
        class MainMenuScene(wame.Scene):
            ...
        ```
        Will generate unique name "MainMenu" and can be used to set the scene later on

        And so forth...
        
        Parameters
        ----------
        folder : `str`
            The folder to register scenes from
        overwrite : `bool`
            If any unique name is already used, overwrite it, else throw an error - Default `False`
        
        Raises
        ------
        `wame.SceneFolderNotFound`
            If the folder path provided does not exist or if the folder path does not direct to a folder
        `wame.UniqueNameAlreadyExists`
            If any unique name already exists and overwriting is not enabled
        '''
        
        if not os.path.exists(folder):
            error:str = f"Folder \"{folder}\" could not be found"
            raise RuntimeError(error)
        
        if not os.path.isdir(folder):
            error:str = f"Item with name \"{folder}\" is not a folder/directory"
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
        '''If the engine is still running the game loop'''

        return self._running

    def set_background(self, color:ColorRGBA=ColorRGBA(0, 0, 0, 1.0)) -> None:
        '''
        Set the background color of the engine rendering scene
        
        Parameters
        ----------
        color : `wame.color.rgb.ColorRGBA`
            The background color to apply to all scenes - Default `ColorRGBA(0, 0, 0, 1.0)`
        '''

        if isinstance(color, tuple):
            color = ColorRGBA.from_tuple(color)

        self._background_color = color

    def set_mouse_visible(self, state:bool=True) -> None:
        '''
        Set if the mouse should be visible or hidden
        
        Parameters
        ----------
        state : `bool`
            If the mouse should be visible or hidden - Default `True`
        '''

        self._mouse_visibility = state
        pygame.mouse.set_visible(state)

    def set_mouse_locked(self, state:bool=False) -> None:
        '''
        Set if the mouse should be immovable
        
        Parameters
        ----------
        state : `bool`
            If the mouse should be locked or not - Default `False`
        '''

        self._mouse_grabbed = state
        pygame.event.set_grab(state)

    def set_pipeline(self, pipeline:Pipeline) -> None:
        '''
        Set the rendering pipeline that the engine should use
        
        Parameters
        ----------
        pipeline : `wame.Pipeline`
            The rendering pipeline to switch to
        '''

        if self.scene and self.scene._first_elapsed:
            error:str = "Switching the rendering pipeline during the game loop is not supported"
            raise RuntimeError(error)

        self._pipeline = pipeline

        if pipeline == Pipeline.PYGAME:
            self.screen = pygame.display.set_mode(self._size.to_tuple(), pygame.HWSURFACE | pygame.DOUBLEBUF, display=self._display, vsync=self.settings.vsync)
        else:
            self.screen = pygame.display.set_mode(self._size.to_tuple(), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL, display=self._display, vsync=self.settings.vsync)

    def set_scene(self, name:str, *args) -> None:
        '''
        Switch the engine to another scene and clean up the previous (if any)
        
        Parameters
        ----------
        name : `str`
            The unique name of the scene to switch to (must be previously registered)
        args : `Any`
            Any data you wish to pass to the scene instance
        
        Raises
        ------
        `wame.UniqueNameNotFound`
            If the name does not exist
        '''
        
        if name not in self.scenes:
            error:str = f"Scene with name \"{name}\" was not registered/found"
            raise RuntimeError(error)
        
        if isinstance(self.scene, self.scenes[name]):
            error:str = f"Scene with name \"{name}\" is already set as the active scene"
            raise RuntimeError(error)
        
        if self.scene is not None:
            self.scene._cleanup()
            del self.scene

        self.scene = self.scenes[name](self, *args)
        self.scene._first()

    def start(self) -> None:
        '''
        Starts the engine

        Warning
        -------
        This is a blocking call. No code below will execute until the engine has stopped running.

        Raises
        ------
        `wame.SceneNotSet`
            If the engine is started without a scene registered and set
        '''
        
        self._mainloop()