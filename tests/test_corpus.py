
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

	def test_len_with_passages(self):
		"""Test __len__ method returns correct count."""
		corpus = CitableCorpus.from_string(self.input_str)
		self.assertEqual(len(corpus), 2)
		self.assertEqual(len(corpus), len(corpus.passages))

	def test_len_empty_corpus(self):
		"""Test __len__ method with empty corpus."""
		corpus = CitableCorpus.from_string("")
		self.assertEqual(len(corpus), 0)

	def test_len_with_cex_file(self):
		"""Test __len__ method with corpus loaded from CEX file."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		# Hyginus corpus has 1234 passages
		self.assertEqual(len(corpus), 1234)
		self.assertEqual(len(corpus), len(corpus.passages))

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


	def test_retrieve_with_version_urn(self):
		"""Test retrieving passages using a version-level URN."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Retrieve using work-level URN (without specific passage)
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:")
		results = corpus.retrieve(ref)
		
		# Should return all passages in the corpus
		self.assertEqual(len(results), len(corpus.passages))

	def test_retrieve_nonexistent_passage(self):
		"""Test retrieving a passage that doesn't exist."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Try to retrieve a non-existent passage
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.999")
		results = corpus.retrieve(ref)
		
		self.assertEqual(len(results), 0)

	def test_retrieve_range_simple(self):
		"""Test retrieving a range of passages."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Retrieve a range from pr.1 to pr.5
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.1-pr.5")
		results = corpus.retrieve_range(ref)
		
		# Should get 5 passages (pr.1, pr.2, pr.3, pr.4, pr.5)
		self.assertEqual(len(results), 5)
		self.assertEqual(str(results[0].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.1")
		self.assertEqual(str(results[-1].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.5")

	def test_retrieve_range_larger_span(self):
		"""Test retrieving a larger range of passages."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Retrieve a range from pr.10 to pr.20
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.10-pr.20")
		results = corpus.retrieve_range(ref)
		
		# Should get 11 passages (pr.10 through pr.20 inclusive)
		self.assertEqual(len(results), 11)
		self.assertEqual(str(results[0].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.10")
		self.assertEqual(str(results[-1].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.20")
		
		# Verify all passages are in order
		for i, passage in enumerate(results):
			expected_num = 10 + i
			self.assertIn(f"pr.{expected_num}", str(passage.urn))

	def test_retrieve_range_cross_sections(self):
		"""Test retrieving a range that spans different sections."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Retrieve from the title to the preface (t.1 to pr.2)
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:t.1-pr.2")
		results = corpus.retrieve_range(ref)
		
		# Should include t.1, pr.1, and pr.2
		self.assertGreaterEqual(len(results), 3)
		self.assertEqual(str(results[0].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:t.1")
		self.assertEqual(str(results[-1].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.2")

	def test_retrieve_range_single_passage(self):
		"""Test retrieving a range where start equals end."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Retrieve a "range" that's just one passage
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.15-pr.15")
		results = corpus.retrieve_range(ref)
		
		self.assertEqual(len(results), 1)
		self.assertEqual(str(results[0].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.15")

	def test_retrieve_range_nonexistent(self):
		"""Test retrieving a range where one or both endpoints don't exist."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Try to retrieve a range with non-existent endpoints
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.999-pr.1000")
		results = corpus.retrieve_range(ref)
		
		# Should return empty list
		self.assertEqual(len(results), 0)

	def test_retrieve_range_with_non_range_urn(self):
		"""Test that retrieve_range raises an error for non-range URNs."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Try to use retrieve_range with a non-range URN
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.1")
		
		with self.assertRaises(ValueError) as context:
			corpus.retrieve_range(ref)
		
		self.assertIn("not a range", str(context.exception))

	def test_retrieve_with_range_urn(self):
		"""Test that retrieve method can handle range URNs (delegates to retrieve_range)."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Use retrieve with a range URN (should delegate to retrieve_range)
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.1-pr.3")
		results = corpus.retrieve(ref)
		
		# Should get 3 passages
		self.assertEqual(len(results), 3)
		self.assertEqual(str(results[0].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.1")
		self.assertEqual(str(results[-1].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.3")

if __name__ == "__main__":
	unittest.main()