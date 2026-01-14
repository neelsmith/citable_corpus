
import unittest
from urn_citation import CtsUrn
from citable_corpus import CitablePassage


class TestCitablePassage(unittest.TestCase):
    def setUp(self):
        self.urn_str = "urn:cts:latinLit:phi0959.phi006:1.1"
        self.urn = CtsUrn.from_string(self.urn_str)
        self.text = "Lorem ipsum dolor sit amet."

    def test_init(self):
        passage = CitablePassage(urn=self.urn, text=self.text)
        self.assertEqual(passage.urn, self.urn)
        self.assertEqual(passage.text, self.text)

    def test_str(self):
        passage = CitablePassage(urn=self.urn, text=self.text)
        self.assertEqual(str(passage), f"{self.urn}: {self.text}")

    def test_from_string_default_delimiter(self):
        s = f"{self.urn_str}|{self.text}"
        passage = CitablePassage.from_string(s)
        self.assertEqual(passage.urn.to_string(), self.urn_str)
        self.assertEqual(passage.text, self.text)

    def test_from_string_custom_delimiter(self):
        s = f"{self.urn_str}---{self.text}"
        passage = CitablePassage.from_string(s, delimiter="---")
        self.assertEqual(passage.urn.to_string(), self.urn_str)
        self.assertEqual(passage.text, self.text)

    def test_from_string_with_whitespace(self):
        s = f"  {self.urn_str}  |  {self.text}  "
        passage = CitablePassage.from_string(s)
        self.assertEqual(passage.urn.to_string(), self.urn_str)
        self.assertEqual(passage.text, self.text)

    def test_from_string_invalid_format(self):
        s = self.urn_str  # No delimiter
        with self.assertRaises(ValueError):
            CitablePassage.from_string(s)

    def test_attribute_types(self):
        passage = CitablePassage(urn=self.urn, text=self.text)
        self.assertIsInstance(passage.urn, CtsUrn)
        self.assertIsInstance(passage.text, str)

if __name__ == "__main__":
    unittest.main()
