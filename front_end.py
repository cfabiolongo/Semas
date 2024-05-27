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
pre_process() >> [show_line("\nAsserting all OWL 2 beliefs triples...\n"), assert_beliefs_triples()]

# Only after get_triple() | pre_process()
process() / TRIPLE(X, "coAuthorWith", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "coAuthorWith", Y), +CoAuthorship(X, Y), process()]
process() / TRIPLE(X, "hasAffiliationWith", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "hasAffiliationWith", Y), +Affiliation(X, Y), process()]
process() / TRIPLE(X, "isTopAuthorIn", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "isTopAuthorIn", Y), +TopAuthorship(X, Y), process()]
process() / TRIPLE(X, "selectedFor", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "selectedFor", Y), +Selectionship(X, Y), process()]
process() / TRIPLE(X, "beTopAuthorOwnField", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "beTopAuthorOwnField", Y), +BeTopAuthorship(X, Y), process()]
process() / TRIPLE(X, "publish", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "publish", Y), +Publicationship(X, Y), process()]
process() / TRIPLE(X, "proposeCoauthorship", Y) >> [show_line("\nAsserting triples...\n"), -TRIPLE(X, "proposeCoauthorship", Y), +ProposeCoauthorship(X, Y), process()]
process() >> [show_line("\nAsserting triples ended.\n")]




