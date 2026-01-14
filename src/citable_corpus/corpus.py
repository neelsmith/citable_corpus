
from pydantic import BaseModel
from .passage import CitablePassage
from typing import List
from cite_exchange import *

class CitableCorpus(BaseModel):
    """A corpus of citable passages of text.
    
    Attributes:
        passages (List[CitablePassage]): the corpus of passages.
    """
    passages: List[CitablePassage]


    @classmethod
    def from_string(cls, s: str, delimiter: str = "|") -> List[CitablePassage]:
        """Create a CitableCorpus from a delimited-text string.
        
        Args:
            s (str): The input string, with each passage on a new line.
            delimiter (str): The delimiter separating the urn and text. Default is '|'.
        
        Returns:
            CitableCorpus: The created CitableCorpus object.
        """
        passages = []
        for line in s.strip().splitlines():
            passage = CitablePassage.from_string(line, delimiter)
            passages.append(passage)
        return cls(passages=passages)


