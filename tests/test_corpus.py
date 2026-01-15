
import unittest
import os
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
		self.test_data_dir = os.path.join(os.path.dirname(__file__), "data")

	def test_from_string_default_delimiter(self):
		corpus = CitableCorpus.from_string(self.input_str)
		self.assertEqual(len(corpus.passages), 2)
		self.assertEqual(str(corpus.passages[0].urn), "urn:cts:latinLit:phi0959.phi006:1.1")
		self.assertEqual(corpus.passages[0].text, "Lorem ipsum")
		self.assertEqual(str(corpus.passages[1].urn), "urn:cts:latinLit:phi0959.phi006:1.2")
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

	def test_from_cex_file_hyginus(self):
		"""Test loading a CEX file with Hyginus data."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Verify corpus is not empty
		self.assertGreater(len(corpus.passages), 0)
		
		# Verify first passage
		first_passage = corpus.passages[0]
		self.assertEqual(str(first_passage.urn), "urn:cts:latinLit:stoa1263.stoa001.hc:t.1")
		self.assertEqual(first_passage.text, "EXCERPTA EX HYGINI GENEALOGIIS, VOLGO FABVLAE.")
		
		# Verify a passage from the middle
		second_passage = corpus.passages[1]
		self.assertEqual(str(second_passage.urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.1")
		self.assertTrue(second_passage.text.startswith("Ex Caligine Chaos:"))

	def test_from_cex_file_burneysample(self):
		"""Test loading a CEX file with Burney sample data."""
		burney_path = os.path.join(self.test_data_dir, "burneysample.cex")
		corpus = CitableCorpus.from_cex_file(burney_path)
		
		# Verify corpus is not empty
		self.assertGreater(len(corpus.passages), 0)
		
		# Verify all passages have valid URNs and text
		for passage in corpus.passages:
			self.assertIsNotNone(passage.urn)
			self.assertIsNotNone(passage.text)
			self.assertIsInstance(passage.urn, CtsUrn)
			self.assertIsInstance(passage.text, str)

	def test_from_cex_file_custom_delimiter(self):
		"""Test that custom delimiter parameter works with CEX files."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path, delimiter="|")
		
		# Should work fine with default delimiter
		self.assertGreater(len(corpus.passages), 0)
		first_passage = corpus.passages[0]
		self.assertEqual(first_passage.text, "EXCERPTA EX HYGINI GENEALOGIIS, VOLGO FABVLAE.")

	def test_from_cex_url_hmt(self):
		"""Test loading CEX data from Homer Multitext Archive URL."""
		url = "https://raw.githubusercontent.com/homermultitext/hmt-archive/refs/heads/master/releases-cex/hmt-2024c.cex"
		corpus = CitableCorpus.from_cex_url(url)
		
		# Verify corpus is not empty
		self.assertGreater(len(corpus.passages), 0)
		
		# Verify all passages have valid URNs and text
		for passage in corpus.passages:
			self.assertIsNotNone(passage.urn)
			self.assertIsNotNone(passage.text)
			self.assertIsInstance(passage.urn, CtsUrn)
			self.assertIsInstance(passage.text, str)
		
		# The HMT corpus should be substantial
		self.assertGreater(len(corpus.passages), 100)

	def test_from_cex_url_hmt_passages_structure(self):
		"""Test specific passages from HMT to verify correct parsing."""
		url = "https://raw.githubusercontent.com/homermultitext/hmt-archive/refs/heads/master/releases-cex/hmt-2024c.cex"
		corpus = CitableCorpus.from_cex_url(url)
		
		# Verify passages contain expected content types
		# HMT contains Iliad passages which should have URNs starting with urn:cts:greekLit:
		iliad_passages = [p for p in corpus.passages if "greekLit" in str(p.urn)]
		self.assertGreater(len(iliad_passages), 0)
		
		# Verify text content is not empty
		for passage in corpus.passages[:10]:
			self.assertTrue(len(passage.text) > 0)

	def test_from_cex_url_custom_delimiter(self):
		"""Test that custom delimiter parameter works with URLs."""
		url = "https://raw.githubusercontent.com/homermultitext/hmt-archive/refs/heads/master/releases-cex/hmt-2024c.cex"
		corpus = CitableCorpus.from_cex_url(url, delimiter="|")
		
		# Should work fine with default delimiter
		self.assertGreater(len(corpus.passages), 0)

if __name__ == "__main__":
	unittest.main()