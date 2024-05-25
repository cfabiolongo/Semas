from phidias.Types import *
import configparser
from owlready2 import *

config = configparser.ConfigParser()
config.read('config.ini')

# SERVICE section
LOG_ACTIVE = config.getboolean('SERVICE', 'LOG_ACTIVE')

# ONTOLOGY section
FILE_NAME = config.get('ONTOLOGY', 'FILE_NAME')
ONTO_NAME = config.get('ONTOLOGY', 'ONTO_NAME')

# REASONING Section
REASONER = config.get('REASONING', 'REASONER').split(",")
PREFIXES = config.get('REASONING', 'PREFIXES').split(",")
PREFIX = " ".join(PREFIXES)
PREFIX = PREFIX + f"PREFIX {ONTO_NAME}: <http://test.org/{FILE_NAME}#> "

# BDI-CLASSES Section
ENTITIES = config.get('BDI-CLASSES', 'Entities').split(",")

# Properties
BELIEFS = config.get('BDI-CLASSES', 'Beliefs').split(",")
DESIRES = config.get('BDI-CLASSES', 'Desires').split(",")
INTENTIONS = config.get('BDI-CLASSES', 'Intentions').split(",")

try:
    my_onto = get_ontology(FILE_NAME).load()
    print("\nLoading worlds "+FILE_NAME+"...")
except IOError:
    my_onto = get_ontology("http://test.org/"+FILE_NAME)
    print("\nCreating new "+FILE_NAME+" file...")
    print("\nPlease Re-Run Semas.")
    my_onto.save(file=FILE_NAME, format="rdfxml")
    exit()


with my_onto:

    class ENTITY(Thing):
        pass

    class BELIEF(Thing):
        pass

    class DESIRE(Thing):
        pass

    class INTENTION(Thing):
        pass

    class PLAN(Thing):
        pass

    class coAuthorWith(ObjectProperty):
        pass

    class hasAffiliationWith(ObjectProperty):
        pass

    class isTopAuthorIn(ObjectProperty):
        pass

    class selectedFor(ObjectProperty):
        pass


    class beTopAuthorOwnField(ObjectProperty):
        pass


    class ProposeCoauthorship(ObjectProperty):
        pass











# Declaring Phidias belief from OWL
for i in range(len(BELIEFS)):
    # creating subclasses BELIEFS
    new_belief = types.new_class(BELIEFS[i].strip(), (BELIEF,))

    globals()[BELIEFS[i].strip()] = type(BELIEFS[i].strip(), (Belief,), {})
    # Ora puoi creare un'istanza della classe
    istanza = globals()[BELIEFS[i].strip()]()


# Phidias Actions

class process_belief(Action):
    """create sparql query from MST"""
    def execute(self, arg1):
        print("\n--------- Processing belief Info---------\n ")

        info = str(arg1).split("'")[3]
        print(f"Operations on belief {info}...")



class check(ActiveBelief):
    """check if var has an admissible value"""
    def evaluate(self, arg):

        var = str(arg).split("'")[3]

        if var == "OK":
            return True
        else:
            return False


class log(Action):
    """log direct assertions from keyboard"""
    def execute(self, *args):
        a = str(args).split("'")

        if LOG_ACTIVE:
            with open("log.txt", "a") as myfile:
                myfile.write("\n"+a[1]+": "+a[5])



# ---------------------- Ontology creation Section


class WFR(ActiveBelief):
    """check if R is a Well Formed Rule"""
    def evaluate(self, arg):

        rule = str(arg).split("'")[3]

        if rule[0] != "-" and rule[-1] != ">":
            return True
        else:
            return False


class declareRules(Action):
    """assert an SWRL rule"""
    def execute(self):
        number_of_rules = int(config.get('SWRL', 'NUMBER_OF_RULES'))
        with my_onto:
           rule = Imp()

           for i in range(number_of_rules):
               rule_str = config.get('SWRL', 'RULE'+str(i+1))
               print(f"\nadding the following rules to ontology: {rule_str}")
               rule.set_as_rule(rule_str)


class initWorld(Action):
    """World entities initialization"""
    def execute(self):

        # Entities
        for i in range(len(ENTITIES)):
            # creating subclasses ENTITY
            entity = types.new_class(ENTITIES[i].strip(), (ENTITY,))

            ENT_INDS = config.get('BDI-INDIVIDUALS', ENTITIES[i].strip()).split(",")

            # creating ENTITY individuals
            for j in range(len(ENT_INDS)):
                new_entity = entity(ENT_INDS[j].strip())



            for i in entity.instances():
                print(i)

        for i in range(len(BELIEFS)):
            # creating subclasses BELIEFS
            new_belief = types.new_class(BELIEFS[i].strip(), (BELIEF,))
            BDI_INDS = config.get('BDI-INDIVIDUALS', BELIEFS[i].strip()).split(" & ")

            for j in range(len(BDI_INDS)):
                triple = BDI_INDS[j].strip()

                subject = triple.split(",")[0][1:]
                prop = triple.split(",")[1]
                object = triple.split(",")[2][:-1]

                print(subject, prop, object)



                #print(entity[subject])

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> QUI!!!!!!!!!!!!


        for i in range(len(DESIRES)):
            # creating subclasses BELIEFS
            new_desire = types.new_class(DESIRES[i].strip(), (DESIRE,))

        for i in range(len(INTENTIONS)):
            # creating subclasses BELIEFS
            new_intention = types.new_class(INTENTIONS[i].strip(), (INTENTION,))


        # for i in range(len(DESIRES)):
        #     # creating subclass DESIRES
        #     desire = types.new_class(DESIRES[i].strip(), (DESIRE,))
        #     # DESIRE individual
        #     new_desire = desire(DESIRES_ind[i].strip())
        #
        # for i in range(len(INTENTIONS)):
        #     # creating subclass INTENTION
        #     desire = types.new_class(INTENTIONS[i].strip(), (INTENTION,))
        #     # INTENTION individual
        #     new_desire = desire(INTENTIONS_ind[i].strip())
        #
        # for i in range(len(PLANS)):
        #     # creating subclass PLAN
        #     plan = types.new_class(PLANS[i].strip(), (PLAN,))
        #     # INTENTION PLAN
        #     new_plan = plan(PLANS_ind[i].strip())
        #
        # for i in range(len(AGENTS)):
        #     # creating subclass AGENT
        #     agent = types.new_class(AGENTS[i].strip(), (AGENT,))
        #     AGT_IND = config.get('INIT-W1', AGENTS[i].strip()+'_ind').split(",")
        #
        #     # AGENT individuals
        #     for j in range(len(AGT_IND)):
        #         new_agent_ind = agent(AGT_IND[j].strip())
        #         new_agent_ind.hasWorld = [new_world]
        #         new_world.hasAgent.append(new_agent_ind)
        #
        #         AGT_BELIEF_LIST = config.get('INIT-W1', AGT_IND[j].strip() + '_beliefs').split(",")
        #         for agent_belief in AGT_BELIEF_LIST:
        #             bel = agent_belief.strip().split(".")[0]
        #             new_agent_ind.hasBelief.append(BELIEF(bel))
        #
        #         AGT_DESIRE_LIST = config.get('INIT-W1', AGT_IND[j].strip() + '_desires').split(",")
        #         for agent_desire in AGT_DESIRE_LIST:
        #             des = agent_desire.strip().split(".")[0]
        #             new_agent_ind.hasDesire.append(DESIRE(des))
        #
        #         AGT_INTENTIONS_LIST = config.get('INIT-W1', AGT_IND[j].strip() + '_intentions').split(",")
        #         for agent_intention in AGT_INTENTIONS_LIST:
        #             intent = agent_intention.strip().split(".")[0]
        #             new_agent_ind.hasIntention.append(INTENTION(intent))
        #
        #         AGT_PLANS_LIST = config.get('INIT-W1', AGT_IND[j].strip() + '_plans').split(",")
        #         for agent_plan in AGT_PLANS_LIST:
        #             plan = agent_plan.strip().split(".")[0]
        #             new_agent_ind.hasPlan.append(PLAN(plan))





# class createSubCustVerb(Action):
#     """Creating a subclass of the class Verb"""
#     def execute(self, arg1, arg2, arg3, arg4):
#
#         id_str = str(arg1).split("'")[3]
#         verb_str = str(arg2).split("'")[3].replace(":", SEP)
#         subj_str = str(arg3).split("'")[3].replace(":", SEP)
#         obj_str = str(arg4).split("'")[3].replace(":", SEP)
#
#         # subclasses
#         new_sub_verb = types.new_class(verb_str, (Transitive,))
#         new_sub_subj = types.new_class(subj_str, (Entity,))
#         new_sub_obj = types.new_class(obj_str, (Entity,))
#
#         # entities individual
#         new_ind_id = Id(id_str)
#         new_ind_verb = new_sub_verb(parser.clean_from_POS(verb_str)+"."+id_str)
#         new_ind_subj = new_sub_subj(parser.clean_from_POS(subj_str)+"."+id_str)
#         new_ind_obj = new_sub_obj(parser.clean_from_POS(obj_str)+"."+id_str)
#
#         # individual entity - hasSubject - subject individual
#         new_ind_verb.hasSubject = [new_ind_subj]
#         # individual entity - hasObject - Object individual
#         new_ind_verb.hasObject = [new_ind_obj]
#         # storing action's id
#         new_ind_verb.hasId = [new_ind_id]






class saveOnto(Action):
    """Creating a subclass of the class Verb"""
    def execute(self):
        with my_onto:
            #sync_reasoner_pellet()
            my_onto.save(file=FILE_NAME, format="rdfxml")
            print("Ontology saved.")





# ----------------------------------
# --------- SPARQL Section ---------
# ----------------------------------


class seek_prep(Action):
    """Seek related entity (verb/subject/object) preposition"""
    def execute(self, arg1):

        subject = str(arg1).split("'")[3]
        print(subject)

        q = PREFIX + f" SELECT ?prep ?obj"+" WHERE { "
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

        q = PREFIX + f" SELECT ?adj"+" WHERE { "
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
