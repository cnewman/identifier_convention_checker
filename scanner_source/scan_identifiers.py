import csv, sys
from enum import Enum
from spiral import ronin
import inflect
import enchant
import sys

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
    "PLURAL MISUSE" : "Plural identifier {identifier} has a non-collection type {typename}",
    "SINGULAR MISUSE" : "Singular identifier {identifier} has a collection type {typename}",
    "MIXED STYLES" : "{identifierName} mixes styles, containing {heuristics}. Please follow the style guidelines."
}

primitiveTypeDict = {"int", "char", "long", "float", "double"}
genericTerms = {"value", "result", "pointer", "output", "input", "content", "ptr", "in", "out", "val", "res", "begin", "end", "start", "finish", "tok", "token"}
collectiontypeDict = {"vector", "list", "set", "dictionary", "map"}

inflect = inflect.engine()
englishDictionary = enchant.Dict("en_US")

def CheckForDictionaryTerms(identifierData):
    dictionaryMisuses = []
    if len(identifierData['name']) <= 2:
        dictionaryMisuses.append(antiPatternDict["TERM LENGTH"]).format(identifierName=identifierData['name'])
    #check if all words are dictionary terms
    splitIdentifierData = ronin.split(identifierData['name'])
    for word in splitIdentifierData:
        if not englishDictionary.check(word):
            dictionaryMisuses.append(antiPatternDict["DICTIONARY TERM"].format(identifierName=identifierData['name']))

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
        reportString.append("underscores")
    if any(capitalUsages):
        reportString.append("upper case letters")
    if not all(lowercaseUsages):
        reportString.append("lower case letters")
    
    if len(reportString) == 3:
        return (antiPatternDict["MIXED STYLES"].format(identifierName=identifierData['name'], heuristics=",".join(reportString)))
    elif any(underscoreUsages) and any(capitalUsages):
        return (antiPatternDict["MIXED STYLES"].format(identifierName=identifierData['name'], heuristics=",".join(reportString)))
    
    return None

def CheckIfIdentifierHasCollectionType(identifierData):
    #If the identifier was used with subscript, it's probably a collection
    if identifierData['array'] == '1':
        return True
    
    #If the identifier is a pointer and has a primitive type, then it is probably a collection (in C/C++)
    if (identifierData['pointer'] == '1') and (identifierData['type'].lower() in primitiveTypeDict):
        return True
    
    if identifierData['type'] in collectiontypeDict:
        return True
    
    return False

def CheckTypeVersusPlurality(identifierData):
    splitIdentifierData = ronin.split(identifierData['name'])
    # First a check to see if identifier name plurality matches its type. If it is a plural identifier,
    # But its type doesn't look like a collection, then this is a linguistic anti-pattern
    isItPlural = inflect.singular_noun(splitIdentifierData[-1])
    if(isItPlural != False): #Inflect is telling us that this word is plural.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if shouldIdentifierBePlural != True:
            return antiPatternDict["PLURAL MISUSE"].format(identifier=identifierData['name'], typename=identifierData['type'])
    else: #Inflect is telling us that this word is singular.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if shouldIdentifierBePlural != False:
            return antiPatternDict["SINGULAR MISUSE"].format(identifier=identifierData['name'], typename=identifierData['type'])
    return None

def CheckLocalIdentifier(identifierData):
    finalReport = FinalIdentifierReport(CheckTypeVersusPlurality(identifierData), CheckHeuristics(identifierData), CheckForDictionaryTerms(identifierData))
    return finalReport

if __name__ == '__main__':
    with open(sys.argv[1]) as identifier_file:
        identifier_csv_reader = csv.DictReader(identifier_file)
        for row in identifier_csv_reader:
            if contextsDict.get(row['context']) == CONTEXTS.DECLARATION:
                identifierAppraisal = CheckLocalIdentifier(row)
                if identifierAppraisal != None:
                    sys.stdout.write(str(identifierAppraisal))