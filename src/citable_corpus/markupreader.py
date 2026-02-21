from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
from .corpus import CitableCorpus



class MarkupReader(ABC):
    @abstractmethod
    def cex(self):
        pass

    @abstractmethod
    def corpus(self) -> CitableCorpus:
        pass
    



nsdict = {'tei': 'http://www.tei-c.org/ns/1.0'}

class TEIDivAbReader(MarkupReader):
    def __init__(self, txt,urnbase):
        self.xml = txt
        self.urnbase = urnbase
 
    def corpus(self) -> CitableCorpus:
        return CitableCorpus.from_string(self.cex(), delimiter="|")

    
    def cex(self):
        parsed = ET.fromstring(self.xml)
        #root = parsed.getroot()
        flatlines = []
        divlist = [div for div in parsed.findall('./tei:text/tei:body/tei:div', nsdict)]
        for d in divlist:
            u1 = self.urnbase + d.get('n')
            sub_abs = d.findall('./tei:ab', nsdict)
            #flatlines.append(f"Found {len(sub_abs)} ab childredn of div {d.get('n')}")
            for ab in d.findall('./tei:ab', nsdict):
                u = u1 + "." + ab.get('n')
                rawline = u + "|" + ET.tostring(ab, encoding='unicode')

                line = rawline.replace("\n", " ").replace("\r", " ").strip()
                tidy = ' '.join(line.split())
                flatlines.append(tidy)

        return "\n".join(flatlines)