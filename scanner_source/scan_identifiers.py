import csv, sys
from enum import Enum

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
    print('hi')


if __name__ == '__main__':
    with open(sys.argv[1]) as identifier_file:
        identifier_csv_reader = csv.reader(identifier_file)
        for row in identifier_csv_reader:
            match contextsDict.get(row[2]):
                case FUNCTION:
                    CheckFunctionIdentifier(row)