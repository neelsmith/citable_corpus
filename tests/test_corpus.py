
import unittest
from citable_corpus.corpus import CitableCorpus
from citable_corpus.passage import CitablePassage
from urn_citation import CtsUrn

class TestCitableCorpus(unittest.TestCase):
	def setUp(self):
		self.lines = [
			"urn:cts:latinLit:phi0959.phi006:1.1|Lorem ipsum",
			"urn:cts:latinLit:phi0959.phi006:1.2|Dolor sit amet."
		]
		self.input_str = "\n".join(self.lines)

	def test_from_string_default_delimiter(self):
		corpus = CitableCorpus.from_string(self.input_str)
		self.assertEqual(len(corpus.passages), 2)
		self.assertEqual(corpus.passages[0].urn.to_string(), "urn:cts:latinLit:phi0959.phi006:1.1")
		self.assertEqual(corpus.passages[0].text, "Lorem ipsum")
		self.assertEqual(corpus.passages[1].urn.to_string(), "urn:cts:latinLit:phi0959.phi006:1.2")
		self.assertEqual(corpus.passages[1].text, "Dolor sit amet.")

	def test_from_string_custom_delimiter(self):
		lines = [
			"urn:cts:latinLit:phi0959.phi006:1.1---Lorem ipsum",
			"urn:cts:latinLit:phi0959.phi006:1.2---Dolor sit amet."
		]
		input_str = "\n".join(lines)
		corpus = CitableCorpus.from_string(input_str, delimiter="---")
		self.assertEqual(len(corpus.passages), 2)
		self.assertEqual(corpus.passages[0].text, "Lorem ipsum")
		self.assertEqual(corpus.passages[1].text, "Dolor sit amet.")

	def test_from_string_with_whitespace(self):
		lines = [
			"  urn:cts:latinLit:phi0959.phi006:1.1  |  Lorem ipsum  ",
			"urn:cts:latinLit:phi0959.phi006:1.2|  Dolor sit amet."
		]
		input_str = "\n".join(lines)
		corpus = CitableCorpus.from_string(input_str)
		self.assertEqual(corpus.passages[0].text, "Lorem ipsum")
		self.assertEqual(corpus.passages[1].text, "Dolor sit amet.")

	def test_from_string_empty_input(self):
		corpus = CitableCorpus.from_string("")
		self.assertEqual(len(corpus.passages), 0)

if __name__ == "__main__":
	unittest.main()