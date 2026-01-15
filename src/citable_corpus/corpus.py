import itertools
import requests
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


    def len(self) -> int:
        """Get the number of passages in the corpus.
        
        Returns:
            int: The number of passages.
        """
        return len(self.passages)
    

    def __str__(self):
        return f"Corpus with {len(self.passages)}citable passages."
    
    @classmethod
    def from_string(cls, s: str, delimiter: str = "|") -> CitableCorpus:
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
    
    @classmethod
    def from_cex_file(cls, f: str, delimiter: str = "|") -> CitableCorpus:
        """Create a CitableCorpus from a source file in CEX format.
        
        Args:
            f (str): Path of file to read.
            delimiter (str): The delimiter separating the urn and text. Default is '|'.
        
        Returns:
            CitableCorpus: The created CitableCorpus object.
        """
        textblocks = CexBlock.from_file(f, "ctsdata")
        datablocks = [b.data for b in textblocks]
        datalines = list(itertools.chain.from_iterable(datablocks))
        passages = [CitablePassage.from_string(line, delimiter) for line in datalines]
        return cls(passages=passages)

    @classmethod
    def from_cex_url(cls, url: str, delimiter: str = "|") -> CitableCorpus:
        """Create a CitableCorpus from source data in CEX format retrieved from a URL.
        
        Args:
            url (str): URL to retrieve data from.
            delimiter (str): The delimiter separating the urn and text. Default is '|'.
        
        Returns:
            CitableCorpus: The created CitableCorpus object.
        """
        textblocks = CexBlock.from_url(url, "ctsdata")
        datablocks = [b.data for b in textblocks]
        datalines = list(itertools.chain.from_iterable(datablocks))
        passages = [CitablePassage.from_string(line, delimiter) for line in datalines]
        return cls(passages=passages)
