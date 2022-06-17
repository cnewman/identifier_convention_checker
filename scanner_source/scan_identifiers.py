import csv, sys
from enum import Enum
from spiral import ronin

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

def CheckFunctionIdentifier(identifierData):
    split_identifier_data = ronin.split(identifierData['name'])
    print(split_identifier_data)


if __name__ == '__main__':
    with open(sys.argv[1]) as identifier_file:
        identifier_csv_reader = csv.DictReader(identifier_file)
        for row in identifier_csv_reader:
            if contextsDict.get(row['context']) == CONTEXTS.DECLARATION:
                CheckFunctionIdentifier(row)