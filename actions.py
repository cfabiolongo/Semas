
from phidias.Types import *
import configparser
from datetime import datetime
from owlready2 import *

config = configparser.ConfigParser()
config.read('config.ini')

cnt = itertools.count(1)
dav = itertools.count(1)

LOG_ACTIVE = config.getboolean('AGENT', 'LOG_ACTIVE')
FILE_NAME = config.get('AGENT', 'FILE_NAME')

owl_obj_dict = {}

try:
    my_onto = get_ontology(FILE_NAME).load()
    print("\nLoading existing "+FILE_NAME+" file...")
except IOError:
    my_onto = get_ontology("http://test.org/"+FILE_NAME)
    print("\nCreating new "+FILE_NAME+" file...")
    print("\nPlease Re-Run Semas.")
    my_onto.save(file=FILE_NAME, format="rdfxml")
    exit()


with my_onto:
    class Id(Thing):
        pass

    class Verb(Thing):
        pass

    class Transitive(Verb):
        pass

    class Intransitive(Verb):
        pass


    class Adjective(Thing):
        pass

    class Adverb(Thing):
        pass

    class Entity(Thing):
        pass

    class Preposition(Thing):
        pass

    class hasAdj(ObjectProperty):
        pass

    class hasAdv(ObjectProperty):
        pass

    class hasObject(ObjectProperty):
        pass

    class hasSubject(ObjectProperty):
        pass

    class hasPrep(ObjectProperty):
        pass

    class hasId(ObjectProperty):
        pass

    class hasDate(DataProperty):
        pass

    class hasPlace(DataProperty):
        pass

    class hasValue(DataProperty):
        range = [int]



# Ontology creation procedures
class create_onto(Procedure): pass
class process_rule(Procedure): pass
class process_onto(Procedure): pass
class create_adj(Procedure): pass
class create_adv(Procedure): pass
class create_verb(Procedure): pass
class create_assrule(Procedure): pass
class create_gnd_prep(Procedure): pass
class create_prep(Procedure): pass
class aggr_ent(Procedure): pass
class create_body(Procedure): pass
class create_head(Procedure): pass
class finalize_onto(Procedure): pass
class create_ner(Procedure): pass
class valorize(Procedure): pass

# initialize Clauses Kb
# mode reactors
class LISTEN(Belief): pass
class REASON(Belief): pass
class IS_RULE(Belief): pass
class WAIT(Belief): pass
class ANSWER(Reactor): pass

# domotic reactive routines
class r1(Procedure): pass
class r2(Procedure): pass

# domotic direct commands
class d1(Procedure): pass
class d2(Procedure): pass

# domotic sensor simulatons
class s1(Procedure): pass
class s2(Procedure): pass

# Fol reasoning utterances
class c1(Procedure): pass
class c2(Procedure): pass
class c3(Procedure): pass
class c4(Procedure): pass
class c5(Procedure): pass
class c6(Procedure): pass

# normal requests beliefs
class GROUND(Belief): pass
class PRE_MOD(Belief): pass
class MOD(Belief): pass
class PRE_INTENT(Belief): pass
class INTENT(Reactor): pass



# action
class ACTION(Belief): pass
# preposition
class PREP(Belief): pass
# ground
class GND(Belief): pass
# adverb
class ADV(Belief): pass
# adjective
class ADJ(Belief): pass
# id individual
class ID(Belief): pass
# rule accumulator
class RULE(Belief): pass
# subject accumulator
class SUBJ(Belief): pass
# subject accumulator
class VALUE(Belief): pass



class feed_sparql(Procedure): pass
class finalize_sparql(Procedure): pass


# Nominal query sparql belief
class SPARQL(Reactor): pass


class log(Action):
    """log direct assertions from keyboard"""
    def execute(self, *args):
        a = str(args).split("'")

        if LOG_ACTIVE:
            with open("log.txt", "a") as myfile:
                myfile.write("\n"+a[1]+": "+a[5])



class create_sparql(Action):
    """create sparql query from MST"""
    def execute(self, *args):
        print("\n--------- MST ---------\n ")

        MST = parser.get_last_MST()
        print("\nMST: \n" + str(MST))
        print("\nGMC_SUPP: \n" + str(parser.GMC_SUPP))
        print("\nGMC_SUPP_REV: \n" + str(parser.GMC_SUPP_REV))
        print("\nLCD: \n" + str(parser.LCD))


# ---------------------- Ontology creation Section


class WFR(ActiveBelief):
    """check if R is a Well Formed Rule"""
    def evaluate(self, arg):

        rule = str(arg).split("'")[3]

        if rule[0] != "-" and rule[-1] != ">":
            return True
        else:
            return False


class declareRule(Action):
    """assert an SWRL rule"""
    def execute(self, arg1):
        rule_str = str(arg1).split("'")[3]

        print("FINALE: ", rule_str)

        with my_onto:
           rule = Imp()
           rule.set_as_rule(rule_str)


class fillActRule(Action):
    """fills a rule with a verbal action"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        rule = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3].replace(":", SEP)
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]

        # creating subclass of Verb
        types.new_class(verb, (Transitive,))

        if rule[0] == "-":
            rule = "hasSubject(?"+dav+", ?"+subj+"), hasObject(?"+dav+", ?"+obj+"), "+verb+"(?"+dav+") "+rule
        else:
            rule = "hasSubject(?"+dav+", ?"+subj+"), hasObject(?"+dav+", ?"+obj+"), "+verb+"(?"+dav+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillPassActRule(Action):
    """fills a rule with a passive verbal action"""
    def execute(self, arg1, arg2, arg3, arg4):

        rule = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3].replace(":", SEP)
        dav = str(arg3).split("'")[3]
        obj = str(arg4).split("'")[3].replace(":", SEP)

        # creating subclass of Verb
        types.new_class(verb, (Intransitive,))

        if rule[0] == "-":
            rule = "hasObject(?"+dav+", ?"+obj+"), "+verb+"(?"+dav+") "+rule
        else:
            rule = "hasObject(?"+dav+", ?"+obj+"), "+verb+"(?"+dav+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillIntraActRule(Action):
    """fills a rule with an intransitive verbal action"""
    def execute(self, arg1, arg2, arg3, arg4):

        rule = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3].replace(":", SEP)
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3].replace(":", SEP)

        # creating subclass of Verb
        types.new_class(verb, (Intransitive,))

        if rule[0] == "-":
            rule = "hasSubject(?"+dav+", ?"+subj+"), "+verb+"(?"+dav+") "+rule
        else:
            rule = "hasSubject(?"+dav+", ?"+subj+"), "+verb+"(?"+dav+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillGndRule(Action):
    """fills a rule with a ground"""
    def execute(self, arg0, arg1, arg2, arg3):

        hand_side = str(arg0).split("'")[1]
        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        value = str(arg3).split("'")[3].replace(":", SEP)

        # creating subclass of Entity
        types.new_class(value, (Entity,))

        if hand_side == "LEFT":
            if rule[0] == "-":
                rule = value+"(?"+var+") "+rule
            else:
                rule = value +"(?"+var+"), "+rule
        else:
            if rule[-1] == ">":
                rule = rule+" "+value+"(?"+var+")"
            else:
                rule = rule+", "+value+"(?"+var+")"

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillHeadAdjRule(Action):
    """fills a rule with an adjective"""
    def execute(self, arg1, arg2, arg3):

        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        adj_str = str(arg3).split("'")[3].replace(":", SEP)

        # creating subclass of Adjective
        types.new_class(adj_str, (Adjective,))

        rule = rule+" "+adj_str+"(?"+var+")"

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillAdjRule(Action):
    """fills a rule with an adjective"""
    def execute(self, arg1, arg2, arg3):

        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        adj_str = str(arg3).split("'")[3].replace(":", SEP)

        # creating subclass of Adjective
        types.new_class(adj_str, (Adjective,))

        new_var = "x" + str(next(cnt))

        if rule[0] == "-":
            rule = "hasAdj(?"+var+", ?"+new_var+"), "+adj_str+"(?"+new_var+") "+rule
        else:
            rule = "hasAdj(?"+var+", ?"+new_var+"), "+adj_str+"(?"+new_var+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillAdvRule(Action):
    """fills a rule with an adverb"""
    def execute(self, arg1, arg2, arg3):

        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        adv_str = str(arg3).split("'")[3].replace(":", SEP)

        # creating subclass of Adverb
        types.new_class(adv_str, (Adverb,))

        new_var = "x" + str(next(cnt))

        if rule[0] == "-":
            rule = "hasAdv(?"+var+", ?"+new_var+"), "+adv_str+"(?"+new_var+") "+rule
        else:
            rule = "hasAdv(?"+var+", ?"+new_var+"), "+adv_str+"(?"+new_var+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillPrepRule(Action):
    """fills a rule with a preposition"""
    def execute(self, arg0, arg1, arg2, arg3, arg4):

        hand_side = str(arg0).split("'")[1]
        rule = str(arg1).split("'")[3]
        var_master = str(arg2).split("'")[3]
        value = str(arg3).split("'")[3].replace(":", SEP)
        var_slave = str(arg4).split("'")[3]

        # creating subclass of preposition
        types.new_class(value, (Preposition,))
        new_index_var = str(next(cnt))

        if hand_side == "LEFT":
            if rule[0] == "-":
                rule = "hasPrep(?"+var_master+", ?x"+new_index_var+"), "+value+"(?x"+new_index_var+"), hasObject(?x"+new_index_var+", ?"+var_slave+") "+rule
            else:
                rule = "hasPrep(?"+var_master+", ?x"+new_index_var+"), "+value+"(?x"+new_index_var+"), hasObject(?x"+new_index_var+", ?"+var_slave+"), " + rule
        else:
            if rule[-1] == ">":
                rule = rule+" hasPrep(?"+var_master+", ?x"+new_index_var+"), "+value+"(?x"+new_index_var+"), hasObject(?x"+new_index_var+", ?"+var_slave+")"
            else:
                rule = rule+", hasPrep(?"+var_master+", ?x"+new_index_var+"), "+value+"(?x"+new_index_var+"), hasObject(?x"+new_index_var+", ?"+var_slave+")"

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillOpRule(Action):
    """fills with comparison operators"""
    def execute(self, arg1, arg2, arg3):

        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        val_str = str(arg3).split("'")[3]

        new_index_var = str(next(cnt))

        if rule[0] == "-":
            rule = "hasValue(?"+var+", ?x"+new_index_var+"), greaterThan(?x"+new_index_var+", "+val_str+") "+rule
        else:
            rule = "hasValue(?"+var+", ?x"+new_index_var+"), greaterThan(?x"+new_index_var+", "+val_str+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class aggrEntity(Action):
    """aggregate two entity beliefs in one"""
    def execute(self, arg1, arg2, arg3, arg4):

        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        label1 = str(arg3).split("'")[3]
        label2 = str(arg4).split("'")[3]

        conc_label = label2 + "_" + label1
        self.assert_belief(GND(id, var, conc_label))


class applyAdv(Action):
    """create an entity and apply an adj to it"""
    def execute(self, arg1, arg2, arg3):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", SEP)
        adv_str = str(arg3).split("'")[3].replace(":", SEP)

        # creating subclass adjective
        adv = types.new_class(adv_str, (Adverb,))
        # adverb individual
        new_adv_ind = adv(parser.clean_from_POS(adv_str)+"."+id_str)

        # creating subclass entity
        new_sub = types.new_class(verb_str, (Verb,))
        # creating entity individual
        new_ind = new_sub(parser.clean_from_POS(verb_str)+"."+id_str)

        # individual entity - hasAdv - adverb individual
        new_ind.hasAdv.append(new_adv_ind)


class createAdj(Action):
    """create an entity and apply an adj to it"""
    def execute(self, arg0, arg1, arg2):

        id_str = str(arg0).split("'")[3]
        ent_str = str(arg1).split("'")[3].replace(":", SEP)
        adj_str = str(arg2).split("'")[3].replace(":", SEP)

        # creating subclass adjective
        adv = types.new_class(adj_str, (Adjective,))
        # adverb individual
        new_adj_ind = adv(parser.clean_from_POS(adj_str)+"."+id_str)

        # creating subclass entity
        ent_sub = types.new_class(ent_str, (Entity,))
        # creating entity individual
        new_ind = ent_sub(parser.clean_from_POS(ent_str)+"."+id_str)

        # individual entity - hasAdv - adverb individual
        new_ind.hasAdj.append(new_adj_ind)


class createSubCustVerb(Action):
    """Creating a subclass of the class Verb"""
    def execute(self, arg1, arg2, arg3, arg4):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", SEP)
        subj_str = str(arg3).split("'")[3].replace(":", SEP)
        obj_str = str(arg4).split("'")[3].replace(":", SEP)

        # subclasses
        new_sub_verb = types.new_class(verb_str, (Transitive,))
        new_sub_subj = types.new_class(subj_str, (Entity,))
        new_sub_obj = types.new_class(obj_str, (Entity,))

        # entities individual
        new_ind_id = Id(id_str)
        new_ind_verb = new_sub_verb(parser.clean_from_POS(verb_str)+"."+id_str)
        new_ind_subj = new_sub_subj(parser.clean_from_POS(subj_str)+"."+id_str)
        new_ind_obj = new_sub_obj(parser.clean_from_POS(obj_str)+"."+id_str)

        # individual entity - hasSubject - subject individual
        new_ind_verb.hasSubject = [new_ind_subj]
        # individual entity - hasObject - Object individual
        new_ind_verb.hasObject = [new_ind_obj]
        # storing action's id
        new_ind_verb.hasId = [new_ind_id]


class createSubVerb(Action):
    """Creating a subclass of the class Verb"""
    def execute(self, arg1, arg2, arg3, arg4):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", SEP)
        subj_str = str(arg3).split("'")[3].replace(":", SEP)
        obj_str = str(arg4).split("'")[3].replace(":", SEP)

        # subclasses
        new_sub_verb = types.new_class(verb_str, (Transitive,))
        new_sub_subj = types.new_class(subj_str, (Entity,))
        new_sub_obj = types.new_class(obj_str, (Entity,))

        # entities individual
        new_ind_id = Id(id_str)
        new_ind_verb = new_sub_verb(parser.clean_from_POS(verb_str)+"."+id_str)
        new_ind_subj = new_sub_subj(parser.clean_from_POS(subj_str)+"."+id_str)
        new_ind_obj = new_sub_obj(parser.clean_from_POS(obj_str)+"."+id_str)

        # individual entity - hasSubject - subject individual
        new_ind_verb.hasSubject = [new_ind_subj]
        # individual entity - hasObject - Object individual
        new_ind_verb.hasObject = [new_ind_obj]
        # storing action's id
        new_ind_verb.hasId = [new_ind_id]


class createEmbVerbs(Action):
    """Creating subclasses of the class Verb/Entity + embedded individuals"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        id_str = str(arg1).split("'")[3]
        main_verb_str = str(arg2).split("'")[3].replace(":", SEP)
        main_subj_str = str(arg3).split("'")[3].replace(":", SEP)
        emb_verb_str = str(arg4).split("'")[3].replace(":", SEP)
        emb_subj_str = str(arg5).split("'")[3].replace(":", SEP)
        emb_obj_str = str(arg6).split("'")[3].replace(":", SEP)

        # subclasses
        main_sub_verb = types.new_class(main_verb_str, (Transitive,))
        main_sub_subj = types.new_class(main_subj_str, (Entity,))
        emb_sub_verb = types.new_class(emb_verb_str, (Transitive,))
        emb_sub_subj = types.new_class(emb_subj_str, (Entity,))
        emb_sub_obj = types.new_class(emb_obj_str, (Entity,))

        # individuals
        new_ind_id = Id(id_str)
        new_ind_main_verb = main_sub_verb(parser.clean_from_POS(main_verb_str)+"."+id_str)
        new_ind_main_subj = main_sub_subj(parser.clean_from_POS(main_subj_str)+"."+id_str)

        new_ind_emb_verb = emb_sub_verb(parser.clean_from_POS(emb_verb_str)+"."+id_str)
        new_ind_emb_subj = emb_sub_subj(parser.clean_from_POS(emb_subj_str)+"."+id_str)
        new_ind_emb_obj = emb_sub_obj(parser.clean_from_POS(emb_obj_str)+"."+id_str)

        # main
        new_ind_main_verb.hasSubject = [new_ind_main_subj]
        new_ind_main_verb.hasObject = [new_ind_emb_verb]

        # embedded
        new_ind_emb_verb.hasSubject = [new_ind_emb_subj]
        new_ind_emb_verb.hasObject = [new_ind_emb_obj]

        # storing action's id
        new_ind_main_verb.hasId = [new_ind_id]
        new_ind_emb_verb.hasId = [new_ind_id]





class createAssRule(Action):
    """Creating new assignment rule between entities"""
    def execute(self, arg1, arg2):

        ent1 = str(arg1).split("'")[3].replace(":", SEP)
        ent2 = str(arg2).split("'")[3].replace(":", SEP)

        types.new_class(ent1, (Entity,))
        types.new_class(ent2, (Entity,))

        rule_str = ent1+"(?x) -> "+ent2+"(?x)"

        rule_adj_legacy = ent1+"(?x2), "+ent2+"(?x1), hasAdj(?x1, ?x3), Adjective(?x3) -> hasAdj(?x2, ?x3)"

        print("New assignment rule: ", rule_str)
        print("New legacy rule: ", rule_adj_legacy)

        with my_onto:
           rule1 = Imp()
           rule1.set_as_rule(rule_str)

           rule2 = Imp()
           rule2.set_as_rule(rule_adj_legacy)


class createPassSubVerb(Action):
    """Creating a subclass of the class Verb (passive)"""
    def execute(self, arg1, arg2, arg3):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", SEP)
        obj_str = str(arg3).split("'")[3].replace(":", SEP)

        # subclasses
        new_sub_verb = types.new_class(verb_str, (Verb,))
        new_sub_obj = types.new_class(obj_str, (Entity,))

        # entities individual
        new_ind_id = Id(id_str)
        new_ind_verb = new_sub_verb(parser.clean_from_POS(verb_str)+"."+id_str)
        new_ind_obj = new_sub_obj(parser.clean_from_POS(obj_str)+"."+id_str)

        # individual entity - hasObject - Object individual
        new_ind_verb.hasObject = [new_ind_obj]
        # storing action's id
        new_ind_verb.hasId = [new_ind_id]


class createIntrSubVerb(Action):
    """Creating a subclass of the class Verb (Intransitive)"""
    def execute(self, arg1, arg2, arg3):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", SEP)
        subj_str = str(arg3).split("'")[3].replace(":", SEP)

        # subclasses
        new_sub_verb = types.new_class(verb_str, (Intransitive, ))
        new_sub_subj = types.new_class(subj_str, (Entity,))

        # entities individual
        new_ind_id = Id(id_str)
        new_ind_verb = new_sub_verb(parser.clean_from_POS(verb_str)+"."+id_str)
        # new_ind_verb.is_a.append(Intransitive)

        new_ind_subj = new_sub_subj(parser.clean_from_POS(subj_str)+"."+id_str)

        # individual entity - hasSubject - subject individual
        new_ind_verb.hasSubject = [new_ind_subj]
        # storing action's id
        new_ind_verb.hasId = [new_ind_id]


class createSubPrep(Action):
    """Creating a subclass of depending action preposition"""
    def execute(self, arg0, arg1, arg2, arg3):

        id_str = str(arg0).split("'")[3]
        verb = str(arg1).split("'")[3].replace(":", SEP)
        prep = str(arg2).split("'")[3].replace(":", SEP)
        ent = str(arg3).split("'")[3].replace(":", SEP)

        v = parser.clean_from_POS(verb) + "." + id_str

        if v in owl_obj_dict:
            print("Getting objects from dict....", owl_obj_dict[v])
            # Getting object from dict
            new_ind_verb = owl_obj_dict[v]
        else:
            print("Creating objects....")
            # Creating subclass of Verb and individual
            new_sub_verb = types.new_class(verb, (Transitive,))
            new_ind_verb = new_sub_verb(v)
            # Updating owl object dict
            owl_obj_dict[verb] = new_sub_verb
            owl_obj_dict[v] = new_ind_verb

        # Creating subclass of Preposition and individual
        new_sub_prep = types.new_class(prep, (Preposition,))
        new_ind_prep = new_sub_prep(parser.clean_from_POS(prep) + "." + id_str)

        # Creating subclass of Entity and individual
        new_sub_ent = types.new_class(ent, (Entity,))
        new_ind_ent = new_sub_ent(parser.clean_from_POS(ent) + "." + id_str)

        # Creating objects properties
        new_ind_verb.hasPrep.append(new_ind_prep)
        new_ind_prep.hasObject.append(new_ind_ent)


class createSubPassPrep(Action):
    """Creating a subclass of depending passive action preposition"""
    def execute(self, arg0, arg1, arg2, arg3):

        id_str = str(arg0).split("'")[3]
        verb = str(arg1).split("'")[3].replace(":", SEP)
        prep = str(arg2).split("'")[3].replace(":", SEP)
        ent = str(arg3).split("'")[3].replace(":", SEP)

        v = parser.clean_from_POS(verb) + "." + id_str

        if v in owl_obj_dict:
            print("Getting objects from dict....", owl_obj_dict[v])
            # Getting object from dict
            new_ind_verb = owl_obj_dict[v]
        else:
            print("Creating objects....")
            # Creating subclass of Verb and individual
            new_sub_verb = types.new_class(verb, (Intransitive,))
            new_ind_verb = new_sub_verb(v)
            # Updating owl object dict
            owl_obj_dict[verb] = new_sub_verb
            owl_obj_dict[v] = new_ind_verb

        # Creating subclass of Preposition and individual
        new_sub_prep = types.new_class(prep, (Preposition,))
        new_ind_prep = new_sub_prep(parser.clean_from_POS(prep) + "." + id_str)

        # Creating subclass of Entity and individual
        new_sub_ent = types.new_class(ent, (Entity,))
        new_ind_ent = new_sub_ent(parser.clean_from_POS(ent) + "." + id_str)

        # Creating objects properties
        new_ind_verb.hasPrep.append(new_ind_prep)
        new_ind_prep.hasObject.append(new_ind_ent)


class createSubIntrPrep(Action):
    """Creating a subclass of depending intransitive action preposition"""
    def execute(self, arg0, arg1, arg2, arg3):

        id_str = str(arg0).split("'")[3]
        verb = str(arg1).split("'")[3].replace(":", SEP)
        prep = str(arg2).split("'")[3].replace(":", SEP)
        ent = str(arg3).split("'")[3].replace(":", SEP)

        v = parser.clean_from_POS(verb) + "." + id_str

        if v in owl_obj_dict:
            print("Getting objects from dict....", owl_obj_dict[v])
            # Getting object from dict
            new_ind_verb = owl_obj_dict[v]
        else:
            print("Creating objects....")
            # Creating subclass of Verb and individual
            new_sub_verb = types.new_class(verb, (Intransitive,))
            new_ind_verb = new_sub_verb(v)
            # Updating owl object dict
            owl_obj_dict[verb] = new_sub_verb
            owl_obj_dict[v] = new_ind_verb

        # Creating subclass of Preposition and individual
        new_sub_prep = types.new_class(prep, (Preposition,))
        new_ind_prep = new_sub_prep(parser.clean_from_POS(prep) + "." + id_str)

        # Creating subclass of Entity and individual
        new_sub_ent = types.new_class(ent, (Entity,))
        new_ind_ent = new_sub_ent(parser.clean_from_POS(ent) + "." + id_str)

        # Creating objects properties
        new_ind_verb.hasPrep.append(new_ind_prep)
        new_ind_prep.hasObject.append(new_ind_ent)



class createSubGndPrep(Action):
    """Creating a subclass of depending gnd preposition"""
    def execute(self, arg0, arg1, arg2, arg3):

        id_str = str(arg0).split("'")[3]
        ent_master = str(arg1).split("'")[3].replace(":", SEP)
        prep = str(arg2).split("'")[3].replace(":", ".")
        ent_slave = str(arg3).split("'")[3].replace(":", SEP)

        # Creating subclasses of Entity and individuals
        new_sub_ent_master = types.new_class(ent_master, (Entity,))
        new_ind_ent_master = new_sub_ent_master(parser.clean_from_POS(ent_master)+"."+id_str)
        new_sub_ent_slave = types.new_class(ent_slave, (Entity,))
        new_ind_ent_slave = new_sub_ent_slave(parser.clean_from_POS(ent_slave)+"."+id_str)

        # Creating subclass of Preposition and individual
        new_sub_prep = types.new_class(prep, (Preposition,))
        new_ind_prep = new_sub_prep(parser.clean_from_POS(prep) + "." + id_str)

        # Creating objects properties
        new_ind_ent_master.hasPrep.append(new_ind_prep)
        new_ind_prep.hasObject.append(new_ind_ent_slave)


class createPlace(Action):
    """Creating DataProperty from NER Place"""
    def execute(self, arg1, arg2):

        id_str = str(arg1).split("'")[3]
        place_str = str(arg2).split("'")[3]

        # entities individual
        new_ind_id = Id(id_str)

        # storing id features
        new_ind_id.hasPlace = [place_str]


class createDate(Action):
    """Creating DataProperty from NER Date"""
    def execute(self, arg1, arg2):

        id_str = str(arg1).split("'")[3]
        date_str = str(arg2).split("'")[3]

        # entities individual
        new_ind_id = Id(id_str)

        # storing id features
        new_ind_id.hasDate = [date_str]


class createValue(Action):
    """Creating DataProperty fro a given value to entity"""
    def execute(self, arg0, arg1, arg2):

        id_str = str(arg0).split("'")[3]
        ent_str = str(arg1).split("'")[3]
        value_str = str(arg2).split("'")[3]

        # creating subclass of entity
        new_sub_obj = types.new_class(ent_str, (Entity,))

        # entities individual
        new_ind_ent = new_sub_obj(parser.clean_from_POS(ent_str)+"."+id_str)

        # storing value
        new_ind_ent.hasValue = [int(value_str)]


class saveOnto(Action):
    """Creating a subclass of the class Verb"""
    def execute(self):
        with my_onto:
            #sync_reasoner_pellet()
            my_onto.save(file=FILE_NAME, format="rdfxml")


class InitOnto(Action):
    """Generating sentence id individual"""
    def execute(self):
        dateTimeObj = datetime.datetime.now()
        id_ind = str(dateTimeObj.microsecond)
        self.assert_belief(ID(id_ind))


class COP(ActiveBelief):
    """ActiveBelief for checking whether a lemma can generate an assignment rule"""
    def evaluate(self, arg1):

        lemma = str(arg1).split("'")[3]
        lemma_decomposed = lemma.split(":")

        POS_ADMITTED = False

        if len(lemma_decomposed) > 1:
            if lemma_decomposed[1] in ASSIGN_RULES_POS:
                POS_ADMITTED = True
        else:
            POS_ADMITTED = True

        # Checking for proper lemma
        if lemma_decomposed[0] in ASSIGN_RULES_LEMMAS and POS_ADMITTED is True:
           return True
        else:
           return False






# ----------------------------------
# --------- SPARQL Section ---------
# ----------------------------------


class seek_prep(Action):
    """Seek related entity (verb/subject/object) preposition"""
    def execute(self, arg1):

        subject = str(arg1).split("'")[3]
        print(subject)

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        q = p + f" SELECT ?prep ?obj"+" WHERE { "
        q = q + f"lodo:{subject} lodo:hasPrep ?prep. ?prep lodo:hasObject ?obj. "+"}"

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        # sync_reasoner_pellet(my_world, infer_property_values = True, infer_data_property_values = True)
        sync_reasoner_hermit(my_world, infer_property_values=True)
        # sync_reasoner_hermit(my_world)

        graph = my_world.as_rdflib_graph()
        result = list(graph.query(q))

        print(result)
        id = subject.split(".")[1]

        for res in result:
            print(res)
            pre_prep = str(res).split(",")[0]
            pre_obj = str(res).split(",")[1]

            prep = pre_prep.split("#")[1][:-2]
            obj = pre_obj.split("#")[1][:-3]

            self.assert_belief(LF_PREP(id, subject, prep, obj))



class seek_adj(Action):
    """Seek related verb adverbs"""
    def execute(self, arg1):

        subject = str(arg1).split("'")[3]
        print(subject)

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        q = p + f" SELECT ?adj"+" WHERE { "
        q = q + f"lodo:{subject} lodo:hasAdj ?adj. "+"}"

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        # sync_reasoner_pellet(my_world, infer_property_values = True, infer_data_property_values = True)
        sync_reasoner_hermit(my_world, infer_property_values=True)
        # sync_reasoner_hermit(my_world)

        graph = my_world.as_rdflib_graph()
        result = list(graph.query(q))

        for res in result:
            adv = str(res).split("#")[1][:-4]
            id = adv.split(".")[1]
            self.assert_belief(LF_ADJ(id, subject, adv))


class seek_adv(Action):
    """Seek related verb adverbs"""
    def execute(self, arg1):

        subject = str(arg1).split("'")[3]
        print(subject)

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        q = p + f" SELECT ?adv"+" WHERE { "
        q = q + f"lodo:{subject} lodo:hasAdv ?adv. "+"}"

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        # sync_reasoner_pellet(my_world, infer_property_values = True, infer_data_property_values = True)
        sync_reasoner_hermit(my_world, infer_property_values=True)
        # sync_reasoner_hermit(my_world)

        graph = my_world.as_rdflib_graph()
        result = list(graph.query(q))

        for res in result:
            adv = str(res).split("#")[1][:-4]
            id = adv.split(".")[1]
            self.assert_belief(LF_ADV(id, adv))


class submit_sparql(Action):
    """Submit a Query Sparql to Reasoner"""
    def execute(self, arg1):

        query = str(arg1).split("'")[3]

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        #sync_reasoner_pellet(my_world, infer_property_values = True, infer_data_property_values = True)
        sync_reasoner_hermit(my_world, infer_property_values=True)
        # sync_reasoner_hermit(my_world)

        graph = my_world.as_rdflib_graph()
        result = list(graph.query(query))

        if (True in result) or (False in result):
            print("\nResult: ", result)
        else:

            names = []
            EXCLUDED = ['Class', 'NamedIndividual']

            for item in result:
                item = str(item).split("#")[1]
                item_filtered = item.split("'")[0]
                if item_filtered not in EXCLUDED:
                    names.append(item_filtered)

            # Rimuovi duplicati
            unique_names = list(set(names))
            print(unique_names)
            self.assert_belief(PREXR(unique_names))


class submit_intr_explo_sparql(Action):
    """Look for LODO intranstive verbal actions"""
    def execute(self, arg1):

        subject = str(arg1).split("'")[3]

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        #sync_reasoner_pellet(my_world, infer_property_values = True, infer_data_property_values = True)
        sync_reasoner_hermit(my_world, infer_property_values=True)
        # sync_reasoner_hermit(my_world)

        graph = my_world.as_rdflib_graph()

        # +Q("Colonel_NNP_West_NNP")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        q = p + f" SELECT ?i ?s"+" WHERE { "
        q = q + f"?i rdf:type/rdfs:subClassOf* lodo:Intransitive. ?i lodo:hasSubject ?s. ?s rdf:type lodo:{subject}."+"}"

        result = list(graph.query(q))

        print("\nIntransitive verb result: ", result)

        for item in result:
            verb = str(item).split(",")[0]
            verb_filtered = verb.split("#")[1][:-2]

            id = verb_filtered.split(".")[1]

            subject = str(item).split(",")[1]
            subject_filtered = subject.split("#")[1][:-2]

            couple = f"{verb_filtered}, {subject_filtered}"
            print(couple)

            self.assert_belief(VF(id, verb_filtered, subject_filtered, "__"))




class submit_explo_membership(Action):
    """Probe all membership of an individual"""
    def execute(self, arg1):

        subject = str(arg1).split("'")[3]

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        #sync_reasoner_pellet(my_world, infer_property_values = True, infer_data_property_values = True)
        sync_reasoner_hermit(my_world, infer_property_values=True)
        # sync_reasoner_hermit(my_world)

        graph = my_world.as_rdflib_graph()

        # +Q("Colonel_NNP_West_NNP")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        q = p + f" SELECT ?t"+" WHERE { "
        q = q + f"?i rdf:type lodo:{subject}. ?i rdf:type ?t. "+"}"

        result = list(graph.query(q))

        # print("\nResult: ", result)

        cls_list = []

        for item in result:
            cls = str(item).split("#")[1][:-4]
            if cls != 'NamedIndividual':
                cls_list.append(cls)

        cls_list_unique = list(set(cls_list))
        print(cls_list_unique)

        #     verb = str(item).split(",")[0]
        #     verb_filtered = verb.split("#")[1][:-2]
        #
        #     id = verb_filtered.split(".")[1]
        #
        #     subject = str(item).split(",")[1]
        #     subject_filtered = subject.split("#")[1][:-2]
        #
        #     object = str(item).split(",")[2]
        #     object_filtered = object.split("#")[1][:-3]
        #
        #     triple = f"{verb_filtered}, {subject_filtered}, {object_filtered}"
        #
        #     self.assert_belief(VF(id, verb_filtered, subject_filtered, object_filtered))
        #
        #     print(triple)



class submit_explo_sparql(Action):
    """Look for LODO transtive verbal actions"""
    def execute(self, arg1):

        subject = str(arg1).split("'")[3]

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        #sync_reasoner_pellet(my_world, infer_property_values = True, infer_data_property_values = True)
        sync_reasoner_hermit(my_world, infer_property_values=True)
        # sync_reasoner_hermit(my_world)

        graph = my_world.as_rdflib_graph()

        # +Q("Colonel_NNP_West_NNP")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        q = p + f" SELECT ?i ?s ?o"+" WHERE { "
        q = q + f"?i rdf:type/rdfs:subClassOf* lodo:Transitive. ?i lodo:hasSubject ?s. ?s rdf:type lodo:{subject}. ?i lodo:hasObject ?o. "+"}"

        result = list(graph.query(q))

        print("\nTransitive verb result: ", result)

        for item in result:
            verb = str(item).split(",")[0]
            verb_filtered = verb.split("#")[1][:-2]

            id = verb_filtered.split(".")[1]

            subject = str(item).split(",")[1]
            subject_filtered = subject.split("#")[1][:-2]

            object = str(item).split(",")[2]
            object_filtered = object.split("#")[1][:-3]

            triple = f"{verb_filtered}, {subject_filtered}, {object_filtered}"

            self.assert_belief(VF(id, verb_filtered, subject_filtered, object_filtered))

            print(triple)






class feed_who_cop_query_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]

        val_x = str(arg4).split("'")[1] # Who

        val_y = str(arg5).split("'")[3]
        val_y = re.sub(r'\d+', '', val_y).replace(":", "_")

        # +QUERY("Who is Colonel West?")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        q = p + f" SELECT ?{val_x} WHERE "+"{ "
        q = q + f"?i rdf:type lodo:{val_y}. ?i rdf:type/rdfs:subClassOf* ?{val_x}. "+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_who_query_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        v = str(arg1).split("'")[3]
        verb = re.sub(r'\d+', '', v).replace(":", "_")

        e = str(arg2).split("'")[3]
        x = str(arg3).split("'")[3]
        y = str(arg4).split("'")[3]

        val_x = str(arg5).split("'")[1] # Who

        val_y = str(arg6).split("'")[3]
        val_y = re.sub(r'\d+', '', val_y).replace(":", "_")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        q = p + f" SELECT ?{val_x} WHERE "+"{ "
        q = q + f"?{e} rdf:type lodo:{verb}. ?{e} lodo:hasSubject ?{x}. ?{e} lodo:hasObject ?{y}. ?{x} rdf:type ?{val_x}. ?{y} rdf:type lodo:{val_y}."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_where_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        v = str(arg1).split("'")[3]
        e = str(arg2).split("'")[3]
        x = str(arg3).split("'")[3]
        y = str(arg4).split("'")[3]

        val_x = str(arg5).split("'")[3]

        verb = re.sub(r'\d+', '', v).replace(":", "_")
        subject = re.sub(r'\d+', '', val_x).replace(":", "_")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        # +QUERY("Where does Colonel West live?")

        q = p + " SELECT ?where WHERE { "

        q = q + f"?{e} rdf:type lodo:{verb}. ?{e} lodo:hasSubject ?{x}. ?{x} rdf:type lodo:{subject}. ?{e} lodo:hasPrep ?p. ?p lodo:hasObject ?w. ?w rdf:type ?where. "+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_where_pass_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        v = str(arg1).split("'")[3]
        e = str(arg2).split("'")[3]
        x = str(arg3).split("'")[3]
        y = str(arg4).split("'")[3]
        val_y = str(arg5).split("'")[3]

        verb = re.sub(r'\d+', '', v).replace(":", "_")

        object = re.sub(r'\d+', '', val_y).replace(":", "_")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        # +QUERY("Where Colonel West was born?")

        q = p + " SELECT ?where WHERE { "

        q = q + f"?{e} rdf:type lodo:{verb}. ?{e} lodo:hasObject ?{y}. ?{y} rdf:type lodo:{object}. ?{e} lodo:hasPrep ?p. ?p lodo:hasObject ?w. ?w rdf:type ?where. "+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))

class feed_when_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        v = str(arg1).split("'")[3]
        e = str(arg2).split("'")[3]
        x = str(arg3).split("'")[3]
        y = str(arg4).split("'")[3]
        val_x = str(arg5).split("'")[3]

        verb = re.sub(r'\d+', '', v).replace(":", "_")
        subject = re.sub(r'\d+', '', val_x).replace(":", "_")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        # +QUERY("When does Colonel West leave?")

        q = p + " SELECT ?when WHERE { "

        q = q + f"?{e} rdf:type lodo:{verb}. ?{e} lodo:hasSubject ?{x}. ?{x} rdf:type lodo:{subject}. ?{e} lodo:hasPrep ?p. ?p lodo:hasObject ?w. ?w rdf:type ?when. "+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_when_pass_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        v = str(arg1).split("'")[3]
        e = str(arg2).split("'")[3]
        x = str(arg3).split("'")[3]
        y = str(arg4).split("'")[3]
        val_y = str(arg5).split("'")[3]

        verb = re.sub(r'\d+', '', v).replace(":", "_")
        object = re.sub(r'\d+', '', val_y).replace(":", "_")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        # +QUERY("When Colonel West was born?")

        q = p + " SELECT ?when WHERE { "

        q = q + f"?{e} rdf:type lodo:{verb}. ?{e} lodo:hasObject ?{y}. ?{y} rdf:type lodo:{object}. ?{e} lodo:hasPrep ?p. ?p lodo:hasObject ?w. ?w rdf:type ?when. "+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))


class feed_what_query_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        v = str(arg1).split("'")[3]
        e = str(arg2).split("'")[3]
        x = str(arg3).split("'")[3]
        y = str(arg4).split("'")[3]
        y_value = str(arg5).split("'")[3]

        verb = re.sub(r'\d+', '', v).replace(":", "_")
        subject = re.sub(r'\d+', '', y_value).replace(":", "_")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        # +QUERY("What does Colonel West sell?")

        q = p + " SELECT ?what WHERE { "

        q = q + f"?{e} rdf:type lodo:{verb}. ?{e} lodo:hasSubject ?{x}. ?{e} lodo:hasObject ?{y}. ?{x} rdf:type lodo:{subject}. ?{y} rdf:type ?what."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_query_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        v = str(arg1).split("'")[3]
        e = str(arg2).split("'")[3]
        x = str(arg3).split("'")[3]
        y = str(arg4).split("'")[3]
        val_x = str(arg5).split("'")[3]
        val_y = str(arg6).split("'")[3]

        verb = re.sub(r'\d+', '', v).replace(":", "_")
        subject = re.sub(r'\d+', '', val_x).replace(":", "_")
        object = re.sub(r'\d+', '', val_y).replace(":", "_")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        # +QUERY("Colonel West sells missiles?")

        q = p + " ASK WHERE { "
        q = q + f"?{e} rdf:type lodo:{verb}. ?{e} lodo:hasSubject ?{x}. ?{e} lodo:hasObject ?{y}. ?{x} rdf:type lodo:{subject}. ?{y} rdf:type lodo:{object}."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))


class feed_cop_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]
        val_x = str(arg4).split("'")[3]
        val_y = str(arg5).split("'")[3]

        subject = re.sub(r'\d+', '', val_x).replace(":","_")
        object = re.sub(r'\d+', '', val_y).replace(":","_")

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + f"PREFIX lodo: <http://test.org/{FILE_NAME}#> "

        q = p + "ASK WHERE { "

        q = q + f"?{y} rdf:type lodo:{subject}. ?{y} rdf:type lodo:{object}."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))


class feed_cop_prep_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]
        p = str(arg4).split("'")[3]
        prep_obj = str(arg5).split("'")[3]
        prep_obj_val = str(arg6).split("'")[3]

        prep = re.sub(r'\d+', '', p).replace(":", "_")
        prep_obj = re.sub(r'\d+', '', prep_obj).replace(":", "_")
        prep_obj_val = re.sub(r'\d+', '', prep_obj_val).replace(":", "_")

        q = str(arg7).split("'")[3][:-1]

        # +QUERY("Colonel West is President of Cuba?")

        q = q + f" ?{y} lodo:hasPrep ?p{y}. ?p{y} rdf:type lodo:{prep}. ?p{y} lodo:hasObject ?{prep_obj}. ?{prep_obj} rdf:type lodo:{prep_obj_val}."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_prep_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]
        prep_obj = str(arg5).split("'")[3]
        prep_obj_val = str(arg6).split("'")[3]
        prep = str(arg4).split("'")[3]

        prep = re.sub(r'\d+', '', prep).replace(":", "_")
        prep_obj_val = re.sub(r'\d+', '', prep_obj_val).replace(":", "_")

        q = str(arg7).split("'")[3][:-1]

        # +QUERY("Colonel West sells missiles to Cuba?")

        q = q + f" ?{e} lodo:hasPrep ?p{e}. ?p{e} rdf:type lodo:{prep}. ?p{e} lodo:hasObject ?{prep_obj}. ?{prep_obj} rdf:type lodo:{prep_obj_val}."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_adj_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]
        target = str(arg4).split("'")[3]
        adj = str(arg5).split("'")[3]

        target = re.sub(r'\d+', '', target).replace(":", "_")
        adj = re.sub(r'\d+', '', adj).replace(":", "_")

        q = str(arg6).split("'")[3][:-1]

        # +QUERY("Colonel West sells long missiles?")
        # +QUERY("The good Colonel West sells missiles?")
        # +QUERY("The good Colonel West sells long missiles?")

        q = q + f" ?{target} lodo:hasAdj ?a{target}. ?a{target} rdf:type lodo:{adj}. "+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_adv_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]
        adv = str(arg4).split("'")[3]

        adv = re.sub(r'\d+', '', adv).replace(":", "_")

        q = str(arg5).split("'")[3][:-1]

        # +QUERY("Colonel West sells slowly missiles?")

        q = q + f" ?{e} lodo:hasAdv ?d{e}. ?d{e} rdf:type lodo:{adv}. "+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))


class join_cmps(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3):

        var = str(arg1).split("'")[3]
        val1 = str(arg2).split("'")[3]
        val2 = str(arg3).split("'")[3]

        new_var = val2+"_"+val1
        self.assert_belief(MST_VAR(var, new_var))



# --------------------------------------
# --------- LODO-to-LF Section ---------
# --------------------------------------


class build_pre(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        sub = str(arg3).split("'")[3]
        obj = str(arg4).split("'")[3]

        print(id)
        print(verb)
        print(sub)
        print(obj)

        verb = verb.split(".")[0] + "("
        sub = sub.split(".")[0]
        obj = obj.split(".")[0] + ")"

        self.assert_belief(PRE_LF(id, verb, sub, obj))



class join_adj_subj(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3].split(".")[0]
        sub = str(arg3).split("'")[3].split(".")[0]
        obj = str(arg4).split("'")[3].split(".")[0]
        adj = str(arg5).split("'")[3].split(".")[0]

        sub = adj+"("+sub+")"

        self.assert_belief(PRE_LF(id, verb, sub, obj))




class join_adj_obj(Action):
    """Add adj to obj"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        sub = str(arg3).split("'")[3]
        obj = str(arg4).split("'")[3]
        adj = str(arg5).split("'")[3].split(".")[0]

        obj = adj + "(" + obj + ")"

        self.assert_belief(PRE_LF(id, verb, sub, obj))


class join_prep_verb(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        sub = str(arg3).split("'")[3]
        obj = str(arg4).split("'")[3]
        prep = str(arg5).split("'")[3].split(".")[0]
        prep_obj = str(arg6).split("'")[3].split(".")[0]

        verb = prep + "(" + verb
        obj = obj+", "+prep_obj+")"

        self.assert_belief(PRE_LF(id, verb, sub, obj))



class join_prep_subj(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        sub = str(arg3).split("'")[3]
        obj = str(arg4).split("'")[3]
        prep = str(arg5).split("'")[3].split(".")[0]
        prep_obj = str(arg6).split("'")[3].split(".")[0]

        sub = prep+"("+sub+", "+prep_obj+")"

        self.assert_belief(PRE_LF(id, verb, sub, obj))


class join_prep_obj(Action):
    """Feed Query Sparql parser"""

    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):
        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        sub = str(arg3).split("'")[3]
        obj = str(arg4).split("'")[3]
        prep = str(arg5).split("'")[3].split(".")[0]
        prep_obj = str(arg6).split("'")[3].split(".")[0]

        obj = prep + "(" + obj + ", " + prep_obj + ")"

        self.assert_belief(PRE_LF(id, verb, sub, obj))


class build_pre_lf(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3):

        verb = str(arg1).split("'")[3]
        sub = str(arg2).split("'")[3]
        obj = str(arg3).split("'")[3]

        logical_form = verb+sub+", "+obj

        self.assert_belief(LF(logical_form))




# -------------------------------
# --------- LLM Section ---------
# -------------------------------

class llm_get(Action):
    """get LLM result"""
    def execute(self, *args):
        a = str(args).split("'")[5]
        result = parser.get_LLM(a)
        print(result)