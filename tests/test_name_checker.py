import unittest
from scanner_source.scan_identifiers import CheckTypeVersusPlurality
class NameCheckerTests(unittest.TestCase):
    def test_identifier_with_no_plural_collection_problems(self):
        identifier_with_no_plurality_problems = {'type': 'vector', 'name': 'names','array':0, 'pointer':0}
        print(CheckTypeVersusPlurality(identifier_with_no_plurality_problems))
        self.assertEqual("", CheckTypeVersusPlurality(identifier_with_no_plurality_problems))
    
    def test_plural_identifier_without_collection_type(self):
        plural_identifier_no_collection = {'type': 'int', 'name': 'tokens','array':0, 'pointer':0}
        assert "Plural identifier tokens has a non-collection type int", CheckTypeVersusPlurality(plural_identifier_no_collection)
    
    def test_singular_identifier_with_collection_type(self):
        singular_identifier_with_collection = {'type': 'vector', 'name': 'token', 'array':0, 'pointer':0}
        assert "Singular identifier token has a collection type vector", CheckTypeVersusPlurality(singular_identifier_with_collection)