class Tool:
    """Base class for all tools"""

    def __init__(self):
        self.name = self.__class__.__name__
