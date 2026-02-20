from abc import ABC, abstractmethod


class EditionBuilder(ABC):
    @abstractmethod
    def edition(self):
        pass

class TEIDiplomatic(EditionBuilder):
    def __init__(self, side):
        self.side = side
    
    def edition(self):
        return ""    
    
class TEINormalized(EditionBuilder):
    def __init__(self, side):
        self.side = side
    
    def edition(self):
        return ""     