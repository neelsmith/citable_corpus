import itertools
import requests
from pydantic import BaseModel
from urn_citation import CtsUrn
from .passage import CitablePassage
from typing import List
from cite_exchange import *

class CitableCorpus(BaseModel):
    """A corpus of citable passages of text.
    
    Attributes:
        passages (List[CitablePassage]): the corpus of passages.
    """
    passages: List[CitablePassage]

    def __len__(self) -> int:
        """Get the number of passages in the corpus.
        
        Returns:
            int: The number of passages.
        """
        return len(self.passages)

    def __str__(self):
        return f"Corpus with {len(self.passages)}citable passages."
    

    def cex(self, delimiter: str = "|", label_block = False) -> str:
        """Return a CEX string representation of the CitableCorpus."""
        data_lines = [f"{p.urn}{delimiter}{p.text}" for p in self.passages]
        if label_block:
            return "#!ctsdata\n" + "\n".join(data_lines)
        else:
            return "\n".join(data_lines)

    @classmethod
    def from_delimited(cls, s: str, delimiter: str = "|") -> CitableCorpus:
        """Create a CitableCorpus from a delimited-text string.
        
        Args:
            s (str): The input string, with each passage on a new line.
            delimiter (str): The delimiter separating the urn and text. Default is '|'.
        
        Returns:
            CitableCorpus: The created CitableCorpus object.
        """
        passages = []
        for line in s.strip().splitlines():
            passage = CitablePassage.from_delimited(line, delimiter)
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
        passages = [CitablePassage.from_delimited(line, delimiter) for line in datalines]
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
        passages = [CitablePassage.from_delimited(line, delimiter) for line in datalines]
        return cls(passages=passages)

    def to_cex(self, delimiter: str = "|", include_label = True) -> str:
        """Convert the CitableCorpus to a CEX-formatted string.
        
        Args:
            delimiter (str): The delimiter separating the urn and text. Default is '|'.
            include_label (bool): Whether to include the ctsdata label block. Default is True.
        
        Returns:
            str: The CEX-formatted string.
        """
        data_lines = [f"{p.urn}{delimiter}{p.text}" for p in self.passages]
        cex_block = CexBlock(label="ctsdata", data=data_lines)
        if include_label:
            return cex_block.to_cex()
        else:
            return "\n".join(data_lines)

    def retrieve_range(self, ref: CtsUrn) -> List[CitablePassage]:
        """Retrieve passages from the corpus matching a given CtsUrn range reference.
        
        Args:
            ref (CtsUrn): The CtsUrn range reference to search for.
        """
        if ref.is_range() == False:
            raise ValueError("retrieve_range: provided CtsUrn is not a range.")
        
        begin_urn = ref.set_passage(ref.range_begin())
        end_urn = ref.set_passage(ref.range_end())

        begin_list = [p for p in self.passages if p.urn.contains(begin_urn)]
        end_list = [p for p in self.passages if p.urn.contains(end_urn)]
        if not begin_list or not end_list:
            return []
        else:
            begin_index = self.passages.index(begin_list[0])
            end_index = self.passages.index(end_list[0])
            return self.passages[begin_index:end_index + 1]

    def retrieve(self, ref: CtsUrn) -> List[CitablePassage]:
        """Retrieve passages from the corpus matching a given CtsUrn reference.
        
        Args:
            ref (CtsUrn): The CtsUrn reference to search for.
            Returns:
                List[CitablePassage]: List of matching CitablePassage objects.
        """
        if ref.is_range():
            return self.retrieve_range(ref)
        else:
            # Handle work-level URNs (passage is None when URN ends with ':')
            if ref.passage is None:
                matches = [p for p in self.passages if p.urn.work == ref.work]
            else:
                matches = [p for p in self.passages if ref.contains(p.urn)]
            return matches
        
