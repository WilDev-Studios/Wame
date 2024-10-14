from wame.vector import IntVector2, IntVector3
from wame.settings import Settings
from wame.render import Renderer
from wame.scene import Scene
from wame.error import *

from OpenGL.GL import *

import importlib
import pygame
import json
import ast
import os

pygame.init()
pygame.font.init()

class Engine:
    '''Game Engine'''
    
    def __init__(self, name:str, renderer:Renderer, *, size:IntVector2=IntVector2(0, 0), iconFilepath:str=None) -> None:
        '''
        Instantiates a game engine that handles all backend code for running games
        
        Parameters
        ----------
        name : `str`
            The name of the engine window
        renderer : `wame.Renderer`
            The rendering pipeline the engine should use
        size : `wame.IntVector2`
            The X and Y sizes for the game window
        iconFilepath : `str`
            The filepath of the game window icon
        
        Raises
        ------
        `wame.RendererNotRecognized`
            If the renderer provided to the engine is not recognized
        '''

        self._name:str = name

        self.screen:pygame.Surface = None
        self._clock:pygame.time.Clock = pygame.time.Clock()
        self._deltaTime:float = 0.001
        self._running:bool = False

        if not os.path.exists("settings.json"):
            with open("settings.json", 'w') as file:
                file.write("{}")
        
        with open("settings.json") as file:
            self.settings:Settings = Settings(json.load(file))

        self._scene:Scene = None
        self._scenes:dict[str, Scene] = {}
        self._set_fps:int = self.settings.max_fps
        self._background_color:IntVector3 = IntVector3(0, 0, 0)

        self._size:IntVector2 = size

        self._mouse_visibility:bool = True
        self._mouse_grabbed:bool = False
        
        self._renderer:Renderer = renderer

        if renderer == Renderer.PYGAME:
            self.screen = pygame.display.set_mode(self._size.to_tuple(), pygame.HWSURFACE | pygame.DOUBLEBUF, display=0)
        elif renderer == Renderer.OPENGL:
            self.screen = pygame.display.set_mode(self._size.to_tuple(), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)

            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)
            glFrontFace(GL_CCW)
        else:
            error:str = f"Renderer option {renderer} provided is not of type `wame.Renderer`"
            raise RendererNotRecognized(error)
        
        if iconFilepath is not None:
            pygame.display.set_icon(pygame.image.load(iconFilepath.replace('\\', '/')))

        pygame.display.set_caption(self._name)

        pygame.mouse.set_visible(self._mouse_visibility)
        pygame.event.set_grab(self._mouse_grabbed)

    def _cleanup(self) -> None:
        with open("settings.json", 'w') as file:
            json.dump(self.settings.export(), file, indent=4)

    def _mainloop(self) -> None:
        if self._scene is None:
            error:str = "A starting scene must be defined before the engine can start. Register a scene with any engine.register_scene ... and set the scene using engine.set_scene()"
            raise SceneNotSet(error)

        self._running = True

        self._scene.on_start()

        while self._running:
            self._scene._check_events()
            self._scene._check_keys()
            self._scene._update()
            self._scene._render()
        
        self._scene._cleanup()
        self._cleanup()

    @property
    def delta_time(self) -> float:
        '''Time since the last frame was rendered'''

        return self._deltaTime

    @property
    def fps(self) -> float:
        '''Frames per second of the engine'''

        return self._clock.get_fps()

    def quit(self) -> None:
        '''
        Stops the engine and cleans up
        '''
        
        self._running = False

        self._scene.on_quit()

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
            if name in self._scenes:
                error:str = f"Scene name \"{name}\" already in use"
                raise UniqueNameAlreadyExists(error)

        self._scenes[name] = scene

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
            - If the folder path provided does not exist
            - If the folder path does not direct to a folder
        `wame.UniqueNameAlreadyExists`
            If any unique name already exists and overwriting is not enabled
        '''
        
        if not os.path.exists(folder):
            error:str = f"Folder \"{folder}\" could not be found"
            raise SceneFolderNotFound(error)
        
        if not os.path.isdir(folder):
            error:str = f"Item with name \"{folder}\" is not a folder/directory"
            raise SceneFolderNotFound(error)
        
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

    def set_background(self, color:IntVector3=IntVector3(0, 0, 0)) -> None:
        '''
        Set the background color of the engine rendering scene
        
        Parameters
        ----------
        color : `wame.IntVector3`
            The background color to apply to all scenes - Default `IntVector3(0, 0, 0)`
        '''

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

    def set_mouse_locked(self, state:bool=False) -> None:
        '''
        Set if the mouse should be immovable
        
        Parameters
        ----------
        state : `bool`
            If the mouse should be locked or not - Default `False`
        '''

        self._mouse_grabbed = state

    def set_scene(self, name:str) -> None:
        '''
        Switch the engine to another scene and clean up the previous (if any)
        
        Parameters
        ----------
        name : `str`
            The unique name of the scene to switch to (must be previously registered)
        
        Raises
        ------
        `wame.UniqueNameNotFound`
            If the name does not exist
        '''
        
        if name not in self._scenes:
            error:str = f"Scene with name \"{name}\" was not registered/found"
            raise UniqueNameNotFound(error)
        
        if isinstance(self._scene, self._scenes[name]):
            error:str = f"Scene with name \"{name}\" is already set as the active scene"
            raise SceneAlreadySet(error)
        
        if self._scene is not None:
            self._scene._cleanup()
        
        self._scene = self._scenes[name](self)._first()

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
        
        os.system("cls")

        self._mainloop()