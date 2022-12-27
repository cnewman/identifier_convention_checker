antiPatternTypes = {
    "TERM LENGTH" : "{identifierName} has less than 3 characters in it. Please only use dictionary terms, or well-known abbreviations.",
    "DICTIONARY TERM" : "{identifierName} is not a dictionary term. This may be okay if the term is a **well known** abbreviation.",
    "PLURAL MISUSE" : "Plural identifier {identifierName} has a non-collection type {typename}. Consider making the identifier name plural, or changing type.",
    "SINGULAR MISUSE" : "Singular identifier {identifierName} has a collection type {typename}. Consider making the identifier plural, or changing the type.",
    "MIXED STYLES" : "{identifierName} mixes styles, containing {heuristics}. Please use a consistent style.",
    "GENERIC TERM SINGLE" : "{identifierName} is a generic term. Please use descriptive terms, and avoid very general terms.",
    "GENERIC TERM MULTI" : "{identifierName} contains a generic term. This might be okay, but consider whether there is a better term to use. Terms like 'result' are typically useless; containing little semantic value.",
    "TYPE NAME MATCH" : "{identifierName} has the same name as its type, {typename}. Generally, an identifier's name should *not* match its type. Please pick another name.",
    "TYPE NAME SIMILAR" : "{identifierName} contains words from {typename}. Generally, an identifier's name should *not* refer to its type. Consider whether this identifier needs to refer to its type.",
    "MAGIC NUMBER" : "{identifierName} contains a number. Numbers tend to be mis-used and can cause confusion for developers that don't understand what the number is for. Consider using a word or just removing the number.",
}