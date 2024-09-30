import sys
import random
import turtle
import threading

sys.path.insert(0, "../lib")

from phidias.Lib import *
from phidias.Agent import *
from phidias.Types import *

import configparser
from owlready2 import *

config = configparser.ConfigParser()
config.read('config_mas.ini')

# ONTOLOGY section
FILE_NAME = config.get('ONTOLOGY', 'FILE_NAME')
ONTO_NAME = config.get('ONTOLOGY', 'ONTO_NAME')

# ID prefix
ID_PREFIX = config.get('AGENT', 'PREFIX_LABEL')
# Agent number
AGENT_NUMBER = int(config.get('AGENT', 'AGENTS_NUMBER'))

# REASONING Section
REASONING_ACTIVE = config.getboolean('REASONING', 'ACTIVE')
REASONER = config.get('REASONING', 'REASONER').split(",")
PREFIXES = config.get('REASONING', 'PREFIXES').split(",")
PREFIX = " ".join(PREFIXES)
PREFIX = PREFIX + f"PREFIX {ONTO_NAME}: <http://test.org/{FILE_NAME}#> "

# BDI-CLASSES Section
ENTITIES = config.get('CLASSES', 'Entities').split(",")

# Properties
BELIEFS = config.get('CLASSES', 'PHI-Beliefs').split(",")
REACTORS = config.get('CLASSES', 'PHI-Reactors').split(",")
DESIRES = config.get('CLASSES', 'PHI-Desires').split(",")
INTENTIONS = config.get('CLASSES', 'PHI-Intentions').split(",")

PROPERTIES = config.get('CLASSES', 'Properties').split(",")
DATAS = config.get('CLASSES', 'Data').split(",")

# ---------------------------------------------------------------------
# Non-ontological rendering variables
# ---------------------------------------------------------------------

# Coordinates spamming range
N = 500

# time-range to get the job done
LOWER_BOUND = 0
UPPER_BOUND = 3

# Breakdown of steps
STEP_BREAKDOWN = 50

# Pause between steps
STEP_DURATIN = 0.005

# Worker-Turtle dictionary
dict_turtle = {}


# ---------------------------------------------------------------------
# Ontology section
# ---------------------------------------------------------------------

# Max work time for a worker (seconds)
Max_WorkDay_Time = 27
# Max work time for a worker (seconds) - MAX_WORKDAY_TIME must be multiple of MAX_WORK_TIME
Max_Work_Time = 7
# Rest time for a worker (seconds)
Rest_Time = 3
# Timer tick
TICK = 0.1



try:
    my_onto = get_ontology(FILE_NAME).load()
    print("\nLoading worlds "+FILE_NAME+"...")
except IOError:
    my_onto = get_ontology("http://test.org/"+FILE_NAME)
    print("\nCreating new "+FILE_NAME+" file...")
    print("\nPlease Re-Run Semas.")
    my_onto.save(file=FILE_NAME, format="rdfxml")
    exit()


# instances name/instances dictionary
dict_ent = {}
# properties name/properites dictionary
dict_prop = {}


# Phidias belief containing OWL triples
class TRIPLE(Belief):
    pass


with my_onto:

    class ENTITY(Thing):
        pass

    class BELIEF(Thing):
        pass

    class REACTOR(Thing):
        pass

    class DESIRE(Thing):
        pass

    class INTENTION(Thing):
        pass

    # Declaring Owlready DataProperties
    for i in range(len(DATAS)):
        globals()[DATAS[i].strip()] = type(DataProperty)
        dict_prop[DATAS[i].strip()] = DATAS[i].strip()

    # Declaring Owlready ObjectProperties
    for i in range(len(PROPERTIES)):
        globals()[PROPERTIES[i].strip()] = type(PROPERTIES[i].strip(), (ObjectProperty,), {})
        istanza = globals()[PROPERTIES[i].strip()]()
        dict_prop[PROPERTIES[i].strip()] = istanza


# Declaring Phidias belief from OWL
for i in range(len(BELIEFS)):
    # creating subclasses BELIEFS
    new_belief = types.new_class(BELIEFS[i].strip(), (BELIEF,))

    globals()[BELIEFS[i].strip()] = type(BELIEFS[i].strip(), (Belief,), {})
    istanza = globals()[BELIEFS[i].strip()]()

for i in range(len(REACTORS)):
    # creating subclasses BELIEFS
    new_belief = types.new_class(REACTORS[i].strip(), (REACTOR,))

    globals()[REACTORS[i].strip()] = type(REACTORS[i].strip(), (Reactor,), {})
    istanza = globals()[REACTORS[i].strip()]()

for i in range(len(DESIRES)):
    # creating subclasses DESIRES
    new_belief = types.new_class(DESIRES[i].strip(), (DESIRE,))

    globals()[DESIRES[i].strip()] = type(DESIRES[i].strip(), (Procedure,), {})
    istanza = globals()[DESIRES[i].strip()]()

for i in range(len(INTENTIONS)):
    # creating subclasses INTENTIONS
    new_belief = types.new_class(INTENTIONS[i].strip(), (INTENTION,))

    globals()[INTENTIONS[i].strip()] = type(INTENTIONS[i].strip(), (Reactor,), {})
    istanza = globals()[INTENTIONS[i].strip()]()



# ---------------------------------------------------------------------
# System procedures section
# ---------------------------------------------------------------------


# Ontology intialization
class init(Procedure): pass

# Import OWL triples
class load(Procedure): pass
# Turning triples to beliefs
class turn(Procedure): pass

class initWorld(Action):
    """World entities initialization"""
    def execute(self):

        # Entities
        for i in range(len(ENTITIES)):
            # creating subclasses ENTITY
            entity = types.new_class(ENTITIES[i].strip(), (ENTITY,))

            ENT_INDS = config.get('INDIVIDUALS', ENTITIES[i].strip()).split(",")

            # creating ENTITY individuals
            for j in range(len(ENT_INDS)):
                new_entity = entity(ENT_INDS[j].strip())
                dict_ent[ENT_INDS[j].strip()] = new_entity

        print("BELIEFS: ", BELIEFS)

        for i in range(len(BELIEFS)):
            BDI_INDS = config.get('INDIVIDUALS', BELIEFS[i].strip()).split(" & ")

            for j in range(len(BDI_INDS)):
                triple = BDI_INDS[j].strip()

                print("BELIEFS: ", BELIEFS)
                print("BDI_INDS: ", BDI_INDS)
                print("triple: ", triple)

                subject = triple.split(",")[0][1:].strip()
                prop = triple.split(",")[1].strip()
                object = triple.split(",")[2][:-1].strip()

                getattr(dict_ent[subject], prop).append(dict_ent[object])



class declareRules(Action):
    """assert an SWRL rule"""
    def execute(self):
        number_of_rules = int(config.get('SWRL', 'NUMBER_OF_RULES'))
        with my_onto:
           rule = Imp()

           print(f"\nAdding the following {number_of_rules} rules to ontology: ")
           for i in range(number_of_rules):
               rule_str = config.get('SWRL', 'RULE'+str(i+1))
               print(f"Rule {str(i+1)}: {rule_str}")
               rule.set_as_rule(rule_str)



class saveOnto(Action):
    """Creating a subclass of the class Verb"""
    def execute(self):
        with my_onto:
            #sync_reasoner_pellet()
            my_onto.save(file=FILE_NAME, format="rdfxml")
            print("Ontology saved.")



class assert_beliefs_triples(Action):
    """create sparql query from MST"""
    def execute(self):

        q = PREFIX + f" SELECT ?subj ?prop ?obj" + " WHERE { "
        q = q + f"?subj ?prop ?obj. ?subj rdf:type/rdfs:subClassOf* {ONTO_NAME}:ENTITY. ?obj rdf:type/rdfs:subClassOf* {ONTO_NAME}:ENTITY." + "}"

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        if REASONING_ACTIVE:
            # sync_reasoner_pellet(my_world, infer_property_values = True, infer_data_property_values = True)
            sync_reasoner_hermit(my_world, infer_property_values=True)
            # sync_reasoner_hermit(my_world)

        graph = my_world.as_rdflib_graph()
        result = list(graph.query(q))

        for res in result:

            subj = str(res).split(",")[0]
            subj = subj.split("#")[1][:-2]

            prop = str(res).split(",")[1]
            prop = prop.split("#")[1][:-2]

            obj = str(res).split(",")[2]
            obj = obj.split("#")[1][:-3]

            self.assert_belief(TRIPLE(subj, prop, obj))



# ---------------------------------------------------------------------
# Sensors section
# ---------------------------------------------------------------------

class TaskDetect(Sensor):

    def on_start(self):
        # Starting task detection
       self.running = True

    def on_restart(self):
        # Re-Starting task detection
        self.do_restart = True

    def on_stop(self):
        #Stopping task detection
        self.running = False

    def sense(self):
        while self.running:
           time.sleep(TICK)

           pos_x = random.randint(-N // 2, N // 2)
           pos_y = random.randint(-N // 2, N // 2)
           self.assert_belief(TASK(pos_x, pos_y))



class Timer(Sensor):

    def on_start(self, uTimeout):
        evt = threading.Event()
        self.event = evt
        self.timeout = uTimeout()
        self.do_restart = False


    def on_restart(self, uTimeout):
        self.do_restart = True
        self.event.set()

    def on_stop(self):
        self.do_restart = False
        self.event.set()

    def sense(self):
        while True:
            time.sleep(self.timeout)
            self.event.clear()
            if self.do_restart:
                self.do_restart = False
                continue
            elif self.stopped:
                self.assert_belief(TIMEOUT("ON"))
                return
            else:
                return


# ---------------------------------------------------------------------
# Agent section
# ---------------------------------------------------------------------



class rest(Action):
    """resting for few seconds"""
    def execute(self, arg):
      rest_time = int(str(arg).split("'")[2][1:-1])
      print(f"\nresting for {rest_time} seconds...")

      for t in dict_turtle:
          dict_turtle[t].color("red")

      time.sleep(rest_time)

      for t in dict_turtle:
          dict_turtle[t].color("black")



class UpdateLedger(Action):
    """Update completed jobs"""
    def execute(self, arg1, arg2):

      agent = str(arg1).split("'")[3]
      jobs = int(str(arg2).split("'")[3])
      jobs = jobs + 1
      print(f"Updating {agent} ledger: {jobs}")
      self.assert_belief(LEDGER(agent, str(jobs)))
      self.assert_belief(DUTY(int(agent[-1:])))


class UpdateWorkTime(Action):
    """Update completed jobs"""
    def execute(self, arg1, arg2):

        arg1_num = str(arg1).split("'")[2][1:-1]
        arg2_num = str(arg2).split("'")[2][1:-1]
        arg_num_tot = int(arg1_num)+int(arg2_num)
        print("WORKTIME: ",arg_num_tot)
        self.assert_belief(WORKTIME(arg_num_tot))


class AssignId(Action):
    """Intialize duty flag with ID"""
    def execute(self, arg):
        entity = str(arg).split("'")[3]

        self.assert_belief(DUTY(int(entity[-1:])))
        self.assert_belief(AGT(entity, int(entity[-1:])))



# ---------------------------------------------------------------------
# Turtle section
# ---------------------------------------------------------------------


class move_turtle(Action):
    """moving turtle to coordinates (x,y)"""
    def execute(self, arg0, arg1, arg2):
        id_turtle = str(arg0).split("'")[2]
        pos_x = str(arg1).split("'")[2]
        pos_y = str(arg2).split("'")[2]

        id_turtle = id_turtle[1:-1]
        pos_x = int(pos_x[1:-1])
        pos_y = int(pos_y[1:-1])

        # Recupera la posizione attuale
        current_x, current_y = dict_turtle["t"+id_turtle].position()

        # Calcola la distanza da percorrere su ciascun asse
        delta_x = (pos_x - current_x) / STEP_BREAKDOWN
        delta_y = (pos_y - current_y) / STEP_BREAKDOWN

        for step in range(STEP_BREAKDOWN):
            # Sposta la tartaruga di una piccola quantità
            current_x += delta_x
            current_y += delta_y
            dict_turtle["t"+id_turtle].goto(current_x, current_y)

            # Rallenta il movimento
            time.sleep(STEP_DURATIN)  # Regola il tempo di pausa per modificare la velocità

        # Pausa finale casuale (se necessaria)
        rnd = random.uniform(LOWER_BOUND, UPPER_BOUND)
        time.sleep(rnd)


def turtle_thread_func():
    wn = turtle.Screen()
    wn.title("Workers jobs assignment")

    for i in range(AGENT_NUMBER):
        dict_turtle["t"+str(i+1)] = turtle.Turtle()

    wn.mainloop()


# Avviare il thread della tartaruga
turtle_thread = threading.Thread(target=turtle_thread_func)
turtle_thread.daemon = True
turtle_thread.start()