import csv, sys
from enum import Enum
from spiral import ronin
import inflect

inflect = inflect.engine()

class NameConventionCharacteristics:
    def __init__(self):
        self.name = str()
        self.usesCamelCase = False
        self.usesUnderscore = False
        self.usesAllCapitals = False
        self.usesAllLowercase = False
        self.usesMixedStyles = False

identifierNames = []

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
collectionTypeDict = {}
primitiveTypeDict = {"int", "char", "long", "float", "double"}


def CheckIfIdentifierHasCollectionType(identifierData):
    #If the identifier was used with subscript, it's probably a collection
    if identifierData['array'] == '1':
        return True
    
    #If the identifier is a pointer and has a primitive type, then it is probably a collection (in C/C++)
    if (identifierData['pointer'] == '1') and (identifierData['type'].lower() in primitiveTypeDict):
        return True
    
    return False

def CheckLocalIdentifier(identifierData):
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

    split_identifier_data = ronin.split(identifierData['name'])
    
    # First a check to see if identifier name plurality matches its type. If it is a plural identifier,
    # But its type doesn't look like a collection, then this is a linguistic anti-pattern
    isItPlural = inflect.singular_noun(split_identifier_data[-1])
    if(isItPlural != False): #Inflect is telling us that this word is plural.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if shouldIdentifierBePlural != True:
            return "Plural identifier {identifier} has a non-collection type {typename}".format(identifier=identifierData['name'], typename=identifierData['type'])
    else: #Inflect is telling us that this word is singular.
        shouldIdentifierBePlural = CheckIfIdentifierHasCollectionType(identifierData)
        if shouldIdentifierBePlural != False:
            return "Singular identifier {identifier} has a collection type {typename}".format(identifier=identifierData['name'], typename=identifierData['type'])
    
    
    #print("{name} in {identifier} is {plurality}".format(name=split_identifier_data[-1], identifier=split_identifier_data, plurality=inflect.singular_noun(split_identifier_data[-1])))


if __name__ == '__main__':
    with open(sys.argv[1]) as identifier_file:
        identifier_csv_reader = csv.DictReader(identifier_file)
        for row in identifier_csv_reader:
            if contextsDict.get(row['context']) == CONTEXTS.DECLARATION:
                identifierAppraisal = CheckLocalIdentifier(row)
                if identifierAppraisal != None:
                    print(identifierAppraisal)