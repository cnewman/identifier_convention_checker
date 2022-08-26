import csv, sys
from enum import Enum
from spiral import ronin
import inflect
import enchant

class FinalIdentifierReport:
    def __init__(self):
        self.pluralityUsage = ""
        self.heuristicsUsage = ""
        self.dictionaryTermUsage = ""
    def setPluralityMessage():
        pass
    def setHeuristicsMessage():
        pass
    def __str__(self):
        finalReportString = str()
        for infoString in [self.pluralityUsage, self.heuristicsUsage, self.dictionaryTermUsage]:
            if infoString:
                finalReportString = finalReportString + infoString
        return finalReportString

class NameConventionCharacteristics:
    def __init__(self):
        self.name = str()
        self.usesCamelCase = False
        self.usesUnderscore = False
        self.usesAllCapitals = False
        self.usesAllLowercase = False
        self.usesMixedStyles = False

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

def CheckForDictionaryTerms(identifierData, finalReport):
    if len(identifierData['name']) <= 2:
        finalReport.dictionaryTermUsage = (antiPatternDict["TERM LENGTH"]).format(identifierName=identifierData['name'])
    #check if all words are dictionary terms
    splitIdentifierData = ronin.split(identifierData['name'])
    for word in splitIdentifierData:
        if not englishDictionary.check(word):
            finalReport.dictionaryTermUsage = finalReport.dictionaryTermUsage + (antiPatternDict["DICTIONARY TERM"]).format(identifierName=identifierData['name'])

    return finalReport

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

def CheckHeuristics(identifierData, finalReport):
    currentIdentifierCharacteristics = NameConventionCharacteristics()
    
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
        finalReport.heuristicsUsage = (antiPatternDict["MIXED STYLES"].format(identifierName=identifierData['name'], heuristics=",".join(reportString)))
    elif any(underscoreUsages) and any(capitalUsages):
        finalReport.heuristicsUsage = (antiPatternDict["MIXED STYLES"].format(identifierName=identifierData['name'], heuristics=",".join(reportString)))
    
    return finalReport

def CheckTypeVersusPlurality(identifierData, finalReport):
    splitIdentifierData = ronin.split(identifierData['name'])
    # First a check to see if identifier name plurality matches its type. If it is a plural identifier,
    # But its type doesn't look like a collection, then this is a linguistic anti-pattern
    isItPlural = inflect.singular_noun(splitIdentifierData[-1])
    if(isItPlural != False): #Inflect is telling us that this word is plural.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if shouldIdentifierBePlural != True:
            finalReport.pluralityUsage = antiPatternDict["PLURAL MISUSE"].format(identifier=identifierData['name'], typename=identifierData['type'])
    else: #Inflect is telling us that this word is singular.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if shouldIdentifierBePlural != False:
            finalReport.pluralityUsage = antiPatternDict["SINGULAR MISUSE"].format(identifier=identifierData['name'], typename=identifierData['type'])
    return finalReport

def CheckLocalIdentifier(identifierData):
    finalReport = FinalIdentifierReport()
    finalReport = CheckHeuristics(identifierData, finalReport)
    finalReport = CheckTypeVersusPlurality(identifierData, finalReport)
    finalReport = CheckForDictionaryTerms(identifierData, finalReport)
    return finalReport
    #print("{name} in {identifier} is {plurality}".format(name=splitIdentifierData[-1], identifier=splitIdentifierData, plurality=inflect.singular_noun(splitIdentifierData[-1])))

if __name__ == '__main__':
    with open(sys.argv[1]) as identifier_file:
        identifier_csv_reader = csv.DictReader(identifier_file)
        for row in identifier_csv_reader:
            if contextsDict.get(row['context']) == CONTEXTS.DECLARATION:
                identifierAppraisal = CheckLocalIdentifier(row)
                if identifierAppraisal != None:
                    print(identifierAppraisal)