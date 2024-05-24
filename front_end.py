from phidias.Lib import *
from actions import *

# Ontology intialization
class init(Procedure): pass

# Import OWL triples
class get_triples(Procedure): pass

# Processing beliefs
class process(Procedure): pass

class pre_process(Procedure): pass

# Worlds Agents initialization
# declareRules()
init() >> [show_line("\nInitialiting Ontology...\n"), initWorld(), saveOnto()]
# Triples import from OWL
get_triples() >> [show_line("\nImporting all triples...\n")]


# Importing related triples
pre_process() / (CoAuthorship(X,Y) & Affiliation(X, Z)) >> [show_line("\nImporting related triples...\n"), process_belief(X)]

# Only after get_triple() | pre_process()
process() / (CoAuthorship(X,Y) & Affiliation(X, Z)) >> [show_line("\nSearching co-authors with ",X,"...\n"), process_belief(X)]

