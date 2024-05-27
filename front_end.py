from phidias.Lib import *
from actions import *

# Ontology intialization
class init(Procedure): pass

# Processing beliefs
class process(Procedure): pass

# Import OWL triples
class pre_process(Procedure): pass


# Desires
class publish(Procedure): pass
class betop(Procedure): pass


# World initialization
# declareRules()
init() >> [show_line("\nInitialiting Ontology...\n"), initWorld(), saveOnto()]

# Importing related triples
pre_process() >> [show_line("\nAsserting all OWL 2 beliefs triples...\n"), assert_beliefs_triples(), process()]

# Only after get_triple() | pre_process()
process() / TRIPLE(X, "coAuthorWith", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "coAuthorWith", Y), +CoAuthorship(X, Y), process()]
process() / TRIPLE(X, "hasAffiliationWith", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "hasAffiliationWith", Y), +Affiliation(X, Y), process()]
process() / TRIPLE(X, "isTopAuthorIn", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "isTopAuthorIn", Y), +TopAuthorship(X, Y), process()]
process() / TRIPLE(X, "selectedFor", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "selectedFor", Y), +Selectionship(X, Y), process()]
process() >> [show_line("\nAsserting triples ended.\n")]


# Desires/Intentions

# Publish in the field X
publish(X) / (CoAuthorship(Z, Y) & TopAuthorship(Y, X)) >> [show_line("\nCoauthor with ",Z," if you want to publish in ",X,".\n")]

# Propose co-authorship in the field
# betop(Z) / (CoAuthorship(X, Y) & TopAuthorship(Y, Z)) >> [show_line("\nCoauthor with ",X," if you want to publish in ",Z,".\n")]




