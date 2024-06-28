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
pre_process() / TRIPLE(X, "Gender", Y) >> [-TRIPLE(X, "Gender", Y), +HasGender(X, Y), pre_process()]
pre_process() >> [show_line("\nAsserting triples ended.\n")]


# Desires/Intentions

# Publish in the field X (return coauthor only), e.g.  Publicationship("Applied-Ontology"), Publicationship("Artificial-Intelligence")
# Publicationship(X) / (CoAuthorship(Z, Y) & TopAuthorship(Y, X)) >> [show_line("\nIndirect match: Coauthor with ",Z," if you want to publish in ",X,".\n"), +ProposeCoauthorship(Z, X)]

# Publish in the field X (return author/coauthor+university)
SelectUniversity(X) / (Selectionship(S,U) & CoAuthorship(Z, Y) & TopAuthorship(Y, X) & Affiliation(Z, U)) >> [show_line("Indirect match found at ",U,".\n"), -CoAuthorship(Z, Y), +AcceptOffer(S,X,U), SelectUniversity(X)]
Publicationship(X) / (Selectionship(S,U) & CoAuthorship(Z, Y) & TopAuthorship(Y, X) & Affiliation(Z, U)) >> [show_line("Indirect match found at ",U,".\n"), -CoAuthorship(Z, Y), +ProposeCoauthorship_2(Z, Y,X),+AcceptOffer(S,X,U), Publicationship(X)]
Publicationship(X) / (TopAuthorship(Y, X) & Affiliation(Y, U)) >> [show_line("Direct match found at ",U,".\n"), -TopAuthorship(Y, X), +ProposeCoauthorship(Y, X), Publicationship(X)]

+ProposeCoauthorship_2(X,Z, Y) >> [show_line("Propose co-authorship with ",X," as co-author with ",Z,", a top-author in the field of ",Y,".\n")]
+ProposeCoauthorship(X,Y) >> [show_line("Propose co-authorship with ",X," as top-author in the field of ",Y,".\n")]
+AcceptOffer(S,X,U) >> [show_line(S," should accept offer from University ",U," with co-authors of top-authors in field of ",X,".\n")]


# Plan to became top author in the field X, e.g. +BeTopAuthorship("Artificial Intelligence")
BeTopAuthorship(X) >> [show_line("\nPlan to become top Authorship in the field ",X,"....\n")]
