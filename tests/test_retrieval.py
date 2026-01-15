
import unittest
import os
from citable_corpus.corpus import CitableCorpus
from citable_corpus.passage import CitablePassage
from urn_citation import CtsUrn
#from pathlib import Path

class TestCitableCorpus(unittest.TestCase):
	def setUp(self):
		self.test_data_dir = os.path.join(os.path.dirname(__file__), "data")
		
        
		
	def test_retrieve_single_passage(self):
		"""Test retrieving a single passage by exact URN."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Retrieve a specific passage
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.1")
		results = corpus.retrieve(ref)
		
		self.assertEqual(len(results), 1)
		self.assertEqual(str(results[0].urn), "urn:cts:latinLit:stoa1263.stoa001.hc:pr.1")
		self.assertTrue(results[0].text.startswith("Ex Caligine Chaos:"))
		
	def test_retrieve_multiple_passages_by_work(self):
		"""Test retrieving multiple passages using a work-level URN."""
		hyginus_path = os.path.join(self.test_data_dir, "hyginus.cex")
		corpus = CitableCorpus.from_cex_file(hyginus_path)
		
		# Retrieve all passages from the preface section (pr.)
		ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr")
		results = corpus.retrieve(ref)
		
		# There should be multiple preface passages (pr.1 through pr.41)
		self.assertGreater(len(results), 20)
		
		# Verify all results are from the preface section
		for passage in results:
			self.assertTrue("pr." in str(passage.urn) or str(passage.urn).endswith(":pr"))
        