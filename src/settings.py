class Settings:
    '''Engine Global Settings'''

    def __init__(self, data:dict[str]) -> None:
        '''
        Initialize the engine settings
        
        Note
        ----
        This should only be instantiated by the engine internally.
        Avoid calling this yourself.
        
        Parameters
        ----------
        data : `dict[str, Any]`
            The raw settings contents from the known settings persistence file
        '''
        
        self.antialiasing:bool = data["antialiasing"] if "antialiasing" in data else True
        '''Graphics technique used to remove jagged edges'''

        self.max_fps:int = data["max_fps"] if "max_fps" in data else 0
        '''The maximum framerate that the engine will render scenes at'''

        self.tabbed_fps:int = data["tabbed_fps"] if "tabbed_fps" in data else 30
        '''The maximum framerate that the engine will render scenes at when tabbed out'''

    def export(self) -> dict[str]:
        '''
        Export the class instance to a raw, storable type
        
        Returns
        -------
        rawSettings : `dict[str, Any]`
            The raw class instance data
        '''
        
        return {
            "antialiasing": self.antialiasing,
            "max_fps": self.max_fps,
            "tabbed_fps": self.tabbed_fps
        }