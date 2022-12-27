import csv, sys
import inflect as inflectLib
import enchant
from enum import Enum
from spiral import ronin
from colorama import Fore, Style, init
from scanner_source.code_antipatterns import antiPatternTypes


class FinalIdentifierReport:
    """
    This class records all of the data gathered about the code analyzed by the tool.
    """
    def __init__(self, identifierData, pluralityViolations, heuristicsViolations, dictionaryViolations, 
                typeAndNameViolations, magicNumberViolations, lengthViolations):
        """
        Parameters
        ----------
        identifierData: list<strings> generated from python csv module
            This is a row passed in from the csv reader. Represents all statically-collected
            information about an identifier
        pluralityViolations: str
            The report generated when we checked the identifier's type and name
        heuristicsViolations: str
            The report generated when we checked the identifier's name for heuristics violations
        dictionaryViolations: str
            The report generated when we checked the identifier name for dictionary term violations
        typeAndNameViolations: str
            The report generated when we checked the identifier name for type and name term violations
        magicNumberViolations: str
            The report generated when we checked the identifier name for magic number violations
        
        """

        self.identifierData = identifierData
        self.pluralityViolations = pluralityViolations
        self.heuristicsViolations = heuristicsViolations
        self.dictionaryViolations = dictionaryViolations
        self.typeAndNameViolations = typeAndNameViolations
        self.magicNumberViolations = magicNumberViolations
        self.lengthViolations = lengthViolations
    def __str__(self):
        """
        When we call print (or anything that converts to string) on FinalIdentifierReport objects, this will
        generate clean output.

        Returns
        -------
        A tab-formatted report of problems present in the FinalIdentifierReport
        """
        violations = [self.pluralityViolations, self.heuristicsViolations, self.dictionaryViolations, self.typeAndNameViolations, self.magicNumberViolations, self.lengthViolations]
        if all(violation is None for violation in violations):
            return ''

        formattedReport = "{}:\n{}\n{}\n{}\n{}\n{}\n{}\n".format(
                          self.identifierData["filename"] + ':' + self.identifierData["line"],
                          str() if self.pluralityViolations is None else self.pluralityViolations, 
                          str() if self.heuristicsViolations is None else self.heuristicsViolations, 
                          str() if self.dictionaryViolations is None else self.dictionaryViolations,
                          str() if self.typeAndNameViolations is None else self.typeAndNameViolations,
                          str() if self.magicNumberViolations is None else self.magicNumberViolations,
                          str() if self.lengthViolations is None else self.lengthViolations,)
        """        
        The blank strs due to thre being no problem detected will cause newlines to appear. 
        The code below strips these out.
        """
        cleanedFormattedReport = []
        for formattedLine in formattedReport.split('\n'):
            #Keep if there is more than just a newline character
            if any([character.isprintable() for character in formattedLine.split()]):
                cleanedFormattedReport.append(formattedLine+'\n')
        
        return '\t'.join(cleanedFormattedReport)

def WrapTextWithColor(text, color):
    """
    This function will correctly wrap text with ANSI color codes that begin the color sequence, then
    resets color at the end of the text.

    Parameters
    ----------
    text: str
        The text that we want to color
    color: Fore (colorama ANSI code enum type)
        The color that we want to wrap the text with
    
    Returns
    -------
    ANSI-colored text ended with a style reset
    """
    return color + text + Style.RESET_ALL

def CheckForGenericTerms(identifierData):
    """
    This function looks for the presence of Generic Terms, which are terms in identifier names
    that convey very little domain or problem-specific information. The function checks for
    two situations: 1) Identifier is a single generic term (i.e., found in the generic terms
    list above). 2) Identifier has multiple terms in it, and some are generic.

    Parameters
    ---------
    identifierData: list<strings> generated from python csv module
        This is a row passed in from the csv reader. Represents all statically-collected
        information about an identifier
    
    Returns
    -------
    An interpolated string filled in with any issues found by the function, or None if no problem
    was found
    """
    genericTerms = {"value", "result", "pointer", "output", "input", "content", "ptr",
                    "in", "out", "val", "res", "begin", "end", "start", "finish", "tok",
                    "test", "token", "temp"}
    
    genericTermMisuses = []
    splitIdentifierName = ronin.split(identifierData['name'])
    IDENTIFIER_OF_LENGTH_ONE = 1
    if len(splitIdentifierName) == IDENTIFIER_OF_LENGTH_ONE:
        if splitIdentifierName[0] in genericTerms:
            genericTermMisuses.append(antiPatternTypes["GENERIC TERM SINGLE"]
                                     .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED)))
    else:
        for word in splitIdentifierName:
            if word in genericTerms:
                genericTermMisuses.append(antiPatternTypes["GENERIC TERM MULTI"]
                                         .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED)))
    return ",".join(genericTermMisuses) if genericTermMisuses else None

def CheckForIdentifierLength(identifierData):
    """
    This function looks for excessively short identifier names, arbitrarily set at 2 characters.
    
    Parameters
    ---------
    identifierData: list<strings> generated from python csv module
        This is a row passed in from the csv reader. Represents all statically-collected
        information about an identifier
    
    Returns
    -------
    An interpolated string filled in with any issues found by the function, or None if no problem
    was found
    """
    IDENTIFIER_WITH_TWO_CHARACTERS = 2
    if len(identifierData['name']) <= IDENTIFIER_WITH_TWO_CHARACTERS:
        return antiPatternTypes["TERM LENGTH"].format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED))

def CheckForDictionaryTerms(identifierData):
    """
    This function looks for the presence of dictionary terms, which are terms in identifier names
    that do not appear in an English dictionary. This includes abbreviations and acronyms.
    
    Parameters
    ---------
    identifierData: list<strings> generated from python csv module
        This is a row passed in from the csv reader. Represents all statically-collected
        information about an identifier
    
    Returns
    -------
    An interpolated string filled in with any issues found by the function, or None if no problem
    was found
    """
    englishDictionary = enchant.Dict("en_US")

    dictionaryMisuses = []
    #Check if all words are dictionary terms
    splitIdentifierName = ronin.split(identifierData['name'])
    for word in splitIdentifierName:
        if not englishDictionary.check(word):
            dictionaryMisuses.append(antiPatternTypes["DICTIONARY TERM"]
                                    .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED)))

    return ",".join(dictionaryMisuses) if dictionaryMisuses else None

def CheckHeuristics(identifierData):
    """
    This function looks for the presence of conflicting heuristics, such as mixing camelCase
    and under_score.
    
    Parameters
    ---------
    identifierData: list<strings> generated from python csv module
        This is a row passed in from the csv reader. Represents all statically-collected
        information about an identifier
    
    Returns
    -------
    An interpolated string filled in with any issues found by the function, or None if no problem
    was found
    """
    underscoreUsages = []
    capitalUsages = []
    lowercaseUsages = []

    for character in identifierData['name']:
        if character == '_':
            underscoreUsages.append(True)
        if character.isupper():
            capitalUsages.append(True)
        if character.islower():
            lowercaseUsages.append(True)
    
    reportString = []
    if any(underscoreUsages):
        reportString.append(WrapTextWithColor("underscores", Fore.MAGENTA))
    if any(capitalUsages):
        reportString.append(WrapTextWithColor("upper case letters", Fore.MAGENTA))
    if not all(lowercaseUsages):
        reportString.append(WrapTextWithColor("lower case letters", Fore.MAGENTA))
    
    if len(reportString) == 3:
        return (antiPatternTypes["MIXED STYLES"]
               .format(identifierName=WrapTextWithColor(identifierData['name'],Fore.RED), heuristics=",".join(reportString)))
    elif any(underscoreUsages) and any(capitalUsages):
        return (antiPatternTypes["MIXED STYLES"]
               .format(identifierName=WrapTextWithColor(identifierData['name'],Fore.RED), heuristics=",".join(reportString)))
    
    return None

def CheckIfIdentifierHasCollectionType(identifierData):
    """
    This function checks the current identifier's type to see if it is a collection type
    
    Parameters
    ---------
    identifierData: list<strings> generated from python csv module
        This is a row passed in from the csv reader. Represents all statically-collected
        information about an identifier
    
    Returns
    -------
    True if it found a type that looks like it represents a collection. False otherwise.
    """
    primitiveTypes = ["int", "char", "long", "float", "double", "bool"]
    collectionTypes = ["vector", "list", "set", "dictionary", "map", "deque", "stack", "queue", "array"]

    #If the identifier was used with subscript, it's probably a collection
    if int(identifierData['array']) == 1:
        return True
    
    #If the identifier is a pointer and has a primitive type, then it is probably a collection (in C/C++)
    isTypePrimitive = any(identifierData['type'].strip('[]*').lower() in typename for typename in primitiveTypes)
    
    if (int(identifierData['pointer']) == 1) and isTypePrimitive:
        return True
    
    isTypeCollection = any(identifierData['type'].strip('[]*').lower() in typename for typename in collectionTypes)
    if isTypeCollection:
        return True
    
    return False

def CheckTypeVersusPlurality(identifierData):
    """
    This function uses CheckIfIdentifierHasCollectionType, then compares the result to the
    plurality of the given identifier's name. If there is a mismatch, it reports such. For example,
    a plural identifier with a singular type means that the identifier should probably be plural
    
    Parameters
    ---------
    identifierData: list<strings> generated from python csv module
        This is a row passed in from the csv reader. Represents all statically-collected
        information about an identifier
    
    Returns
    -------
    An interpolated string filled in with any issues found by the function, or None if no problem
    was found
    """
    inflect = inflectLib.engine()

    #plural rules don't apply to function names
    if identifierData['context'] == 'FUNCTION':
        return None
    
    splitIdentifierName = ronin.split(identifierData['name'])
    # First a check to see if identifier name plurality matches its type. If it is a plural identifier,
    # But its type doesn't look like a collection, then this is a linguistic anti-pattern
    isItPlural = inflect.singular_noun(splitIdentifierName[-1])
    if isItPlural: #Inflect is telling us that this word is plural.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if not shouldIdentifierBePlural:
            return (antiPatternTypes["PLURAL MISUSE"]
                  .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED), 
                          typename=WrapTextWithColor(identifierData['type'], Fore.BLUE)))
    else: #Inflect is telling us that this word is singular.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if shouldIdentifierBePlural:
            return (antiPatternTypes["SINGULAR MISUSE"]
                  .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED),
                          typename=WrapTextWithColor(identifierData['type'], Fore.BLUE)))
    return None

def CheckIfIdentifierAndTypeNamesMatch(identifierData):
    """
    This function checks to see if the given identifier has the same, or similar, name as its type.
    
    Parameters
    ---------
    identifierData: list<strings> generated from python csv module
        This is a row passed in from the csv reader. Represents all statically-collected
        information about an identifier
    
    Returns
    -------
    An interpolated string filled in with any issues found by the function, or None if no problem
    was found
    """
    identifierName = identifierData['name'].lower()
    identifierType = identifierData['type'].lower()

    #Exact match between name and type
    if identifierName == identifierType:
        return antiPatternTypes["TYPE NAME MATCH"].format(identifierName=identifierData['name'], typename=identifierData['type'])
    
    splitIdentifierName = ronin.split(identifierData['name'])
    
    #Partial match between name and type. We don't split type name for now; it makes a lot of weird corner cases.
    if any(identifierType == identifierTerm.lower() for identifierTerm in splitIdentifierName):
        return antiPatternTypes["TYPE NAME SIMILAR"].format(identifierName=identifierData['name'], typename=identifierData['type'])

    return None

def CheckForMagicNumbers(identifierData):
    """
    This function checks to see if the given identifier contains numbers (i.e., potentially magic numbers)
    
    Parameters
    ---------
    identifierData: list<strings> generated from python csv module
        This is a row passed in from the csv reader. Represents all statically-collected
        information about an identifier
    
    Returns
    -------
    An interpolated string filled in with any issues found by the function, or None if no problem
    was found
    """
    splitIdentifierName = ronin.split(identifierData['name'])
    
    if any(term.isdigit() for term in splitIdentifierName):
        return antiPatternTypes["MAGIC NUMBER"].format(identifierName= WrapTextWithColor(identifierData['name'], Fore.RED))
    return None

def CheckLocalIdentifier(identifierData):
    """
    Runs all of the checks on a given identifiers and produces a FinalIdentifierReport
    
    Parameters
    ---------
    identifierData: list<strings> generated from python csv module
        This is a row passed in from the csv reader. Represents all statically-collected
        information about an identifier
    
    Returns
    -------
    A FinalIdentifierReport
    """
    finalReport = FinalIdentifierReport(identifierData, 
                                        CheckTypeVersusPlurality(identifierData), 
                                        CheckHeuristics(identifierData), 
                                        CheckForDictionaryTerms(identifierData),
                                        CheckIfIdentifierAndTypeNamesMatch(identifierData),
                                        CheckForMagicNumbers(identifierData),
                                        CheckForIdentifierLength(identifierData))
    return finalReport