from phidias.Lib import *
from actions import *

# Ontology intialization
class init(Procedure): pass

# Processing beliefs
class load(Procedure): pass

# Import OWL triples
class pre_process(Procedure): pass



# World initialization
# declareRules()
init() >> [show_line("\nInitialiting Ontology...\n"), initWorld(), declareRules(), saveOnto()]

# Importing related triples
load() >> [show_line("\nAsserting all OWL 2 beliefs triples...\n"), assert_beliefs_triples(), pre_process()]

# Only after get_triple() | pre_process()
pre_process() / TRIPLE(X, "coAuthorWith", Y) >> [-TRIPLE(X, "coAuthorWith", Y), +CoAuthorship(X, Y), pre_process()]
pre_process() / TRIPLE(X, "hasAffiliationWith", Y) >> [-TRIPLE(X, "hasAffiliationWith", Y), +Affiliation(X, Y), pre_process()]
pre_process() / TRIPLE(X, "isTopAuthorIn", Y) >> [-TRIPLE(X, "isTopAuthorIn", Y), +TopAuthorship(X, Y), pre_process()]
pre_process() / TRIPLE(X, "selectedFor", Y) >> [-TRIPLE(X, "selectedFor", Y), +Selectionship(X, Y), pre_process()]
pre_process() >> [show_line("\nAsserting triples ended.\n")]


# Desires/Intentions

# Publish in the field X (return coauthor only), e.g.  Publicationship("Applied-Ontology"), Publicationship("Artificial-Intelligence")
# Publicationship(X) / (CoAuthorship(Z, Y) & TopAuthorship(Y, X)) >> [show_line("\nIndirect match: Coauthor with ",Z," if you want to publish in ",X,".\n"), +ProposeCoauthorship(Z, X)]

# Publish in the field X (return author/coauthor+university)
Publicationship(X) / (TopAuthorship(Y, X) & Affiliation(Y, U)) >> [show_line("\nDirect coathor match with ",Y," to publish in ",X," at ",U,".\n"), +ProposeCoauthorship(Y, X)]
Publicationship(X) / (CoAuthorship(Z, Y) & TopAuthorship(Y, X) & Affiliation(Z, U)) >> [show_line("\nIndirect coauthor match with ",Z," to publish in ",X," at ",U,".\n"), +ProposeCoauthorship(Z, X)]

# Plan to became top author in the field X, e.g. +BeTopAuthorship("Artificial Intelligence")
BeTopAuthorship(X) >> [show_line("\nPlan to become top Authorship in the field ",X,"....\n")]

+ProposeCoauthorship(X, Y) >> [show_line("Propose co-authorship with ",X," to publish in the field of ",Y,".\n")]