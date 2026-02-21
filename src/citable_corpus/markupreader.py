from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
from .corpus import CitableCorpus



class MarkupReader(ABC):
    @abstractmethod
    def cex(xmlstring, baseurn):
        pass

    @abstractmethod
    def corpus(xmlstring, baseurn) -> CitableCorpus:
        pass
    
nsdict = {'tei': 'http://www.tei-c.org/ns/1.0'}

class TEIDivAbReader(MarkupReader):
 
    def corpus(txt, urnbase) -> CitableCorpus:
        return CitableCorpus.from_string(TEIDivAbReader.cex(txt, urnbase), delimiter="|")

    
    def cex(xmlstring, baseurn):
        parsed = ET.fromstring(xmlstring)
        #root = parsed.getroot()
        flatlines = []
        divlist = [div for div in parsed.findall('./tei:text/tei:body/tei:div', nsdict)]
        for d in divlist:
            u1 = baseurn + d.get('n')
            sub_abs = d.findall('./tei:ab', nsdict)
            #flatlines.append(f"Found {len(sub_abs)} ab childredn of div {d.get('n')}")
            for ab in d.findall('./tei:ab', nsdict):
                u = u1 + "." + ab.get('n')
                rawline = u + "|" + ET.tostring(ab, encoding='unicode')

                line = rawline.replace("\n", " ").replace("\r", " ").strip()
                tidy = ' '.join(line.split())
                flatlines.append(tidy)

        return "\n".join(flatlines)