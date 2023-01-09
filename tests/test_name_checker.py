import unittest
from identifier_analysis_src.scan_identifiers import CheckTypeVersusPlurality, CheckHeuristics, CheckForDictionaryTerms, CheckForGenericTerms, CheckIfIdentifierAndTypeNamesMatch, CheckForMagicNumbers, CheckForIdentifierLength
from colorama import init
from strip_ansi import strip_ansi
from identifier_analysis_src.code_antipatterns import antiPatternTypes
class NameCheckerTests(unittest.TestCase):
    
    #Plurality tests
    def test_plural_identifier_with_no_plural_collection_problems(self):
        identifier_with_no_plurality_problems = {'context':'DECLARATION','type': 'vector', 'name': 'names','array':0, 'pointer':0}
        self.assertEqual(None, CheckTypeVersusPlurality(identifier_with_no_plurality_problems))
    def test_singular_identifier_with_no_plural_collection_problems(self):
        identifier_with_no_plurality_problems = {'context':'PARAMETER','type': 'int', 'name': 'argc','array':0, 'pointer':0}
        self.assertEqual(None, CheckTypeVersusPlurality(identifier_with_no_plurality_problems))
    def test_plural_identifier_without_collection_type(self):
        plural_identifier_no_collection = {'context':'DECLARATION','type': 'int', 'name': 'tokens','array':0, 'pointer':0}
        self.assertEqual(antiPatternTypes["PLURAL MISUSE"].format(identifierName="tokens", typename="int"), 
                        strip_ansi(CheckTypeVersusPlurality(plural_identifier_no_collection)))
    def test_singular_identifier_with_collection_type(self):
        singular_identifier_with_collection = {'context':'DECLARATION','type': 'vector', 'name': 'token', 'array':0, 'pointer':0}
        self.assertEqual(antiPatternTypes["SINGULAR MISUSE"].format(identifierName="token", typename="vector"), 
                        strip_ansi(CheckTypeVersusPlurality(singular_identifier_with_collection)))
    def test_singular_identifier_with_pointer_collection_type(self):
        singular_identifier_with_pointer_collection = {'context':'DECLARATION','type': 'int*', 'name': 'token', 'array':0, 'pointer':1}
        self.assertEqual(antiPatternTypes["SINGULAR MISUSE"].format(identifierName="token", typename="int*"), 
                        strip_ansi(CheckTypeVersusPlurality(singular_identifier_with_pointer_collection)))
    def test_singular_identifier_with_array_collection_type(self):
        singular_identifier_with_array_collection = {'context':'DECLARATION','type': 'unsigned short int', 'name': 'token[]', 'array':1, 'pointer':0}
        self.assertEqual(antiPatternTypes["SINGULAR MISUSE"].format(identifierName="token[]", typename="unsigned short int"),
                        strip_ansi(CheckTypeVersusPlurality(singular_identifier_with_array_collection)))
    def test_should_skip_function_names(self):
        singular_identifier_with_array_collection = {'context':'FUNCTION', 'type': 'unsigned short int', 'name': 'token[]', 'array':1, 'pointer':0}
        self.assertEqual(None, CheckTypeVersusPlurality(singular_identifier_with_array_collection))

    #Heuristics tests
    def test_mixed_heuristics_capital_underscore(self):
        identifier_with_mixed_capital_underscore_heuristics = {'context':'DECLARATION','type': 'int', 'name': 'tokenMax_count','array':0, 'pointer':0}
        self.assertEqual(antiPatternTypes["MIXED STYLES"].format(identifierName="tokenMax_count", heuristics="underscores,upper case letters"), 
                         strip_ansi(CheckHeuristics(identifier_with_mixed_capital_underscore_heuristics)) )
    def test_consistent_heuristics(self):
        identifier_with_mixed_capital_underscore_heuristics = {'context':'DECLARATION','type': 'int', 'name': 'Token','array':0, 'pointer':0}
        self.assertEqual (None, CheckHeuristics(identifier_with_mixed_capital_underscore_heuristics))
    
    #Dictionary term tests
    def test_identifier_with_dictionary_term_misuse(self):
        identifier_with_dictionary_term_misuse = {'context':'DECLARATION','type': 'int', 'name': 'tkn','array':0, 'pointer':0}
        self.assertEqual (antiPatternTypes["DICTIONARY TERM"].format(identifierName="tkn"),
                          strip_ansi(CheckForDictionaryTerms(identifier_with_dictionary_term_misuse)))
    def test_identifier_with_good_dictionary_term_usage(self):
        identifier_with_good_dictionary_term_usage = {'context':'DECLARATION','type': 'int', 'name': 'token','array':0, 'pointer':0}
        self.assertEqual (None, CheckForDictionaryTerms(identifier_with_good_dictionary_term_usage))
    
    #Length Tests
    def test_identifier_with_short_identifier(self):
        identifier_with_short_term = {'context':'DECLARATION','type': 'int', 'name': 'tk','array':0, 'pointer':0}
        self.assertEqual (antiPatternTypes["TERM LENGTH"].format(identifierName="tk"),
                           strip_ansi(CheckForIdentifierLength(identifier_with_short_term)))

    #Generic term tests
    def test_identifier_with_generic_term_misuse(self):
        identifier_with_generic_term_misuse = {'context':'DECLARATION','type': 'int', 'name': 'result','array':0, 'pointer':0}
        self.assertEqual (antiPatternTypes["GENERIC TERM SINGLE"].format(identifierName="result"), 
                          strip_ansi(CheckForGenericTerms(identifier_with_generic_term_misuse)))
    def test_identifier_with_okay_generic_term_usage(self):
        identifier_with_okay_generic_term_usage = {'context':'DECLARATION','type': 'int', 'name': 'startOfWord','array':0, 'pointer':0}
        self.assertEqual (antiPatternTypes["GENERIC TERM MULTI"].format(identifierName="startOfWord"), 
                         strip_ansi(CheckForGenericTerms(identifier_with_okay_generic_term_usage)))
    def test_identifier_with_no_generic_term_usage(self):
        identifier_with_no_generic_term_usage = {'context':'DECLARATION','type': 'int', 'name': 'employeeName','array':0, 'pointer':0}
        self.assertEqual (None, CheckForGenericTerms(identifier_with_no_generic_term_usage))
    
    #Type and Name Match Tests
    def test_identifier_and_type_names_match(self):
        identifier_with_matching_type_name = {'context':'DECLARATION','type': 'ListPointer', 'name': 'listPointer','array':0, 'pointer':0}
        self.assertEqual (antiPatternTypes["TYPE NAME MATCH"].format(identifierName="listPointer", typename="ListPointer"),
                          strip_ansi(CheckIfIdentifierAndTypeNamesMatch(identifier_with_matching_type_name)))
    def test_identifier_and_type_names_do_not_match(self):
        identifier_with_matching_type_name = {'context':'DECLARATION','type': 'ListPointer', 'name': 'employeeNames','array':0, 'pointer':0}
        self.assertEqual (None, CheckIfIdentifierAndTypeNamesMatch(identifier_with_matching_type_name))
    
    #Type and Name Similar Tests
    def test_identifier_and_type_names_are_similar(self):
        identifier_with_matching_type_name = {'context':'DECLARATION','type': 'List', 'name': 'employeeList','array':0, 'pointer':0}
        self.assertEqual (antiPatternTypes["TYPE NAME SIMILAR"].format(identifierName="employeeList", typename="List"),
                          strip_ansi(CheckIfIdentifierAndTypeNamesMatch(identifier_with_matching_type_name)))
    def test_identifier_and_type_names_are_not_similar(self):
        identifier_with_matching_type_name = {'context':'DECLARATION','type': 'ListPointer', 'name': 'employeeNames','array':0, 'pointer':0}
        self.assertEqual (None, CheckIfIdentifierAndTypeNamesMatch(identifier_with_matching_type_name))
    
    def test_identifier_contains_magic_number(self):
        identifier_with_matching_type_name = {'context':'DECLARATION','type': 'ListPointer', 'name': 'employeeNames1','array':0, 'pointer':0}
        self.assertEqual (antiPatternTypes["MAGIC NUMBER"].format(identifierName="employeeNames1"), strip_ansi(CheckForMagicNumbers(identifier_with_matching_type_name)))
    def test_identifier_does_not_contain_magic_number(self):
        identifier_with_matching_type_name = {'context':'DECLARATION','type': 'ListPointer', 'name': 'employeeNames','array':0, 'pointer':0}
        self.assertEqual (None, CheckForMagicNumbers(identifier_with_matching_type_name))