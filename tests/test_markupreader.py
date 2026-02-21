
import unittest
import os
from abc import ABC
from citable_corpus.markupreader import MarkupReader, TEIDivAbReader
from citable_corpus.corpus import CitableCorpus


class TestMarkupReader(unittest.TestCase):
    """Test the abstract MarkupReader base class."""
    
    def test_cannot_instantiate_abstract_class(self):
        """Test that MarkupReader cannot be directly instantiated."""
        with self.assertRaises(TypeError):
            MarkupReader()
    
    def test_is_abstract_base_class(self):
        """Test that MarkupReader is an abstract base class."""
        self.assertTrue(issubclass(MarkupReader, ABC))
    
    def test_has_required_abstract_methods(self):
        """Test that MarkupReader defines required abstract methods."""
        abstract_methods = MarkupReader.__abstractmethods__
        self.assertIn('cex', abstract_methods)
        self.assertIn('corpus', abstract_methods)


class TestTEIDivAbReader(unittest.TestCase):
    """Test the TEIDivAbReader implementation with static methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "data")
        
        # Simple test XML with basic structure
        self.simple_xml = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <div n="1">
        <ab n="1">First passage text.</ab>
        <ab n="2">Second passage text.</ab>
      </div>
    </body>
  </text>
</TEI>"""
        
        # XML with multiple divs
        self.multi_div_xml = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <div n="1">
        <ab n="1">Chapter 1, verse 1.</ab>
        <ab n="2">Chapter 1, verse 2.</ab>
      </div>
      <div n="2">
        <ab n="1">Chapter 2, verse 1.</ab>
        <ab n="2">Chapter 2, verse 2.</ab>
      </div>
    </body>
  </text>
</TEI>"""
        
        # XML with special characters and formatting
        self.formatted_xml = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <div n="1">
        <ab n="1">Text with
        newlines and  multiple   spaces.</ab>
        <ab n="2">Text with <choice><abbr>abbr.</abbr><expan>abbreviation</expan></choice> markup.</ab>
      </div>
    </body>
  </text>
</TEI>"""
        
        self.urnbase = "urn:cts:latinLit:phi0959.phi006:"
    
    def test_is_markup_reader_subclass(self):
        """Test that TEIDivAbReader is a subclass of MarkupReader."""
        self.assertTrue(issubclass(TEIDivAbReader, MarkupReader))
    
    def test_cex_simple_structure(self):
        """Test cex() static method with simple XML structure."""
        cex_output = TEIDivAbReader.cex(self.simple_xml, self.urnbase)
        
        # Split into lines and verify
        lines = cex_output.strip().split("\n")
        self.assertEqual(len(lines), 2)
        
        # Check first line
        self.assertIn("urn:cts:latinLit:phi0959.phi006:1.1|", lines[0])
        self.assertIn("First passage text.", lines[0])
        
        # Check second line
        self.assertIn("urn:cts:latinLit:phi0959.phi006:1.2|", lines[1])
        self.assertIn("Second passage text.", lines[1])
    
    def test_cex_multiple_divs(self):
        """Test cex() method with multiple div elements."""
        cex_output = TEIDivAbReader.cex(self.multi_div_xml, self.urnbase)
        
        lines = cex_output.strip().split("\n")
        self.assertEqual(len(lines), 4)
        
        # Check URN structure for different divs
        self.assertIn("urn:cts:latinLit:phi0959.phi006:1.1|", lines[0])
        self.assertIn("urn:cts:latinLit:phi0959.phi006:1.2|", lines[1])
        self.assertIn("urn:cts:latinLit:phi0959.phi006:2.1|", lines[2])
        self.assertIn("urn:cts:latinLit:phi0959.phi006:2.2|", lines[3])
    
    def test_cex_whitespace_normalization(self):
        """Test that cex() normalizes whitespace correctly."""
        cex_output = TEIDivAbReader.cex(self.formatted_xml, self.urnbase)
        
        lines = cex_output.strip().split("\n")
        
        # Check that newlines are replaced with spaces
        self.assertNotIn("\n", lines[0].split("|")[1])
        self.assertNotIn("\r", lines[0].split("|")[1])
        
        # Check that multiple spaces are normalized to single space
        text_part = lines[0].split("|")[1]
        self.assertNotIn("  ", text_part)  # No double spaces
    
    def test_cex_preserves_markup(self):
        """Test that cex() preserves XML markup within ab elements."""
        cex_output = TEIDivAbReader.cex(self.formatted_xml, self.urnbase)
        
        lines = cex_output.strip().split("\n")
        
        # Second line should contain the choice/abbr/expan markup (with namespace prefix)
        self.assertIn("choice>", lines[1])  # Check for the tag regardless of namespace prefix
        self.assertIn("abbr>", lines[1])
        self.assertIn("expan>", lines[1])
    
    def test_corpus_returns_citable_corpus(self):
        """Test that corpus() static method returns a CitableCorpus object."""
        corpus = TEIDivAbReader.corpus(self.simple_xml, self.urnbase)
        
        self.assertIsInstance(corpus, CitableCorpus)
    
    def test_corpus_has_correct_passage_count(self):
        """Test that corpus() returns correct number of passages."""
        corpus = TEIDivAbReader.corpus(self.multi_div_xml, self.urnbase)
        
        self.assertEqual(len(corpus.passages), 4)
    
    def test_corpus_passages_have_correct_urns(self):
        """Test that corpus passages have correctly formed URNs."""
        corpus = TEIDivAbReader.corpus(self.simple_xml, self.urnbase)
        
        self.assertEqual(str(corpus.passages[0].urn), "urn:cts:latinLit:phi0959.phi006:1.1")
        self.assertEqual(str(corpus.passages[1].urn), "urn:cts:latinLit:phi0959.phi006:1.2")
    
    def test_corpus_passages_have_correct_text(self):
        """Test that corpus passages contain the expected text."""
        corpus = TEIDivAbReader.corpus(self.simple_xml, self.urnbase)
        
        # Text should contain the ab content (with XML tags)
        self.assertIn("First passage text.", corpus.passages[0].text)
        self.assertIn("Second passage text.", corpus.passages[1].text)
    
    def test_empty_div(self):
        """Test handling of div elements with no ab children."""
        empty_div_xml = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <div n="1">
      </div>
    </body>
  </text>
</TEI>"""
        cex_output = TEIDivAbReader.cex(empty_div_xml, self.urnbase)
        
        # Should produce empty string or no lines
        self.assertEqual(cex_output.strip(), "")
    
    def test_no_divs(self):
        """Test handling of XML with no div elements."""
        no_div_xml = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
    </body>
  </text>
</TEI>"""
        cex_output = TEIDivAbReader.cex(no_div_xml, self.urnbase)
        
        self.assertEqual(cex_output.strip(), "")
    
    def test_with_real_septuagint_file(self):
        """Test with the actual Septuagint Latin Genesis XML file."""
        xml_path = os.path.join(self.test_data_dir, "septuagint_latin_genesis.xml")
        
        if os.path.exists(xml_path):
            with open(xml_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            corpus = TEIDivAbReader.corpus(xml_content, "urn:cts:greekLit:tlg0527.tlg001.lat:")
            
            # Should have passages
            self.assertGreater(len(corpus.passages), 0)
            
            # First passage should have proper URN structure
            first_urn_str = str(corpus.passages[0].urn)
            self.assertTrue(first_urn_str.startswith("urn:cts:greekLit:tlg0527.tlg001.lat:"))
            
            # Passages should have text content
            for passage in corpus.passages[:5]:  # Check first 5
                self.assertIsNotNone(passage.text)
                self.assertGreater(len(passage.text), 0)
    
    def test_urnbase_format(self):
        """Test that urnbase should not have a trailing dot."""
        # URNbase should not end with a dot; the code concatenates with '.'
        cex_output = TEIDivAbReader.cex(self.simple_xml, self.urnbase)
        
        lines = cex_output.strip().split("\n")
        # Verify URNs are properly formed with correct number of colons
        for line in lines:
            urn_part = line.split("|")[0]
            colon_count = urn_part.count(":")
            self.assertEqual(colon_count, 4, f"URN should have 4 colons, got {colon_count} in {urn_part}")
    
    def test_cex_output_format(self):
        """Test that CEX output has correct delimiter format."""
        cex_output = TEIDivAbReader.cex(self.simple_xml, self.urnbase)
        
        lines = cex_output.strip().split("\n")
        for line in lines:
            # Each line should have exactly one pipe delimiter separating URN and text
            parts = line.split("|")
            self.assertGreaterEqual(len(parts), 2, "CEX line should have at least URN|text")
            self.assertTrue(parts[0].startswith("urn:"), "First part should be a URN")
    
    def test_cex_with_different_baseurn(self):
        """Test cex() with a different base URN."""
        baseurn = "urn:cts:greekLit:tlg0012.tlg001:"
        cex_output = TEIDivAbReader.cex(self.simple_xml, baseurn)
        
        lines = cex_output.strip().split("\n")
        self.assertIn("urn:cts:greekLit:tlg0012.tlg001:1.1|", lines[0])
        self.assertIn("urn:cts:greekLit:tlg0012.tlg001:1.2|", lines[1])
    
    def test_corpus_integration(self):
        """Test that corpus() correctly uses cex() output."""
        # Test that corpus() is properly calling cex() and parsing result
        corpus = TEIDivAbReader.corpus(self.multi_div_xml, self.urnbase)
        
        # Verify all passages are present
        self.assertEqual(len(corpus.passages), 4)
        
        # Verify passages match what cex() produces
        cex_output = TEIDivAbReader.cex(self.multi_div_xml, self.urnbase)
        cex_lines = cex_output.strip().split("\n")
        
        for i, line in enumerate(cex_lines):
            urn_str, text = line.split("|", 1)
            self.assertEqual(str(corpus.passages[i].urn), urn_str)
            self.assertIn(text, corpus.passages[i].text)


if __name__ == '__main__':
    unittest.main()
