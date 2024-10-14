class MissingArgumentException(Exception):
    '''Raised when a `wame` object tries to call a method when missing a required argument'''
    ...

class UniqueNameAlreadyExists(Exception):
    '''Raised when a `wame` object tries to register an object with a unique name that already exists'''
    ...

class UniqueNameNotFound(Exception):
    '''Raised when a `wame` object tries to access an object with a unique name that does not exist'''
    ...

class RendererNotRecognized(Exception):
    '''Raised when an engine tries to run with a set renderer that does not exist or is not recognized'''
    ...

class RendererNotSet(Exception):
    '''Raised when an engine tries to run without a renderer set/configured'''
    ...

class SceneAlreadySet(Exception):
    '''Raised when an engine tries to set a scene that is already used by the engine'''
    ...

class SceneFolderNotFound(Exception):
    '''Raised when an engine tries to register scenes in a folder that does not exist or the path destination is not a folder'''
    ...

class SceneNotSet(Exception):
    '''Raised when an engine tries to run without a scene set/configured'''
    ...