antiPatternTypes = {
    "TERM LENGTH" : "{identifierName} has less than 3 characters in it. Typically, identifiers should be made up of dictionary terms",
    "DICTIONARY TERM" : "{identifierName} is not a dictionary term",
    "PLURAL MISUSE" : "Plural identifier {identifierName} has a non-collection type {typename}",
    "SINGULAR MISUSE" : "Singular identifier {identifierName} has a collection type {typename}",
    "MIXED STYLES" : "{identifierName} mixes styles, containing {heuristics}",
    "GENERIC TERM SINGLE" : "{identifierName} is a generic term",
    "GENERIC TERM MULTI" : "{identifierName} contains a generic term. This might be okay, as long as the generic term helps others comprehend this identifier",
    "TYPE NAME MATCH" : "{identifierName} has the same name as its type, {typename}. Generally, an identifier's name should *not* match its type",
}