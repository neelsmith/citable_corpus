from abc import ABC, abstractmethod

class MarkupReader(ABC):
    @abstractmethod
    def cex(self):
        pass

class TEIDivAbReader(MarkupReader):
    def __init__(self, side):
        self.side = side
    
    def cex(self):
        return "" 