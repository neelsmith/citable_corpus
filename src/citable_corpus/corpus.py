
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





