import csv, sys
from enum import Enum
from spiral import ronin
from colorama import Fore, Style, init
import inflect
import enchant
import sys

class CONTEXTS(Enum):
    DECLARATION = 0
    PARAMETER = 1
    FUNCTION = 2
    ATTRIBUTE = 3
    CLASSNAME = 4

contextsDict = {"DECLARATION": CONTEXTS.DECLARATION,
                "PARAMETER": CONTEXTS.PARAMETER,
                "FUNCTION": CONTEXTS.FUNCTION,
                "ATTRIBUTE": CONTEXTS.ATTRIBUTE,
                "CLASSNAME": CONTEXTS.CLASSNAME}

antiPatternDict = {
    "TERM LENGTH" : "{identifierName} has less than 3 characters in it. Typically, identifiers should be made up of dictionary terms."
                                    "Please follow the style guidelines.",
    "DICTIONARY TERM" : "{identifierName} is not a dictionary term.",
    "PLURAL MISUSE" : "Plural identifier {identifierName} has a non-collection type {typename}",
    "SINGULAR MISUSE" : "Singular identifier {identifierName} has a collection type {typename}",
    "MIXED STYLES" : "{identifierName} mixes styles, containing {heuristics}. Please follow the style guidelines.",
    "GENERIC TERM SINGLE" : "{identifierName} is a generic term. Please follow the style guidelines.",
    "GENERIC TERM MULTI" : "{identifierName} contains a generic term. This might be okay, as long as the generic term helps others comprehend this identifier.",
    "TYPE NAME MATCH" : "{identifierName} has the same name as its type, {typename}. Generally, an identifier's name should *not* match its type.",
}

primitiveTypeList = ["int", "char", "long", "float", "double", "bool"]
genericTerms = {"value", "result", "pointer", "output", "input", "content", "ptr",
                "in", "out", "val", "res", "begin", "end", "start", "finish", "tok",
                "test", "token", "temp"}
collectiontypeDict = {"vector", "list", "set", "dictionary", "map"}

inflect = inflect.engine()
englishDictionary = enchant.Dict("en_US")

class FinalIdentifierReport:
    def __init__(self, plurality, heuristics, dictionary):
        self.pluralityUsage = plurality
        self.heuristicsUsage = heuristics
        self.dictionaryTermUsage = dictionary
    def __str__(self):
        formatted = "{}\n{}\n{}\n".format(str() if self.pluralityUsage is None else self.pluralityUsage, 
                     str() if self.heuristicsUsage is None else self.heuristicsUsage, 
                     str() if self.dictionaryTermUsage is None else self.dictionaryTermUsage)
        
        #The blank strs will cause newlines to appear. Need to strip those.
        cleanReport = []
        for line in formatted.split('\n'):
            #are any characters NOT a newline??? keep
            if any([c.isalnum() for c in line.split()]):
                cleanReport.append(line+'\n')
        
        return ''.join(cleanReport)
def WrapTextWithColor(text, color):
    return color + text + Style.RESET_ALL

def CheckForGenericTerms(identifierData):
    genericTermMisuses = []
    splitIdentifierData = ronin.split(identifierData['name'])
    if len(splitIdentifierData) == 1:
        if splitIdentifierData[0] in genericTerms:
            genericTermMisuses.append(antiPatternDict["GENERIC TERM SINGLE"]
                                     .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED)))
    else:
        for word in splitIdentifierData:
            if word in genericTerms:
                genericTermMisuses.append(antiPatternDict["GENERIC TERM MULTI"]
                                         .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED)))
    return ",".join(genericTermMisuses) if genericTermMisuses else None

def CheckForDictionaryTerms(identifierData):
    dictionaryMisuses = []
    if len(identifierData['name']) <= 2:
        dictionaryMisuses.append(antiPatternDict["TERM LENGTH"]
                                .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED)))
    #check if all words are dictionary terms
    splitIdentifierData = ronin.split(identifierData['name'])
    for word in splitIdentifierData:
        if not englishDictionary.check(word):
            dictionaryMisuses.append(antiPatternDict["DICTIONARY TERM"]
                                    .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED)))

    return ",".join(dictionaryMisuses) if dictionaryMisuses else None

def CheckHeuristics(identifierData):
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
        return (antiPatternDict["MIXED STYLES"]
               .format(identifierName=WrapTextWithColor(identifierData['name'],Fore.RED), heuristics=",".join(reportString)))
    elif any(underscoreUsages) and any(capitalUsages):
        return (antiPatternDict["MIXED STYLES"]
               .format(identifierName=WrapTextWithColor(identifierData['name'],Fore.RED), heuristics=",".join(reportString)))
    
    return None

def CheckIfIdentifierHasCollectionType(identifierData):
    #If the identifier was used with subscript, it's probably a collection
    if identifierData['array'] == 1:
        return True
    
    #If the identifier is a pointer and has a primitive type, then it is probably a collection (in C/C++)
    isTypePrimitive = any(identifierData['type'].strip('[]*').lower() in typename for typename in primitiveTypeList)
    if (identifierData['pointer'] == 1) and isTypePrimitive:
        return True
    
    if identifierData['type'] in collectiontypeDict:
        return True
    
    return False

def CheckTypeVersusPlurality(identifierData):
    splitIdentifierData = ronin.split(identifierData['name'])
    # First a check to see if identifier name plurality matches its type. If it is a plural identifier,
    # But its type doesn't look like a collection, then this is a linguistic anti-pattern
    isItPlural = inflect.singular_noun(splitIdentifierData[-1])
    if(isItPlural): #Inflect is telling us that this word is plural.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if not shouldIdentifierBePlural:
            return (antiPatternDict["PLURAL MISUSE"]
                  .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED), 
                          typename=WrapTextWithColor(identifierData['type'], Fore.BLUE)))
    else: #Inflect is telling us that this word is singular.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if shouldIdentifierBePlural:
            return (antiPatternDict["SINGULAR MISUSE"]
                  .format(identifierName=WrapTextWithColor(identifierData['name'], Fore.RED),
                          typename=WrapTextWithColor(identifierData['type'], Fore.BLUE)))
    return None

def CheckIfIdentifierAndTypeNamesMatch(identifierData):
    identifierName = identifierData['name'].lower()
    identifierType = identifierData['type'].lower()

    if identifierName == identifierType:
        return antiPatternDict["TYPE NAME MATCH"].format(identifierName=identifierData['name'], typename=identifierData['type'])
    
    return None


def CheckLocalIdentifier(identifierData):
    finalReport = FinalIdentifierReport(CheckTypeVersusPlurality(identifierData), CheckHeuristics(identifierData), CheckForDictionaryTerms(identifierData))
    return finalReport