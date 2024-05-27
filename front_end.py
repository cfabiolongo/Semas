from phidias.Lib import *
from actions import *

# Ontology intialization
class init(Procedure): pass

# Processing beliefs
class process(Procedure): pass

# Import OWL triples
class pre_process(Procedure): pass


# Worlds Agents initialization
# declareRules()
init() >> [show_line("\nInitialiting Ontology...\n"), initWorld(), declareRules(), saveOnto()]

# Importing related triples
pre_process() >> [show_line("\nAsserting OWL 2 beliefs triples...\n"), assert_beliefs_triples()]

# Only after get_triple() | pre_process()
process() / (CoAuthorship(X,Y) & Affiliation(X, Z)) >> [show_line("\nSearching co-authors with ",X,"...\n"), process_belief(X)]

