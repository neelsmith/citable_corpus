from abc import ABC, abstractmethod
from xml.dom import minidom
from .corpus import CitableCorpus, CitablePassage
from .markupreader import MarkupReader

class EditionBuilder(ABC):
    @abstractmethod
    def edition(xmlcorpus: CitableCorpus):
        pass
    


teins = "http://www.tei-c.org/ns/1.0"

def set_edition_exemplar(urn, exemplar):
    "Set exemplar on a CTS URN, ensuring a version component exists first."
    versioned = urn if urn.version is not None else urn.set_version("v1")
    return versioned.set_exemplar(exemplar)

def tidy_ws(text):
    "Clean up whitespace in a string by reducing each sequence of whitespace characters to a single space, and stripping leading/trailing whitespace."
    # .split() splits on any whitespace and removes empty segments
    # " ".join() puts the resulting words back together with a single space
    return " ".join(text.split())

def extract_text(node, cumulation, omitlist):
    "Recursively extract text from an XML node, omitting contents of specified elements. Text from included nodes is accumulated in the `cumulation` list."
    # Continue walking the tree
    for kid in node.childNodes:
        if kid.nodeType == kid.TEXT_NODE:
            cumulation.append(kid.data)
        elif kid.nodeType == kid.ELEMENT_NODE and kid.localName not in omitlist:
            #cumulation.append(f"- Found element: `{kid.localName}`")
            extract_text(kid, cumulation, omitlist)
    return "".join(cumulation)

class TEIDiplomatic(EditionBuilder):

    def edition(xmlcorpus: CitableCorpus):
        "Compose a citable diplomatic edition by extracting text from the XML of each passage in the corpus, omitting specified elements."

        omitlist = ['expan'] 
        
        plist = xmlcorpus.passages
        psgs = []
        for p in plist:
            extracted = extract_text(minidom.parseString(p.text).documentElement, [],  omitlist )

            # What's up?
            #tidy = tidy_ws(' '.join(extracted))

            psgs.append(CitablePassage(urn = p.urn,text = extracted )) 

        fullurls = [CitablePassage(urn = set_edition_exemplar(p.urn, "diplomatic"), text =p.text) for p in psgs]
        return CitableCorpus(passages = fullurls)
    
class TEINormalized(EditionBuilder):
    "Compose a citable normalized edition by extracting text from the XML of each passage in the corpus, omitting specified elements."
    def edition(xmlcorpus: CitableCorpus):
        omitlist = ['abbr'] 
        
        plist = xmlcorpus.passages
        psgs = []
        for p in plist:
            extracted = extract_text(minidom.parseString(p.text).documentElement, [],  omitlist )

            # What's up?
            #tidy = tidy_ws(' '.join(extracted))

            psgs.append(CitablePassage(urn = p.urn,text = extracted )) 

        fullurls = [CitablePassage(urn = set_edition_exemplar(p.urn, "normalized"), text =p.text) for p in psgs] 
        return CitableCorpus(passages = fullurls)     
    