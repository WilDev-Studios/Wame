class Renderer:
    '''Engine Rendering Pipeline'''

    PYGAME:int = 0
    '''
    PyGame will render all elements/objects
    
    Info
    ----
    PyGame cannot render 3D objects natively. Use this to make 2D games.'''

    OPENGL:int = 1
    '''
    OpenGL will render all elements/objects
    
    Info
    ----
    OpenGL is capable of rendering 2D and 3D objects
    '''