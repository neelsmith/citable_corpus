from pydantic import BaseModel
from urn_citation import CtsUrn

class CitablePassage(BaseModel):
    """A passage of text citable by CtsUrn
    
    Attributes:
        urn (CtsUrn): Leaf-node CtsUrn for the passage.
        text (str): The text of the passage.
    """
    urn: CtsUrn
    text: str

    def __str__(self):
        return f"{self.urn}: {self.text}"
    
    @classmethod
    def from_string(cls, src: str, delimiter: str = "|") -> "CitablePassage":
        """Create a CitablePassage from a delimited-text string.
        
        Args:
            s (str): The input string.
            delimiter (str): The delimiter separating the urn and text. Default is '|'.
        
        Returns:
            CitablePassage: The created CitablePassage object.
        """
        urn_str, text = src.split(delimiter, 1)
        urn = CtsUrn.from_string(urn_str.strip())
        return cls(urn=urn, text=text.strip())
    
