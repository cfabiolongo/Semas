from phidias.Lib import *
from actions import *

# Beliefs declaration

class INFO(Belief): pass

# Informative beliefs about current desires
class DESIRE(Belief): pass

# Informative beliefs about current pre-conditions
class COND(Belief): pass

# Informative beliefs about occurring plans
class PLAN(Belief): pass

# Informative beliefs about occurring intentions
class INTENT(Belief): pass

# Worlds Agents initialization
init() >> [initWorld(), initAgent(), initBeliefs(), initIntentions(), initPlans(), initDesire(), saveOnto()]


# Intention (Case #1)

INFO(I) / (PLAN(X) & INTENT(Y)) >> [show_line("\nGot Belief: ",I,"\n"), -INFO(I), process_belief(I)]
DESIRE(D) / (PLAN(X) & INTENT(Y)) >> [show_line("\nDesire achieved with value: ",D,"\n")]


# Intention (Case #2) - with Conditionals (COND)

INFO(X) >> [show_line("\nGot it Belief: ",X,"\n"), process_belief(X), -INFO(X)]
DESIRE(X) / COND(Y) >> [show_line("\nDesire achieved with value: ",X," and conditional: ",Y," \n")]


# Intention (Case #1) - with Active Belief (check)

INFO(X) / check(X) >> [show_line("\nGot it Belief: ",X,"\n"), process_belief(X), -INFO(X)]
DESIRE(X) >> [show_line("\nDesire achieved with value: ",X,"\n")]


#+Q(X) >> [reset_ct(), log("Q", X), show_ct(), +ALL(X), feed_sparql()]
# +QUERY(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_sparql(), log("Query", X), show_ct()]
#+QUERY(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), log("Query",X), show_ct()]

# +PROCESS_STORED_MST("OK") / LISTEN("TEST") >> [show_line("\nGot it.\n"), create_onto(), process_rule(), -LISTEN("TEST")]
# +PROCESS_STORED_MST("OK") / REASON("TEST") >> [show_line("\nProcessing query.....\n"), create_sparql(), -REASON("TEST")]

# Nominal ontology assertion --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
# +PROCESS_STORED_MST("OK") / LISTEN("ON") >> [show_line("\nGot it.\n"), create_onto(), process_rule()]
# processing rule
# process_rule() / IS_RULE("TRUE") >> [show_line("\n------> rule detected!\n"), -IS_RULE("TRUE"), create_onto("RULE")]

# Ontology creation
# create_onto() >> [preprocess_onto(), InitOnto(), process_onto(), show_line("\n------------- Done:", T, "\n")]
