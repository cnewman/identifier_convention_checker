import unittest
from scanner_source.scan_identifiers import CheckTypeVersusPlurality, CheckHeuristics, CheckForDictionaryTerms
class NameCheckerTests(unittest.TestCase):
    
    #Plurality tests
    def test_identifier_with_no_plural_collection_problems(self):
        identifier_with_no_plurality_problems = {'type': 'vector', 'name': 'names','array':0, 'pointer':0}
        print(CheckTypeVersusPlurality(identifier_with_no_plurality_problems))
        self.assertEqual(None, CheckTypeVersusPlurality(identifier_with_no_plurality_problems))
    def test_plural_identifier_without_collection_type(self):
        plural_identifier_no_collection = {'type': 'int', 'name': 'tokens','array':0, 'pointer':0}
        self.assertEqual("Plural identifier tokens has a non-collection type int", CheckTypeVersusPlurality(plural_identifier_no_collection))
    def test_singular_identifier_with_collection_type(self):
        singular_identifier_with_collection = {'type': 'vector', 'name': 'token', 'array':0, 'pointer':0}
        self.assertEqual("Singular identifier token has a collection type vector", CheckTypeVersusPlurality(singular_identifier_with_collection))
    
    #Heuristics tests
    def test_mixed_heuristics_capital_underscore(self):
        identifier_with_mixed_capital_underscore_heuristics = {'type': 'int', 'name': 'tokenMax_count','array':0, 'pointer':0}
        self.assertEqual("tokenMax_count mixes styles, containing underscores,upper case letters. Please follow the style guidelines.", 
                         CheckHeuristics(identifier_with_mixed_capital_underscore_heuristics)) 
    def test_consistent_heuristics(self):
        identifier_with_mixed_capital_underscore_heuristics = {'type': 'int', 'name': 'Token','array':0, 'pointer':0}
        self.assertEqual (None, CheckHeuristics(identifier_with_mixed_capital_underscore_heuristics))
    
    #Dictionary term tests
    def test_identifier_with_dictionary_term_misuse(self):
        identifier_with_mixed_capital_underscore_heuristics = {'type': 'int', 'name': 'tkn','array':0, 'pointer':0}
        self.assertEqual ('tkn is not a dictionary term.', CheckForDictionaryTerms(identifier_with_mixed_capital_underscore_heuristics))
    def test_identifier_with_good_dictionary_term_usage(self):
        identifier_with_mixed_capital_underscore_heuristics = {'type': 'int', 'name': 'token','array':0, 'pointer':0}
        self.assertEqual (None, CheckForDictionaryTerms(identifier_with_mixed_capital_underscore_heuristics))
    