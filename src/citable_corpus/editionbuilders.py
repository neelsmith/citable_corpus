from abc import ABC, abstractmethod
from xml.dom import minidom
from .corpus import CitableCorpus, CitablePassage

from nbs.testxml import walkdomtree

class EditionBuilder(ABC):
    @abstractmethod
    def edition(self):
        pass

teins = "http://www.tei-c.org/ns/1.0"

def tidy_ws(text):
    # .split() splits on any whitespace and removes empty segments
    # " ".join() puts the resulting words back together with a single space
    return " ".join(text.split())

def extract_text(node, cumulation, omitlist):
    # Continue walking the tree
    for kid in node.childNodes:
        if kid.nodeType == kid.TEXT_NODE:
            cumulation.append(kid.data)
        elif kid.nodeType == kid.ELEMENT_NODE and kid.localName not in omitlist:
            #cumulation.append(f"- Found element: `{kid.localName}`")
            extract_text(kid, cumulation, omitlist)
    return "".join(cumulation)

class TEIDiplomatic(EditionBuilder):
    def __init__(self, xmlcorpus: CitableCorpus):
        self.xmlcorpus = xmlcorpus
    
    def edition(self):
        omitlist = ['expan'] 
        
        plist = self.xmlcorpus.passages
        psgs = []
        for p in plist:
            extracted = extract_text(minidom.parseString(p.text).documentElement, [],  omitlist )

            # What's up?
            #tidy = tidy_ws(' '.join(extracted))

            psgs.append(CitablePassage(urn = p.urn,text = extracted )) 
            
        return CitableCorpus(passages = psgs)
    
class TEINormalized(EditionBuilder):
    def __init__(self, side):
        self.side = side
    
    def edition(self):
        return ""     