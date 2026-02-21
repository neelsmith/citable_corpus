
import unittest
import os
from xml.dom import minidom
from abc import ABC
from citable_corpus.editionbuilders import (
    EditionBuilder, 
    tidy_ws, 
    extract_text, 
    TEIDiplomatic, 
    TEINormalized
)
from citable_corpus.corpus import CitableCorpus, CitablePassage
from citable_corpus.markupreader import TEIDivAbReader
from urn_citation import CtsUrn


class TestEditionBuilder(unittest.TestCase):
    """Test the abstract EditionBuilder base class."""
    
    def test_cannot_instantiate_abstract_class(self):
        """Test that EditionBuilder cannot be directly instantiated."""
        with self.assertRaises(TypeError):
            EditionBuilder()
    
    def test_is_abstract_base_class(self):
        """Test that EditionBuilder is an abstract base class."""
        self.assertTrue(issubclass(EditionBuilder, ABC))
    
    def test_has_required_abstract_methods(self):
        """Test that EditionBuilder defines required abstract method."""
        abstract_methods = EditionBuilder.__abstractmethods__
        self.assertIn('edition', abstract_methods)


class TestTidyWs(unittest.TestCase):
    """Test the tidy_ws helper function."""
    
    def test_single_space_unchanged(self):
        """Test that text with single spaces remains unchanged."""
        text = "Hello world test"
        result = tidy_ws(text)
        self.assertEqual(result, "Hello world test")
    
    def test_multiple_spaces_reduced(self):
        """Test that multiple spaces are reduced to single space."""
        text = "Hello    world     test"
        result = tidy_ws(text)
        self.assertEqual(result, "Hello world test")
    
    def test_leading_whitespace_removed(self):
        """Test that leading whitespace is removed."""
        text = "   Hello world"
        result = tidy_ws(text)
        self.assertEqual(result, "Hello world")
    
    def test_trailing_whitespace_removed(self):
        """Test that trailing whitespace is removed."""
        text = "Hello world   "
        result = tidy_ws(text)
        self.assertEqual(result, "Hello world")
    
    def test_newlines_normalized(self):
        """Test that newlines are converted to single spaces."""
        text = "Hello\nworld\ntest"
        result = tidy_ws(text)
        self.assertEqual(result, "Hello world test")
    
    def test_tabs_normalized(self):
        """Test that tabs are converted to single spaces."""
        text = "Hello\tworld\ttest"
        result = tidy_ws(text)
        self.assertEqual(result, "Hello world test")
    
    def test_mixed_whitespace_normalized(self):
        """Test that mixed whitespace is normalized."""
        text = "  Hello \n\t world  \r\n  test  "
        result = tidy_ws(text)
        self.assertEqual(result, "Hello world test")
    
    def test_empty_string(self):
        """Test handling of empty string."""
        text = ""
        result = tidy_ws(text)
        self.assertEqual(result, "")
    
    def test_only_whitespace(self):
        """Test handling of string with only whitespace."""
        text = "   \n\t  "
        result = tidy_ws(text)
        self.assertEqual(result, "")


class TestExtractText(unittest.TestCase):
    """Test the extract_text function."""
    
    def test_extract_simple_text(self):
        """Test extracting text from simple XML."""
        xml = "<p>Hello world</p>"
        doc = minidom.parseString(xml)
        result = extract_text(doc.documentElement, [], [])
        self.assertEqual(result, "Hello world")
    
    def test_extract_nested_text(self):
        """Test extracting text from nested XML elements."""
        xml = "<p>Hello <em>world</em> test</p>"
        doc = minidom.parseString(xml)
        result = extract_text(doc.documentElement, [], [])
        self.assertEqual(result, "Hello world test")
    
    def test_omit_single_element(self):
        """Test omitting content from specified element."""
        xml = "<p>Keep this <expan>omit this</expan> text</p>"
        doc = minidom.parseString(xml)
        result = extract_text(doc.documentElement, [], ['expan'])
        self.assertEqual(result, "Keep this  text")
    
    def test_omit_multiple_elements(self):
        """Test omitting content from multiple element types."""
        xml = "<p>Keep <expan>omit1</expan> this <note>omit2</note> text</p>"
        doc = minidom.parseString(xml)
        result = extract_text(doc.documentElement, [], ['expan', 'note'])
        self.assertEqual(result, "Keep  this  text")
    
    def test_omit_nested_elements(self):
        """Test omitting nested elements."""
        xml = "<p>Keep <choice><abbr>keep</abbr><expan>omit this</expan></choice> text</p>"
        doc = minidom.parseString(xml)
        result = extract_text(doc.documentElement, [], ['expan'])
        self.assertEqual(result, "Keep keep text")
    
    def test_empty_element(self):
        """Test extracting from empty element."""
        xml = "<p></p>"
        doc = minidom.parseString(xml)
        result = extract_text(doc.documentElement, [], [])
        self.assertEqual(result, "")
    
    def test_element_with_only_omitted_children(self):
        """Test element containing only omitted children."""
        xml = "<p><expan>omit</expan><note>omit</note></p>"
        doc = minidom.parseString(xml)
        result = extract_text(doc.documentElement, [], ['expan', 'note'])
        self.assertEqual(result, "")
    
    def test_mixed_content(self):
        """Test mixed text and element content."""
        xml = "<p>Text1<em>Text2</em>Text3<strong>Text4</strong>Text5</p>"
        doc = minidom.parseString(xml)
        result = extract_text(doc.documentElement, [], [])
        self.assertEqual(result, "Text1Text2Text3Text4Text5")
    
    def test_cumulation_parameter(self):
        """Test that cumulation list is properly used."""
        xml = "<p>Test text</p>"
        doc = minidom.parseString(xml)
        cumulation = ["Prefix: "]
        result = extract_text(doc.documentElement, cumulation, [])
        self.assertEqual(result, "Prefix: Test text")


class TestTEIDiplomatic(unittest.TestCase):
    """Test the TEIDiplomatic edition builder."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Simple TEI XML with abbreviations
        self.simple_tei = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <div n="1">
        <ab n="1">Text with <choice><abbr>abbr.</abbr><expan>abbreviation</expan></choice> here.</ab>
        <ab n="2">More <choice><abbr>txt</abbr><expan>text</expan></choice> content.</ab>
      </div>
    </body>
  </text>
</TEI>"""
        
        self.urnbase = "urn:cts:latinLit:phi0959.phi006:"
        
    def test_is_edition_builder_subclass(self):
        """Test that TEIDiplomatic is a subclass of EditionBuilder."""
        self.assertTrue(issubclass(TEIDiplomatic, EditionBuilder))
    
    def test_edition_omits_expan(self):
        """Test that diplomatic edition omits expan elements."""
        # Create corpus from TEI
        corpus = TEIDivAbReader.corpus(self.simple_tei, self.urnbase)
        
        # Build diplomatic edition
        diplomatic = TEIDiplomatic.edition(corpus)
        
        # Check result is a CitableCorpus
        self.assertIsInstance(diplomatic, CitableCorpus)
        self.assertEqual(len(diplomatic.passages), 2)
        
        # Check that expanded forms are omitted
        self.assertIn("abbr.", diplomatic.passages[0].text)
        self.assertNotIn("abbreviation", diplomatic.passages[0].text)
        
        self.assertIn("txt", diplomatic.passages[1].text)
        self.assertNotIn("text", diplomatic.passages[1].text)
    
    def test_edition_sets_diplomatic_exemplar(self):
        """Test that diplomatic edition sets exemplar to 'diplomatic'."""
        corpus = TEIDivAbReader.corpus(self.simple_tei, self.urnbase)
        diplomatic = TEIDiplomatic.edition(corpus)
        
        # Check that URNs have diplomatic exemplar
        for passage in diplomatic.passages:
            self.assertEqual(passage.urn.exemplar, "diplomatic")
    
    def test_edition_preserves_passage_count(self):
        """Test that diplomatic edition preserves number of passages."""
        corpus = TEIDivAbReader.corpus(self.simple_tei, self.urnbase)
        diplomatic = TEIDiplomatic.edition(corpus)
        
        self.assertEqual(len(corpus.passages), len(diplomatic.passages))
    
    def test_edition_with_simple_text(self):
        """Test diplomatic edition with simple text without abbreviations."""
        simple_xml = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <div n="1">
        <ab n="1">Simple text only.</ab>
      </div>
    </body>
  </text>
</TEI>"""
        corpus = TEIDivAbReader.corpus(simple_xml, self.urnbase)
        diplomatic = TEIDiplomatic.edition(corpus)
        
        self.assertEqual(len(diplomatic.passages), 1)
        self.assertIn("Simple text only.", diplomatic.passages[0].text)
    
    def test_edition_maintains_urn_structure(self):
        """Test that diplomatic edition maintains URN work hierarchy."""
        corpus = TEIDivAbReader.corpus(self.simple_tei, self.urnbase)
        diplomatic = TEIDiplomatic.edition(corpus)
        
        # Check that base URN structure is maintained
        for orig, dipl in zip(corpus.passages, diplomatic.passages):
            self.assertEqual(orig.urn.work, dipl.urn.work)
            self.assertEqual(orig.urn.passage, dipl.urn.passage)


class TestTEINormalized(unittest.TestCase):
    """Test the TEINormalized edition builder."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Simple TEI XML with abbreviations
        self.simple_tei = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <div n="1">
        <ab n="1">Text with <choice><abbr>abbr.</abbr><expan>abbreviation</expan></choice> here.</ab>
        <ab n="2">More <choice><abbr>txt</abbr><expan>text</expan></choice> content.</ab>
      </div>
    </body>
  </text>
</TEI>"""
        
        self.urnbase = "urn:cts:latinLit:phi0959.phi006:"
    
    def test_is_edition_builder_subclass(self):
        """Test that TEINormalized is a subclass of EditionBuilder."""
        self.assertTrue(issubclass(TEINormalized, EditionBuilder))
    
    def test_edition_omits_abbr(self):
        """Test that normalized edition omits abbr elements."""
        # Create corpus from TEI
        corpus = TEIDivAbReader.corpus(self.simple_tei, self.urnbase)
        
        # Build normalized edition
        normalized = TEINormalized.edition(corpus)
        
        # Check result is a CitableCorpus
        self.assertIsInstance(normalized, CitableCorpus)
        self.assertEqual(len(normalized.passages), 2)
        
        # Check that abbreviations are omitted and expansions kept
        self.assertNotIn("abbr.", normalized.passages[0].text)
        self.assertIn("abbreviation", normalized.passages[0].text)
        
        self.assertNotIn("txt", normalized.passages[1].text)
        self.assertIn("text", normalized.passages[1].text)
    
    def test_edition_sets_normalized_exemplar(self):
        """Test that normalized edition sets exemplar to 'normalized'."""
        corpus = TEIDivAbReader.corpus(self.simple_tei, self.urnbase)
        normalized = TEINormalized.edition(corpus)
        
        # Check that URNs have normalized exemplar
        for passage in normalized.passages:
            self.assertEqual(passage.urn.exemplar, "normalized")
    
    def test_edition_preserves_passage_count(self):
        """Test that normalized edition preserves number of passages."""
        corpus = TEIDivAbReader.corpus(self.simple_tei, self.urnbase)
        normalized = TEINormalized.edition(corpus)
        
        self.assertEqual(len(corpus.passages), len(normalized.passages))
    
    def test_edition_with_simple_text(self):
        """Test normalized edition with simple text without abbreviations."""
        simple_xml = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <div n="1">
        <ab n="1">Simple text only.</ab>
      </div>
    </body>
  </text>
</TEI>"""
        corpus = TEIDivAbReader.corpus(simple_xml, self.urnbase)
        normalized = TEINormalized.edition(corpus)
        
        self.assertEqual(len(normalized.passages), 1)
        self.assertIn("Simple text only.", normalized.passages[0].text)
    
    def test_edition_maintains_urn_structure(self):
        """Test that normalized edition maintains URN work hierarchy."""
        corpus = TEIDivAbReader.corpus(self.simple_tei, self.urnbase)
        normalized = TEINormalized.edition(corpus)
        
        # Check that base URN structure is maintained
        for orig, norm in zip(corpus.passages, normalized.passages):
            self.assertEqual(orig.urn.work, norm.urn.work)
            self.assertEqual(orig.urn.passage, norm.urn.passage)


class TestEditionComparison(unittest.TestCase):
    """Test comparing diplomatic and normalized editions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tei_xml = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <div n="1">
        <ab n="1">The <choice><abbr>dr.</abbr><expan>doctor</expan></choice> arrived.</ab>
      </div>
    </body>
  </text>
</TEI>"""
        self.urnbase = "urn:cts:latinLit:phi0959.phi006:"
    
    def test_diplomatic_vs_normalized_content(self):
        """Test that diplomatic and normalized editions differ as expected."""
        corpus = TEIDivAbReader.corpus(self.tei_xml, self.urnbase)
        
        diplomatic = TEIDiplomatic.edition(corpus)
        normalized = TEINormalized.edition(corpus)
        
        # Both should have same number of passages
        self.assertEqual(len(diplomatic.passages), len(normalized.passages))
        
        # Content should differ
        dipl_text = diplomatic.passages[0].text
        norm_text = normalized.passages[0].text
        
        self.assertNotEqual(dipl_text, norm_text)
        self.assertIn("dr.", dipl_text)
        self.assertNotIn("doctor", dipl_text)
        self.assertNotIn("dr.", norm_text)
        self.assertIn("doctor", norm_text)
    
    def test_diplomatic_vs_normalized_exemplars(self):
        """Test that diplomatic and normalized have different exemplars."""
        corpus = TEIDivAbReader.corpus(self.tei_xml, self.urnbase)
        
        diplomatic = TEIDiplomatic.edition(corpus)
        normalized = TEINormalized.edition(corpus)
        
        self.assertEqual(diplomatic.passages[0].urn.exemplar, "diplomatic")
        self.assertEqual(normalized.passages[0].urn.exemplar, "normalized")
    
    def test_both_editions_share_base_urn(self):
        """Test that both editions share the base URN structure."""
        corpus = TEIDivAbReader.corpus(self.tei_xml, self.urnbase)
        
        diplomatic = TEIDiplomatic.edition(corpus)
        normalized = TEINormalized.edition(corpus)
        
        # Same work
        self.assertEqual(diplomatic.passages[0].urn.work, normalized.passages[0].urn.work)
        # Same passage
        self.assertEqual(diplomatic.passages[0].urn.passage, normalized.passages[0].urn.passage)


if __name__ == '__main__':
    unittest.main()
