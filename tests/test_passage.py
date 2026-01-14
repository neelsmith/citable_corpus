import unittest
from urn_citation import CtsUrn
from citable_corpus import CitablePassage


class TestCitablePassage(unittest.TestCase):
    def test_init(self):
        urn = CtsUrn.from_string("urn:cts:latinLit:phi0959.phi006:1.1")
        text = "Lorem ipsum dolor sit amet."
        passage = CitablePassage(urn=urn, text=text)
        self.assertEqual(passage.urn, urn)
        self.assertEqual(passage.text, text)
