from phidias.Lib import *
from actions import *



# ONTOLOGY BUILDER

process_onto() / ID(I) >> [aggr_ent(), valorize(), create_adj(), create_adv(), create_gnd_prep(), create_ner(), create_prep(), create_verb(), create_head(), create_body(), finalize_onto(), saveOnto(), -ID(I)]

# Grounds aggregation
aggr_ent() / (GND(X, Y, Z) & GND(X, Y, K) & neq(Z, K)) >> [show_line("\naggregating entity: ", Y), -GND(X, Y, Z), -GND(X, Y, K), aggrEntity(X, Y, Z, K), aggr_ent()]
aggr_ent() >> [show_line("\nentities aggregation done.")]

valorize() / (GND("FLAT", X, Y) & ADJ("FLAT", X, "Equal") & PREP("FLAT", X, "To", S) & VALUE("FLAT", S, V) & ID(I)) >> [show_line("\ngiving value: ", V), -ADJ("FLAT", X, "Equal"), -PREP("FLAT", X, "To", S), -VALUE("FLAT", S, V), createValue(I, Y, V)]
valorize() >> [show_line("\nvalues attribution completed.")]

# Adjective production
create_adj() / (GND("FLAT", X, K) & ADJ("FLAT", X, J) & ID(I)) >> [show_line("\ncreating adjective: ", J), -ADJ("FLAT", X, J), createAdj(I, K, J), create_adj()]
create_adj() >> [show_line("\nadjective creation done.")]

# Adverb productions
create_adv() / (ACTION("FLAT", V, D, X, Y) & ADV("FLAT", D, K) & ID(I)) >> [show_line("\ncreating adverbs: ", Y), -ADV("FLAT", D, K), applyAdv(I, V, K), create_adv()]
create_adv() / (ACTION("ROOT", "FLAT", V, D, X, Y) & ADV("FLAT", D, K) & ID(I)) >> [show_line("\ncreating adverbs (ROOT): ", Y), -ADV("FLAT", D, K), applyAdv(I, V, K), create_adv()]
create_adv() >> [show_line("\nadverbs creation done.")]

# Verb-related prepositions
create_prep() / (ACTION("FLAT", V, D, "__", Y) & PREP("FLAT", D, K, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating pass. verb related prep: ", K), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, S), createSubPassPrep(I, V, K, S), create_prep()]
create_prep() / (ACTION("FLAT", V, D, X, "__") & PREP("FLAT", D, K, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating intr. verb related prep: ", K), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, S), createSubIntrPrep(I, V, K, S), create_prep()]
create_prep() / (ACTION("FLAT", V, D, X, Y) & PREP("FLAT", D, K, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating verb related prep: ", K), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, S), createSubPrep(I, V, K, S), create_prep()]

create_prep() / (ACTION("ROOT", "FLAT", V, D, "__", Y) & PREP("FLAT", D, K, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating pass. verb related (ROOT): ", K), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, S), createSubPassPrep(I, V, K, S), create_prep()]
create_prep() / (ACTION("ROOT", "FLAT", V, D, X, "__") & PREP("FLAT", D, K, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating intr. verb related (ROOT): ", K), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, S), createSubIntrPrep(I, V, K, S), create_prep()]
create_prep() / (ACTION("ROOT", "FLAT", V, D, X, Y) & PREP("FLAT", D, K, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating verb related prep (ROOT): ", K), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, S), createSubPrep(I, V, K, S), create_prep()]

create_prep() >> [show_line("\nverb related preps creation done.")]

# Ground-related Prepositions
create_gnd_prep() / (GND("FLAT", X, K) & PREP("FLAT", X, Y, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating gnd related prep: ", Y), -PREP("FLAT", X, Y, Z), -GND("FLAT", Z, S), createSubGndPrep(I, K, Y, S), create_prep()]
create_gnd_prep() >> [show_line("\ngnd related prep creation done.")]

# Verbs production - copula
create_verb() / (ACTION("ROOT", "FLAT", Z, D, X, Y) & GND("FLAT", X, K) & GND("FLAT", Y, J) & ID(I) & COP(Z)) >> [show_line("\nVERB+Ass.Rule (ROOT-VBZ)"), -ACTION("ROOT", "FLAT", Z, D, X, Y), -GND("FLAT", X, K), -GND("FLAT", Y, J), createSubCustVerb(I, Z, K, J), createAssRule(K, J), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", Z, D, X, Y) & GND("FLAT", X, K) & ADJ("FLAT", Y, J) & ID(I) & COP(Z)) >> [show_line("\nVERB+Ass.Rule ADJ (ROOT-VBP)"), -ACTION("ROOT", "FLAT", Z, D, X, Y), -GND("FLAT", X, K), -ADJ("FLAT", Y, J), createSubCustVerb(I, Z, K, J), createAdj(K, J), create_verb()]

# Verbs production - embedded
create_verb() / (ACTION("ROOT", "FLAT", V, D, X, E) & GND("FLAT", X, H) & ACTION("FLAT", L, E, S, Y) & GND("FLAT", S, K) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating embedded verbs (ROOT): ", V), -ACTION("ROOT", "FLAT", V, D, X, E), -GND("FLAT", X, H), -ACTION("FLAT", L, E, S, Y), -GND("FLAT", S, K), -GND("FLAT", Y, J), createEmbVerbs(I, V, H, L, K, J), create_verb()]

# Verbs production - ordinary
create_verb() / (ACTION("FLAT", V, D, X, Y) & GND("FLAT", X, K) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating normal verb: ", V), -ACTION("FLAT", V, D, X, Y), -GND("FLAT", X, K), -GND("FLAT", Y, J), createSubVerb(I, V, K, J), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", V, D, X, Y) & GND("FLAT", X, K) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating normal verb (ROOT): ", V), -ACTION("ROOT", "FLAT", V, D, X, Y), -GND("FLAT", X, K), -GND("FLAT", Y, J), createSubVerb(I, V, K, J), create_verb()]

# Verbs production - passive/intransitive
create_verb() / (ACTION("FLAT", V, D, "__", Y) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating passive verb: ", V), -ACTION("FLAT", V, D, "__", Y), -GND("FLAT", Y, J), createPassSubVerb(I, V, J), create_verb()]
create_verb() / (ACTION("FLAT", V, D, X, "__") & GND("FLAT", X, K) & ID(I)) >> [show_line("\ncreating intransitive verb: ", V), -ACTION("FLAT", V, D, X, "__"), -GND("FLAT", X, K), createIntrSubVerb(I, V, K), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", V, D, "__", Y) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating passive verb (ROOT): ", V), -ACTION("ROOT", "FLAT", V, D, "__", Y), -GND("FLAT", Y, J), createPassSubVerb(I, V, J), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", V, D, X, "__") & GND("FLAT", X, K) & ID(I)) >> [show_line("\ncreating intransitive verb (ROOT): ", V), -ACTION("ROOT", "FLAT", V, D, X, "__"), -GND("FLAT", X, K), createIntrSubVerb(I, V, K), create_verb()]

create_verb() >> [show_line("\nverb creation done.")]

# Named Entity Recognition production
create_ner() / (NER("GPE", Y) & PREP("FLAT", D, K, Z) & GND("FLAT", Z, Y) & ID(I)) >> [show_line("\nCreating GPE NER: ", Y), -NER("GPE", Y), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, Y), createPlace(I, Y), create_ner()]
create_ner() / (NER("DATE", Y) & PREP("FLAT", D, K, Z) & GND("FLAT", Z, Y) & ID(I)) >> [show_line("\nCreating DATE NER: ", Y), -NER("DATE", Y), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, Y), createDate(I, Y), create_ner()]
create_ner() / (NER(X, Y) & ID(I)) >> [-NER(X, Y), create_ner()]
create_ner() / ID(I) >> [show_line("\nNER creation done.")]


#  COPULAR VERBS IMPLICATIONS

# updating head/absorbing copular verb
create_head() / (ACTION("RIGHT", Z, E, X, Y) & GND("RIGHT", X, K) & GND("RIGHT", Y, V) & RULE(R) & COP(Z)) >> [show_line("\nupdating implication head: ", V), -ACTION("RIGHT", Z, E, X, Y), -GND("RIGHT", X, K), -GND("RIGHT", Y, V), +SUBJ(Y, K), -RULE(R), fillGndRule("RIGHT", R, Y, V), create_head()]
create_head() / (ACTION("RIGHT", Z, E, X, Y) & GND("RIGHT", X, K) & ADJ("RIGHT", Y, V) & RULE(R) & COP(Z)) >> [show_line("\nupdating implication head (ADJ-obj): ", V), -ACTION("RIGHT", Z, E, X, Y), -GND("RIGHT", X, K), -ADJ("RIGHT", Y, V), +SUBJ(Y, K), -RULE(R), fillHeadAdjRule(R, Y, V), create_head()]

create_head() / ACTION("RIGHT", V, E, X, Y) >> [show_line("\nnon-copular verb not admitted for head: ", V), -ACTION("RIGHT", V, E, X, Y), create_head()]
create_head() / (ACTION("ROOT", "RIGHT", Z, E, X, Y) & GND("RIGHT", X, K) & GND("RIGHT", Y, V) & RULE(R) & COP(Z)) >> [show_line("\nupdating implication head (ROOT): ", V), -ACTION("ROOT", "RIGHT", Z, E, X, Y), -GND("RIGHT", X, K), -GND("RIGHT", Y, V), +SUBJ(Y, K), -RULE(R), fillGndRule("RIGHT", R, Y, V), create_head()]
create_head() / ACTION("ROOT", "RIGHT", V, E, X, Y) >> [show_line("\nnon-copular verb not admitted for head (ROOT): ", V), -ACTION("ROOT", "RIGHT", V, E, X, Y), create_head()]

create_head() / GND("RIGHT", X, K) >> [show_line("\ngnd linked to non-copular verbs not admitted for head: ", K), -GND("RIGHT", X, K), create_head()]
create_head() / PREP("RIGHT", E, X, Y) >> [show_line("\npreps not admitted for head: ", X), -PREP("RIGHT", E, X, Y), create_head()]
create_head() / ADJ("RIGHT", X, K) >> [show_line("\nadjectives not admitted for head: ", K), -ADJ("RIGHT", X, K), create_head()]
create_head() / ADV("RIGHT", D, K) >> [show_line("\nadverbs not admitted for head: ", K), -ADV("RIGHT", D, K), create_head()]
create_head() / RULE(R) >> [show_line("\nhead creation completed")]

# updating body with grounds
create_body() / (GND("LEFT", X, Y) & RULE(R) & SUBJ(Z, Y)) >> [show_line("\nupdating body with gnd: ", Y), -SUBJ(Z, Y), +SUBJ(X, Z), -GND("LEFT", X, Y), -RULE(R), fillGndRule("LEFT", R, Z, Y), create_body()]
create_body() / (GND("LEFT", X, Y) & RULE(R)) >> [show_line("\nupdating body with gnd: ", Y), -GND("LEFT", X, Y), -RULE(R), fillGndRule("LEFT", R, X, Y), create_body()]

create_body() / (ACTION("LEFT", V, D, "__", Y) & RULE(R) & SUBJ(Y, Z)) >> [show_line("\nupdating body with passive verb: ", V), -ACTION("LEFT", V, D, "__", Y), -RULE(R), fillPassActRule(R, V, D, Z), create_body()]
create_body() / (ACTION("LEFT", V, D, X, "__") & RULE(R) & SUBJ(X, Z)) >> [show_line("\nupdating body with intransitive verb: ", V), -ACTION("LEFT", V, D, X, "__"), -RULE(R), fillIntraActRule(R, V, D, Z), create_body()]
create_body() / (ACTION("LEFT", V, E, X, Y) & RULE(R) & SUBJ(X, Z)) >> [show_line("\nupdating body with normal verb: ", V), -ACTION("LEFT", V, E, X, Y), -RULE(R), fillActRule(R, V, E, Z, Y), create_body()]
create_body() / (ACTION("ROOT", "LEFT", V, D, "__", Y) & RULE(R) & SUBJ(Y, Z)) >> [show_line("\nupdating body with passive verb (ROOT): ", V), -ACTION("ROOT","LEFT", V, D, "__", Y), -RULE(R), fillPassActRule(R, V, D, Z), create_body()]
create_body() / (ACTION("ROOT", "LEFT", V, D, X, "__") & RULE(R) & SUBJ(X, Z)) >> [show_line("\nupdating body with intransitive verb (ROOT): ", V), -ACTION("ROOT", "LEFT", V, D, X, "__"), -RULE(R), fillIntraActRule(R, V, D, Z), create_body()]
create_body() / (ACTION("ROOT", "LEFT", V, E, X, Y) & RULE(R) & SUBJ(X, Z)) >> [show_line("\nupdating body with normal verb (ROOT): ", V), -ACTION("ROOT","LEFT", V, E, X, Y), -RULE(R), fillActRule(R, V, E, Z, Y), create_body()]

# updating body with comparison operators
create_body() / (ADJ("LEFT", X, "Great") & PREP("LEFT", X, "Than", S) & VALUE("LEFT", S, V) & RULE(R) & SUBJ(X, Z)) >> [show_line("\nupdating body (SUBJ) with greater than ", V), -ADJ("LEFT", X, "Great"), -PREP("LEFT", X, "Than", S), -VALUE("LEFT", S, V), -RULE(R), fillOpRule(R, Z, V), create_body()]
create_body() / (ADJ("LEFT", X, "Great") & PREP("LEFT", X, "Than", S) & VALUE("LEFT", S, V) & RULE(R)) >> [show_line("\nupdating body with greater than ", V), -ADJ("LEFT", X, "Great"), -PREP("LEFT", X, "Than", S), -VALUE("LEFT", S, V), -RULE(R), fillOpRule(R, X, V), create_body()]

# updating body with adjectives
create_body() / (ADJ("LEFT", X, K) & RULE(R) & SUBJ(X, Z)) >> [show_line("\nupdating body (SUBJ) with adj: ", K), -ADJ("LEFT", X, K), -RULE(R), fillAdjRule(R, Z, K), create_body()]
create_body() / (ADJ("LEFT", X, K) & RULE(R)) >> [show_line("\nupdating body with adj: ", K), -ADJ("LEFT", X, K), -RULE(R), fillAdjRule(R, X, K), create_body()]

# updating body with adverbs
create_body() / (ADV("LEFT", D, K) & RULE(R)) >> [show_line("\nupdating body with adv: ", K), -ADV("LEFT", D, K), -RULE(R), fillAdjRule(R, D, K), create_body()]

#updating body with prepositions
create_body() / (PREP("LEFT", E, X, Y) & RULE(R) & SUBJ(X, Z)) >> [show_line("\nupdating body (SUBJ) with prep: ", X), -RULE(R), -PREP("LEFT", E, X, Y), fillPrepRule("LEFT", R, E, Z, Y), create_body()]
create_body() / (PREP("LEFT", E, X, Y) & RULE(R)) >> [show_line("\nupdating body with prep: ", X), -RULE(R), -PREP("LEFT", E, X, Y), fillPrepRule("LEFT", R, E, X, Y), create_body()]

create_body() / (RULE(R) & SUBJ(X, Y)) >> [show_line("\nupdating body with gnd completed."),  -SUBJ(X, Y)]

finalize_onto() / (RULE(R) & WFR(R)) >> [show_line("\nfinalizing well formed rule..."), -RULE(R), declareRule(R), finalize_onto()]

finalize_onto() / RULE(R) >> [show_line("\nthe rule is not well formed!"), -RULE(R), finalize_onto()]
finalize_onto() / ACTION(S, V, D, X, Y) >> [show_line("\nremoving unuseful action: ", V), -ACTION(S, V, D, X, Y), finalize_onto()]
finalize_onto() / ACTION("ROOT", S, V, D, X, Y) >> [show_line("\nremoving unuseful action (ROOT): ", V), -ACTION("ROOT", S, V, D, X, Y), finalize_onto()]
finalize_onto() / GND(S, X, Y) >> [show_line("\nremoving unuseful gnd: ", Y), -GND(S, X, Y), finalize_onto()]
finalize_onto() / ADJ(S, X, Y) >> [show_line("\nremoving unuseful adj: ", Y), -ADJ(S, X, Y), finalize_onto()]
finalize_onto() / ADV(S, X, Y) >> [show_line("\nremoving unuseful adv: ", Y), -ADV(S, X, Y), finalize_onto()]
finalize_onto() / PREP(S, D, X, Y) >> [show_line("\nremoving unuseful prep: ", Y), -PREP(S, D, X, Y), finalize_onto()]

finalize_onto() >> [show_line("\nontology finalization done.")]








