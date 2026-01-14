from pydantic import BaseModel
from urn_citation import CtsUrn

class CitablePassage(BaseModel):
    urn: CtsUrn
    text: str