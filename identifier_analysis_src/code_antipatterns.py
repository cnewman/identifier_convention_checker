antiPatternTypes = {
    "TERM LENGTH" : "{identifierName} has less than 3 characters in it. This may be okay if this is a **well-known** abbreviation or a dictionary term. Please only use dictionary terms, or well-known abbreviations in your identifiers.",
    "DICTIONARY TERM" : "{identifierName} contains the non-dictionary terms: {words}. This may be okay if all terms are **well-known** abbreviations. Please only use dictionary terms, or well-known abbreviations in your identifiers.",
    "PLURAL MISUSE" : "Plural identifier {identifierName} has a non-collection type {typename}. A plural identifier name is typically best used to represent collection types.",
    "SINGULAR MISUSE" : "Singular identifier {identifierName} has a collection type {typename}. A singular identifier name should not be used to represent an object with a collection type.",
    "MIXED STYLES" : "{identifierName} mixes styles, containing {heuristics}. Please use a consistent style. Refer to any naming convention documentation you have been provided.",
    "GENERIC TERM SINGLE" : "{identifierName} is a generic term. Please use descriptive terms, and avoid very general terms. Terms like 'result' are typically useless; they do not provide any information about the object they represent.",
    "GENERIC TERM MULTI" : "{identifierName} contains a generic term. This might be okay, but consider whether there is a better term to use. Terms like 'result' do very little to convey the data represented by a variable.",
    "TYPE NAME MATCH" : "{identifierName} has the same name as its type, {typename}. Generally, an identifier's name should *not* match its type because you can look at its type for that information.",
    "TYPE NAME SIMILAR" : "{identifierName} contains words from {typename}. Generally, an identifier's name should *not* refer to its type because you can look at its type for that information. Does this identifier need to?",
    "NUMBER IN NAME" : "{identifierName} contains a number. Numbers tend to be mis-used and can cause confusion for developers that don't understand what the number means.",
}