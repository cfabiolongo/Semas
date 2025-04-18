from phidias.Lib import *
from actions import *
from phidias.Types import *

# ---------------------------------------------------------------------
# PHIDIAS rules variable declaration
# ---------------------------------------------------------------------

def_vars('X', 'Y', 'Z', 'U')

# Ontology intialization
class init(Procedure): pass

# Processing beliefs
class load(Procedure): pass
class load_local(Procedure): pass

# Import OWL triples
class pre_process(Procedure): pass

class REST(Belief): pass


# World initialization (only for local usage ontologies)
init() >> [show_line("\nInitialiting Ontology...\n"), initWorld(), declareRules(), saveOnto()]

# Importing all related triples
# Importing filtered triples
load(X, Y) >> [show_line("\nAsserting all OWL 2 beliefs related to ",X," and ",Y," from triple-store...\n"), assert_beliefs_triples(X, Y), pre_process()]
load() >> [show_line("\nAsserting all OWL 2 beliefs from triple-store...\n"), assert_beliefs_triples(), pre_process()]
load_local() >> [show_line("\nAsserting all OWL 2 beliefs...\n"), assert_beliefs_local_triples(), pre_process()]


# Starting RESTful flask service
start_rest() >> [show_line("\nStarting RESTful service...\n"), +REST("ACTIVE"), start_rest_service()]

# Only after get_triple() | pre_process()
pre_process() / TRIPLE(X, "coAuthorWith", Y) >> [-TRIPLE(X, "coAuthorWith", Y), +CoAuthorship(X, Y), pre_process()]
pre_process() / TRIPLE(X, "hasAffiliationWith", Y) >> [-TRIPLE(X, "hasAffiliationWith", Y), +Affiliation(X, Y), pre_process()]
pre_process() / TRIPLE(X, "isTopAuthorIn", Y) >> [-TRIPLE(X, "isTopAuthorIn", Y), +ConsiderTopAuthor(X, Y), pre_process()]
pre_process() / TRIPLE(X, "selectedFor", Y) >> [-TRIPLE(X, "selectedFor", Y), +Selectionship(X, Y), pre_process()]
pre_process() >> [show_line("\nAsserting triples ended.\n")]


# Desires/Intentions (shell)

# Publish in the field X
# e.g. BeTopAuthorship('http://fossr.eu/kg/data/topics/2003') ----> Finance

BeTopAuthorship(X) >> [show_line("\nPlanning to be top-author in ",X,"..."), load("acad:isTopAuthorIn", X), FindAffiliation()]

FindAffiliation() / ConsiderTopAuthor(X, Y) >> [-ConsiderTopAuthor(X, Y), +TopAuthorship(X, Y), show_line("\nFinding triples related with ",X,"..."), load("acad:hasAffiliationWith", X), load("acad:isCoathorWith", X), FindAffiliation()]
FindAffiliation() >> [show_line("\nFinding triples related with ",X,"..."), ]

Publicationship(X) / (CoAuthorship(Z, Y) & TopAuthorship(Y, X) & Affiliation(Z, U)) >> [show_line("Indirect match found at ",U,".\n"), -CoAuthorship(Z, Y), +ProposeCoauthorship(Z, X), Publicationship(X)]
Publicationship(X) / (TopAuthorship(Y, X) & Affiliation(Y, U)) >> [show_line("Direct match found at ",U,".\n"), -TopAuthorship(Y, X), +ProposeCoauthorship(Y, X), Publicationship(X)]

+ProposeCoauthorship(X, Y) / REST("ACTIVE") >> [show_line("Propose co-authorship with ",X," to publish in the field of ",Y,".\n"), build_json_response(Y, X)]
+ProposeCoauthorship(X, Y) >> [show_line("Propose co-authorship with ",X," to publish in the field of ",Y,".\n")]


# Put here desires to automatically execute on start-up

#PHIDIAS.achieve(start_rest(), "main")
#PHIDIAS.achieve(load(), "main")
